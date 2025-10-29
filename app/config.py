"""
Maharaga Configuration File
---------------------------
Loads and validates all environment variables required
for backend services, AI operations, and authentication.
"""

import os
from dotenv import load_dotenv
from app.utils.logger import logger
from app.utils.database import connect_databases

# =============================================================
# 🔹 load .env file
# =============================================================
load_dotenv()

# =============================================================
# 🔹 core application metadata
# =============================================================
APP_NAME = os.getenv("APP_NAME", "Maharaga")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# =============================================================
# 🔹 security / authentication
# =============================================================
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# =============================================================
# 🔹 database connections
# =============================================================
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:123@localhost:5432/maharaga_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/maharaga")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# =============================================================
# 🔹 AI / model configuration
# =============================================================
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 150))

# =============================================================
# 🔹 misc and logging
# =============================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/maharaga.log")

# =============================================================
# 🔹 startup diagnostics
# =============================================================
def show_environment_summary():
    """print summarized environment info for diagnostics"""
    logger.info("──────────────────────────────────────────────")
    logger.info(f"⚙️ app: {APP_NAME} v{APP_VERSION}")
    logger.info(f"🌍 environment: {ENVIRONMENT}")
    logger.info(f"🔐 jwt algorithm: {JWT_ALGORITHM}")
    logger.info(f"🧠 model: {MODEL_NAME}")
    logger.info(f"🧩 embedding model: {EMBEDDING_MODEL}")
    logger.info(f"🗄️ postgres: {POSTGRES_URL.split('@')[-1]}")
    logger.info(f"🍃 mongo: {MONGO_URI.split('@')[-1]}")
    logger.info(f"📦 qdrant: {QDRANT_URL}")
    logger.info("──────────────────────────────────────────────")


# =============================================================
# 🔹 environment validation
# =============================================================
def validate_environment():
    """ensures all critical environment variables exist"""
    missing = []
    required = ["JWT_SECRET", "POSTGRES_URL", "MONGO_URI"]

    for var in required:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        logger.warning(f"⚠️ missing required environment variables: {', '.join(missing)}")
    else:
        logger.info("✅ all critical environment variables loaded successfully.")


# =============================================================
# 🔹 system lifecycle management
# =============================================================
def initialize_system():
    """initialize core components during app startup"""
    try:
        logger.info("🚀 initializing maharaga core systems...")
        connect_databases()
        logger.info("✅ maharaga system initialization complete.")
    except Exception as e:
        logger.error(f"❌ system initialization failed: {e}")


def shutdown_system():
    """cleanup or safely shutdown services"""
    try:
        logger.info("🛑 shutting down maharaga services...")
        # TODO: add session cleanup, cache clear, etc.
        logger.info("✅ system shutdown complete.")
    except Exception as e:
        logger.error(f"❌ system shutdown error: {e}")


# =============================================================
# 🔹 module initialization summary
# =============================================================
logger.info(f"⚙️ environment: {ENVIRONMENT}")
validate_environment()
show_environment_summary()
