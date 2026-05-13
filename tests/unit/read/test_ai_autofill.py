"""
AI autofill client tests.
"""

from lute.read.ai_autofill import TermAutofillClient


class FakeConfig:  # pylint: disable=too-few-public-methods
    "Minimal autofill config for tests."

    ai_autofill_enabled = True
    ai_autofill_base_url = "https://openrouter.test/api/v1"
    ai_autofill_api_key = "test-key"
    ai_autofill_model = "openrouter/free"
    ai_autofill_target_lang = "es"
    ai_autofill_fill_parents = True


class FakeResponse:  # pylint: disable=too-few-public-methods
    "Minimal requests response for tests."

    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        "No-op success."

    def json(self):
        "Return OpenAI-compatible response."
        return {"choices": [{"message": {"content": self.content}}]}


def test_autofill_client_parses_strict_json(monkeypatch):
    "Client parses valid OpenRouter JSON content."

    def fake_post(*args, **kwargs):  # pylint: disable=unused-argument
        return FakeResponse(
            '{"translation":"deletreo","parents":["spell"],"confidence":"high"}'
        )

    monkeypatch.setattr("lute.read.ai_autofill.requests.post", fake_post)

    result = TermAutofillClient(FakeConfig()).suggest(
        "English", "spelling", "A spelling mistake."
    )

    assert result == {
        "translation": "deletreo",
        "parents": ["spell"],
        "confidence": "high",
        "provider_error": None,
    }


def test_autofill_client_returns_provider_error_for_invalid_json(monkeypatch):
    "Invalid model output becomes a non-fatal provider error."

    def fake_post(*args, **kwargs):  # pylint: disable=unused-argument
        return FakeResponse("not json")

    monkeypatch.setattr("lute.read.ai_autofill.requests.post", fake_post)

    result = TermAutofillClient(FakeConfig()).suggest("English", "spelling")

    assert result["translation"] == ""
    assert result["parents"] == []
    assert result["provider_error"] is not None


def test_autofill_client_does_not_call_provider_without_api_key(monkeypatch):
    "Missing API key returns an error before making a request."
    config = FakeConfig()
    config.ai_autofill_api_key = ""
    called = False

    def fake_post(*args, **kwargs):  # pylint: disable=unused-argument
        nonlocal called
        called = True
        return FakeResponse("{}")

    monkeypatch.setattr("lute.read.ai_autofill.requests.post", fake_post)

    result = TermAutofillClient(config).suggest("English", "spelling")

    assert called is False
    assert result["provider_error"] == "AI autofill API key missing"
