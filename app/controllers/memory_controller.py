from fastapi import Request
from pydantic import BaseModel
from app.utils.database import get_mongo_db
from app.models.session_model import SessionBase, session_document
from app.models.feedback_model import FeedbackBase, feedback_document
from app.utils.logger import logger
from datetime import datetime


# -------------------------------------------------------------
# database connection
# -------------------------------------------------------------
db = get_mongo_db()


# -------------------------------------------------------------
# schema for api requests
# -------------------------------------------------------------
class MemoryRequest(BaseModel):
    user_id: str
    query: str
    response: str
    domain: str | None = "general"


class FeedbackRequest(BaseModel):
    user_id: str
    session_id: str
    rating: int
    comment: str | None = None


class HistoryRequest(BaseModel):
    user_id: str
    limit: int | None = 10


# =============================================================
# 1️⃣ save chat session
# =============================================================
async def save_session(request: Request, body: MemoryRequest):
    """saves chat sessions and responses to mongodb"""
    try:
        session = SessionBase(
            user_id=body.user_id,
            query=body.query.lower(),
            response=body.response.lower(),
            domain=body.domain or "general",
            created_at=datetime.utcnow()
        )

        db["sessions"].insert_one(session_document(session))
        logger.info(f"💾 session saved for user: {body.user_id}")

        return {
            "status": "success",
            "message": "session stored successfully."
        }

    except Exception as e:
        logger.error(f"❌ save_session failed: {e}")
        return {
            "status": "error",
            "message": "failed to store session data."
        }


# =============================================================
# 2️⃣ retrieve recent sessions
# =============================================================
async def get_user_sessions(request: Request, body: HistoryRequest):
    """retrieves recent chat history for a given user"""
    try:
        user_id = body.user_id.strip()
        limit = body.limit or 10

        sessions = list(
            db["sessions"]
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(limit)
        )

        if not sessions:
            return {
                "status": "success",
                "message": "no previous sessions found.",
                "sessions": []
            }

        for s in sessions:
            s["_id"] = str(s["_id"])  # make json serializable

        return {
            "status": "success",
            "message": "user session history retrieved successfully.",
            "count": len(sessions),
            "sessions": sessions
        }

    except Exception as e:
        logger.error(f"❌ get_user_sessions failed: {e}")
        return {
            "status": "error",
            "message": "failed to fetch session history."
        }


# =============================================================
# 3️⃣ store feedback for a session
# =============================================================
async def save_feedback(request: Request, body: FeedbackRequest):
    """saves user feedback on chatbot responses"""
    try:
        feedback = FeedbackBase(
            user_id=body.user_id,
            session_id=body.session_id,
            rating=body.rating,
            comment=(body.comment or "").lower(),
            created_at=datetime.utcnow()
        )

        db["feedbacks"].insert_one(feedback_document(feedback))
        logger.info(f"📝 feedback recorded for user {body.user_id}")

        return {
            "status": "success",
            "message": "feedback submitted successfully."
        }

    except Exception as e:
        logger.error(f"❌ save_feedback failed: {e}")
        return {
            "status": "error",
            "message": "failed to submit feedback."
        }


# =============================================================
# 4️⃣ fetch feedback by user
# =============================================================
async def get_user_feedback(request: Request, body: HistoryRequest):
    """retrieves user feedback records"""
    try:
        user_id = body.user_id.strip()
        feedbacks = list(
            db["feedbacks"]
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(20)
        )

        if not feedbacks:
            return {
                "status": "success",
                "message": "no feedback found for this user.",
                "feedbacks": []
            }

        for f in feedbacks:
            f["_id"] = str(f["_id"])

        return {
            "status": "success",
            "message": "user feedback retrieved successfully.",
            "count": len(feedbacks),
            "feedbacks": feedbacks
        }

    except Exception as e:
        logger.error(f"❌ get_user_feedback failed: {e}")
        return {
            "status": "error",
            "message": "failed to retrieve user feedback."
        }
