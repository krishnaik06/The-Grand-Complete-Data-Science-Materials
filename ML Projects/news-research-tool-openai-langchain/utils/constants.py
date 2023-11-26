import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

FILE_PATH = "data/indexes/faiss_store_openai.pkl"
PROCESSED_URLS_PATH = "data/indexes/processed_urls.pkl"
