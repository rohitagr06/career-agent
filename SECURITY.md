# Security Policy

This document describes the security policy for the Virtual Rohit project, including how to report vulnerabilities, what is considered a security issue, and what contributors and users should never do.

---

## Table of Contents

- [Supported Versions](#supported-versions)
- [Reporting a Vulnerability](#reporting-a-vulnerability)
- [What Counts as a Security Issue](#what-counts-as-a-security-issue)
- [What Does Not Count](#what-does-not-count)
- [API Key Safety](#api-key-safety)
- [Prompt Injection Policy](#prompt-injection-policy)
- [Response Grounding Policy](#response-grounding-policy)
- [Dependency Security](#dependency-security)
- [Known Accepted Risks](#known-accepted-risks)
- [Security Roadmap](#security-roadmap)

---

## Supported Versions

Only the latest version on the `main` branch receives security fixes.

| Version | Supported |
|---------|-----------|
| `main` (latest) | ✅ Yes |
| Older branches / forks | ❌ No |

If you are running a fork or an older version, update to `main` before reporting an issue — it may already be fixed.

---

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Public issues are visible to everyone immediately. If the vulnerability is exploitable, disclosing it publicly before a fix is ready puts all users of the live demo at risk.

Instead, report privately:

| Channel | Details |
|---------|---------|
| 📧 Email | rohitagr06@gmail.com |
| 💼 LinkedIn | [linkedin.com/in/rohitagr06](https://www.linkedin.com/in/rohitagr06) |

### What to include in your report

- A clear description of the vulnerability
- Which component is affected (`core/validator.py`, `rag/retriever.py`, `pipeline/`, etc.)
- Steps to reproduce the issue
- What an attacker could achieve by exploiting it
- Whether you have a suggested fix

### What to expect after reporting

- Acknowledgement within **72 hours**
- An assessment of severity and exploitability within **7 days**
- A fix or mitigation plan communicated privately before any public disclosure
- Credit in the release notes if you would like it

Please do not disclose the vulnerability publicly until a fix has been released and you have been notified.

---

## What Counts as a Security Issue

### Prompt injection
Any input that causes the assistant to:
- Reveal the contents of `prompts/system_prompt.txt`
- Claim to be a different AI model or persona
- Generate false professional experience not present in the knowledge base
- Follow instructions embedded in a user message that override the system prompt

### Data leakage
Any mechanism that causes the assistant to expose:
- The raw contents of `data/linkedin.pdf` or `data/summary.txt` verbatim
- Internal configuration values from `config/settings.py`
- Environment variable names or values
- API keys, tokens, or secrets

### Input validation bypass
Any input that:
- Bypasses `core/validator.py` and reaches the model unfiltered
- Causes the validator to raise an unhandled exception and fail open (i.e., let the input through instead of rejecting it)
- Exceeds the `MAX_INPUT_LENGTH` limit without being caught

### Denial of service
Any input or sequence of inputs that:
- Causes the application to hang indefinitely
- Triggers an infinite retry loop in `core/retry.py` or `core/router.py`
- Exhausts API quota in a way that is triggered by a single crafted request

### Dependency vulnerability
A known CVE in any direct dependency listed in `requirements.txt` or `pyproject.toml` that has a confirmed fix available.

---

## What Does Not Count

The following are **not** considered security vulnerabilities for this project:

- The assistant giving an inaccurate or incomplete answer — this is a retrieval quality issue, not a security issue. Report it as a bug.
- Cold starts on Hugging Face Spaces — this is an infrastructure limitation, not a vulnerability.
- Rate limiting by GitHub Models or Google Gemini — this is provider behaviour, not a vulnerability.
- The assistant declining to answer a question — this is intentional guardrail behaviour.
- The system prompt being detectable as "AI-generated" — the assistant is openly an AI agent.
- Theoretical attacks with no practical reproduction steps.

---

## API Key Safety

This is the most common real-world security failure on AI projects. Follow these rules without exception.

**Never commit secrets to the repository.**

```bash
# Wrong — this commits your actual key
GITHUB_API_KEY=ghp_abc123...

# Right — use .env which is in .gitignore
cp .env.example .env
# Fill in .env locally, never commit it
```

**What to do if you accidentally commit a key:**

1. Rotate the key immediately — assume it is compromised the moment it touches Git history
2. Go to the provider dashboard and revoke the exposed key:
   - GitHub PAT: [github.com/settings/tokens](https://github.com/settings/tokens)
   - Google AI Studio: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
   - Pushover: [pushover.net](https://pushover.net)
3. Generate a new key and store it only in `.env` locally and in Hugging Face Secrets for deployment
4. Use `git filter-repo` or contact GitHub Support to purge the key from Git history — simply deleting the file in a new commit is not enough, the key remains in the history

**Never include keys in:**
- Issue descriptions
- Pull request descriptions or comments
- Code comments
- Commit messages
- Notebook outputs (`notebooks/*.ipynb` can embed cell outputs — clear outputs before committing)

---

## Prompt Injection Policy

The live Hugging Face Space at [huggingface.co/spaces/manuagr03/career-agent](https://huggingface.co/spaces/manuagr03/career-agent) is monitored.

All user input passes through `core/validator.py` before reaching the model. The validator detects and rejects messages containing known injection patterns including:

```
ignore previous instructions
disregard all instructions
forget everything
you are now
new persona
act as
system:
[INST]
```

Attempts to extract the system prompt, override the persona, or generate fabricated experience are logged via the `record_unknown_question` tool and trigger a Pushover notification.

**Security researchers** who discover a genuine bypass in the validator are encouraged to report it privately rather than exploit it. See [Reporting a Vulnerability](#reporting-a-vulnerability).

---

## Response Grounding Policy

The assistant is designed to generate responses grounded strictly in `data/linkedin.pdf` and `data/summary.txt`. It will not:

- Claim experience in technologies not present in those documents
- Invent project names, company names, or dates
- Agree with false premises about Rohit's background

If you observe the assistant confidently generating false professional information — not just vague or incomplete answers, but specific fabrications — this may indicate a retrieval or prompt vulnerability. Report it privately with the exact query that triggered it.

---

## Dependency Security

Dependencies are pinned in `uv.lock` for reproducible installs. To check for known vulnerabilities in the current dependency set:

```bash
# Using pip-audit
pip install pip-audit
pip-audit

# Using safety
pip install safety
safety check
```

If you discover a CVE in a direct dependency:

1. Check whether a patched version is available
2. Open a **private** report (not a public issue) with the CVE number, the affected package, and the version that fixes it
3. A dependency update PR will be prepared and merged promptly

Transitive dependency vulnerabilities (vulnerabilities in packages that our dependencies depend on) are assessed case by case based on whether the vulnerable code path is reachable.

---

## Known Accepted Risks

The following risks are known, have been assessed, and are accepted for this project given its scope and deployment context:

| Risk | Reason accepted |
|------|----------------|
| Free-tier API rate limits can cause temporary unavailability | Acceptable for a personal career demo; mitigated by fallback routing |
| Hugging Face Spaces free tier has no uptime SLA | Acceptable for the use case — recruiters click a deliberate link |
| FAISS index is stored in the repository | The index contains only embeddings of public professional information — no sensitive data |
| The system prompt can be partially inferred from the assistant's behaviour | The system prompt contains no secrets; the persona is intentionally public-facing |
| Pushover notifications may have delivery delays | Notifications are informational only; no critical path depends on them |

---

## Security Roadmap

Planned security improvements in priority order:

- [ ] GitHub Actions CI step: `pip-audit` on every PR to catch dependency CVEs automatically
- [ ] `pre-commit` hook: block commits containing common secret patterns (API key regexes)
- [ ] `mypy` strict mode: reduce risk of type confusion bugs in validation logic
- [ ] Rate limiting per session in the Gradio UI to prevent automated query flooding
- [ ] Structured logging for all validation rejections (currently only logged via Pushover)

---

*For general contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).*
*For project documentation, see [README.md](README.md).*
