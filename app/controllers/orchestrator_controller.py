from fastapi import Request
from pydantic import BaseModel
from app.services.generation_service import MaharagaModel

# Initialize model globally
maharaga_model = MaharagaModel()

class QueryRequest(BaseModel):
    query: str

async def process_query(request: Request, body: QueryRequest):
    """Core orchestration logic"""
    query = body.query.strip()

    # Generate AI response via model service
    ai_response = maharaga_model.generate_text(query)

    return {
        "status": "success",
        "query": query,
        "response": ai_response,
        "model": "distilgpt2",
        "source": "Maharaga Core v1.0"
    }
