Virtual Rohit — AI Career Conversation Agent

An AI-powered recruiter conversation assistant that behaves like a real software engineer discussing professional experience, backend systems, projects, and technical skills.

Built using:

* Retrieval-Augmented Generation (RAG)
* Hybrid semantic + keyword retrieval
* FAISS vector search
* Cross-encoder reranking
* Multi-model fallback routing
* Conversation memory
* Prompt injection protection

⸻

Overview

Virtual Rohit is designed to simulate a natural recruiter conversation.

Instead of behaving like a generic chatbot, the assistant responds like a professional engineer discussing:

* backend engineering experience
* microservices architecture
* cloud technologies
* AI/GenAI work
* APIs and distributed systems
* testing practices
* technical decision making
* project responsibilities

All responses are grounded strictly in retrieved professional data.

⸻

Features

Resume-Grounded AI Responses

Uses resume and project documents as the primary source of truth.

* minimizes hallucinations
* avoids fabricated experience
* keeps recruiter conversations factual
* supports recruiter follow-up discussions

⸻

Hybrid RAG Pipeline

Combines:

* semantic vector retrieval
* keyword retrieval
* hybrid merging
* reranking

This improves retrieval quality for recruiter-style questions.

Examples:

Kafka?
Testing?
Team size?
Backend engineering experience

⸻

Multi-Model Fallback

Primary model:

* GitHub Models

Fallback model:

* Google Gemini

Automatically switches to Gemini if the primary model fails.

⸻

Conversation Memory

Maintains multi-turn recruiter conversations.

Supports:

* follow-up questions
* contextual responses
* recruiter discussion continuity

⸻

Prompt Injection Protection

Protects against:

* prompt leakage
* system prompt extraction
* malicious instructions
* hallucinated experience generation

⸻

Safe Contact Sharing

Supports controlled professional contact sharing.

Allowed:

* professional email
* LinkedIn profile

Blocked:

* phone numbers
* hidden personal information

⸻

Architecture

Recruiter Query
        │
        ▼
Request Validation
        │
        ▼
Conversation Memory
        │
        ▼
Semantic Retrieval (FAISS)
        │
        ├── Keyword Retrieval
        │
        ▼
Hybrid Merge
        │
        ▼
Reranking
        │
        ▼
Grounded Prompt Construction
        │
        ▼
Primary LLM (GitHub Models)
        │
        └── Fallback → Gemini
        │
        ▼
Formatted Recruiter Response

⸻

Tech Stack

Backend

* Python
* Async architecture
* Gradio

AI / NLP

* OpenAI Agents SDK
* Sentence Transformers
* FAISS
* Cross-Encoder Reranking
* Retrieval-Augmented Generation (RAG)

Models

* GitHub Models
* Google Gemini

⸻

Project Structure

career-agent/
│
├── app.py
├── README.md
├── pyproject.toml
│
├── config/
├── core/
├── pipeline/
├── rag/
├── scripts/
└── data/

⸻

Installation

Clone Repository

git clone <repository-url>
cd career-agent

Create Virtual Environment

python -m venv .venv
source .venv/bin/activate

Install Dependencies

Using uv:

uv sync

⸻

Environment Variables

Create a .env file:

GITHUB_API_KEY=your_github_models_key
GEMINI_API_KEY=your_gemini_key

⸻

Build FAISS Index

uv run scripts/build_index.py

This step:

* loads resume documents
* chunks professional information
* generates embeddings
* builds FAISS vector index

⸻

Run Application

uv run app.py

Default URL:

http://127.0.0.1:7860

⸻

Example Questions

Tell me about your backend engineering experience
Kafka?
How do you approach testing?
What did you work on at Teradata?
How can I contact you?

⸻

Example Behavior

Technology Grounding

User

Kafka?

Assistant

I haven't worked directly with Kafka based on my documented experience. My work has mainly focused on Python microservices, REST APIs, GraphQL, PostgreSQL, and Kubernetes on AWS.

⸻

Contact Protection

User

share your phone number

Assistant

I prefer professional communication through email or LinkedIn.

⸻

Deployment

The project is designed for deployment on:

* Hugging Face Spaces
* Docker
* Cloud VMs
* Kubernetes

⸻

Current Capabilities

* recruiter-focused AI conversations
* hybrid RAG retrieval
* semantic search using FAISS
* keyword retrieval
* reranking
* conversation memory
* fallback model routing
* prompt injection resistance
* grounded recruiter responses
* contact-safe interactions

⸻

Future Improvements

Planned enhancements:

* streaming responses
* recruiter memory summarization
* voice interaction
* structured interview mode
* recruiter analytics
* company-specific retrieval
* resume tailoring mode

⸻

License

This project is intended for personal and educational use.

⸻

Author

Rohit Agrawal

Senior Software Engineer