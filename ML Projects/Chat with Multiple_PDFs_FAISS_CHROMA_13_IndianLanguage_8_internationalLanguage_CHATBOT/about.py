import streamlit as st
from utils import add_company_logo
st.set_page_config(layout='wide')

def main():
    add_company_logo()
    st.title('About Page  🎈!!')
    st.subheader('Hi, My name is Shankesh Raju MS')
    st.markdown('This is my first Generative AI project for internship. I completed my Engineering in Computer Science in 2013 and worked as Vmware Cloud system administrator in Wipro. Later I quit my job for UPSC preparation till 2021. After that I started studying Machine Learning to get a job for financial reasons... Step by step I studied frameworks necessary for impelementing and deploying ML modules in realtime.')

if __name__ == '__main__':
    main()