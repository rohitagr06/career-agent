from agents import Runner
from google.genai import types

from config.logging_config import logger
from config.settings import settings
from core.models import gemini_client
from core.schemas import ChatResponse
from pipeline.instructions import FALLBACK_AGENT_INSTRUCTIONS


class ModelRouter:
    """
    Handles model routing and fallback logic.
    """

    @staticmethod
    async def run_with_fallback(agent, message: str) -> ChatResponse:
        """
        Run primary GitHub model first.
        Fallback to Gemini if primary fails.
        """

        # =====================================
        # Primary Model Attempt
        # =====================================

        try:
            logger.info("Attempting GitHub Models request")
            result = await Runner.run(
                starting_agent=agent,
                input=message,
            )
            logger.info("GitHub Models request successful")

            return ChatResponse(
                answer=result.final_output,
                model_used=settings.github_model,
                fallback_triggered=False,
            )

        # =====================================
        # Fallback Model
        # =====================================
        except Exception as github_error:
            logger.warning(
                "GitHub model failed. "
                f"Switching to Gemini fallback. Error: {github_error}"
            )

            try:
                fallback_message = f"""
                {FALLBACK_AGENT_INSTRUCTIONS}
                
                =====================================
                
                USER REQUEST
                
                =====================================
                {message}
                """
                response = gemini_client.models.generate_content(
                    model=settings.gemini_model,
                    contents=fallback_message,
                    config=types.GenerateContentConfig(
                        temperature=settings.temperature,
                        max_output_tokens=settings.max_tokens,
                    ),
                )

                logger.info("Gemini fallback successful")

                return ChatResponse(
                    answer=response.text or "",
                    model_used=settings.gemini_model,
                    fallback_triggered=True,
                )

            except Exception as gemini_error:
                logger.error(f"Gemini fallback also failed. Error: {gemini_error}")
                return ChatResponse(
                    answer=(
                        "I'm currently experiencing technical difficulties. "
                        "Please try again in a few moments."
                    ),
                    model_used="none",
                    fallback_triggered=True,
                )
