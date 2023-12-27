from dataclasses import dataclass
from typing import Literal
import streamlit as st
import os
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.embeddings import HuggingFaceEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import streamlit.components.v1 as components
import time

HUGGINGFACEHUB_API_TOKEN = st.secrets['HUGGINGFACEHUB_API_TOKEN']
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
speed = 10


@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["👤 Human", "👨🏻‍⚖️ Ai"]
    message: str


def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings


def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "conversation" not in st.session_state:
        llama = LlamaAPI(st.secrets["LlamaAPI"])
        model = ChatLlamaAPI(client=llama)

        embeddings = download_hugging_face_embeddings()

        # Initializing the Pinecone
        pinecone.init(
            api_key=st.secrets["PINECONE_API_KEY"],  # find at app.pinecone.io
            environment=st.secrets["PINECONE_API_ENV"]  # next to api key in console
        )
        index_name = "legal-advisor"  # put in the name of your pinecone index here

        docsearch = Pinecone.from_existing_index(index_name, embeddings)

        prompt_template = """
            You are a trained bot to guide people about Indian Law. You will answer user's query with your knowledge and the context provided. 
            If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
            Do not say thank you and tell you are an AI Assistant and be open about everything.
            Use the following pieces of context to answer the users question.
            Context: {context}
            Question: {question}
            Only return the helpful answer below and nothing else.
            Helpful answer:
            """

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}
        retrieval_chain = RetrievalQA.from_chain_type(llm=model,
                                                      chain_type="stuff",
                                                      retriever=docsearch.as_retriever(
                                                          search_kwargs={'k': 2}),
                                                      return_source_documents=True,
                                                      chain_type_kwargs=chain_type_kwargs)

        st.session_state.conversation = retrieval_chain


def on_click_callback():
    human_prompt = st.session_state.human_prompt
    response = st.session_state.conversation(
        human_prompt
    )
    llm_response = response['result']
    st.session_state.history.append(
        Message("👤 Human", human_prompt)
    )
    st.session_state.history.append(
        Message("👨🏻‍⚖️ Ai", llm_response)
    )


initialize_session_state()

st.title("LegalEase Advisor Chatbot 🇮🇳")

st.markdown(
    """
    👋 **Namaste! Welcome to LegalEase Advisor!**
    I'm here to assist you with your legal queries within the framework of Indian law. Whether you're navigating through specific legal issues or seeking general advice, I'm here to help.
    
    📚 **How I Can Assist:**
    
    - Answer questions on various aspects of Indian law.
    - Guide you through legal processes relevant to India.
    - Provide information on your rights and responsibilities as per Indian legal standards.
    
    ⚖️ **Disclaimer:**
    
    While I can provide general information, it's essential to consult with a qualified Indian attorney for advice tailored to your specific situation.
    
    🤖 **Getting Started:**
    
    Feel free to ask any legal question related to Indian law, using keywords like "property rights," "labor laws," or "family law." I'm here to assist you!
    Let's get started! How can I assist you today?
    """
)

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

with chat_placeholder:
    for chat in st.session_state.history:
        st.markdown(f"{chat.origin} : {chat.message}")

with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit",
        type="primary",
        on_click=on_click_callback,
    )