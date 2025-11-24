import os
from pypdf import PdfReader
from agents import function_tool

PDF_TEXT_CACHE_FILE = "pdf_text_cache.txt"

# ──────────────────────────────────────────────
# Regular Python Functions (for Streamlit app)
# ──────────────────────────────────────────────

def extract_pdf_text(file_path: str) -> str:
    """
    Extracts text from a PDF file. This is a regular function callable
    by the application, not an AI tool.
    """
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""
    return text

def cache_pdf_text(text: str):
    """
    Saves extracted text content into a cache file. This is a regular
    function callable by the application.
    """
    try:
        with open(PDF_TEXT_CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error caching PDF text: {e}")

# ──────────────────────────────────────────────
# AI Tool for Agent
# ──────────────────────────────────────────────

@function_tool
def read_cached_pdf_text() -> str:
    """
    Reads cached PDF text from the cache file. The agent uses this tool
    to access the content of the uploaded PDF for summarization and quizzing.
    """
    try:
        with open(PDF_TEXT_CACHE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error reading cached PDF text: {e}")
        return ""