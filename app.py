import streamlit as st
from google import genai
from pypdf import PdfReader

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="SPPU AI Exam Analyzer 2026", layout="wide", page_icon="📚")

st.title("📚 SPPU Syllabus & Exam Paper Analyzer")
st.markdown("Automated Analysis for Savitribai Phule Pune University Engineering Curriculum.")

# --- 2. SIDEBAR SETUP ---
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Updated 2026 Model Selection
model_options = {
    "Gemini 3.1 Pro (Best Reasoning)": "gemini-3.1-pro-preview",
    "Gemini 3 Flash (Fast & Balanced)": "gemini-3-flash-preview",
    "Gemini 2.5 Pro (Stable Deep Analysis)": "gemini-2.5-pro"
}
selected_model_name = st.sidebar.selectbox("Select AI Model", list(model_options.keys()))
model_id = model_options[selected_model_name]

# --- 3. HELPER FUNCTIONS ---
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted: text += extracted
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    return text

# --- 4. MAIN LOGIC ---
if api_key:
    try:
        # Initializing the 2026 Client
        client = genai.Client(api_key=api_key)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Step 1: Upload Syllabus")
            syllabus_file = st.file_uploader("Upload Syllabus PDF", type="pdf")
            
        with col2:
            st.subheader("Step 2: Upload Past Papers")
            exam_files = st.file_uploader("Upload Question Papers", type="pdf", accept_multiple_files=True)

        if st.button("🚀 Analyze Exam Pattern"):
            if syllabus_file and exam_files:
                with st.spinner(f"Analyzing using {selected_model_name}..."):
                    syllabus_content = get_pdf_text([syllabus_file])
                    exams_content = get_pdf_text(exam_files)

                    prompt = rf"""
You are an expert academic analyst for SPPU. Analyze the Syllabus and Past Papers.

SYLLABUS: {syllabus_content[:10000]} 
PAST PAPERS: {exams_content[:20000]}

Format:
### 1. 📈 Unit-Wise Weightage
Identify In-Sem (30m) vs End-Sem (70m) focus units.
### 2. 🔥 The Gold List
Repeated topics (3+ appearances).
### 3. 🎯 Predicted Questions
5 high-probability questions with difficulty ratings.
### 4. 💡 Smart Study Strategy
80/20 rule application for this subject.
"""
                    try:
                        # Updated Generation Call
                        response = client.models.generate_content(
                            model=model_id,
                            contents=prompt
                        )
                        st.success("Analysis Complete!")
                        st.markdown("---")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"AI Generation Error: {e}")
                        st.info("If you see a 404, please check if your API key has 'Gemini 3' enabled in Google AI Studio.")
            else:
                st.warning("Please upload all required PDFs.")
                
    except Exception as e:
        st.error(f"Client Configuration Error: {e}")
else:
    st.info("👋 Enter your API Key in the sidebar to begin.")

st.caption("2026 Edition | SPPU Engineering Success Tool")
