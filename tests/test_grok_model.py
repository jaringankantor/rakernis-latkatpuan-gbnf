import sys
from types import SimpleNamespace

import pytest

from src.model import GrokAPIModel, load_xai_api_key


class FakeCompletions:
    def __init__(self, content: str = '{"nama":"Dinda"}') -> None:
        self.content = content
        self.request = None

    def create(self, **request):
        self.request = request
        message = SimpleNamespace(content=self.content)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeOpenAI:
    instance = None

    def __init__(self, **options) -> None:
        self.options = options
        self.chat = SimpleNamespace(completions=FakeCompletions())
        FakeOpenAI.instance = self


@pytest.fixture
def fake_openai(monkeypatch):
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))
    return FakeOpenAI


def test_grok_uses_xai_endpoint_and_json_schema(fake_openai) -> None:
    model = GrokAPIModel("secret")
    result = model.generate("Buat profil", "user-profile")

    assert result == '{"nama":"Dinda"}'
    assert fake_openai.instance.options == {
        "api_key": "secret",
        "base_url": "https://api.x.ai/v1",
    }
    request = fake_openai.instance.chat.completions.request
    assert request["model"] == "grok-4.5"
    assert request["response_format"]["type"] == "json_schema"
    assert request["response_format"]["json_schema"]["strict"] is True


def test_grok_rejects_invalid_yes_no_output(fake_openai) -> None:
    model = GrokAPIModel("secret")
    fake_openai.instance.chat.completions.content = "mungkin"

    with pytest.raises(RuntimeError, match="di luar grammar"):
        model.generate("Apakah benar?", "yes-no")


def test_load_xai_api_key_from_dotenv(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text('XAI_API_KEY="secret-from-env"\n', encoding="utf-8")
    assert load_xai_api_key(env_path) == "secret-from-env"


def test_load_xai_api_key_rejects_empty_value(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text("XAI_API_KEY=\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="XAI_API_KEY belum diisi"):
        load_xai_api_key(env_path)
