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
        # Hybrid Retrieval
        # =====================================

        if is_contact_query:
            retrieved_chunks = CareerPipeline.retriever.retrieve(
                query="professional email linkedin contact information",
                semantic_top_k=10,
                keyword_top_k=10,
                final_top_k=10,
            )

        else:
            retrieved_chunks = CareerPipeline.retriever.retrieve(
                query=request.message,
                semantic_top_k=5,
                keyword_top_k=5,
                final_top_k=3,
            )

        logger.info(
            f"Hybrid retrieval completed. Total chunks: {len(retrieved_chunks)}"
        )

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1,
        ):
            logger.info(f"[Final Chunk {index}] {chunk['text'][:300]}")

        # =====================================
        # Build Context
        # =====================================

        context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)

        # =====================================
        # Conversation Memory
        # =====================================

        memory_context = CareerPipeline.memory.get_context()

        # =====================================
        # Grounded Prompt
        # =====================================
        grounded_prompt = f"""
        You are Virtual Rohit.

        Answer recruiter questions ONLY using the retrieved information.

        STRICT RULES:

        1. Never assume missing experience.
        2. Never infer that Rohit lacks a skill unless explicitly stated.
        3. If the retrieved context does not mention a technology,
        say:
        "I could not find that technology mentioned in the available experience data."
        4. Do not invent projects, tools, responsibilities, or expertise.
        5. Keep answers concise and recruiter-friendly.
        6. Prefer exact wording from retrieved chunks.

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
