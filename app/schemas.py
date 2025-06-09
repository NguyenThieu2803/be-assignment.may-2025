# Pydantic models
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str

class User(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    sender_id: UUID
    subject: Optional[str] = None
    content: str
    recipient_ids: List[UUID]

class Message(BaseModel):
    id: UUID
    sender_id: UUID
    subject: Optional[str]
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
class MessageDetail(Message):
    recipient_ids: List[UUID]