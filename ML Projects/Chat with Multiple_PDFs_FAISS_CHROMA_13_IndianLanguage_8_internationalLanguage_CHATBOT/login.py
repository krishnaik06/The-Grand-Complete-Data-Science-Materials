import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from utils import add_company_logo, extract_pdf, process_text, hide_bar
from st_pages import Page, show_pages, add_indentation
from dotenv import load_dotenv

st.set_page_config(page_title='Login')
def main():
    load_dotenv()
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
    authenticator.login('Login', 'main')

    if st.session_state["authentication_status"]:
        with st.container():
            st.title(f'Welcome *{st.session_state["name"]}*')
            with st.sidebar:
                authenticator.logout("Logout", "sidebar")
            pdf_folder = st.file_uploader("Upload your PDF Document",type="pdf",accept_multiple_files=True)           

        process_button=st.button("Proceed")
        if process_button:
            raw_text = extract_pdf(pdf_folder)
            process_text(raw_text)        

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

if __name__ == '__main__':
    main()