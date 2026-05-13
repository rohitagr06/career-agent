from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPTS_DIR = BASE_DIR / "prompts"

# =====================================
# System Prompt
# =====================================

with open(
    PROMPTS_DIR / "system_prompt.txt",
    "r",
    encoding="utf-8",
) as file:
    CAREER_AGENT_INSTRUCTIONS = file.read()

# =====================================
# Fallback Prompt
# =====================================

with open(
    PROMPTS_DIR / "fallback_prompt.txt",
    "r",
    encoding="utf-8",
) as file:
    FALLBACK_AGENT_INSTRUCTIONS = file.read()
