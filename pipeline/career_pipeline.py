from agents import Agent

from config.logging_config import logger
from core.formatter import ResponseFormatter
from core.models import github_model
from core.router import ModelRouter
from core.schemas import ChatRequest, ChatResponse
from core.validator import RequestValidator
from pipeline.instructions import CAREER_AGENT_INSTRUCTIONS
from pipeline.memory import ConversationMemory
from rag.faiss_store import FAISSStore
from rag.keyword_search import KeywordSearch
from rag.reranker import Reranker
from rag.retriever import Retriever
from rag.storage import index_exists


class CareerPipeline:
    # =====================================
    # Conversation Memory
    # =====================================

    memory = ConversationMemory()

    # =====================================
    # Initialize Persistent RAG
    # =====================================

    logger.info("Initializing persistent RAG pipeline")

    if not index_exists():
        raise FileNotFoundError(
            "FAISS index not found. Run scripts/build_index.py first."
        )

    vector_store = FAISSStore()

    vector_store.load()

    chunks = vector_store.chunks

    retriever = Retriever(
        vector_store=vector_store,
    )

    logger.info("Persistent RAG pipeline initialized successfully")

    # =====================================
    # Contact Query Keywords
    # =====================================

    CONTACT_KEYWORDS = [
        "email",
        "mail",
        "gmail",
        "contact",
        "phone",
        "mobile",
        "linkedin",
        "reach you",
        "reach out",
        "connect with you",
    ]

    # =====================================
    # Main Execution
    # =====================================

    @staticmethod
    async def run(
        message: str,
    ) -> ChatResponse:
        """
        Execute recruiter workflow.
        """

        logger.info("Career pipeline started")

        # =====================================
        # Build Request
        # =====================================

        request = ChatRequest(message=message)

        # =====================================
        # Validate Request
        # =====================================

        is_valid, validation_message = RequestValidator.validate(request.message)

        if not is_valid:
            logger.warning("Recruiter query validation failed")

            return ChatResponse(
                answer=validation_message,
                model_used="validator",
                fallback_triggered=False,
            )

        logger.info("Request validation successful")

        # =====================================
        # Store User Message
        # =====================================

        CareerPipeline.memory.add_user_message(request.message)

        # =====================================
        # Detect Contact Queries
        # =====================================

        is_contact_query = any(
            keyword in request.message.lower()
            for keyword in CareerPipeline.CONTACT_KEYWORDS
        )

        if is_contact_query:
            logger.info("Contact-related query detected")

        # =====================================
        # Semantic Retrieval
        # =====================================

        if is_contact_query:
            semantic_chunks = CareerPipeline.retriever.retrieve(
                query="professional email linkedin contact information",
                top_k=10,
            )

        else:
            semantic_chunks = CareerPipeline.retriever.retrieve(
                query=request.message,
                top_k=5,
            )

        # =====================================
        # Keyword Retrieval
        # =====================================

        if is_contact_query:
            keyword_chunks = KeywordSearch.search(
                query="email linkedin contact",
                chunks=CareerPipeline.chunks,
                top_k=10,
            )

        else:
            keyword_chunks = KeywordSearch.search(
                query=request.message,
                chunks=CareerPipeline.chunks,
                top_k=5,
            )

        # =====================================
        # Hybrid Merge
        # =====================================

        candidate_chunks = list(dict.fromkeys(semantic_chunks + keyword_chunks))

        logger.info(f"Retrieved candidate chunks: {len(candidate_chunks)}")

        for index, chunk in enumerate(
            candidate_chunks,
            start=1,
        ):
            logger.info(f"[Candidate Chunk {index}] {chunk[:300]}")

        # =====================================
        # Reranking
        # =====================================

        if is_contact_query:
            logger.info("Skipping reranking for contact query")
            retrieved_chunks = candidate_chunks[:10]
        else:
            retrieved_chunks = Reranker.rerank(
                query=request.message,
                chunks=candidate_chunks,
                top_k=3,
            )

        logger.info("Final reranked chunks")

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1,
        ):
            logger.info(f"[Final Chunk {index}] {chunk[:300]}")

        logger.info(
            f"Hybrid retrieval completed. Total chunks: {len(retrieved_chunks)}"
        )

        # =====================================
        # Build Context
        # =====================================

        context = "\n\n".join(retrieved_chunks)

        # =====================================
        # Conversation Memory
        # =====================================

        memory_context = CareerPipeline.memory.get_context()

        # =====================================
        # Grounded Prompt
        # =====================================
        grounded_prompt = f"""
        Use the following recruiter conversation history and
        retrieved professional information to answer naturally
        as Virtual Rohit.

        Only answer using retrieved information.

        If information is unavailable:

        * say so naturally
        * do not hallucinate
        * do not invent experience
        * do not fabricate technologies

        ==================================================
        CONVERSATION HISTORY

        {memory_context}

        ==================================================
        RETRIEVED PROFESSIONAL INFORMATION

        {context}

        ==================================================
        RECRUITER QUESTION

        {request.message}
        """

        career_agent = Agent(
            name="Career Agent",
            instructions=CAREER_AGENT_INSTRUCTIONS,
            model=github_model,
        )

        logger.info("Career agent initialized")

        # =====================================
        # Execute
        # =====================================

        response = await ModelRouter.run_with_fallback(
            agent=career_agent,
            message=grounded_prompt,
        )

        logger.info("Pipeline execution completed")

        # =====================================
        # Format Response
        # =====================================

        response.answer = ResponseFormatter.clean_response(response.answer)

        # =====================================
        # Store Assistant Response
        # =====================================

        CareerPipeline.memory.add_assistant_message(response.answer)

        return response
