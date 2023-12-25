'''
Below helper functions are implemented in this script:

build_sentence_window_index - VectorStore Index for Sentence window RAG technique
get_sentence_window_query_engine - query enginer for the above index
build_automerging_index - VectorStore Index for Auto-merging RAG technique
get_automerging_query_engine - query enginer for the above index

Evaluation function:

get_prebuilt_trulens_recorder - evaluation function with all the feedback functions
'''

import os
import numpy as np
from llama_index import ServiceContext, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.node_parser import SentenceWindowNodeParser, HierarchicalNodeParser, get_leaf_nodes
from llama_index.indices.postprocessor import MetadataReplacementPostProcessor, SentenceTransformerRerank
from llama_index.retrievers import AutoMergingRetriever
from llama_index.query_engine import RetrieverQueryEngine
from trulens_eval import Feedback, TruLlama
from trulens_eval import OpenAI as fOpenAI
from trulens_eval.feedback import Groundedness

############################################################################## Function 1 ###########################################################
def build_sentence_window_index(
    documents,
    llm,
    embed_model="local:BAAI/bge-small-en-v1.5",
    sentence_window_size=3,
    save_dir="sentence_index",
):
    # create the sentence window node parser w/ default settings
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=sentence_window_size,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )
    sentence_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=node_parser,
    )
    if not os.path.exists(save_dir):
        sentence_index = VectorStoreIndex.from_documents(
            documents, service_context=sentence_context
        )
        sentence_index.storage_context.persist(persist_dir=save_dir)
    else:
        sentence_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=sentence_context,
        )

    return sentence_index

############################################################################## Function 2 ###########################################################
def get_sentence_window_query_engine(
    sentence_index, similarity_top_k=6, rerank_top_n=2
):
    # define postprocessors
    postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )

    sentence_window_engine = sentence_index.as_query_engine(
        similarity_top_k=similarity_top_k, node_postprocessors=[postproc, rerank]
    )
    return sentence_window_engine

############################################################################## Function 3 ###########################################################
def build_automerging_index(
        documents,
        llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        save_dir="merging_index",
        chunk_sizes=None
):
    # chunk sizes for all the layers (factor of 4)
    chunk_sizes = chunk_sizes or [2048, 512, 128]

    # Hierarchical node parser to parse the tree nodes (parent and children)
    node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)

    # getting all intermediate and parent nodes
    nodes = node_parser.get_nodes_from_documents(documents)

    # getting only the leaf nodes
    leaf_nodes = get_leaf_nodes(nodes)

    # required service context to initialize both llm and embed model
    merging_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model
    )

    # storage context to store the intermediate and parent nodes in a docstore, because the index is built only on the leaf nodes
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)

    if not os.path.exists(save_dir):
        automerging_index = VectorStoreIndex(
            leaf_nodes, storage_context=storage_context, service_context=merging_context
        )
        automerging_index.storage_context.persist(persist_dir=save_dir)

    else:
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=merging_context
        )
    
    return automerging_index

############################################################################## Function 4 ###########################################################
def get_automerging_query_engine(
        automerging_index,
        similarity_top_k=12,
        rerank_top_n=6,
):
    # retriever is used to merge the child nodes into the parent nodes
    base_retriever = automerging_index.as_retriever(similarity_top_k=similarity_top_k)
    retriever = AutoMergingRetriever(
        base_retriever, automerging_index.storage_context, verbose=True
    )

    # Ranking is used to select top k relevant chunks from similarity_top_k
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model='BAAI/bge-reranker-base'
    )

    # getting query engine with the above mentioned retiriever and reranker
    automerging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )

    return automerging_engine

############################################################################## Function 5 ###########################################################
def get_prebuilt_trulens_recorder(query_engine, app_id):

    # Feedback functions
    # Answer Relevance
    provider = fOpenAI()

    f_qa_relevance = Feedback(
        provider.relevance_with_cot_reasons,
        name="Answer Relevance"
    ).on_input_output()

    # Context Relevance
    context_selection = TruLlama.select_source_nodes().node.text

    f_qs_relevance = (
    Feedback(provider.qs_relevance,
            name="Context Relevance")
        .on_input()
        .on(context_selection)
        .aggregate(np.mean)
    )

    # Groundedness
    grounded = Groundedness(groundedness_provider=provider)

    f_groundedness = (
        Feedback(grounded.groundedness_measure_with_cot_reasons,
                name="Groundedness"
                )
        .on(context_selection)
        .on_output()
        .aggregate(grounded.grounded_statements_aggregator)
    )

    tru_recorder = TruLlama(
        query_engine,
        app_id=app_id,
        feedbacks = [
            f_qa_relevance,
            f_qs_relevance,
            f_groundedness
        ]
    )

    return tru_recorder
