# app.py (Main entry point)
import streamlit as st

st.set_page_config(
    page_title="RAG Q&A System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
#loading the logo
import base64

# Convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("assets/Knowlens.png")

st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

div.block-container{padding-top:2rem;}    
.stApp {
    background: #fafafa;
    font-family: "Comic Neue", "Poppins", "Segoe UI", system-ui, sans-serif;
}
.card {
    background: #ffffff;
    padding: 2.3rem 2rem;
    border-radius: 0;       
    border: 4px solid #000;
    box-shadow:
        8px 8px 0px #000,
        0 14px 32px rgba(0, 0, 0, 0.22);
    margin: 1.5rem;
    text-align: center;
    transition: all 0.25s ease;
    position: relative;
}
.card:hover {
    transform: translate(-5px, -5px);
    box-shadow:
        14px 14px 0px #000,
        0 20px 44px rgba(0, 0, 0, 0.28);
}
.icon {
    font-size: 4.5rem;
    margin-bottom: 1rem;
    text-shadow:
        3px 3px 0px rgba(0, 0, 0, 0.35);
}
.card h2 {
    font-size: 1.7rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}
.card p {
    color: #333;
    font-size: 1rem;
    line-height: 1.6;
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

.stMarkdown p:last-child {
    font-size: 0.9rem;
    opacity: 0.9;
}
img {
    border-radius: 0 !important;
}
.header-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 0.4rem;
}

.header-logo {
    width: 70px;
    height: 70px;
    object-fit: contain;
}

.header-title {
    font-size: 3.2rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #111;
    line-height: 1;
}

</style>
""", unsafe_allow_html=True)



st.markdown(f"""
<div class="header-row">
    <img 
        src="data:image/png;base64,{logo_base64}" 
        class="header-logo"
        alt="Knowlens Logo"
    />
    <div class="header-title">Knowlens</div>
</div>

<div style="
    text-align:center;
    font-size:1.5rem;
    letter-spacing:0.18em;
    color:#555;
    margin-bottom:3rem;
">
    INTELLIGENT Q&A SYSTEM
</div>
""", unsafe_allow_html=True)



st.markdown("<p style='text-align: center; color: black; font-size: 1.2rem; margin-bottom: 3rem;'>Choose your input method</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='icon'>📄</div>
        <h2 style='color: #667eea;'>PDF Documents</h2>
        <p style='color: #666;'>Upload and analyze PDF documents with AI-powered Q&A</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📄 Go to PDF Q&A", use_container_width=True):
        st.switch_page("pages/1_PDF_QA.py")

with col2:
    st.markdown("""
    <div class='card'>
        <div class='icon'>🌐</div>
        <h2 style='color: #764ba2;'>Website Content</h2>
        <p style='color: #666;'>Extract and analyze content from any website URL</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌐 Go to Website Q&A", use_container_width=True):
        st.switch_page("pages/2_Website_QA.py")

st.markdown('<hr style="border: 0; border-top: 2px solid black; margin: 20px 0; background: transparent;">', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black; opacity: 0.8;'>Powered by AI • Built with Streamlit</p>", unsafe_allow_html=True)