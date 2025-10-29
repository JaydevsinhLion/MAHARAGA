from fastapi import APIRouter, Request
from app.controllers.orchestrator_controller import process_query
from app.controllers.safety_controller import safety_check, SafetyCheckRequest
from app.services.ml_service import MaharagaMLService
from app.utils.logger import logger

router = APIRouter(tags=["maharaga api"])

# =============================================================
# 🩺 HEALTH CHECK
# =============================================================
@router.get("/health")
async def health_check():
    """simple API health check"""
    logger.info("🩺 health check ping received.")
    return {
        "status": "ok",
        "message": "🧠 maharaga api operational.",
    }


# =============================================================
# 🧠 MAIN CONVERSATION ENDPOINT
# =============================================================
@router.post("/query")
async def query(request: Request):
    """
    receives user input → passes through safety + orchestrator layers
    for intelligent response generation.
    """
    try:
        data = await request.json()
        user_query = data.get("query", "").strip()
        user_age = data.get("user_age", 0)

        if not user_query:
            return {"status": "error", "message": "query cannot be empty."}

        # 1️⃣ run safety layer
        safety_body = SafetyCheckRequest(query=user_query, user_age=user_age)
        safe_check = await safety_check(request, safety_body)

        if safe_check.get("status") != "success":
            logger.warning("⚠️ query blocked by safety layer.")
            return safe_check

        # 2️⃣ run orchestrator (main AI logic)
        response = await process_query(request)
        return response

    except Exception as e:
        logger.error(f"❌ query route error: {e}")
        return {"status": "error", "message": "internal server failure."}


# =============================================================
# 🧩 TRAIN MAHARAGA MODEL
# =============================================================
@router.post("/train")
async def train_model(request: Request):
    """
    train the maharaga model from a provided csv file.
    auto-creates folders and placeholder files if missing.
    """
    try:
        data = await request.json()
        csv_path = data.get("csv_path", "").strip()
        epochs = int(data.get("epochs", 1))
        text_column = data.get("text_column", "text")

        if not csv_path:
            return {
                "status": "error",
                "message": "csv_path is required to start training.",
            }

        logger.info(f"⚙️ starting model training from {csv_path} for {epochs} epoch(s).")
        ml = MaharagaMLService()
        result = ml.train_from_csv(csv_path, text_column=text_column, epochs=epochs)

        logger.info(f"✅ training process completed with status: {result.get('status')}")
        return result

    except Exception as e:
        logger.error(f"❌ training route error: {e}")
        return {"status": "error", "message": f"training failed: {e}"}


# =============================================================
# 💬 GENERATE TEXT FROM MAHARAGA MODEL
# =============================================================
@router.post("/generate")
async def generate_text(request: Request):
    """
    generate intelligent text using the fine-tuned or base maharaga model.
    accepts a text prompt and returns generated output.
    """
    try:
        data = await request.json()
        prompt = data.get("prompt", "").strip()
        max_length = int(data.get("max_length", 150))

        if not prompt:
            return {"status": "error", "message": "prompt cannot be empty."}

        logger.info("🧠 generating response via maharaga model...")
        ml = MaharagaMLService()
        output = ml.generate_text(prompt, max_length=max_length)

        logger.info("✅ generation completed successfully.")
        return {"status": "success", "response": output}

    except Exception as e:
        logger.error(f"❌ generation route error: {e}")
        return {"status": "error", "message": f"generation failed: {e}"}
