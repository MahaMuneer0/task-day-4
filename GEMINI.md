# Role: Senior Python AI Engineer
**Objective:** Build a Study Notes Summarizer + Quiz Generator Agent using Streamlit, PyPDF, Gemini CLI, and the openai-agents SDK (with Context7 MCP server connected).
## 1. Project OverviewThe goal is to build an AI-powered study agent that:

**A. PDF Summarizer**
*   User uploads a PDF.
*   Text is extracted using PyPDF.
*   Agent generates a clean, structured summary.
**B. Quiz Generator**

*   After summary, user clicks “Create Quiz”.
*   Agent analyzes the original PDF text.
*   Generates MCQs or mixed quizzes.
```bash
UI: Streamlit (recommended)
Model: gemini-2.0-flash (via OpenAI Agents SDK)
Tools: PyPDF (extraction),
MCP (Context7 documentation), 
custom tools for PDF text extraction
```
## 2. Critical Technical Constraints⚠️
You must follow these rules exactly. No extra creativity. No bloat code.
1.  Zero-Bloat Protocol (CRITICAL)
*   No unnecessary logic, no extra error handling beyond required, no random comments.
*   Focus strictly on:    
*   PDF extraction    
*   Agent integration    
*   UI (minimal)
2.  API Configuration
*   Use OpenAI Agents SDK with Gemini base URL:    `https://generativelanguage.googleapis.com/v1beta/openai/`
*   Load key from environment variable:    `GEMINI_API_KEY`
*   Use `OpenaiChatCompletionModel` → `gemini-2.0-flash`
3.  SDK Accuracy
*   MUST use official patterns from `openai-agents` SDK docs    (verify via Context7 MCP before writing code)
4.  Error Recovery Protocol
*   If you get:    
*   `AttributeError`    
*   `TypeError`    
*   `ImportError`    
*   Wrong function format    ➡️ STOP    ➡️ Immediately call `get-library-docs` from Context7    ➡️ Re-write code EXACTLY according to docs.
5.  Dependency Management
*   Use `uv` for installing dependencies.
*   If packages already exist → DO NOT reinstall.
## 3. Architecture & File Structure
*Note: The current directory is the root. Do not create a subfolder named `study_agent`.*
```
├── .env                 # Environment variables
├── tools.py             # PDF extraction tool
├── agent.py             # Agent setup & tool registration
├── app.py               # Streamlit-based UI
├── pdf_text_cache.txt   # Text extracted from PDF (auto-created)
└── pyproject.toml       # UV config
```

## 4. Implementation Steps
Follow EXACT order. No skipping.
### Step 1: Documentation & Pattern Analysis
Before writing code:
Action (MANDATORY):
*   Run in Gemini CLI:    `get-library-docs openai-agents`
*   Analyze for:    
*   How tools are declared (`@tool` or `FunctionTool`)    
*   Correct format of:        
*   `Agent`        
*   `OpenaiChatCompletionModel`    
*   Tool binding    
*   Running agent normally (non-streaming)    
*   How arguments are structured
*   If ANY confusion → run docs again.
### Step 2: Tool Implementation (tools.py)
Create a PDF extraction tool following the EXACT structure from SDK docs.
Required Functions
*   `extract_pdf_text(file_path: str) -> str`
*   `cache_pdf_text(text: str)`
*   `read_cached_pdf_text() -> str`
Logic
*   Use PyPDF to load text from the uploaded PDF.
*   Save extracted text into `pdf_text_cache.txt`.
*   Handle `FileNotFoundError` for cache by returning empty string.
Constraints
*   Tool format must match exactly the SDK docs (decorator or wrapper).
*   Absolutely no custom error messages beyond required.
### Step 3: Agent Configuration (agent.py)
Required Steps
*   Initialize Gemini client using base URL.
*   Create `OpenaiChatCompletionModel("gemini-2.0-flash")`.*   Load tools from `tools.py`.
*   Bind tools to the agent using EXACT SDK syntax.
*   Set system prompt:

```    
You are a Study Assistant. Summarize academic PDFs and generate quizzes based strictly on the PDF content. When generating quizzes, DO NOT use the summary—use the full PDF text.
```
No Extra Features Allowed
*   No memory*   No caching besides `pdf_text_cache.txt`*   No streaming mode
### Step 4: Application Logic (app.py)
Framework: StreamlitUI Structure:
*   PDF Upload Section
*   Summarization Button
*   Quiz Generator Button
*   Display Areas
Flow Requirements
*   When PDF is uploaded:    
*   Save file temporarily    
*   Call the tool `extract_pdf_text()`    
*   Cache extracted text
*   When user clicks Summarize PDF:    
*   Call agent with instruction:
        `Summarize the extracted PDF text.`
*   When user clicks Create Quiz:    
*   Call agent with:        
`Based strictly on the full PDF text, generate 5–10 quiz questions (MCQs or mixed).`
Output Restrictions
*   Display results in clean sections—no styling beyond headings/cards.
### Step 5: Environment & Dependencies
`.env`
```GEMINI_API_KEY=your_key_here```
Required packages:
*   `openai-agents`
*   `streamlit`
*   `pypdf`
*   `python-dotenv`

Smart Install Rule
*   If package exists in environment → do not reinstall.