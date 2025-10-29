from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class FeedbackBase(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: Optional[str] = Field(None, example="Very insightful answer!")
    created_at: datetime = Field(default_factory=datetime.utcnow)

def feedback_document(feedback: FeedbackBase):
    return {
        "user_id": feedback.user_id,
        "session_id": feedback.session_id,
        "rating": feedback.rating,
        "comment": feedback.comment,
        "created_at": datetime.utcnow(),
    }
