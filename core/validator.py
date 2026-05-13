import re


class RequestValidator:
    """
    Handles recruiter query validation.
    """

    # =====================================
    # Prompt Injection / Unsafe Patterns
    # =====================================

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "reveal system prompt",
        "show hidden prompt",
        "system instructions",
        "disable guardrails",
        "bypass safety",
        "api key",
        "password",
        "token",
        "secret",
        "malware",
        "how to hack",
    ]

    # =====================================
    # Allowed Recruiter Intent Patterns
    # =====================================

    ALLOWED_PATTERNS = [
        r"tell me about",
        r"explain",
        r"describe",
        r"did rohit",
        r"does rohit",
        r"has rohit",
        r"how did rohit",
        r"what experience",
        r"what skills",
        r"which technologies",
        r"which tools",
    ]

    # =====================================
    # Professional / Technical Topics
    # =====================================

    DOMAIN_TERMS = [
        # Backend
        "python",
        "backend",
        "microservices",
        "rest api",
        "graphql",
        "postgres",
        "sql",
        # Cloud / DevOps
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "jenkins",
        "devops",
        "ci/cd",
        "linux",
        "vmware",
        "cloud",
        "cloud architecture",
        # AI / ML
        "ai",
        "artificial intelligence",
        "genai",
        "generative ai",
        "ml",
        "machine learning",
        "llm",
        "llms",
        "rag",
        "agentic ai",
        "agents",
        "ai agents",
        "embeddings",
        "inference",
        "nlp",
        "deep learning",
        "transformers",
        "prompt engineering",
        "fine tuning",
        "model evaluation",
        "model serving",
        # RAG / Retrieval
        "semantic search",
        "vector database",
        "faiss",
        "retrieval",
        # AI Frameworks / Platforms
        "langchain",
        "openai",
        "gemini",
        "github models",
        "huggingface",
        # Testing
        "testing",
        "tdd",
        "unit test",
        "unit tests",
        "pact",
        "functional test",
        "functional tests",
        # Career / Profile
        "leadership",
        "software engineering",
        "certification",
        "certifications",
        "api",
        "apis",
        "deployment",
        "deployments",
        "pipeline",
        "pipelines",
        "automation",
        "containerization",
        "orchestration",
        "distributed systems",
        # Data / Analytics
        "data science",
        "data scientist",
        "analytics",
        "predictive analytics",
        "forecasting",
        "forecast",
        "statistics",
        "feature engineering",
        "data engineering",
        "data pipeline",
        "visualization",
        "experimentation",
        "model catalog",
        "scoring",
        # Domain / Business
        "credit",
        "loan",
        "legal",
        "documents",
        "industry",
        "memo",
        "scenario",
        "peer analysis",
        # Search / Storage
        "elasticsearch",
        # Teradata Specific
        "teradata",
        "mle",
        "val",
        "fastexport",
        "nos",
        "geospatial",
        # Companies / Enterprise
        "oaknorth",
        "dbt",
    ]

    # =====================================
    # Precompiled Regex Patterns
    # =====================================

    COMPILED_PATTERNS = [re.compile(pattern) for pattern in ALLOWED_PATTERNS]

    # =====================================
    # Validation
    # =====================================

    # @classmethod
    # def validate(cls, query: str) -> tuple[bool, str]:

    #     logger.info("Validating recruiter query")

    #     # =====================================
    #     # Empty Query Check
    #     # =====================================

    #     if not query or not query.strip():
    #         return (
    #             False,
    #             "Please enter a valid recruiter question.",
    #         )

    #     normalized_query = query.lower().strip()

    #     # =====================================
    #     # Query Length Protection
    #     # =====================================

    #     if len(normalized_query) > 500:
    #         logger.warning(f"Very long query detected: {query}")

    #         return (
    #             False,
    #             "Recruiter query is too long.",
    #         )

    #     # =====================================
    #     # Gibberish / Very Short Query Check
    #     # =====================================

    #     if len(normalized_query.split()) < 3:
    #         return (
    #             False,
    #             "Please enter a complete recruiter question.",
    #         )

    #     # =====================================
    #     # Prompt Injection Detection
    #     # =====================================

    #     for pattern in cls.BLOCKED_PATTERNS:
    #         if pattern in normalized_query:
    #             logger.warning(f"Blocked unsafe query detected: {query}")

    #             return (
    #                 False,
    #                 "I cannot comply with unsafe instructions.",
    #             )

    #     # =====================================
    #     # Recruiter Intent Validation
    #     # =====================================

    #     has_allowed_pattern = any(
    #         pattern.search(normalized_query) for pattern in cls.COMPILED_PATTERNS
    #     )

    #     # =====================================
    #     # Domain Relevance Validation
    #     # =====================================

    #     has_domain_term = any(
    #         re.search(rf"\b{re.escape(term)}\b", normalized_query)
    #         for term in cls.DOMAIN_TERMS
    #     )

    #     # =====================================
    #     # Final Validation Decision
    #     # =====================================

    #     if not (has_allowed_pattern or has_domain_term):
    #         logger.warning(f"Irrelevant recruiter query detected: {query}")

    #         return (
    #             False,
    #             "Please ask questions related to Rohit's "
    #             "professional experience, skills, projects, "
    #             "or technical background.",
    #         )

    #     logger.info("Recruiter query validation successful")

    #     return True, ""

    @staticmethod
    def validate(message: str):

        if not message or not message.strip():
            return False, "Please enter a recruiter question."

        normalized = message.lower().strip()

        for pattern in RequestValidator.BLOCKED_PATTERNS:
            if pattern in normalized:
                return False, (
                    "I can only discuss Rohit's professional "
                    "experience and technical background."
                )

        return True, ""
