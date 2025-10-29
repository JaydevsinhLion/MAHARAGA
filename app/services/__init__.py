"""
maharaga services package
-------------------------
this package houses all core AI subsystems — vector retrieval, 
RAG (retrieval-augmented generation), intent detection, 
generation pipeline, and safety policy handling.

each service operates independently but can be orchestrated 
together via the main orchestrator controller.
"""

from app.services.vector_service import VectorService, vector_service
from app.services.intent_service import detect_intent
from app.services.generation_service import MaharagaModel
from app.services.policy_service import PolicyService
from app.services import rag_service  # ✅ functional-style RAG module
from app.utils.logger import logger


# =============================================================
# 🔹 global instances (lazy-loaded singletons)
# =============================================================
try:
    vector_service_instance = vector_service  # already instantiated in vector_service.py
except Exception as e:
    logger.warning(f"⚠️ vector service not ready: {e}")
    vector_service_instance = None

try:
    maharaga_model = MaharagaModel()
except Exception as e:
    logger.warning(f"⚠️ maharaga model initialization failed: {e}")
    maharaga_model = None

try:
    policy_service = PolicyService()
except Exception as e:
    logger.warning(f"⚠️ policy service initialization failed: {e}")
    policy_service = None


# =============================================================
# 🔹 exported symbols
# =============================================================
__all__ = [
    # core systems
    "VectorService",
    "MaharagaModel",
    "PolicyService",
    "detect_intent",
    # instances
    "vector_service_instance",
    "maharaga_model",
    "policy_service",
    # modules
    "rag_service",
]

# =============================================================
# 🔹 startup log confirmation
# =============================================================
logger.info("🧩 services package initialized — vector, rag, intent, policy, and generation subsystems ready.")
