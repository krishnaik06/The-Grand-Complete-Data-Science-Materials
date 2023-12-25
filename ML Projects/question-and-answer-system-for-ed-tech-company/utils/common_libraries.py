import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

# For Loading environment variables
from dotenv import load_dotenv, find_dotenv

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
from langchain.embeddings import HuggingFaceInstructEmbeddings
import faiss
import pickle

# Libraries for retrieval
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# API
from fastapi import FastAPI
from pydantic import BaseModel