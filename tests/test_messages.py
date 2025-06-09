import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
import uuid

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Tạo user với email ngẫu nhiên
        email = f"alice_{uuid.uuid4()}@example.com"
        response = await ac.post("/users/", json={"email": email, "name": "Alice"})
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Alice"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Tạo user với email ngẫu nhiên
        email = f"bob_{uuid.uuid4()}@example.com"
        response = await ac.post("/users/", json={"email": email, "name": "Bob"})
        assert response.status_code == 200 or response.status_code == 201
        user_id = response.json()["id"]
        # Lấy user theo id
        response = await ac.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Bob"
    assert data["id"] == user_id