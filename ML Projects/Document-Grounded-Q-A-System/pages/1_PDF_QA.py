# pages/1_PDF_QA.py
import streamlit as st
from ingest.pdf_Ingest import load_pdf
from retrieval.retriever import create_vector_store
from retrieval.qa_chain import build_qa_chain
from utils import format_sources
import os

st.set_page_config(
    page_title="PDF Q&A",
    page_icon="📄",
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
</style>
""", unsafe_allow_html=True)

pdf_keys = [
    "web_docs",
    "web_vector_store",
    "web_qa_chain",
    "web_retriever",
    "web_current_file",
    "web_question",
    "web_uploader"
]

for k in pdf_keys:
    if k in st.session_state:
        del st.session_state[k]

# Initialize session state for PDF page ONLY
if 'pdf_docs' not in st.session_state:
    st.session_state.pdf_docs = []
if 'pdf_vector_store' not in st.session_state:
    st.session_state.pdf_vector_store = None
if 'pdf_qa_chain' not in st.session_state:
    st.session_state.pdf_qa_chain = None
if 'pdf_retriever' not in st.session_state:
    st.session_state.pdf_retriever = None
if 'pdf_current_file' not in st.session_state:
    st.session_state.pdf_current_file = None


st.markdown("<h2>📄 PDF Q&A System</h2>", unsafe_allow_html=True)

# Back button
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)

# File uploader
uploaded_pdf = st.file_uploader(
    "Upload a PDF document",
    type=["pdf", "txt", "doc", "docx", "csv"],
    help="Select a PDF, TXT, DOC, DOCX, or CSV file to analyze",
    key="pdf_uploader"
)

if uploaded_pdf:
    file_id = f"{uploaded_pdf.name}_{uploaded_pdf.size}"
    
    # Check if it's a DIFFERENT file (new upload)
    if file_id != st.session_state.pdf_current_file:
        # Clear old PDF context completely
        st.session_state.pdf_docs = []
        st.session_state.pdf_vector_store = None
        st.session_state.pdf_qa_chain = None
        st.session_state.pdf_retriever = None
        
        with st.spinner("📄 Processing PDF..."):
            import time
            temp_filename = f"temp_pdf_{int(time.time())}.pdf"
            
            try:
                # Save file
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_pdf.read())
                
                # Load and process NEW PDF
                st.session_state.pdf_docs = load_pdf(temp_filename)
                st.session_state.pdf_current_file = file_id
                
                if len(st.session_state.pdf_docs) == 0:
                    st.error("❌ No text could be extracted from this document. This might be:")
                    st.error("• A scanned PDF (image-based) - needs OCR")
                    st.error("• An encrypted/protected PDF")
                    st.error("• A corrupted file")
                    st.info("💡 Try converting the PDF to a searchable format or use a text-based version.")
                    
                    # Clear the failed attempt
                    st.session_state.pdf_docs = []
                    st.session_state.pdf_current_file = None
                    st.session_state.pdf_vector_store = None
                    st.session_state.pdf_qa_chain = None
                    st.session_state.pdf_retriever = None
                else:
                    # Success - set the current file
                    st.session_state.pdf_current_file = file_id
                # Vector store will be rebuilt in the next section
                
                # Cleanup temp file
                try:
                    os.remove(temp_filename)
                except:
                    pass
                
                st.success(f"✅ Successfully loaded {len(st.session_state.pdf_docs)} chunks from NEW PDF!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if os.path.exists(temp_filename):
                    try:
                        os.remove(temp_filename)
                    except:
                        pass
elif not uploaded_pdf and st.session_state.pdf_docs:
    keys_to_clear = [
        "pdf_docs",
        "pdf_vector_store",
        "pdf_qa_chain",
        "pdf_retriever",
        "pdf_current_file",
        "pdf_question",
        "pdf_uploader"
    ]

    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]

    st.rerun()


# Display status and Q&A section
if st.session_state.pdf_docs:
    st.markdown(f"<div class='info-msg'><strong>Current PDF:</strong> {uploaded_pdf.name if uploaded_pdf else 'Loaded'}<br><strong>Chunks:</strong> {len(st.session_state.pdf_docs)} text chunks ready</div>", unsafe_allow_html=True)
    
    # Build vector store
    if st.session_state.pdf_vector_store is None:
        with st.spinner("🔧 Building knowledge base..."):
            st.session_state.pdf_vector_store = create_vector_store(st.session_state.pdf_docs)
            st.session_state.pdf_qa_chain, st.session_state.pdf_retriever = build_qa_chain(st.session_state.pdf_vector_store)
    
    st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)

    st.markdown('<h3 style="color: black;">💬 Ask Your Question</h3>', unsafe_allow_html=True)
    
    question = st.text_input(
        "What would you like to know?",
        placeholder="Type your question here...",
        key="pdf_question"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ask_button = st.button("🚀 Get Answer", use_container_width=True)
    
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            keys_to_clear = [
                "pdf_docs",
                "pdf_vector_store",
                "pdf_qa_chain",
                "pdf_retriever",
                "pdf_current_file",
                "pdf_question",
                "pdf_uploader"
            ]

            for k in keys_to_clear:
                if k in st.session_state:
                    del st.session_state[k]

            st.rerun()

    
    if question and ask_button:
        with st.spinner("🤔 Thinking..."):
            result = st.session_state.pdf_qa_chain.invoke(question)
            
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
            source_docs = st.session_state.pdf_retriever.invoke(question)
            sources = format_sources(source_docs)
            
            for i, src in enumerate(sources, 1):
                st.markdown(f"""
                <div style='background: #262626 ; 
                            padding: 1.5rem; 
                            border-radius: 12px;
                            color:white; 
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
                        <strong style='color: #fafafa;'>📄 {src['source']}</strong>
                    </div>
                    <div style='color: #fafafa; margin-bottom: 0.5rem;'>
                        📍 Page {src['page']} of {src['total_pages']}
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
    st.info("👆 Upload a PDF document above to get started")

st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black; opacity: 0.8;'>PDF Q&A • Powered by AI</p>", unsafe_allow_html=True)