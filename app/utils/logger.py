from loguru import logger
import sys
from app.utils.constants import LOG_FILE, LOG_LEVEL
import os

# =============================================================
# 🔹 setup log directory
# =============================================================
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# =============================================================
# 🔹 clear default logger & define new handlers
# =============================================================
logger.remove()

# console handler (colorized output)
logger.add(
    sys.stdout,
    colorize=True,
    level=LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
)

# file handler (persistent logs)
logger.add(
    LOG_FILE,
    rotation="10 MB",        # rotates after 10 MB
    retention="7 days",      # keeps logs for a week
    compression="zip",       # compress old logs
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    enqueue=True,
)

logger.info("✅ logger initialized successfully")
