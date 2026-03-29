import streamlit as st
from google import genai
from pypdf import PdfReader

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SPPU Exam AI", layout="wide", page_icon="🎓")

st.title("🎓 SPPU Syllabus & Exam Pattern Analyzer")
st.markdown("Automated Pattern Analysis for Engineering Students.")

# --- 2. API KEY SETUP ---
# Priority 1: Streamlit Secrets (for published app)
# Priority 2: Sidebar Input (for local testing)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key (Dev Mode)", type="password")

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
    syllabus_file = st.file_uploader("Upload Syllabus PDF", type="pdf")
with col2:
    st.subheader("Step 2: Upload Past Papers")
    exam_files = st.file_uploader("Upload Question Papers", type="pdf", accept_multiple_files=True)

if st.button("🚀 Run AI Analysis"):
    if not api_key:
        st.warning("Please provide an API Key in the sidebar or Secrets.")
    elif syllabus_file and exam_files:
        try:
            # Initialize the 2026 SDK Client
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Analyzing papers... please wait."):
                # Extract text
                syl_content = get_pdf_text([syllabus_file])
                exam_content = get_pdf_text(exam_files)

                # Construct Prompt
                prompt = rf"""
                Analyze these SPPU Engineering documents.
                SYLLABUS: {syl_content[:10000]}
                PAST PAPERS: {exam_content[:20000]}

                Provide:
                1. UNIT WEIGHTAGE: High vs Low priority units.
                2. THE GOLD LIST: Most repeated topics.
                3. PREDICTIONS: 5 likely questions for the next exam.
                """

                # Generate Content
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Application Error: {e}")
    else:
        st.info("Please upload both the syllabus and exam papers to begin.")

st.sidebar.markdown("---")
st.sidebar.caption("v
