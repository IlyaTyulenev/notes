import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    # register
    resp = await client.post("/auth/register", json={"email": "john@example.com", "password": "secret"})
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["email"] == "john@example.com"
    assert "id" in body

    # login
    resp = await client.post("/auth/login", json={"email": "john@example.com", "password": "secret"})
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    assert token and isinstance(token, str)
