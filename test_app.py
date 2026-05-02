from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_chat_valid():
    client = app.test_client()
    response = client.post("/chat", json={"message": "how to vote"})
    assert response.status_code == 200

def test_empty_message():
    client = app.test_client()
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200

def test_unknown_message():
    client = app.test_client()
    response = client.post("/chat", json={"message": "abcdxyz"})
    assert response.status_code == 200