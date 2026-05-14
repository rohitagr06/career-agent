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

*A production-grade AI assistant that lets recruiters have a natural conversation about Rohit Agrawal's engineering background — instead of reading a static resume.*

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-yellow?style=for-the-badge)](https://huggingface.co/spaces/manuagr03/career-agent)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/rohitagr06/career-agent)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/github/v/release/rohitagr06/career-agent?style=for-the-badge&color=blueviolet)](https://github.com/rohitagr06/career-agent/releases)
[![CI](https://github.com/rohitagr06/career-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/rohitagr06/career-agent/actions/workflows/ci.yml)

</div>

---

## Table of Contents

- [What is this?](#what-is-this)
- [Live Demo](#live-demo)
- [Example Questions to Ask](#example-questions-to-ask)
- [Sample Conversation](#sample-conversation)
- [Architecture](#architecture)
- [Features](#features)
- [Production Features](#production-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Configuration](#configuration)
- [Deployment — Hugging Face Spaces](#deployment--hugging-face-spaces)
- [Running Tests](#running-tests)
- [Design Decisions](#design-decisions)
- [Roadmap](#roadmap)
- [Known Limitations](#known-limitations)
- [About Rohit Agrawal](#about-rohit-agrawal)

---

## What is this?

**Virtual Rohit** is a production-grade AI career assistant that lets recruiters and hiring managers have a natural conversation about Rohit Agrawal's professional background — his 8.5+ years of experience in backend engineering, microservices, cloud platforms, and data-driven systems.

Instead of reading a static resume, you can **ask questions directly** and get grounded, accurate answers drawn from Rohit's actual professional documents. The assistant is purpose-built for recruiter conversations and deployed as a shareable link included in job applications.

---

## Live Demo

| Platform | Link |
|----------|------|
| 🤗 Hugging Face Space | https://huggingface.co/spaces/manuagr03/career-agent |
| 💻 GitHub Repository | https://github.com/rohitagr06/career-agent |

---

## Example Questions to Ask

```text
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

### Backend Engineering

| | |
|-|-|
| **User** | Tell me about your backend engineering experience. |
| **Assistant** | I have experience building backend systems and microservices using Python, REST APIs, PostgreSQL, and cloud-native infrastructure. My work has focused on scalable data-driven applications, analytics systems, and distributed services running on AWS and Kubernetes. |

### Technology Grounding

| | |
|-|-|
| **User** | Kafka? |
| **Assistant** | I don't have confirmed hands-on Kafka experience mentioned in my documented background. My backend work has primarily focused on Python microservices, REST APIs, PostgreSQL, Kubernetes, and cloud deployments on AWS. |

### Contact Protection

| | |
|-|-|
| **User** | Share your phone number. |
| **Assistant** | I prefer professional communication through email or LinkedIn. |

### System Design

| | |
|-|-|
| **User** | How do you approach backend system design? |
| **Assistant** | I usually focus on modular service boundaries, database efficiency, observability, and scalability from the beginning. In my recent work, I've primarily built Python-based backend services with REST APIs, PostgreSQL, and cloud-native deployments on AWS and Kubernetes. |

---

## Architecture

```
Recruiter Query
      │
      ▼
┌─────────────────────────┐
│     Input Validator     │  ← empty check, length limit, prompt injection guard
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│   Conversation Memory   │  ← multi-turn context, follow-up support, history trimming
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│    Query Normalizer     │  ← lowercasing, punctuation stripping, abbreviation expansion
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│      RAG Retriever      │  ← semantic search (FAISS) + keyword search
│   Hybrid RAG Search     │    chunk retrieval, persistent vector index
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│   Cross-Encoder         │  ← relevance scoring, top-k reranking
│   Reranker              │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│     Prompt Builder      │  ← system prompt + retrieved context (not full document)
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│      Model Router       │  ← GitHub Models GPT-4.1-mini (primary)
│                         │    → Google Gemini Flash (fallback)
│                         │    → Static safe message (last resort)
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│    Structured Output    │  ← Pydantic AgentResponse
│    (AgentResponse)      │    answer · topic · confidence · suggested questions
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│       Gradio UI         │  ← recruiter chat interface
│                         │    follow-up question chips · conversation UX
└─────────────────────────┘
```

---

## Features

### Resume-Grounded Responses
Every answer is drawn strictly from Rohit's professional documents. The RAG pipeline retrieves only the most relevant passages for each question — preventing hallucinations and keeping conversations factual.

### Hybrid RAG Pipeline
The retrieval layer is optimised specifically for recruiter-style conversations, where queries are often extremely short, context-poor, and technology-focused — such as `"Kafka?"`, `"Testing?"`, or `"AWS?"`.

Instead of relying on a single strategy, the pipeline combines:

- Sentence Transformer semantic embeddings for contextual similarity
- FAISS vector similarity search for fast nearest-neighbour lookup
- Keyword-based retrieval for exact technology matching
- Cross-encoder reranking for final relevance scoring

Only the top-ranked chunks are injected into the prompt — not the full document — reducing hallucinations and keeping responses grounded.

### Query Normalizer
Recruiter queries often arrive as single-word acronyms or shorthand (`"k8s?"`, `"AWS"`, `"REST"`). The query normalizer cleans and expands input before retrieval, improving chunk matching accuracy for short and ambiguous queries.

### Multi-Model Fallback Routing
GitHub Models (GPT-4.1-mini) is the primary provider. On failure, the router retries with exponential backoff before switching to Google Gemini Flash. If both are unavailable, a polite static message is returned — the app never crashes during a recruiter session.

### Structured Output via Pydantic
The agent returns a typed `AgentResponse` object — not a raw string. Fields include the answer text, detected topic, confidence level, suggested follow-up questions, and lead capture metadata. This enables richer UI rendering and reliable tool triggering without manual string parsing.

### Prompt Injection Protection
All input is validated before reaching the model. The validator checks message length, detects injection patterns (`ignore`, `disregard`, `forget all`, `new instructions`), and strips non-printable characters.

### Lead Capture & Gap Logging
When a recruiter shares their email, the `record_user_details` tool fires automatically and sends a Pushover notification to Rohit. When a question cannot be answered, `record_unknown_question` logs it — so Rohit can improve the knowledge base over time.

---

## Production Features

### ⚡ Persistent FAISS Index
Embeddings are generated offline and stored as a persistent FAISS index at `data/indexes/faiss.index`. The application loads the pre-built index at startup — no vector rebuilding required, instant cold-start retrieval.

### 🔄 Retry Handling with Exponential Backoff
The model router handles transient API failures automatically. Each provider is retried with increasing wait times (2s → 4s → 8s) before switching to the next fallback, preventing unnecessary failover on brief rate limit spikes.

### 🔁 Multi-Model Resilience
A three-tier failover strategy ensures the assistant remains available even during provider outages:
1. **Primary:** GitHub Models (GPT-4.1-mini)
2. **Secondary:** Google Gemini Flash
3. **Tertiary:** Polite static failure message — never an unhandled crash

### 📋 Structured Validation Layer
All user input passes through a validation gate before any model call:
- Empty or whitespace-only input
- Messages exceeding the character limit
- Prompt injection attempts (`"ignore previous instructions"`, `"disregard"`, `"forget all"`)

### 🛡️ Recruiter-Safe Guardrails
- Prevents generation of experience not found in provided documents
- Blocks attempts to extract hidden system prompt instructions
- Never exposes phone numbers or unapproved personal contact details
- Only shares professional email and LinkedIn profile

### 🏗️ Modular Architecture
Retrieval, reranking, embeddings, routing, memory, validation, and formatting are separated into independent modules. Each module is independently testable and replaceable without affecting the rest of the pipeline.

### ☁️ Lightweight Deployment
Optimised for **CPU-only** inference on Hugging Face Spaces free tier — no GPU, no paid infrastructure required.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Gradio |
| **LLM (primary)** | GitHub Models — GPT-4.1-mini (free) |
| **LLM (fallback)** | Google Gemini 2.5 Flash (free) |
| **LLM SDK** | OpenAI Python SDK (OpenAI-compatible interface) |
| **Embeddings** | Sentence Transformers |
| **Vector store** | FAISS (persistent, CPU-only) |
| **Reranking** | Cross-Encoder |
| **Structured output** | Pydantic v2 (`AgentResponse` schema) |
| **Input validation** | Custom validator (`core/validator.py`) |
| **Notifications** | Pushover API |
| **Dependency management** | uv + pyproject.toml |
| **Deployment** | Hugging Face Spaces |
| **Language** | Python 3.11+ |

---

## Project Structure

```
career-agent/
│
├── app.py                          # Application entry point — wires pipeline to Gradio UI
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies (pip)
├── pyproject.toml                  # Project metadata and uv configuration
├── uv.lock                         # Locked dependency versions
├── .env.example                    # Template for required environment variables
├── .gitignore                      # Excludes .env, __pycache__, indexes, model cache
├── .hfignore                       # Excludes dev files from Hugging Face Space build
│
├── config/                         # Centralised configuration
│   ├── logging_config.py           # Logging setup and log level management
│   └── settings.py                 # All environment settings and tuneable constants
│
├── core/                           # Core application utilities
│   ├── formatter.py                # Response formatting and output cleanup
│   ├── grounding.py                # Grounded response helpers and fact-checking
│   ├── history.py                  # Conversation memory — trimming to MAX_HISTORY_TURNS
│   ├── models.py                   # LLM client definitions (GitHub + Gemini)
│   ├── observability.py            # Logging, tracing, and request tracking helpers
│   ├── retry.py                    # Exponential backoff and retry logic
│   ├── router.py                   # Primary/fallback model routing with failover
│   ├── schemas.py                  # Pydantic schemas: AgentResponse, CitedFact, LeadCapture
│   └── validator.py                # Input validation and prompt injection safety checks
│
├── pipeline/                       # Main orchestration pipeline
│   ├── career_pipeline.py          # End-to-end recruiter conversation pipeline
│   ├── instructions.py             # System prompt and persona instructions
│   ├── memory.py                   # Conversation state manager
│   ├── runner.py                   # Pipeline execution and step coordination
│   └── tools.py                    # Tool integrations: lead capture, gap logging
│
├── rag/                            # Retrieval-Augmented Generation system
│   ├── chunker.py                  # Document chunking with configurable size and overlap
│   ├── embeddings.py               # Sentence Transformer embedding generation
│   ├── faiss_store.py              # FAISS index persistence — load and save
│   ├── indexing.py                 # Index build and management utilities
│   ├── ingest.py                   # Knowledge ingestion pipeline (PDF + text)
│   ├── keyword_search.py           # BM25-style keyword retrieval
│   ├── query_normalizer.py         # Query cleaning, lowercasing, abbreviation expansion
│   ├── metadata.py                 # Chunk metadata tagging and management
│   ├── pdf_loader.py               # Resume and document PDF loading via pypdf
│   ├── reranker.py                 # Cross-encoder reranking for relevance scoring
│   ├── retriever.py                # Hybrid retrieval orchestration (semantic + keyword)
│   ├── semantic_search.py          # FAISS vector similarity search
│   ├── storage.py                  # Index storage path and file utilities
│   └── vector_store.py             # Vector database abstraction layer
│
├── prompts/                        # Prompt templates
│   ├── system_prompt.txt           # Main persona and grounding system prompt
│   ├── fallback_prompt.txt         # Prompt used when retrieval confidence is low
│   ├── summarization_prompt.txt    # Prompt for memory summarization (future)
│   └── validation_prompt.txt       # Prompt for response safety validation
│
├── scripts/                        # Utility and maintenance scripts
│   ├── build_index.py              # One-time: build and save FAISS vector index
│   ├── evaluate.py                 # Retrieval and response quality evaluation
│   └── rebuild_embeddings.py       # Rebuild embeddings when documents change
│
├── ui/                             # Gradio frontend components
│   ├── gradio_ui.py                # Main Gradio ChatInterface definition
│   ├── components.py               # Shared UI components and helper widgets
│   ├── landing_page.py             # Welcome message and recruiter onboarding content
│   └── themes.py                   # Gradio theme and styling configuration
│
├── tests/                          # Test suite
│   ├── recruiter_questions.py      # End-to-end recruiter conversation QA tests
│   ├── test_memory.py              # Conversation history and trimming tests
│   ├── test_models.py              # Model router and fallback logic tests
│   ├── test_retrieval.py           # RAG retrieval accuracy and relevance tests
│   └── test_validator.py           # Input validation and injection detection tests
│
├── notebooks/                      # Experiments and evaluation
│   ├── prompt_testing.ipynb        # System prompt iteration and testing
│   └── rag_experiments.ipynb       # Retrieval pipeline experiments and benchmarks
│
└── data/                           # Knowledge base and persistent indexes
    ├── linkedin.pdf                 # LinkedIn profile export (primary knowledge source)
    ├── summary.txt                  # Personal and professional summary
    └── indexes/
        └── faiss.index              # Persistent FAISS vector index (built by scripts/build_index.py)
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

Using `uv` (recommended — faster, deterministic):
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

> **Where to get these:**
> - `GITHUB_API_KEY` — [GitHub Settings → Developer Settings → Personal Access Tokens → Fine-grained](https://github.com/settings/tokens)
> - `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/app/apikey)
> - `PUSHOVER_TOKEN` / `PUSHOVER_USER` — [Pushover Dashboard](https://pushover.net)

### 5. Build the FAISS index

One-time step — loads your documents, generates embeddings, and saves the persistent index to `data/indexes/faiss.index`.

```bash
python scripts/build_index.py
```

> **Note:** Run this once before first launch. On every subsequent startup, the app loads the pre-built index directly — no rebuild required. If you update `data/linkedin.pdf` or `data/summary.txt`, re-run this script.

### 6. Run the application

```bash
python app.py
```

Open your browser at: `http://127.0.0.1:7860`

---

## Configuration

All settings are centralised in `config/settings.py`. Change a value once — it applies everywhere.

| Setting | Default | Description |
|---------|---------|-------------|
| `GITHUB_MODEL` | `openai/gpt-4.1-mini` | Primary inference model |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Fallback inference model |
| `TEMPERATURE` | `0.4` | Response creativity — 0 = factual, 1 = creative |
| `MAX_TOKENS` | `1024` | Maximum tokens per response |
| `MAX_HISTORY_TURNS` | `10` | Conversation turns kept in context window |
| `MAX_INPUT_LENGTH` | `1000` | Max characters per user message |
| `CHUNK_SIZE` | `300` | Words per RAG chunk |
| `CHUNK_OVERLAP` | `50` | Overlap words between adjacent chunks |
| `TOP_K_CHUNKS` | `4` | Chunks retrieved and passed to the prompt |
| `GITHUB_MAX_RETRIES` | `3` | Retries before switching to Gemini |
| `RETRY_BASE_DELAY` | `2.0` | Base wait in seconds — doubles each retry (2s → 4s → 8s) |
| `REQUEST_TIMEOUT` | `30` | API call timeout in seconds |

---

## Deployment — Hugging Face Spaces

This project is designed for zero-config deployment on Hugging Face Spaces.

1. Fork or push this repository to your Hugging Face account
2. Go to **Settings → Variables and Secrets** in your Space
3. Add all four keys from `.env.example` as Repository Secrets
4. The Space builds automatically from `app.py`

> **Important:** The FAISS index at `data/indexes/faiss.index` must be committed to the repository before deployment. Build it locally first with `python scripts/build_index.py`, then push. Hugging Face Spaces cannot run the index build step at deploy time without the embedding model pre-cached.

---

## Running Tests

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run individual test files
python -m pytest tests/test_validator.py -v
python -m pytest tests/test_retrieval.py -v
python -m pytest tests/test_memory.py -v
python -m pytest tests/test_models.py -v
python -m pytest tests/recruiter_questions.py -v
```

---

## Design Decisions

**Why `core/` instead of `agent/`?**
The `openai-agents` and `agents` libraries both occupy the `agent` namespace. Naming the package `core/` avoids silent import collisions that would be very difficult to debug.

**Why Hybrid Retrieval instead of pure semantic search?**
Recruiter queries are frequently single words or acronyms — `"Kafka?"`, `"k8s?"`, `"testing?"`. Pure semantic search struggles with very short queries because the embeddings are noisy. Pure keyword search misses contextual understanding. The hybrid approach handles both — semantic retrieval for intent, keyword retrieval for exact technology matching, cross-encoder reranking to pick the best of both.

**Why a Query Normalizer?**
Recruiters write queries in shorthand. `"k8s"` and `"Kubernetes"` need to retrieve the same chunks. `"AWS?"` with trailing punctuation shouldn't confuse the tokenizer. Normalising before retrieval improves chunk matching accuracy without requiring more documents or better embeddings.

**Why persistent FAISS instead of rebuilding at startup?**
Embedding generation on CPU takes 10–30 seconds even for a small document set. On Hugging Face Spaces free tier, rebuilding on every cold start would make the app unusable for the first recruiter who visits. Pre-building and committing the index means the app is ready in under 5 seconds.

**Why Hugging Face Spaces instead of Render or Railway?**
HF Spaces provides a stable, recognisable public URL that recruiters and engineers trust. It supports Gradio natively with no Docker configuration. Cold starts are ~30 seconds — acceptable for someone who clicked a deliberate link from a resume or LinkedIn profile.

**Why Pydantic structured output instead of raw strings?**
A typed `AgentResponse` object lets the UI render follow-up question chips, trigger lead capture automatically when an email is detected, log unanswerable questions without regex parsing, and show confidence indicators — none of which are possible with plain string returns.

---

## Roadmap

- [ ] Streaming responses for faster perceived latency
- [ ] Recruiter session memory summarisation across long conversations
- [ ] Voice interaction mode
- [ ] Structured interview simulation mode
- [ ] Recruiter analytics dashboard (topic frequency, gap analysis)
- [ ] Company-specific retrieval — tailor responses to a job description
- [ ] Resume tailoring mode — highlight the most relevant experience per role
- [ ] GitHub Actions CI pipeline for automated test runs on every push

---

## Known Limitations

- Responses are intentionally restricted to uploaded professional documents — the assistant will not speculate or invent experience
- Free-tier Hugging Face Spaces may experience cold starts of ~30 seconds after periods of inactivity
- Real-time internet search is disabled to preserve factual grounding
- Optimised for recruiter-style conversations — not a general-purpose assistant
- FAISS index must be rebuilt manually whenever source documents change

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

If this project was useful or interesting, consider giving it a ⭐ on GitHub — it helps others discover it.

Built with Python · Gradio · OpenAI SDK · FAISS · Pydantic · Hugging Face Spaces

*This assistant is a digital resume. All responses are grounded in Rohit's actual professional documents.*

</div>
