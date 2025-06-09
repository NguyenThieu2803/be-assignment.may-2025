# FastAPI routes
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import get_db
import uuid

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=list[schemas.User])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.post("/messages/", response_model=schemas.Message)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = crud.create_message(db=db, message=message)
    return db_message

@router.get("/messages/sent/{user_id}", response_model=list[schemas.Message])
def view_sent_messages(user_id: uuid.UUID, db: Session = Depends(get_db)):
    messages = crud.get_sent_messages(db=db, user_id=user_id)
    return messages

@router.get("/messages/inbox/{user_id}", response_model=list[schemas.Message])
def view_inbox_messages(user_id: uuid.UUID, db: Session = Depends(get_db)):
    messages = crud.get_inbox_messages(db=db, user_id=user_id)
    return messages

@router.get("/messages/unread/{user_id}", response_model=list[schemas.Message])
def view_unread_messages(user_id: uuid.UUID, db: Session = Depends(get_db)):
    messages = crud.get_unread_messages(db=db, user_id=user_id)
    return messages

@router.get("/messages/{message_id}", response_model=schemas.MessageDetail)
def view_message(message_id: uuid.UUID, db: Session = Depends(get_db)):
    message = crud.get_message(db=db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    recipient_ids = [mr.recipient_id for mr in message.recipients]
    return {
        **message.__dict__,
        "recipient_ids": recipient_ids
    }

@router.post("/messages/{message_id}/read", response_model=schemas.Message)
def mark_message_as_read(message_id: uuid.UUID, db: Session = Depends(get_db)):
    message = crud.mark_message_as_read(db=db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message