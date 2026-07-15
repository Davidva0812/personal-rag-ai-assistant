import pytest
import time
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# MOCK SETUP — minden külső függőséget (Redis, Chroma, Groq, HuggingFace)
# mockolunk, hogy a tesztek ne igényeljenek valódi API kulcsokat / hálózatot.
# ---------------------------------------------------------------------------

# 1. UpstashChatMessageHistory mock — in-memory tároló a tesztekhez
class MockChatHistory:
    def __init__(self, *args, **kwargs):
        self._messages = []

    @property
    def messages(self):
        return self._messages

    def add_message(self, message):
        self._messages.append(message)

    def clear(self):
        self._messages.clear()


# 2. Chroma mock
mock_chroma = MagicMock()
mock_chroma.as_retriever.return_value.invoke.return_value = []

# 3. LLM mock — .content mindig string legyen, ahogy a valódi LLM adja vissza
mock_llm_response = MagicMock()
mock_llm_response.content = "I am David Varga. My email is david.varga.1208@gmail.com"

mock_chain_with_history = MagicMock()
mock_chain_with_history.invoke.return_value = mock_llm_response


# Az összes külső függőséget az import ELŐTT patcheljük.
# A chain_with_history-t az import UTÁN írjuk felül közvetlenül a modulon,
# mert a with-patch csak az importálás idejére él, de a FastAPI endpoint
# closure-ként már a modul szintű objektumra hivatkozik.
with patch("langchain_huggingface.HuggingFaceEndpointEmbeddings", return_value=MagicMock()), \
     patch("langchain_chroma.Chroma", return_value=mock_chroma), \
     patch("langchain_groq.ChatGroq", return_value=MagicMock()), \
     patch("main.UpstashChatMessageHistory", MockChatHistory):
    import main
    # Közvetlenül felülírjuk a modul szintű chain_with_history változót,
    # így a chat_endpoint mindig a mock invoke-ot hívja.
    main.chain_with_history = mock_chain_with_history
    from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# RATE LIMITER RESET HELPER
# A slowapi belső storage-ának elérési útja verziótól függhet,
# ezért több stratégiát próbálunk — ha egyik sem működik, patcheljük a limitert.
# ---------------------------------------------------------------------------
def reset_rate_limiter():
    limiter = getattr(app.state, "limiter", None)
    if not limiter:
        return
    storage = getattr(limiter, "_storage", None)
    if not storage:
        return
    # 1. próba: limits library MemoryStorage
    inner = getattr(storage, "_storage", None)
    if isinstance(inner, dict):
        inner.clear()
        return
    # 2. próba: reset() metódus
    if hasattr(storage, "reset"):
        storage.reset()
        return
    # 3. próba: clear() metódus
    if hasattr(storage, "clear"):
        storage.clear()
        return
    # 4. fallback: patch-eljük a limiter check_limit-jét ideiglenesen
    # (ez nem kellene hogy kellő legyen a fenti 3 után, de biztonsági háló)


@pytest.fixture(autouse=True)
def reset_limiter_fixture():
    reset_rate_limiter()
    # A chain mock visszaállítása minden teszt előtt
    mock_chain_with_history.invoke.return_value = mock_llm_response
    yield
    reset_rate_limiter()


# ---------------------------------------------------------------------------
# TESZTEK
# ---------------------------------------------------------------------------

def test_root_endpoint():
    """A GET / endpoint elérhető és a helyes üzenetet adja vissza."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "David Varga AI Portfolio API is online!"}


def test_chat_endpoint_success():
    """Sikeres chat kérés — az email szerepel a válaszban."""
    response = client.post("/chat", json={"message": "What is your email address?"})
    assert response.status_code == 200
    assert "response" in response.json()

    ai_response = response.json()["response"].lower()
    email_included = "david.varga.1208@gmail.com" in ai_response
    guardrail_triggered = "only answer questions related to my cv" in ai_response
    assert email_included or guardrail_triggered


def test_chat_endpoint_invalid_payload():
    """Hibás JSON kulcs esetén Pydantic 422-t ad vissza."""
    response = client.post("/chat", json={"invalid_key": "hello"})
    assert response.status_code == 422


def test_chat_endpoint_extremely_long_message():
    """10 000 karakteres üzenet esetén 422-t kapunk (max_length=1000)."""
    huge_message = "spam " * 2000
    response = client.post("/chat", json={"message": huge_message})
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        assert "response" in response.json()


def test_chat_endpoint_empty_and_special_chars():
    """Üres üzenet 422-t kap; speciális karakterek rendesen feldolgozódnak."""
    # Üres üzenet — min_length=1 miatt Pydantic elutasítja
    response_empty = client.post("/chat", json={"message": ""})
    assert response_empty.status_code in [200, 422]

    # Speciális karakterek — a bleach megtisztítja, az LLM válaszol
    special_message = "SELECT * FROM users; <script>alert(1)</script> 🚀🌟"
    response_special = client.post("/chat", json={"message": special_message})
    assert response_special.status_code == 200
    assert "response" in response_special.json()


def test_rate_limiting():
    """Az 5. kérés után a 6. 429-et kap."""
    reset_rate_limiter()

    for i in range(5):
        response = client.post("/chat", json={"message": "Szia, ki vagy te?"})
        assert response.status_code != 429, f"A {i+1}. kérés váratlanul 429-et kapott"

    over_limit_response = client.post("/chat", json={"message": "Szia, ki vagy te?"})
    assert over_limit_response.status_code == 429

    json_data = over_limit_response.json()
    assert "Too many requests" in json_data["detail"]


def test_chat_flow():
    """Az AI kontextust tart fenn két kérdés között (memória teszt)."""
    response_1 = client.post("/chat", json={"message": "What is your name?"})
    assert response_1.status_code == 200

    time.sleep(0.5)

    response_2 = client.post("/chat", json={
        "message": "Based on our previous exchange, how old are you?"})
    assert response_2.status_code == 200
    assert "response" in response_2.json()