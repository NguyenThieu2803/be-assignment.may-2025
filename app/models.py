# SQLAlchemy or Tortoise models
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sent_messages = relationship("Message", back_populates="sender")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="sent_messages")
    recipients = relationship("MessageRecipient", back_populates="message")

class MessageRecipient(Base):
    __tablename__ = "message_recipients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"))
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    message = relationship("Message", back_populates="recipients")
