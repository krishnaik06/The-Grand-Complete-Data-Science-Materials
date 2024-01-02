import streamlit as st
from Algorithms.Abstraction import abstraction_call
from Algorithms.Extraction import extraction_summ
from Algorithms.open_ai import open_ai_gpt_call
from Algorithms.Fetch_text import fetch_from_url, fetch_from_documents, clean_text
from Algorithms.rouge_eval import rouge_eval
import validators

st.title('Text Summarization')
st.markdown('Source Code : [Github Repository]()')
st.write('Feel free to utilize our summarization service by either uploading a document in the specified format, '
         'entering text directly, or providing a URL link. Our summarization process ensures precision while '
         'retaining the authentic meaning of the content')
summ_type = st.sidebar.selectbox('Summarization type', ('Abstraction', 'Extraction', 'GPT-3.5-turbo'))
open_ai_key = ''
if summ_type == 'GPT-3.5-turbo':
    open_ai_key = st.sidebar.text_input('Open_ai_key')

st.markdown("""- Enter text in text box
 - Uploads Documents in .pdf/.txt/.docx format
 - Enter URL of article to get summered""")

st.markdown(
    "This app supports two type of summarization:\n"
    "\n"
    "1. **Extractive Summarization**: Condenses information by selecting key phrases directly from the original text.\n"
    "2. **Abstractive Summarization** : Rewrites the document's content to create a more human-like and concise summary.\n"
    "3. **OPEN-AI Summarization** : Provides abstraction based summarization using OPEN-AI GPT 3.5."
)

st.divider()

inputs = st.text_input('Enter the text or URL')
st.write("<h3 style='text-align: center; color: Black;'>OR</h3>",
         unsafe_allow_html=True, )
file_upload = st.file_uploader('Upload you pdf or Documents(.pdf,.docx,.txt)', type=['pdf', 'txt', '.docx'])
if validators.url(inputs):
    input_text_corpus = clean_text(fetch_from_url(inputs))
elif file_upload:
    input_text_corpus = fetch_from_documents(file_upload)
else:
    input_text_corpus = clean_text(inputs)
summarize = st.button('Summarize')
if summarize:
    if not input_text_corpus:
        st.error('NO INPUT TEXT FOUND')
    try:
        st.subheader('Input Text')
        st.write(input_text_corpus)
        if summ_type == 'Abstraction':
            with st.status('Wait for Abstraction Summarization'):
                response_text = abstraction_call(input_text_corpus)
        elif summ_type == 'Extraction':
            with st.status('Wait for Extraction Summarization'):
                response_text = extraction_summ(input_text_corpus)
        else:
            if not open_ai_key:
                st.error('NO GPT 3.5 KEYS FOUND', icon="🚨")
            with st.status('Wait for OpenAI GPT'):
                response_text = open_ai_gpt_call(input_text_corpus, open_ai_key)
        st.subheader('Summarized Text')
        st.write(response_text)
        st.subheader('Rouge Score')
        rouge_score = rouge_eval(input_text_corpus, response_text)
        st.json(rouge_score)
    except Exception:
        pass

