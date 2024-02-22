from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain_openai.llms.base import OpenAI
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, Chroma, Qdrant
from utils import translate_text, add_company_logo, lang_select
import time
import configparser

# Initialization
config = configparser.ConfigParser()
config.read('./config.ini') 
vec_db_name = config['VECTOR_DB']['MODEL_NAME']
llm = OpenAI(model_name = 'gpt-3.5-turbo-instruct')
embeddings = OpenAIEmbeddings()
if vec_db_name == 'FAISS':
    vector_db = FAISS.load_local("faiss_index", embeddings)
if vec_db_name == 'CHROMA':
    vector_db = Chroma(persist_directory="chroma_index", embedding_function=embeddings)
# if vec_db_name == 'QDRANT':
#     vector_db = Qdrant.load_local("qdrant_index", embeddings)
chain = load_qa_chain(llm, chain_type='stuff')
add_company_logo()


# Generate OpenAI Embeddings and indexing vector DB
def query_answer(query):
    docs = vector_db.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response
        
user_lang =st.selectbox('Select Language', (
    'English', 
    'Tamil', 
    'Hindi', 
    'Malayalam',
    'Kannada',
    'Telugu',
    'Marathi', 
    'Assamese', 
    'Bengali', 
    'Gujarati',
    'Konkani',
    'Oriya',
    'Punjabi',
    'Sanskrit',
    'Urdu',
    'Chinese(simplified)',
    'French',
    'Korean',
    'Japanese',
    'Portuguese',
    'Italian',
    'Russian'
    ))

def chatbox(target):
    if not st.session_state["authentication_status"]:
        st.subheader('Login and upload PDFs to access the chat module')
    
    else:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask question about PDF content?"):
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty() 
                raw_prompt = translate_text(prompt, 'auto', 'en')
                result = translate_text(query_answer(raw_prompt), 'en', target) 
                result2 = ""
                for chunk in result.split():
                    result2 += chunk + " "
                    time.sleep(0.1)
                    message_placeholder.markdown(result2 + "▌")

            st.session_state.messages.append({"role": "assistant", "content": result})

chatbox(lang_select(user_lang))
