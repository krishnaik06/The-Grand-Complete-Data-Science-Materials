from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader, PDFMinerLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import Filter
from qdrant_client.http import models as rest
from sentence_transformers import SentenceTransformer
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from config import settings
import uuid
import logging


logging.basicConfig(level=logging.INFO, format='=========== %(asctime)s :: %(levelname)s :: %(message)s')

MetadataFilter = Dict[str, Union[str, int, bool]]
COLLECTION_NAME = 'qa_collection'

embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

qa_chain = load_qa_chain(llm=OpenAI(openai_api_key=settings.openai_api_key, streaming=False), chain_type="stuff", verbose=False)


class QdrantIndex():

    def __init__(self, qdrant_host: str, qdrant_api_key: str, prefer_grpc: bool):
        if qdrant_host == 'localhost':
            self.qdrant_client = QdrantClient(
                url="10.0.222.59", #change it according to cluster ip address kubernetes
            )
        else:
            self.qdrant_client = QdrantClient(
                host=qdrant_host, 
                prefer_grpc=prefer_grpc,
                api_key=qdrant_api_key
            )
        self.embedding_model =  embedding_model
        self.embedding_size = self.embedding_model.get_sentence_embedding_dimension()
        self.collection_name = COLLECTION_NAME
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.embedding_size, distance=Distance.COSINE),
        ) 
        logging.info(f"Collection {COLLECTION_NAME} is successfully created.")

    
    def insert_into_index(self, filepath: str, filename: str):
        """ Adds new documents into the index

        Args:
            filepath (str): full path of the pdf file
            filename (str): name of pdf file
        """
        loader = PDFMinerLoader(filepath)
        docs = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=30)
        documents = text_splitter.split_documents(docs)

        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        ids = [uuid.uuid4().hex for _ in texts]
        vectors = self.embedding_model.encode(texts, show_progress_bar=False, batch_size=128).tolist()
        payloads = self.build_payloads(
                    texts,
                    metadatas,
                    'page_content',
                    'metadata',
                )
        # Upload points in bactches
        self.qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=rest.Batch(
                ids=ids,
                vectors=vectors,
                payloads=payloads
            ),
        )
        logging.info("Index update successfully done!")
        

    def generate_response(self, question: str):
        relevant_docs = self.similarity_search_with_score(query=question)
        return (qa_chain.run(input_documents=relevant_docs, question=question), relevant_docs)
    
     
    # Adopted from lanchain github            
    def build_payloads(self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]],
        content_payload_key: str,
        metadata_payload_key: str,
    ) -> List[dict]:
        payloads = []
        for i, text in enumerate(texts):
            if text is None:
                raise ValueError(
                    "At least one of the texts is None. Please remove it before "
                    "calling .from_texts or .add_texts on Qdrant instance."
                )
            metadata = metadatas[i] if metadatas is not None else None
            payloads.append(
                {
                    content_payload_key: text,
                    metadata_payload_key: metadata,
                }
            )

        return payloads
    
    def similarity_search_with_score(
        self, query: str, k: int = 5, filter: Optional[MetadataFilter] = None
    ) -> List[Tuple[Document, float]]:
        """Return docs most similar to query.
        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: Filter by metadata. Defaults to None.
        Returns:
            List of Documents most similar to the query and score for each
        """
        embedding = self.embedding_model.encode(query)
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            query_filter=Filter(**filter) if filter else None,
            with_payload=True,
            limit=k,
        )
        for r in results:
            print(r)
            print()
        return [
            Document(
                 page_content=result.payload['page_content'],
                 metadata=result.payload['metadata']
            )
            for result in results
        ]










