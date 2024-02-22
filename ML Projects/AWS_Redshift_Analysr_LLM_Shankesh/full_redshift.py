from lyzr import DataConnector, DataAnalyzr
from streamlit_extras.grid import grid
import streamlit as st
from dotenv import load_dotenv
import shutil
import os


st.set_page_config(layout='wide')
st.title('AWS RedShift Analyser with Lyzr')
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

with st.sidebar:
    host_url = st.text_input('Enter the RedShift host URL')
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    with col1:
        username = st.text_input('Enter the username')
    with col2:
        password = st.text_input('Enter the password', type="password")
    with col3:
        db_name = st.text_input('database name')
    with col4:
        schema = st.text_input('Enter the schema')
    with col5:
        table_name = st.text_input('Enter the table name')
    with col6:
        st.session_state.api_key = st.text_input('OpenAI API Key', type='password')
    submitBtn = st.button('Proceed')

if submitBtn:
    st.session_state.dataframe = DataConnector().fetch_dataframe_from_redshift(
        host=host_url,  
        database=db_name,  
        user=username, 
        password=password,  
        schema=schema,  
        table=table_name, 
        port=5439,
    )
col1, col2 = st.columns([0.7, 0.3], gap='large')
with col1:
    if st.session_state.dataframe is not None:
        st.dataframe(st.session_state.dataframe)
    else:
        st.write('Enter credentials to view the database')

with col2:
    st.subheader('Suggestions')

    mygrid = grid(3, 1, 2, vertical_align="center")
    data_desc = mygrid.button('Data Description')
    analysis_query = mygrid.button('Exploratory Analysis')
    analysis_recom = mygrid.button('Recommended Analysis')

    st.subheader('User queries')
    user_input = st.text_input('Enter the query?')

    col1, col2 = st.columns(2)
    with col1:
        user_query = st.button('Text Query')
    with col2:
        visual_query = st.button('Visualization Query')

try:
    data_analyzr = DataAnalyzr(df=st.session_state.dataframe, api_key=st.session_state.api_key)
except:
    print('load credentials')

if user_query:
    analysis = data_analyzr.analysis_insights(user_input=user_input)
    st.write(analysis)
if analysis_recom:
    analysis_recommendation = data_analyzr.analysis_recommendation()
    st.write(analysis_recommendation)
if data_desc:
    description = data_analyzr.dataset_description()
    st.write(description)
if analysis_query:
    queries = data_analyzr.ai_queries_df()
    st.write(queries)
if visual_query:
    shutil.rmtree('./generated_plots')
    visualization = data_analyzr.visualizations(user_input=user_input)
    folder = "./generated_plots"
    for images in os.listdir(folder):
        if images.endswith('.png'):
            st.image(f"./generated_plots/{images}")
    



    
    
    
    
    
    
