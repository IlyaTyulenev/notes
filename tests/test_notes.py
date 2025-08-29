import pytest


async def auth_header(client, email="user1@example.com", password="pass"):
    await client.post("/auth/register", json={"email": email, "password": password})
    r = await client.post("/auth/login", json={"email": email, "password": password})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_crud_notes_isolated_by_user(client):
    h1 = await auth_header(client, "user1@example.com", "pass1")
    h2 = await auth_header(client, "user2@example.com", "pass2")

    # user1 creates 2 notes
    r = await client.post("/notes", headers=h1, json={"title": "N1", "content": "C1"})
    assert r.status_code == 201
    n1 = r.json()

    r = await client.post("/notes", headers=h1, json={"title": "N2", "content": "C2"})
    assert r.status_code == 201
    n2 = r.json()

    # user2 creates 1 note
    r = await client.post("/notes", headers=h2, json={"title": "U2N1", "content": "U2C1"})
    assert r.status_code == 201
    u2n1 = r.json()

    # list notes per user
    r = await client.get("/notes", headers=h1)
    assert r.status_code == 200
    user1_notes = r.json()
    assert len(user1_notes) == 2
    assert {user1_notes[0]["title"], user1_notes[1]["title"]} == {"N1", "N2"}

    r = await client.get("/notes", headers=h2)
    assert r.status_code == 200
    user2_notes = r.json()
    assert len(user2_notes) == 1
    assert user2_notes[0]["title"] == "U2N1"

    # get by id protected
    r = await client.get(f"/notes/{u2n1['id']}", headers=h1)
    assert r.status_code == 404

    # update own
    r = await client.put(f"/notes/{n1['id']}", headers=h1, json={"content": "UPDATED"})
    assert r.status_code == 200
    assert r.json()["content"] == "UPDATED"

    # delete own
    r = await client.delete(f"/notes/{n2['id']}", headers=h1)
    assert r.status_code == 204

    # ensure deleted
    r = await client.get("/notes", headers=h1)
    ids = [item["id"] for item in r.json()]
    assert n2["id"] not in ids
