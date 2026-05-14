# Contributing to Virtual Rohit

Thank you for taking the time to contribute. This document explains how the project is structured, how to set up a development environment, and what to expect during the contribution process.

---

## Table of Contents

- [Who Should Contribute?](#who-should-contribute)
- [What Can I Work On?](#what-can-i-work-on)
- [Project Structure Overview](#project-structure-overview)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Making Changes](#making-changes)
- [Commit Message Format](#commit-message-format)
- [Running Tests](#running-tests)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [CI — Continuous Integration](#ci--continuous-integration)
- [Architecture Philosophy](#architecture-philosophy)
- [Issue Templates](#issue-templates)
- [Security](#security)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [What Not to Change](#what-not-to-change)
- [Questions](#questions)

---

## Who Should Contribute?

Virtual Rohit is an open-source AI career conversation system designed for recruiter-facing interactions. Contributions are welcome from:

- Engineers who spot a bug or a factual error in the RAG pipeline
- Developers who want to improve retrieval quality, prompt design, or model routing
- Anyone who finds the architecture useful and wants to adapt it for their own career agent

If you are unsure whether your contribution fits, open an issue first and describe what you want to change. That avoids wasted effort on both sides.

---

## What Can I Work On?

Good areas for contribution:

| Area | Examples |
|------|---------|
| **RAG pipeline** | Improve chunking strategy, retrieval accuracy, reranking quality |
| **Query normalizer** | Add more abbreviation expansions, improve edge case handling |
| **Model router** | Better retry logic, smarter fallback decisions |
| **Prompt engineering** | Improve system prompt, fallback prompt, or validation prompt |
| **Tests** | Add missing test cases, improve coverage for edge cases |
| **UI** | Gradio theme improvements, better suggested questions, layout fixes |
| **Documentation** | Fix typos, clarify setup steps, improve code comments |
| **Evaluation** | Improve `scripts/evaluate.py` with better metrics or test datasets |

The [Roadmap section in README](README.md#roadmap) lists planned features that are good candidates for contribution.

---

## Project Structure Overview

Before making changes, understand which layer your change belongs to:

```
config/       — all settings live here, never hardcode values elsewhere
core/         — utilities: validation, routing, retry, schemas, history
pipeline/     — orchestration: how components connect end-to-end
rag/          — retrieval system: embeddings, FAISS, chunking, reranking
prompts/      — prompt templates as plain text files
ui/           — Gradio interface components
scripts/      — one-off utilities: build index, evaluate, rebuild
tests/        — pytest test suite
data/         — knowledge files and FAISS index (not for editing)
```

A change to retrieval logic belongs in `rag/`. A change to how the pipeline runs belongs in `pipeline/`. A new tuneable setting belongs in `config/settings.py` — never hardcoded inside a module.

---

## Development Setup

### 1. Fork and clone

```bash
git clone https://github.com/your-username/career-agent.git
cd career-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
# Recommended
uv sync

# Or with pip
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Fill in GITHUB_API_KEY, GOOGLE_API_KEY, PUSHOVER_TOKEN, PUSHOVER_USER
```

### 5. Build the FAISS index

```bash
python scripts/build_index.py
```

### 6. Verify your setup

```bash
python -m pytest tests/ -v
```

All tests should pass before you make any changes. If they do not, open an issue.

---

## Branching Strategy

Always branch off `main`. Use this naming convention:

| Type | Branch name |
|------|-------------|
| Bug fix | `fix/short-description` |
| New feature | `feat/short-description` |
| Documentation | `docs/short-description` |
| Refactor | `refactor/short-description` |
| Tests | `test/short-description` |

Examples:

```bash
git checkout -b fix/reranker-empty-query-crash
git checkout -b feat/query-normalizer-abbreviations
git checkout -b docs/improve-local-setup-steps
```

Never commit directly to `main`.

---

## Making Changes

### Before you start

- Open an issue describing what you plan to change and why
- Wait for acknowledgement before investing significant time
- Check open pull requests to avoid duplicating work

### While making changes

- Change one thing per pull request — do not bundle unrelated fixes together
- If you add a new tuneable parameter, add it to `config/settings.py` with a sensible default and document it in the `README.md` configuration table
- If you add a new module or file, add it to the Project Structure section in `README.md`
- If you change retrieval logic, rebuild the FAISS index and verify retrieval still works: `python scripts/build_index.py`
- If you change prompt templates in `prompts/`, test with at least the sample questions in `tests/recruiter_questions.py`

---

## Commit Message Format

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

| Type | When to use |
|------|-------------|
| `feat` | A new feature or capability |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `refactor` | Code restructuring with no behaviour change |
| `test` | Adding or updating tests |
| `chore` | Dependency updates, config changes, tooling |
| `perf` | Performance improvements |

**Scopes** (optional but helpful):

`rag`, `core`, `pipeline`, `ui`, `prompts`, `config`, `scripts`, `tests`

**Examples:**

```
feat(rag): add BM25 keyword weight tuning to retriever
fix(core): prevent infinite retry loop when both APIs are unavailable
docs(readme): add FAISS deployment note to Hugging Face setup section
test(rag): add retrieval accuracy tests for short acronym queries
refactor(pipeline): extract tool dispatch into standalone function
chore: bump sentence-transformers to 3.1.0
```

Keep the subject line under 72 characters. Use the body to explain *why*, not *what* — the diff shows what changed.

---

## Running Tests

```bash
# Full test suite
python -m pytest tests/ -v

# Specific file
python -m pytest tests/test_retrieval.py -v

# With coverage report
python -m pytest tests/ --cov=. --cov-report=term-missing
```

**Requirements before submitting a pull request:**

- All existing tests must pass
- New features must include tests
- Bug fixes should include a test that would have caught the bug

If your change affects retrieval quality, run the recruiter QA suite and include the output in your pull request description:

```bash
python -m pytest tests/recruiter_questions.py -v
```

---

## Pull Request Process

1. **Push your branch** to your fork
2. **Open a pull request** against `main` on this repository
3. **Fill in the PR template** — describe what changed, why, and how to test it
4. **Link the related issue** using `Closes #issue-number` in the description
5. **Wait for review** — changes may be requested before merging

### PR description should include

- What problem this solves or what it adds
- Which files were changed and why
- How to test the change manually
- Whether the FAISS index needs to be rebuilt after merging
- Whether `README.md` or `CONTRIBUTING.md` was updated to reflect the change

### A pull request will not be merged if

- CI checks are failing (tests, formatting, or linting)
- Tests are failing locally but were not run before pushing
- A new setting was hardcoded instead of added to `config/settings.py`
- The change modifies `data/linkedin.pdf` or `data/summary.txt` (these are personal documents and not open for contribution)
- The change alters personal information, contact details, or the persona definition

---

## Code Style

This project follows standard Python conventions:

- **Formatter:** `black` with default settings (`line-length = 88`)
- **Linter:** `ruff`
- **Type hints:** required for all new functions and class methods
- **Docstrings:** required for all public functions and classes — use Google style

**Pinned versions** (defined in `pyproject.toml`):

```toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "N", "W"]
```

If you add a new dev dependency (formatter, linter, test tool), pin it in `pyproject.toml` under `[dependency-groups]` so CI and local environments stay consistent. A `pre-commit` config is planned — see the [Roadmap](README.md#roadmap).

**Format before committing:**

```bash
black .
ruff check . --fix
```

**Type hint example:**

```python
def retrieve(self, query: str, top_k: int = 4) -> str:
    """
    Retrieve the most relevant document chunks for a given query.

    Args:
        query: The normalised user query string.
        top_k: Number of top chunks to return.

    Returns:
        A single string with the top-k chunks joined by separators.
    """
```

---

## CI — Continuous Integration

All pull requests are automatically validated using GitHub Actions.

The CI pipeline runs on every push to a PR branch and checks:

| Check | Tool | Blocks merge? |
|-------|------|---------------|
| Unit tests | `pytest` | ✅ Yes |
| Formatting | `black --check` | ✅ Yes |
| Linting | `ruff check` | ✅ Yes |
| Type checking | `mypy` (planned) | 🔜 Soon |

**A pull request will not be merged if any CI check fails.**

To replicate CI locally before pushing:

```bash
# Tests
python -m pytest tests/ -v

# Formatting check (does not auto-fix — same as CI)
black --check .

# Linting check
ruff check .
```

Fix all failures locally before opening a PR. Do not push a PR expecting CI to tell you what to fix — that wastes review time.

> **Note:** The GitHub Actions workflow file lives at `.github/workflows/ci.yml`. If you are adding a new test file, make sure it follows the `test_*.py` naming convention so pytest discovers it automatically.

---

## Architecture Philosophy

Understanding the design principles helps you make contributions that fit the project's direction rather than pulling it in a different one.

**Retrieval-first grounding.**
The agent never generates experience from memory. Every factual claim must be retrievable from `data/linkedin.pdf` or `data/summary.txt`. If a question cannot be answered from those documents, the bot says so honestly. This is non-negotiable — contributions that loosen this constraint will not be accepted.

**Free-tier deployment philosophy.**
The entire stack runs on free infrastructure: GitHub Models, Google Gemini free tier, Hugging Face Spaces free tier, CPU-only FAISS. Any contribution that introduces a paid dependency (OpenAI paid API, paid vector DB, GPU requirement) must come with a free fallback path or it will not be merged.

**Recruiter-first UX.**
Recruiters are not developers. Queries will be short, ambiguous, and sometimes one word (`"Kafka?"`). The pipeline is optimised for this — short query handling, query normalisation, hybrid retrieval — not for long technical paragraphs. Contributions should make short queries work better, not assume well-formed input.

**Deterministic over creative.**
Temperature is set low (`0.4`) deliberately. Recruiters need consistent, factual answers — not creative paraphrasing that might introduce inaccuracies. Contributions that raise temperature or introduce more "personality" without improving accuracy will be questioned.

**Modular and independently testable.**
Each component (`rag/`, `core/`, `pipeline/`) is designed to work and be tested in isolation. Contributions that tightly couple previously independent modules make the codebase harder to maintain. Keep the layers clean.

---

## Issue Templates

Bug report and feature request templates are planned for `.github/ISSUE_TEMPLATE/`. Until they are added, follow the guidance in [Reporting Bugs](#reporting-bugs) and [Suggesting Features](#suggesting-features) when opening issues.

When templates are available, they will cover:

- **Bug report:** reproduction steps, expected vs actual behaviour, environment info
- **Feature request:** problem statement, proposed solution, layer affected, free-tier compatibility

---

## Security

Please read [SECURITY.md](SECURITY.md) before reporting any security-related issue.

The short version:

- **Do not open a public GitHub issue for security vulnerabilities.** Report them privately via the contact details in `SECURITY.md`.
- **Never include API keys** — not in issues, not in pull requests, not in commit messages. If you accidentally commit a key, rotate it immediately.
- **Do not attempt to extract the system prompt** through the live Hugging Face Space. This is prompt injection and is logged.
- **Do not submit pull requests that weaken input validation** in `core/validator.py` without a clear security justification.

---

## Reporting Bugs

Open a GitHub issue using the Bug Report template. Include:

- A clear description of the unexpected behaviour
- The query or input that triggered it
- What you expected to happen
- What actually happened (include any error messages or tracebacks)
- Your Python version and operating system

Do not include your actual API keys in any issue or pull request.

---

## Suggesting Features

Open a GitHub issue using the Feature Request template. Include:

- What problem the feature solves
- Which layer of the project it would touch (`rag/`, `core/`, `pipeline/`, etc.)
- Any implementation ideas you have
- Whether it fits within the free-API-only constraint of the project

Check the [Roadmap](README.md#roadmap) first — if it is already listed there, comment on the existing issue rather than opening a new one.

---

## What Not to Change

The following are out of scope for external contributions:

| Item | Reason |
|------|--------|
| `data/linkedin.pdf` | Personal document — not open for editing |
| `data/summary.txt` | Personal document — not open for editing |
| `prompts/system_prompt.txt` persona definition | Controls Rohit's professional identity — only Rohit changes this |
| Contact details in `README.md` | Personal information |
| Hugging Face Space URL or username references | Deployment-specific to Rohit's account |

---

## Questions

If anything in this guide is unclear, open a GitHub Discussion or raise it in an issue before starting work. It is better to ask upfront than to submit a pull request that cannot be merged.

---

*Thank you for contributing to Virtual Rohit.*
