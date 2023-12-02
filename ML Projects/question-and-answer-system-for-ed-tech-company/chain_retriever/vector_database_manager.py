import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils import *


class VectorDatabaseManager:
    def __init__(
        self,
        store_path,
        model_name,
        encode_kwargs,
        data_file_path,
        source_column,
        encoding,
    ):
        self.store_path = store_path
        self.model_name = model_name
        self.encode_kwargs = encode_kwargs
        self.data_file_path = data_file_path
        self.source_column = source_column
        self.encoding = encoding
        self.vectordb = None
        self._ensure_vector_db()

    def _ensure_vector_db(self):
        if not os.path.exists(self.store_path):
            self._create_vector_db()
        else:
            self._load_vector_db()

    def _create_vector_db(self):
        print("Downloading Instruct Embeddings Model...")
        instruct_embeddings = HuggingFaceInstructEmbeddings(
            model_name=self.model_name,
            encode_kwargs=self.encode_kwargs,
        )
        print("Downloading Instruct Embeddings Model completed.")

        print("Chunking CSV Data...")
        loader = CSVLoader(
            file_path=self.data_file_path,
            source_column=self.source_column,
            encoding=self.encoding,
        )
        data = loader.load()
        print("Chunking CSV Data completed.")

        print("Creating Word Embeddings...")
        self.vectordb = FAISS.from_documents(
            documents=data, embedding=instruct_embeddings
        )
        print("Creating Word Embeddings completed.")

        print("Saving the FAISS database as a pickle file...")
        with open(self.store_path, "wb") as f:
            pickle.dump(self.vectordb, f)
        print("Saving the FAISS database file completed.")

    def _load_vector_db(self):
        print("Loading the FAISS database as a pickle file...")
        with open(self.store_path, "rb") as f:
            self.vectordb = pickle.load(f)
        print("Loading the FAISS database as a pickle file completed.")

    def get_vector_db(self):
        return self.vectordb


vector_db_manager = VectorDatabaseManager(
    store_path=FAISS_STORE_PATH,
    model_name=HF_EMBEDDING_MODEL,
    encode_kwargs=ENCODE_KWARGS,
    data_file_path="data/codebasics_faqs.csv",
    source_column="prompt",
    encoding="cp1252",
)

