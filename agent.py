import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from tools import extract_pdf_text, read_cached_pdf_text

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Gemini base URL (from GEMINI.md)
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Initialize OpenAI client (configured for Gemini)
# This will be the client used by the OpenAIChatCompletionsModel
custom_openai_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=GEMINI_API_KEY,
)


# Create OpenAIChatCompletionsModel for Gemini
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=custom_openai_client, # Explicitly pass the configured client
)


# Define the Study Assistant Agent
study_agent = Agent(
    name="Study Assistant",
    instructions=(
        "You are a Study Assistant. Summarize academic PDFs and generate quizzes based strictly on the PDF content. "
        "When generating quizzes, DO NOT use the summary—use the full PDF text."
    ),
    tools=[read_cached_pdf_text],
    model=gemini_model,
      # Bind the tools
)