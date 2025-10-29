from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class SessionBase(BaseModel):
    user_id: Optional[str] = None
    query: str
    response: str
    domain: Optional[str] = Field(default="conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# MongoDB-friendly schema creator
def session_document(session: SessionBase):
    return {
        "user_id": session.user_id,
        "query": session.query,
        "response": session.response,
        "domain": session.domain,
        "created_at": datetime.utcnow(),
    }
