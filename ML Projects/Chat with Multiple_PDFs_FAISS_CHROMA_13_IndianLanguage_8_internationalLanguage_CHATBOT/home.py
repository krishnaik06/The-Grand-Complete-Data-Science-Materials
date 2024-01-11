import streamlit as st
import streamlit_authenticator as stauth
import yaml
from utils import add_company_logo
from yaml.loader import SafeLoader
from st_pages import Page, show_pages
st.set_page_config(layout = "wide")

def main():
    add_company_logo()

    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    st.title("Welcome to Shankesh Chatbot with PDF 🎈")
    st.subheader('Introduction')
    st.write('This application is designed to retrieve information from a PDF file by asking question related to it. We have used OpenAI Embeddings and LLM with FAISS and CHROMA vector stores.')
    st.subheader('Guidance')
    st.write('Initally step is a create a username and password using Register tab in sidebar. Then login to the application and upload single/multiple PDFs to extract the data into textual format. Then OpenAI embeddings are created and stored in vector DB(either FAISS or CHROMA). After creating embeddings click on the chat tab to begin the conversation with AI. You can choose the language as per your interest (English and Major Indian Languages')
    show_pages([Page("home.py", "Home"),
                Page("chat.py", "Chat", in_section=False),
                Page("login.py", "Login"), 
                Page("register.py", "Register"), 
                Page("reset_pass.py", "Change Password"),
                Page("forgot_pass.py", "Forgot Password"), 
                Page("update_profile.py", "Update Profile"), 
                Page("about.py", "About")
                ])
    

if __name__ == '__main__':
    main()