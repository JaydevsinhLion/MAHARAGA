"""
maharaga utils package
----------------------
provides all utility-level helpers used across the maharaga system,
including configuration constants, database connectors, logging setup,
and semantic embedding services.
"""

# =============================================================
# 🔹 core imports (lazy-loaded utilities)
# =============================================================
from app.utils import constants
from app.utils.logger import logger
from app.utils.database import (
    connect_databases,
    get_postgres_engine,
    get_mongo_db,
    get_qdrant_client,
)
from app.utils.embeddings import embedding_helper


# =============================================================
# 🔹 exposed utility symbols
# =============================================================
__all__ = [
    "constants",
    "logger",
    "connect_databases",
    "get_postgres_engine",
    "get_mongo_db",
    "get_qdrant_client",
    "embedding_helper",
]


# =============================================================
# 🔹 startup log confirmation
# =============================================================
logger.info("🧩 utils package initialized successfully — constants, logger, db, embeddings ready.")
