import asyncio

import gradio as gr

from config.logging_config import logger
from config.settings import settings
from pipeline.career_pipeline import CareerPipeline

# =====================================
# Chat Handler
# =====================================


async def chat_handler(message, history):
    """
    Main recruiter chat handler.
    """

    try:
        logger.info("Incoming recruiter query received")
        response = await CareerPipeline.run(message)
        formatted_response = response.answer
        partial_response = ""

        for character in formatted_response:
            partial_response += character
            yield partial_response
            await asyncio.sleep(0.02)

        logger.info("Pipeline response generated successfully")

    except Exception as error:
        logger.error(f"Application error: {error}")
        yield (
            "I'm currently experiencing technical difficulties. "
            "Please try again in a few moments."
        )


# =====================================
# Suggested Questions
# =====================================

EXAMPLE_QUESTIONS = [
    "Tell me about Rohit's backend engineering experience",
    "What AI projects has Rohit built?",
    "What technologies does Rohit work with?",
    "Tell me about Rohit's GenAI experience",
    "What are Rohit's strongest technical skills?",
]

# =====================================
# Gradio UI
# =====================================

with gr.Blocks(title="Rohit AI Career Agent") as app:
    gr.Markdown("""
Welcome to Rohit's AI-powered career conversation assistant.
""")
    gr.ChatInterface(
        fn=chat_handler,
        examples=EXAMPLE_QUESTIONS,
        title="Virtual Rohit — AI Career Conversation Agent",
        description=(
            "Ask questions about Rohit's professional experience, "
            "projects, and technical expertise."
        ),
    )

# =====================================
# Launch Application
# =====================================

if __name__ == "__main__":
    logger.info("Starting Career Agent application")
    app.launch(
        server_port=settings.gradio_server_port,
        share=settings.gradio_share,
    )
