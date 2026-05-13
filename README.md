---
title: Virtual Rohit — AI Career Conversation Agent
colorFrom: indigo
colorTo: teal
sdk: gradio
app_file: app.py
pinned: true
license: mit
---

<div align="center">

# Virtual Rohit AI
### AI-Powered Career Conversation Agent

*AI-powered recruiter assistant for exploring Rohit Agrawal’s engineering experience, projects, and technical expertise.*

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

## Sample Conversation

| User Query | Assistant Response |
|------------|--------------------|
| **"Tell me about your backend engineering experience."** | "I have experience building backend systems and microservices using Python, REST APIs, PostgreSQL, and cloud-native infrastructure. My work has focused on scalable data-driven applications, analytics systems, and distributed services running on AWS and Kubernetes." |
| **"Kafka?"** | "I don't have confirmed hands-on Kafka experience mentioned in my documented background. My backend work has primarily focused on Python microservices, REST APIs, PostgreSQL, Kubernetes, and cloud deployments on AWS." |
| **"Share your phone number."** | "I prefer professional communication through email or LinkedIn." |
| **"How do you approach backend system design?"** | "I usually focus on modular service boundaries, database efficiency, observability, and scalability from the beginning. In my recent work, I’ve primarily built Python-based backend services with REST APIs, PostgreSQL, and cloud-native deployments on AWS and Kubernetes." |

---

## Production Features

### 🛡️ Recruiter-Safe Guardrails
The assistant is designed with professional safety in mind:
* **Avoids Hallucination:** Prevents the generation of experience not found in provided documents.
* **Instruction Protection:** Blocks attempts to disclose hidden system prompts.
* **Privacy First:** Never exposes phone numbers; only shares approved professional contact details.

### 🏗️ Modular RAG Architecture
The system is decoupled into independent modules (Retrieval, Reranking, Embeddings, Routing, Memory, and Validation), ensuring high extensibility and easier unit testing.

### ⚡ Persistent FAISS Index
Embeddings are generated offline and stored in a persistent FAISS index. This ensures the application starts instantly on Hugging Face Spaces without needing to rebuild vectors from scratch.

### 🔄 Multi-Model Resilience
Uses a robust failover strategy:
1. **Primary:** GitHub Models (GPT-4o-mini).
2. **Secondary (Fallback):** Google Gemini Flash.
3. **Tertiary:** Polite static failure message.

### 📈 Retry Handling with Exponential Backoff
The model router automatically handles transient API failures (like rate limits) using exponential backoff before attempting a switch to the fallback provider.

### 📋 Structured Validation Layer
All user input passes through a validation gate checking for:
* Empty or nonsense input.
* Excessive character length.
* Malicious prompt injection attempts (e.g., "ignore previous instructions").

### ☁️ Lightweight Deployment
Optimized for **CPU-only** deployment on Hugging Face Spaces, eliminating the need for expensive GPU infrastructure while maintaining lightweight and responsive inference.

---

## Known Limitations

* Responses are intentionally restricted to uploaded professional documents.
* The assistant avoids speculative or unverified answers.
* Free-tier Hugging Face Spaces may experience occasional cold starts.
* Real-time internet search is disabled to preserve factual grounding.
* The system is optimized for recruiter-style conversations rather than general-purpose chat.

---

## Architecture

```
Recruiter Query
      │
      ▼
┌─────────────────────┐
│   Input Validator   │  ← empty check, length validation, prompt injection
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Conversation Memory │  ← recruiter context, follow-up support, multi-turn state   
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   RAG Retriever     │  ← semantic search, keyword search, 
│ Hybrid RAG Search   │    FAISS vector DB, chunk retrieval 
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   Cross-Encoder     │  ← relevance scoring, top-k reranking 
│   Reranker          │    
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   Prompt Builder    │  ← system prompt, retrieved context, grounded answers
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
│  Structured Output  │  ← formatted answer
│  (AgentResponse)    │    · recruiter-safe · grounded output
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Gradio UI          │  ← recruiter chat 
│                     │  ← conversation UX 
│                     │  ← follow-up flow
└─────────────────────┘
```

---

## Key Features

### Resume-Grounded Responses
Every answer is drawn strictly from Rohit's professional documents. The RAG pipeline retrieves only the most relevant passages for each question — preventing hallucinations and keeping conversations factual.

### Hybrid RAG Pipeline
The retrieval layer is optimized specifically for recruiter-style conversations, where queries are often extremely short, context-poor, and technology-focused.

Instead of relying on a single retrieval strategy, the pipeline combines:

* semantic retrieval using Sentence Transformer embeddings
* FAISS vector similarity search
* keyword-based retrieval
* cross-encoder reranking for relevance scoring

This layered retrieval approach improves answer grounding for questions such as:

* "Kafka?"
* "Testing?"
* "Architecture?"
* "AWS?"

After retrieval and reranking, only the most relevant chunks are injected into the final prompt. This reduces hallucinations, improves factual consistency, and keeps responses aligned with the underlying professional documents.

### Multi-Model Fallback Routing
GitHub Models (GPT-4.1-mini) serves as the primary inference provider. If it hits a rate limit or error, the router automatically retries with exponential backoff, then switches to Google Gemini Flash. If both fail, a polite static message is returned. This prevents failed recruiter sessions during provider outages or rate limits.

### Structured Output via Pydantic
The agent returns a typed `AgentResponse` object (not a raw string), with fields for the answer text, detected topic, confidence level, suggested follow-up questions, and lead capture metadata. This enables richer UI rendering and reliable tool triggering.

### Prompt Injection Protection
All user input is validated before reaching the model. The validator checks message length, detects common injection patterns (`ignore`, `disregard`, `forget all`, `new instructions`), and strips non-printable characters.

### Lead Capture & Gap Logging
When a recruiter shares their email, the `record_user_details` tool fires automatically and sends a Pushover notification to Rohit. When the bot cannot answer a question, it logs it via `record_unknown_question` — so Rohit can improve the knowledge base over time.

### Configurable via Single Config File
All tuneable parameters (history limit, chunk size, retry counts, model names, temperature) live in `core/config.py`. Change a value once, it applies everywhere.

---

## Engineering Focus Areas

* Backend Engineering
* Retrieval-Augmented Generation (RAG)
* AI Career Agents
* Microservices & APIs
* LLM Routing & Fallback Systems
* Prompt Safety & Guardrails
* Semantic Search & Reranking
* Conversation Memory Systems
* Cloud-Native Deployment
* Recruiter-Focused AI UX

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Gradio |
| **LLM (primary)** | GitHub Models — GPT-4.1-mini (free) |
| **LLM (fallback)** | Google Gemini 2.5 Flash (free) |
| **LLM SDK** | OpenAI Python SDK (OpenAI-compatible interface) |
| **RAG** | FAISS, Sentence Transformers, Hybrid Retrieval |
| **Structured Response** | Pydantic validation |
| **Validation** | schema-safe output |
| **Notifications** | Pushover API |
| **Deployment** | Hugging Face Spaces |
| **Language** | Python 3.11+ |

---

## Project Structure

```
career-agent/
│
├── app.py                          # Application entry point
├── README.md                       # Project documentation
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
├── uv.lock                        # Locked dependency versions
├── .env.example                   # Environment variable template
├── .gitignore
├── .hfignore
│
├── config/                        # Centralized configuration
│   ├── logging_config.py          # Logging setup
│   └── settings.py                # Environment settings and secrets
│
├── core/                          # Core application utilities
│   ├── formatter.py               # Response formatting
│   ├── grounding.py               # Grounded response helpers
│   ├── history.py                 # Conversation memory handling
│   ├── models.py                  # LLM model definitions
│   ├── observability.py           # Logging and tracing helpers
│   ├── retry.py                   # Retry and backoff logic
│   ├── router.py                  # Primary/fallback model routing
│   ├── schemas.py                 # Pydantic response schemas
│   └── validator.py               # Input validation and safety checks
│
├── pipeline/                      # Main orchestration pipeline
│   ├── career_pipeline.py         # End-to-end recruiter pipeline
│   ├── instructions.py            # System instructions
│   ├── memory.py                  # Conversation state manager
│   ├── runner.py                  # Pipeline execution flow
│   └── tools.py                   # Tool integrations and handlers
│
├── rag/                           # Retrieval-Augmented Generation system
│   ├── chunker.py                 # Document chunking
│   ├── embeddings.py              # Embedding generation
│   ├── faiss_store.py             # FAISS persistence layer
│   ├── indexing.py                # Index management
│   ├── ingest.py                  # Knowledge ingestion pipeline
│   ├── keyword_search.py          # Keyword retrieval
│   ├── metadata.py                # Chunk metadata handling
│   ├── pdf_loader.py              # Resume/document loading
│   ├── reranker.py                # Cross-encoder reranking
│   ├── retriever.py               # Hybrid retrieval orchestration
│   ├── semantic_search.py         # Semantic vector search
│   ├── storage.py                 # Index storage utilities
│   └── vector_store.py            # Vector database abstraction
│
├── prompts/                       # Prompt templates
│   ├── fallback_prompt.txt
│   ├── summarization_prompt.txt
│   ├── system_prompt.txt
│   └── validation_prompt.txt
│
├── scripts/                       # Utility and maintenance scripts
│   ├── build_index.py             # Build FAISS vector index
│   ├── evaluate.py                # Evaluation utilities
│   └── rebuild_embeddings.py      # Recreate embeddings/index
│
├── ui/                            # Gradio frontend components
│   ├── components.py              # Shared UI components
│   ├── gradio_ui.py               # Main Gradio interface
│   ├── landing_page.py            # Landing page content
│   └── themes.py                  # UI themes and styling
│
├── tests/                         # Test suite
│   ├── recruiter_questions.py     # Recruiter-style QA tests
│   ├── test_memory.py
│   ├── test_models.py
│   ├── test_retrieval.py
│   └── test_validator.py
│
├── notebooks/                     # Experiments and prompt testing
│   ├── prompt_testing.ipynb
│   └── rag_experiments.ipynb
│
└── data/                          # Knowledge base and indexes
    ├── linkedin.pdf               # LinkedIn profile export
    ├── summary.txt                # Professional summary
    └── indexes/
        └── faiss.index            # Persistent FAISS vector index
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

All application settings and environment configuration are centralized in `config/settings.py` for easier maintainability and deployment management.

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

Designed for lightweight deployment on Hugging Face Spaces with minimal operational overhead.
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

**Why Hybrid Retrieval instead of Pure Semantic Search?**
Recruiter conversations behave very differently from traditional search queries.

Questions are often:

* extremely short
* ambiguous
* acronym-heavy
* technology-specific

Examples:
* “Kafka?”
* “Testing?”
* “Architecture?”
* “AWS?”

Pure semantic retrieval can miss exact technical matches, while pure keyword search struggles with contextual understanding.

To improve retrieval quality, the system combines:

* semantic embedding search for contextual similarity
* FAISS vector retrieval for fast nearest-neighbour lookup
* keyword retrieval for exact technology matching
* cross-encoder reranking for final relevance scoring

This hybrid architecture improves retrieval precision while remaining lightweight enough for CPU-only deployment on Hugging Face Spaces.

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
