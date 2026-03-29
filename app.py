import streamlit as st
from google import genai
from pypdf import PdfReader

# --- 1. PAGE & STYLE ---
st.set_page_config(page_title="SPPU Exam AI", layout="wide", page_icon="🎓")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .report-text { font-size: 1.1rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 SPPU Syllabus & Exam Pattern Analyzer")
st.info("Upload your Syllabus and Past Papers to generate an AI-powered success roadmap.")

# --- 2. SECURE API CONFIGURATION ---
# Checks Streamlit Secrets first, then falls back to sidebar for local testing
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.warning("API Key not found in Secrets.")
        api_key = st.text_input("Enter API Key for Local Testing", type="password")

# --- 3. CORE FUNCTIONS ---
def extract_text_from_pdfs(pdf_list):
    full_text = ""
    for pdf in pdf_list:
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                content = page.extract_text()
                if content: full_text += content + "\n"
        except Exception as e:
            st.error(f"Error reading {pdf.name}: {e}")
    return full_text

# --- 4. APP LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Step 1: Syllabus")
    syllabus_file = st.file_uploader("Upload PDF", type="pdf", key="syl")

with col2:
    st.subheader("📝 Step 2: Past Papers")
    paper_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True, key="papers")

if st.button("🚀 Generate Success Blueprint"):
    if not api_key:
        st.error("Please provide an API Key to continue.")
    elif syllabus_file and paper_files:
        try:
            # Initialize 2026 Client
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Analyzing SPPU patterns... this takes about 30 seconds."):
                # Process Data
                syl_text = extract_text_from_pdfs([syllabus_file])
                exam_text = extract_text_from_pdfs(paper_files)

                # 2026 Ref
