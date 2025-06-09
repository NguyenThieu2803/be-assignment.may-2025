import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

@pytest.mark.asyncio
async def test_send_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Tạo 2 user với email ngẫu nhiên
        sender_email = f"sender_{uuid.uuid4()}@example.com"
        receiver_email = f"receiver_{uuid.uuid4()}@example.com"
        r1 = await ac.post("/users/", json={"email": sender_email, "name": "Sender"})
        r2 = await ac.post("/users/", json={"email": receiver_email, "name": "Receiver"})
        sender_id = r1.json()["id"]
        receiver_id = r2.json()["id"]
        # Gửi message
        payload = {
            "sender_id": sender_id,
            "subject": "Hello",
            "content": "Hello Receiver",
            "recipient_ids": [receiver_id]
        }
        response = await ac.post("/messages/", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello Receiver"
    assert data["sender_id"] == sender_id

@pytest.mark.asyncio
async def test_get_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Tạo 2 user với email ngẫu nhiên
        sender_email = f"sender2_{uuid.uuid4()}@example.com"
        receiver_email = f"receiver2_{uuid.uuid4()}@example.com"
        r1 = await ac.post("/users/", json={"email": sender_email, "name": "Sender2"})
        r2 = await ac.post("/users/", json={"email": receiver_email, "name": "Receiver2"})
        sender_id = r1.json()["id"]
        receiver_id = r2.json()["id"]
        # Gửi message
        payload = {
            "sender_id": sender_id,
            "subject": "Hi",
            "content": "Hi Receiver2",
            "recipient_ids": [receiver_id]
        }
        r_msg = await ac.post("/messages/", json=payload)
        msg_id = r_msg.json()["id"]
        # Lấy message
        response = await ac.get(f"/messages/{msg_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == msg_id
    assert data["content"] == "Hi Receiver2"

@pytest.mark.asyncio
async def test_user_creation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = f"alice_{uuid.uuid4()}@example.com"
        response = await ac.post("/users/", json={"email": email, "name": "Alice"})
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Alice"