import streamlit as st
from google import genai
from pypdf import PdfReader

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SPPU Exam AI", layout="wide", page_icon="🎓")

st.title("🎓 SPPU Syllabus & Exam Pattern Analyzer")
st.markdown("Automated Pattern Analysis for Savitribai Phule Pune University.")

# --- 2. SECURE API SETUP ---
# It looks for "GEMINI_API_KEY" in the Streamlit Cloud Secrets dashboard.
# If found, the sidebar input will stay hidden.
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    st.sidebar.success("✅ Connected to SPPU AI Engine")
else:
    st.sidebar.warning("⚠️ Developer Mode: Secret Key Not Found")
    api_key = st.sidebar.text_input("Enter Gemini API Key (Manual)", type="password")

# --- 3. PDF EXTRACTION HELPER ---
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted: text += extracted + "\n"
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    return text

# --- 4. MAIN INTERFACE ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Step 1: Upload Syllabus")
    syllabus_file = st.file_uploader("Upload Syllabus PDF", type="pdf", key="syl")
with col2:
    st.subheader("Step 2: Upload Past Papers")
    exam_files = st.file_uploader("Upload Question Papers", type="pdf", accept_multiple_files=True, key="papers")

if st.button("🚀 Run AI Analysis"):
    if not api_key:
        st.error("Missing API Key. Please add it to Streamlit Secrets.")
    elif syllabus_file and exam_files:
        try:
            # Initialize the 2026 SDK Client
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Analyzing papers... please wait."):
                syl_content = get_pdf_text([syllabus_file])
                exam_content = get_pdf_
