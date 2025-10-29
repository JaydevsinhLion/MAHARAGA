from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter(tags=["admin"])

# -------------------------------------------------------------
# 🧾 list feedback or logs
# -------------------------------------------------------------
@router.get("/feedback")
async def get_feedback():
    """placeholder: returns system feedback list"""
    logger.info("📊 admin requested feedback records.")
    return {"status": "success", "data": [], "message": "feedback records (placeholder)"}


# -------------------------------------------------------------
# 🧠 system status
# -------------------------------------------------------------
@router.get("/status")
async def system_status():
    """returns current system stats"""
    logger.info("🧠 admin requested system status.")
    return {
        "status": "running",
        "uptime": "active",
        "message": "maharaga system stable and responsive."
    }
