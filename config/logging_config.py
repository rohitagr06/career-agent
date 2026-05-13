import logging
from pathlib import Path

from config.settings import settings

# =====================================
# Create Logs Directory
# =====================================

LOG_DIR = Path("telemetry/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# =====================================
# Log Format
# =====================================

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# =====================================
# Configure Logging
# =====================================

logging.basicConfig(
    level=settings.log_level,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "app.log"),
    ],
)

# =====================================
# Reusable Application Logger
# =====================================

logger = logging.getLogger("career_agent")
