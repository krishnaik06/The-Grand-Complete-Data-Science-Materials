import streamlit as st
import os
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings  import OpenAIEmbeddings

from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback # helps us to know how much it costs us for each query

from dotenv import load_dotenv


#side bar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.markdown("""
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [Langchain](https://python.langchian.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    - [Github](https://github.com/praj2408/Langchain-PDF-App-GUI) Repository
                
    """)
    add_vertical_space(5)
    st.write("Made by Tejaswini N R.")
    
    
load_dotenv()
    
def main():
    st.header("Chat with PDF 💬")
    
    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    #st.write(pdf)
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, # it will divide the text into 800 chunk size each (800 tokens)
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)
        
        #st.write(chunks)
        
        
        ## embeddings
        
        store_name = pdf.name[:-4]
        
        
        vector_store_path = os.path.join('vector_store', store_name)
        
        
        if os.path.exists(f"{vector_store_path}.pkl"):
            with open(f"{vector_store_path}.pkl", 'rb') as f:
                VectorStore = pickle.load(f)
            # st.write("Embeddings loaded from the Disk")
                
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{vector_store_path}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
            
            # st.write("Embeddings Computation Completed ")
            
        
        # Accept user questions/query
        query = st.text_input("Ask questions about your PDF file")
        #st.write(query)
        
        if query:
            
            docs = VectorStore.similarity_search(query=query, k=3) # k return the most relevent information
            
            llm = OpenAI(model_name='gpt-3.5-turbo')
            chain = load_qa_chain(llm=llm, chain_type='stuff')
            with get_openai_callback() as cb:
                
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)
            
            
            

    
    
    
if __name__ == "__main__":
    main()
    