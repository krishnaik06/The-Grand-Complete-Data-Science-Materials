import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils import *

from chain_retriever.vector_database_manager import *


class QARetriever:
    def __init__(
        self,
        vector_db_manager,
        google_api_key,
        score_threshold,
        chain_type,
        input_key,
        return_source_documents,
        chain_type_kwargs,
    ):
        self.vector_db_manager = vector_db_manager
        self.google_api_key = google_api_key
        self.score_threshold = score_threshold
        self.chain_type = chain_type
        self.input_key = input_key
        self.return_source_documents = return_source_documents
        self.chain_type_kwargs = chain_type_kwargs

    def get_qa_chain(self, temperature, max_output_tokens):
        llm = GooglePalm(
            google_api_key=self.google_api_key,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        vectordb = self.vector_db_manager.get_vector_db()
        retriever = vectordb.as_retriever(score_threshold=self.score_threshold)

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type=self.chain_type,
            retriever=retriever,
            input_key=self.input_key,
            return_source_documents=self.return_source_documents,
            chain_type_kwargs=self.chain_type_kwargs,
        )
        return chain


# Initialize QARetriever
qa_retriever = QARetriever(
    vector_db_manager=vector_db_manager,
    google_api_key=PALM_API_KEY,
    score_threshold=0.7,
    chain_type="stuff",
    input_key="query",
    return_source_documents=True,
    chain_type_kwargs=CHAIN_TYPE_KWARGS,
)
