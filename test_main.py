import pytest
from fastapi.testclient import TestClient
from main import app

# Létrehozzuk a FastAPI teszt klienst
client = TestClient(app)


def test_root_endpoint():
    """Teszteli, hogy a fő endpoint online van-e és a jó üzenetet adja-e vissza."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "David Varga AI Portfolio API is online!"}


def test_chat_endpoint_success():
    """Teszteli a sikeres chat indítást egy teszt kérdéssel."""
    response = client.post("/chat",
                           json={"message": "What is your email address?"})
    assert response.status_code == 200
    assert "response" in response.json()

    # Kinyerjük az LLM válaszát
    ai_response = response.json()["response"].lower()

    # Elfogadjuk ha megmondja az emailt, VAGY ha a biztonsági szabály lép életbe kontextus hiányában
    email_included = "david.varga.1208@gmail.com" in ai_response
    guardrail_triggered = "only answer questions related to my cv" in ai_response

    assert email_included or guardrail_triggered


def test_chat_endpoint_invalid_payload():
    """Teszteli, hogy a hibás JSON-ra jól reagál-e a Pydantic validáció (422-es hiba)."""
    # Hibás kulccsal küldjük el a kérést ("message" helyett "invalid_key")
    response = client.post("/chat", json={"invalid_key": "hello"})
    assert response.status_code == 422


def test_chat_endpoint_extremely_long_message():
    """Teszteli, hogyan kezeli a rendszer az extrém hosszú bemeneteket."""
    # Generálunk egy óriási, 10 000 karakteres spammelő szöveget
    huge_message = "spam " * 2000
    response = client.post("/chat", json={"message": huge_message})

    # Elvárjuk, hogy a backend ne omoljon össze (vagy 200-at ad vissza, vagy ha limitálva van, akkor hibaüzenetet)
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        assert "response" in response.json()


def test_chat_endpoint_empty_and_special_chars():
    """Teszteli az üres bemenetet és a speciális karaktereket."""
    # 1. Teszt: Teljesen üres üzenet
    response_empty = client.post("/chat", json={"message": ""})
    assert response_empty.status_code in [200, 422] # A Pydantic beállításaidtól függően vagy átmegy, vagy elutasítja

    # 2. Teszt: Speciális karakterek, kód részletek és emojik
    special_message = "SELECT * FROM users; <script>alert(1)</script> 🚀🌟"
    response_special = client.post("/chat", json={"message": special_message})
    assert response_special.status_code == 200
    assert "response" in response_special.json()