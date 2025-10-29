from fastapi import Request
from pydantic import BaseModel
from app.services.generation_service import MaharagaModel
from app.services.policy_service import check_age_access, check_safety
from app.services.intent_service import detect_intent
from app.services.vector_service import retrieve_context
from app.services.rag_service import build_contextual_prompt
from app.utils.logger import logger

# -------------------------------------------------------------
# global model instance (loaded once on app startup)
# -------------------------------------------------------------
maharaga_model = MaharagaModel()


# -------------------------------------------------------------
# input schema
# -------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    user_age: int | None = None


# =============================================================
# 1️⃣ DEFAULT CONVERSATION HANDLER
# =============================================================
async def process_query(request: Request, body: QueryRequest):
    """core conversational logic with full safety & error handling"""
    try:
        query = body.query.strip().lower()
        user_age = body.user_age or 0

        # age validation
        if not check_age_access(user_age):
            return {
                "status": "error",
                "message": "access denied. age-restricted content available for 25+ only.",
            }

        # safety validation
        if not check_safety(query):
            return {
                "status": "error",
                "message": "query blocked due to unsafe or restricted content.",
            }

        # detect intent
        intent = detect_intent(query)
        logger.info(f"🧭 intent detected: {intent}")

        # generate model response
        ai_response = maharaga_model.generate_text(query)

        if not ai_response or ai_response.strip() == "":
            ai_response = "i'm not sure about that yet, but i'm learning every day."

        logger.info(f"🤖 response: {ai_response[:150]}...")

        return {
            "status": "success",
            "query": query,
            "intent": intent,
            "response": ai_response.lower(),
            "model": "distilgpt2",
            "source": "maharaga core v1.0",
        }

    except Exception as e:
        logger.error(f"❌ process_query failed: {e}")
        return {
            "status": "error",
            "message": "internal system error occurred while processing query.",
        }


# =============================================================
# 2️⃣ CONTEXTUAL QUERY HANDLER (RAG MODE)
# =============================================================
async def process_contextual_query(request: Request, body: QueryRequest):
    """handles context-aware generation using rag pipeline"""
    try:
        query = body.query.strip().lower()
        user_age = body.user_age or 0

        # safety & access checks
        if not check_age_access(user_age):
            return {
                "status": "error",
                "message": "restricted access. only 25+ users can use contextual mode.",
            }

        if not check_safety(query):
            return {
                "status": "error",
                "message": "query blocked due to policy restrictions.",
            }

        # intent detection
        intent = detect_intent(query)
        logger.info(f"📚 contextual mode intent: {intent}")

        # retrieve context
        try:
            context_docs = retrieve_context(query, intent=intent)
        except Exception as ctx_err:
            logger.error(f"❌ context retrieval failed: {ctx_err}")
            context_docs = []

        # build rag prompt
        full_prompt = build_contextual_prompt(query, context_docs or [])

        # generate text
        ai_response = maharaga_model.generate_text(full_prompt)

        return {
            "status": "success",
            "mode": "contextual",
            "intent": intent,
            "query": query,
            "response": ai_response.lower(),
            "context_used": bool(context_docs),
            "model": "distilgpt2",
            "source": "maharaga rag v1.0",
        }

    except Exception as e:
        logger.error(f"❌ process_contextual_query failed: {e}")
        return {
            "status": "error",
            "message": "internal system error while generating contextual response.",
        }


# =============================================================
# 3️⃣ INTENT DETECTION ENDPOINT
# =============================================================
async def detect_query_intent(request: Request, body: QueryRequest):
    """analyzes the intent/domain of a query only"""
    try:
        query = body.query.strip().lower()
        intent = detect_intent(query)
        confidence = "high" if intent != "unknown" else "low"

        return {
            "status": "success",
            "query": query,
            "detected_intent": intent,
            "confidence": confidence,
        }

    except Exception as e:
        logger.error(f"❌ detect_query_intent failed: {e}")
        return {
            "status": "error",
            "message": "failed to detect intent for the given query.",
        }


# =============================================================
# 4️⃣ SUPPORTED DOMAINS LIST
# =============================================================
async def list_supported_domains():
    """returns all available knowledge areas supported by maharaga"""
    try:
        domains = [
            "general conversation",
            "mathematics & logic reasoning",
            "programming & code assistance",
            "philosophy & scriptures",
            "science & biology",
            "health, anatomy & medicine",
            "relationship & 25+ education",
            "social sciences & human behavior",
            "operating systems & computing",
            "mythology & cultural knowledge",
        ]

        return {
            "status": "success",
            "total_domains": len(domains),
            "supported_domains": domains,
            "version": "maharaga core v1.0",
        }

    except Exception as e:
        logger.error(f"❌ list_supported_domains failed: {e}")
        return {
            "status": "error",
            "message": "could not retrieve domain list.",
        }
