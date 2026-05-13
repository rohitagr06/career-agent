---
title: Virtual Rohit — AI Career Conversation Agent
emoji: 🤖
colorFrom: indigo
colorTo: teal
sdk: gradio
app_file: app.py
pinned: true
license: mit
---

<div align="center">

# 🤖 Virtual Rohit
### AI-Powered Career Conversation Agent

*Ask me anything about Rohit's engineering background, skills, and experience.*

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-yellow?style=for-the-badge)](https://huggingface.co/spaces/manuagr03/career-agent)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/rohitagr06/career-agent)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## What is this?

**Virtual Rohit** is a production-grade AI career assistant that lets recruiters and hiring managers have a natural conversation about Rohit Agrawal's professional background — his 8.5+ years of experience in backend engineering, microservices, cloud platforms, and data-driven systems.

Instead of reading a static resume, you can **ask questions directly** and get grounded, accurate answers drawn from Rohit's actual professional documents. The assistant is purpose-built for recruiter conversations and deployed as a shareable link that Rohit includes in job applications.

---

## Live Demo

| Platform | Link |
|----------|------|
| 🤗 Hugging Face Space | https://huggingface.co/spaces/manuagr03/career-agent |
| 💻 GitHub Repository | https://github.com/rohitagr06/career-agent |

---

## Example Questions to Ask

```
Tell me about your backend engineering experience.
What did you work on at OakNorth?
What cloud platforms have you used?
How do you approach testing?
What Python frameworks do you know?
Tell me about your work at Teradata.
Do you have experience with microservices?
How can I get in touch with you?
```

---

## Architecture

```
Recruiter Query
      │
      ▼
┌─────────────────────┐
│   Input Validator   │  ← length check, injection guard, empty check
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   RAG Retriever     │  ← TF-IDF over chunked PDF + summary
│   (Hybrid Search)   │    semantic + keyword, top-4 chunks
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   Prompt Builder    │  ← persona + retrieved context only (not full PDF)
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   Model Router      │  ← GitHub Models (primary)
│                     │    → Gemini Flash (fallback)
│                     │    → Static message (last resort)
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Structured Output  │  ← Pydantic AgentResponse schema
│  (AgentResponse)    │    answer · confidence · suggested questions
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Tool Handler       │  ← record_user_details (lead capture)
│                     │    record_unknown_question (gap logging)
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Conversation       │  ← trims to last N turns (configurable)
│  History Manager    │
└─────────────────────┘
      │
      ▼
   Gradio UI
   (answer + clickable follow-up question chips)
```

---

## Key Features

### Resume-Grounded Responses
Every answer is drawn strictly from Rohit's professional documents. The RAG pipeline retrieves only the most relevant passages for each question — preventing hallucinations and keeping conversations factual.

### Hybrid RAG Pipeline
Combines TF-IDF keyword retrieval with semantic chunking. The retriever splits documents into overlapping 300-word chunks, builds a TF-IDF index, and fetches the top-4 most relevant passages per query. Only those passages — not the full document — are sent to the model.

### Multi-Model Fallback Routing
GitHub Models (GPT-4.1-mini) serves as the primary inference provider. If it hits a rate limit or error, the router automatically retries with exponential backoff, then switches to Google Gemini Flash. If both fail, a polite static message is returned. The app never crashes on a recruiter's screen.

### Structured Output via Pydantic
The agent returns a typed `AgentResponse` object (not a raw string), with fields for the answer text, detected topic, confidence level, suggested follow-up questions, and lead capture metadata. This enables richer UI rendering and reliable tool triggering.

### Prompt Injection Protection
All user input is validated before reaching the model. The validator checks message length, detects common injection patterns (`ignore`, `disregard`, `forget all`, `new instructions`), and strips non-printable characters.

### Lead Capture & Gap Logging
When a recruiter shares their email, the `record_user_details` tool fires automatically and sends a Pushover notification to Rohit. When the bot cannot answer a question, it logs it via `record_unknown_question` — so Rohit can improve the knowledge base over time.

### Configurable via Single Config File
All tuneable parameters (history limit, chunk size, retry counts, model names, temperature) live in `core/config.py`. Change a value once, it applies everywhere.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Gradio |
| **LLM (primary)** | GitHub Models — GPT-4.1-mini (free) |
| **LLM (fallback)** | Google Gemini 2.5 Flash (free) |
| **LLM SDK** | OpenAI Python SDK (OpenAI-compatible interface) |
| **RAG** | TF-IDF via scikit-learn, pypdf |
| **Structured output** | Pydantic v2 |
| **Validation** | Custom input validator |
| **Notifications** | Pushover API |
| **Deployment** | Hugging Face Spaces |
| **Language** | Python 3.11+ |

---

## Project Structure

```
career-agent/
│
├── app.py                   # Entry point — Gradio UI, wires all components
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # This file
├── .env.example             # Template for required environment variables
│
├── core/                    # All business logic (no name collision with agent libs)
│   ├── __init__.py          # Exports CareerAgent
│   ├── config.py            # ★ All tuneable settings in one place
│   ├── schemas.py           # Pydantic models: AgentResponse, CitedFact, LeadCapture, etc.
│   ├── agent.py             # CareerAgent class — orchestrates all components
│   ├── retriever.py         # KnowledgeRetriever — chunking, TF-IDF index, retrieve()
│   ├── models.py            # GitHub + Gemini clients, model_router() with retry logic
│   ├── prompt.py            # build_system_prompt() — persona + retrieved context
│   ├── tools.py             # Tool schemas, Pushover functions, handle_tool_calls()
│   ├── validator.py         # validate_input() — length, injection, empty guard
│   └── history.py           # ConversationHistory — trim to config.MAX_HISTORY_TURNS
│
├── data/                    # Knowledge base (source of truth)
│   ├── linkedin.pdf         # LinkedIn profile export
│   └── summary.txt          # Personal and professional summary
│
└── tests/                   # Test suite
    ├── test_agent.py        # 20+ recruiter question scenarios + edge cases
    ├── test_retriever.py    # Unit tests: chunking accuracy, retrieval relevance
    └── test_validator.py    # Unit tests: injection, length, empty, clean input
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/rohitagr06/career-agent.git
cd career-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows
```

### 3. Install dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
GITHUB_API_KEY=your_github_models_pat
GOOGLE_API_KEY=your_gemini_api_key
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_USER=your_pushover_user_key
```

### 5. Run the application

```bash
python app.py
```

Open your browser at: `http://127.0.0.1:7860`

---

## Configuration

All settings are in `core/config.py`. You never need to grep through multiple files to find a value.

| Setting | Default | Description |
|---------|---------|-------------|
| `GITHUB_MODEL` | `openai/gpt-4.1-mini` | Primary inference model |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Fallback inference model |
| `TEMPERATURE` | `0.4` | Response creativity (0 = factual, 1 = creative) |
| `MAX_TOKENS` | `1024` | Maximum tokens per response |
| `MAX_HISTORY_TURNS` | `10` | Conversation turns kept in context |
| `MAX_INPUT_LENGTH` | `1000` | Max characters per user message |
| `CHUNK_SIZE` | `300` | Words per RAG chunk |
| `CHUNK_OVERLAP` | `50` | Overlap words between chunks |
| `TOP_K_CHUNKS` | `4` | Chunks retrieved per query |
| `GITHUB_MAX_RETRIES` | `3` | Retries before switching to Gemini |
| `RETRY_BASE_DELAY` | `2.0` | Base delay in seconds (exponential backoff) |
| `REQUEST_TIMEOUT` | `30` | API timeout in seconds |

---

## Deployment — Hugging Face Spaces

This project is designed for zero-config deployment on Hugging Face Spaces.

1. Fork or push this repository to your Hugging Face account
2. Go to **Settings → Variables and Secrets** in your Space
3. Add each of the four keys from `.env.example` as Repository Secrets
4. The Space will build automatically from `app.py`

No Docker, no build scripts, no paid infrastructure required.

---

## Running Tests

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run individual test files
python -m pytest tests/test_validator.py -v
python -m pytest tests/test_retriever.py -v
python -m pytest tests/test_agent.py -v
```

---

## Design Decisions

**Why `core/` instead of `agent/`?**
The `openai-agents` and `agents` libraries both use `agent` as a namespace. Naming the package `core/` avoids import collisions entirely.

**Why TF-IDF instead of FAISS or embeddings?**
For a 4-page LinkedIn PDF and a short summary file (~25 chunks total), TF-IDF retrieval is fast, accurate, and requires zero API calls or GPU resources. Embeddings become worthwhile when the knowledge base grows beyond 50+ documents.

**Why keep Hugging Face instead of Render or Railway?**
HF Spaces provides a stable, recognisable public URL that recruiters trust. Cold starts are ~30 seconds — acceptable for someone who clicked a link intentionally from a resume or LinkedIn profile.

**Why Pydantic structured output instead of raw strings?**
Structured output (`AgentResponse`) lets the UI render suggested follow-up questions as clickable chips, trigger lead capture automatically when an email is detected, log unknown questions without manual parsing, and display confidence indicators — none of which are possible with a plain string return.

---

## About Rohit Agrawal

Senior Software Engineer with 8.5+ years of experience building scalable backend systems and data-driven applications. Currently at OakNorth (Hyderabad), previously at Teradata.

Specialises in Python, microservices, REST APIs, PostgreSQL, AWS, Kubernetes, and analytics platforms.

| | |
|-|-|
| 📧 Email | rohitagr06@gmail.com |
| 💼 LinkedIn | [linkedin.com/in/rohitagr06](https://www.linkedin.com/in/rohitagr06) |
| 💻 GitHub | [github.com/rohitagr06](https://github.com/rohitagr06) |

---

<div align="center">

Built with Python · Gradio · OpenAI SDK · Pydantic · Hugging Face Spaces

*This assistant is a digital resume. All responses are grounded in Rohit's actual professional documents.*

</div>
