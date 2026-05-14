# ruff: noqa: E402
import asyncio
import sys
from pathlib import Path

from openai import RateLimitError

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pipeline.career_pipeline import CareerPipeline
from tests.recruiter_questions import RECRUITER_QUESTIONS

# =====================================
# Evaluation Settings
# =====================================

MAX_QUESTIONS = 10
QUESTION_COOLDOWN_SECONDS = 8
RATE_LIMIT_WAIT_SECONDS = 60
BATCH_COOLDOWN_SIZE = 5
BATCH_COOLDOWN_SECONDS = 30


# =====================================
# Main Evaluation Runner
# =====================================


async def run_evaluation():

    print("\n==============================")
    print("CAREER AGENT EVALUATION")
    print("==============================\n")

    questions = RECRUITER_QUESTIONS[:MAX_QUESTIONS]

    total_questions = len(questions)

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print(f"\n{'=' * 80}")
        print(f"[QUESTION {index}/{total_questions}]")
        print(f"Recruiter: {question}\n")

        try:
            response = await CareerPipeline.run(question)

            print("Assistant:\n")
            print(response.answer)

        except RateLimitError as error:
            print(f"Rate limit error detected: {error}")

            print(f"Waiting {RATE_LIMIT_WAIT_SECONDS} seconds...")

            await asyncio.sleep(RATE_LIMIT_WAIT_SECONDS)

            continue

        except Exception as error:
            print(f"Evaluation failed: {error}")

            continue

        # =====================================
        # Batch Cooldown
        # =====================================

        if index % BATCH_COOLDOWN_SIZE == 0:
            print(f"\nCooling down for {BATCH_COOLDOWN_SECONDS} seconds...")

            await asyncio.sleep(BATCH_COOLDOWN_SECONDS)

        # =====================================
        # Per Question Cooldown
        # =====================================

        print(f"\nWaiting {QUESTION_COOLDOWN_SECONDS} seconds...")

        await asyncio.sleep(QUESTION_COOLDOWN_SECONDS)

        print(f"\n{'=' * 80}\n")


# =====================================
# Entry Point
# =====================================

if __name__ == "__main__":
    asyncio.run(run_evaluation())
