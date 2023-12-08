
from constant import #API KEY FILE
from constant import #API KEY FILE
import streamlit as st
import os
from langchain.llms import OpenAI,GooglePalm
from langchain.embeddings import OpenAIEmbeddings,GooglePalmEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from langchain.callbacks import get_openai_callback

os.environ['OPENAI_API_KEY'] =
os.environ['GOOGLE_API_KEY'] =
text=""
def main():
    global text
    st.set_page_config("LangChain application to chat with PDFs")
    st.header("Ask a Question")

    pdf = st.file_uploader("Upload your PDF",type="pdf")

    if pdf is not None:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()

    text_splitter=CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    chunks=text_splitter.split_text(text)

    embeddings=OpenAIEmbeddings()
    knowledge=FAISS.from_texts(chunks,embeddings)

    user=st.text_input("Ask a question about your PDFs: ")
    if user:
        docs=knowledge.similarity_search(user)
        llm=OpenAI()
        chain=load_qa_chain(llm,chain_type="stuff")
        with get_openai_callback() as cb:
            response=chain.run(input_documents=docs,question=user)
            print(cb)
        st.write(response)

main()

