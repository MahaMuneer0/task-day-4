import streamlit as st

import nest_asyncio
import os
import asyncio
from agents import Runner
from agent import study_agent
from tools import extract_pdf_text, cache_pdf_text, read_cached_pdf_text, PDF_TEXT_CACHE_FILE

# Apply nest_asyncio to allow nested event loops (necessary for Streamlit with asyncio)
nest_asyncio.apply()

st.set_page_config(page_title="Study Notes Summarizer & Quiz Generator", layout="wide")
st.title("📚 Study Notes Summarizer & Quiz Generator")

# --- PDF Upload Section ---
st.header("1. Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Ensure a temporary directory exists for saving uploaded PDFs
if not os.path.exists("temp_pdfs"):
    os.makedirs("temp_pdfs")

# Placeholder for PDF text
pdf_text = ""

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_file_path = os.path.join("temp_pdfs", uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"PDF uploaded: {uploaded_file.name}")

    # Extract text from PDF
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_pdf_text(temp_file_path)
        cache_pdf_text(pdf_text) # Cache the extracted text

    if pdf_text:
        st.subheader("Extracted PDF Text (first 500 chars):")
        st.code(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
        st.session_state["pdf_extracted"] = True
        st.session_state["pdf_text_available"] = True
    else:
        st.error("Could not extract text from PDF.")
        st.session_state["pdf_extracted"] = False
        st.session_state["pdf_text_available"] = False
else:
    st.session_state["pdf_extracted"] = False
    st.session_state["pdf_text_available"] = False


# --- Summarization and Quiz Generation ---
st.header("2. Generate Study Aids")

if st.session_state.get("pdf_extracted"):
    # Summarize PDF
    if st.button("Summarize PDF", key="summarize_button"):
        st.subheader("Summary:")
        with st.spinner("Generating summary..."):
            # Ensure the agent has access to the extracted text
            # The agent will use the read_cached_pdf_text tool
            summary_result = asyncio.run(
                Runner.run(
                    study_agent,
                    "Summarize the extracted PDF text. Use the 'read_cached_pdf_text' tool to get the content."
                )
            )

            st.write(summary_result.final_output)

    # Create Quiz
    if st.button("Create Quiz", key="quiz_button"):
        st.subheader("Quiz Questions:")
        with st.spinner("Generating quiz..."):
            # Ensure the agent has access to the full PDF text for quiz generation
            # The agent will use the read_cached_pdf_text tool
            quiz_result = asyncio.run(
                Runner.run(
                    study_agent,
                    "Based strictly on the full PDF text, generate 5–10 quiz questions (MCQs or mixed). Use the 'read_cached_pdf_text' tool to get the content."
                )
            )

            st.markdown(quiz_result.final_output)
else:
    st.info("Please upload a PDF file first to enable summarization and quiz generation.")

# Clean up temp_pdfs directory and pdf_text_cache.txt on app rerun or close if needed (more complex to implement reliably in Streamlit)
# For this task, we'll leave them for now.