from fastapi import APIRouter, Request
from app.controllers.orchestrator_controller import process_query, QueryRequest

router = APIRouter(prefix="/api/v1", tags=["Maharaga"])

@router.get("/")
async def root():
    return {"message": "🧠 MAHARAGA API is running successfully!"}

@router.post("/maharaga")
async def maharaga_api(request: Request, body: QueryRequest):
    """Main endpoint for Maharaga AI"""
    return await process_query(request, body)
