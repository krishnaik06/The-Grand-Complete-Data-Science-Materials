import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils.common_libraries import *

_ = load_dotenv(find_dotenv())
PALM_API_KEY = os.getenv("PALM_API_KEY")

HF_EMBEDDING_MODEL = "thenlper/gte-large"
MODEL_KWARGS = {"device": "cuda"}
ENCODE_KWARGS = {"normalize_embeddings": True}

FAISS_STORE_PATH = "models/faiss_store.pkl"

prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
CHAIN_TYPE_KWARGS = {"prompt": PROMPT}