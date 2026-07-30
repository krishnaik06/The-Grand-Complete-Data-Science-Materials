from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu",
                    "token": os.getenv("HF_TOKEN"),
                      },
        encode_kwargs={
            "batch_size": 32,
            "normalize_embeddings": True
        }
    )

    # ALWAYS build fresh vector store
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


def get_retriever(vector_store):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
