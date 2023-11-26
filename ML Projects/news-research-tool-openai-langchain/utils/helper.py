import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

#load openAI api key - environment variable
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# import necessary libraries
import pandas as pd
import numpy as np

# Libraries for Document Loaders
from langchain.document_loaders import TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import UnstructuredURLLoader

# Text Splitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Vector Database and Sentence Embeddings
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import faiss

# Libraries required for retrieval 
import streamlit as st
import pickle
import time
import langchain
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.embeddings import OpenAIEmbeddings
