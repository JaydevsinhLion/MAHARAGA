from fastapi import APIRouter, HTTPException
from app.config import JWT_SECRET, JWT_ALGORITHM
from datetime import datetime, timedelta
import jwt
from app.utils.logger import logger

router = APIRouter(tags=["auth"])

# -------------------------------------------------------------
# 🧩 token generator
# -------------------------------------------------------------
@router.post("/token")
async def generate_token(username: str):
    """generate jwt for admin or future users"""
    try:
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=60),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logger.info(f"🔐 token generated for user: {username}")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"❌ jwt generation failed: {e}")
        raise HTTPException(status_code=500, detail="token generation failed")


# -------------------------------------------------------------
# 🔍 verify token
# -------------------------------------------------------------
@router.get("/verify")
async def verify_token(token: str):
    """verify jwt token validity"""
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"status": "valid", "message": "token is active"}
    except jwt.ExpiredSignatureError:
        return {"status": "expired", "message": "token expired"}
    except jwt.InvalidTokenError:
        return {"status": "invalid", "message": "invalid token"}
