from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.MessageCreate, sender_id: UUID = None):
    # Nếu sender_id không truyền vào, lấy từ message
    if sender_id is None:
        sender_id = message.sender_id
    db_message = models.Message(
        sender_id=sender_id,
        subject=message.subject,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    # Thêm các recipient
    for rid in message.recipient_ids:
        db_recipient = models.MessageRecipient(message_id=db_message.id, recipient_id=rid)
        db.add(db_recipient)
    db.commit()
    return db_message

def send_message(db: Session, message: schemas.MessageCreate, sender_id: UUID):
    db_message = models.Message(**message.dict(), sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_sent_messages(db: Session, sender_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.sender_id == sender_id).offset(skip).limit(limit).all()

def get_inbox_messages(db: Session, recipient_id: UUID, skip: int = 0, limit: int = 100):
    return (db.query(models.Message)
            .join(models.MessageRecipient)
            .filter(models.MessageRecipient.recipient_id == recipient_id)
            .offset(skip).limit(limit).all())

def mark_message_as_read(db: Session, message_id: UUID, recipient_id: UUID):
    message_recipient = db.query(models.MessageRecipient).filter(
        models.MessageRecipient.message_id == message_id,
        models.MessageRecipient.recipient_id == recipient_id
    ).first()
    if message_recipient:
        message_recipient.read = True
        message_recipient.read_at = datetime.utcnow()
        db.commit()
    return message_recipient

def get_unread_messages(db: Session, recipient_id: UUID):
    return (db.query(models.Message)
            .join(models.MessageRecipient)
            .filter(models.MessageRecipient.recipient_id == recipient_id,
                    models.MessageRecipient.read == False).all())

def get_message(db: Session, message_id: UUID):
    return db.query(models.Message).filter(models.Message.id == message_id).first()