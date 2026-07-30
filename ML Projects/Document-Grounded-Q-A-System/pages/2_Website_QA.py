# pages/2_Website_QA.py
import streamlit as st
from ingest.web_Ingestion import load_website
from retrieval.retriever import create_vector_store
from retrieval.qa_chain import build_qa_chain
from utils import format_sources

st.set_page_config(
    page_title="Website Q&A",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container{padding-top:2rem;}
    .stApp {
        background: #fafafa;
        font-family: "Comic Neue", "Poppins", "Segoe UI", system-ui, sans-serif;
    }
    h2 {
        text-align:center;
        font-size:1.5rem;
        text-transform:uppercase;
        letter-spacing:0.1em;
        color:black !important;
        margin-bottom:3rem;
    }
    .stButton > button {
    background: #ffdd57;
    color: black !important;   
    border: 3px solid #000;
    padding: 0.75rem 2.2rem;
    border-radius: 0;          
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    box-shadow: 5px 5px 0px #000;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #ffd000;
    transform: translate(-3px, -3px);
    box-shadow: 8px 8px 0px #000;
}
.stButton > button:active {
    transform: translate(2px, 2px);
    box-shadow: 3px 3px 0px #000;
}
    .stTextInput>div>div>input {
        color:white;
        border-radius: 10px;
        border: 0px solid #000 !important;
        padding: 0.75rem;
        background-color: black !important;
    }
    .stFileUploader>div>div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px dashed #9f7aea !important;
        border-radius: 10px;
        color:black;
    }
    .info-msg {
        background: #262626;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .stSpinner > div {
        border-top-color: black !important;
    }
    .stSpinner > div > div {
        color: black !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stSuccess {
        background-color: #10b981 !important;
        color: white !important;
        border-left: 5px solid #059669 !important;
        font-weight: 600;
    }
    
    .stSuccess > div {
        color: white !important;
    }
    p {
        color: black;
        font-weight:bold;
        font-size: 1.2rem;
        text-align: center;
    }
    .stFileUploader section[data-testid="stFileUploaderDropzoneInstructions"] + div {
        color: black !important;
    }

    .stFileUploader [data-testid="stFileUploaderFileName"] {
        color: black !important;
        font-weight: 600 !important;
    }

    .stFileUploader [data-testid="stFileUploaderFileSize"] {
        color: #666 !important;
    }
    p {
        color: black;
        font-weight:bold;
        font-size: 1.2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

pdf_keys = [
    "pdf_docs",
    "pdf_vector_store",
    "pdf_qa_chain",
    "pdf_retriever",
    "pdf_current_file",
    "pdf_question",
    "pdf_uploader"
]

for k in pdf_keys:
    if k in st.session_state:
        del st.session_state[k]


# Initialize session state for Website page
if 'web_docs' not in st.session_state:
    st.session_state.web_docs = []
if 'web_vector_store' not in st.session_state:
    st.session_state.web_vector_store = None
if 'web_qa_chain' not in st.session_state:
    st.session_state.web_qa_chain = None
if 'web_retriever' not in st.session_state:
    st.session_state.web_retriever = None
if 'web_current_url' not in st.session_state:
    st.session_state.web_current_url = None

st.markdown("<h2>🌐 Website Q&A System</h2>", unsafe_allow_html=True)

# Back button
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)

# URL input
url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com",
    help="Provide a website URL to extract content",
    key="web_url_input"
)


load_btn = st.button("🔍 Load Website")

if url and load_btn and url != st.session_state.web_current_url:

    # Check if it's a DIFFERENT URL (new website)
    if url != st.session_state.web_current_url:
        # Clear old website context completely
        st.session_state.web_docs = []
        st.session_state.web_vector_store = None
        st.session_state.web_qa_chain = None
        st.session_state.web_retriever = None
        
        with st.spinner("🌐 Fetching website content..."):
            try:
                st.session_state.web_docs = load_website(url)
                st.session_state.web_current_url = url
                
                st.success(f"✅ Successfully loaded {len(st.session_state.web_docs)} chunks from NEW website!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error loading website: {str(e)}")
    else:
        st.info("ℹ️ This URL is already loaded")

# Display status and Q&A section
if st.session_state.web_docs:
    st.markdown(f"<div class='info-msg'><strong>Current Website:</strong> {st.session_state.web_current_url}<br><strong>Chunks:</strong> {len(st.session_state.web_docs)} text chunks ready</div>", unsafe_allow_html=True)
    
    # Build vector store
    if st.session_state.web_vector_store is None:
        with st.spinner("🔧 Building knowledge base..."):
            st.session_state.web_vector_store = create_vector_store(st.session_state.web_docs)
            st.session_state.web_qa_chain, st.session_state.web_retriever = build_qa_chain(st.session_state.web_vector_store)
    
    st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: black;">💬 Ask Your Question</h3>', unsafe_allow_html=True)

    
    question = st.text_input(
        "What would you like to know?",
        placeholder="Type your question here...",
        key="web_question"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ask_button = st.button("🚀 Get Answer", use_container_width=True)
    
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            keys_to_clear = [
                "web_docs",
                "web_vector_store",
                "web_qa_chain",
                "web_retriever",
                "web_current_url",
                "web_question",
                "web_url_input"
            ]

            for k in keys_to_clear:
                if k in st.session_state:
                    del st.session_state[k]

            st.rerun()

    
    if question and ask_button:
        with st.spinner("🤔 Thinking..."):
            result = st.session_state.web_qa_chain.invoke(question)
            
            # Display answer
            st.markdown('<h3 style="color: black;">💡 Answer</h3>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#262626; 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        color: white; 
                        font-size: 1.1rem;
                        line-height: 1.6;'>
                {result}
            </div>
            """, unsafe_allow_html=True)
            
            # Display sources
            st.markdown('<h3 style="color: black;">📚 Sources</h3>', unsafe_allow_html=True)
            source_docs = st.session_state.web_retriever.invoke(question)
            sources = format_sources(source_docs)
            
            for i, src in enumerate(sources, 1):
                st.markdown(f"""
                <div style='background: #262626; 
                            padding: 1.5rem; 
                            border-radius: 12px; 
                            border-left: 8px solid #ffdd57; 
                            margin: 1rem 0;'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <span style='background: #262626; 
                                     color: white; 
                                     border-radius: 50%; 
                                     width: 30px; 
                                     height: 30px; 
                                     display: inline-flex; 
                                     align-items: center; 
                                     justify-content: center; 
                                     margin-right: 0.5rem;
                                     font-weight: bold;'>{i}</span>
                        <strong style='color: #fafafa;'>🌐 {src['source']}</strong>
                    </div>
                    <div style='background: white; 
                                padding: 1rem; 
                                border-radius: 8px; 
                                font-family: monospace;
                                color: #555;
                                border-left: 3px solid #e0e0e0;
                                white-space: pre-wrap;'>
                        "{src['excerpt']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("👆 Enter a website URL above and click Load Website to get started")

st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black; opacity: 0.8;'>Website Q&A • Powered by AI</p>", unsafe_allow_html=True)