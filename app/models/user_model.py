from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Pydantic schema (for validation and fastapi docs)
class UserBase(BaseModel):
    username: str = Field(..., example="Jaydevsinh")
    email: EmailStr
    age: Optional[int] = None
    is_verified_25plus: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# MongoDB schema (for internal DB ops)
def user_document(user: UserCreate):
    return {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "is_verified_25plus": bool(user.age and user.age >= 25),
        "password": user.password,  # will be hashed before saving
        "created_at": datetime.utcnow(),
    }
