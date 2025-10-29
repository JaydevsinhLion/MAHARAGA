from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Maharaga"])

@router.get("/")
async def root():
    return {"message": "🧠 MAHARAGA API is running successfully!"}
