import pytest


class DummyResp:
    def __init__(self, json_data):
        self._json = json_data
        self.text = str(json_data)

    def json(self):
        return self._json


@pytest.fixture(autouse=True)
def mock_mf_global(monkeypatch):
    """Global default: MF reports NIP as active ('Czynny')."""

    def fake_get(url, timeout=10):
        return DummyResp({'result': {'subject': {'statusVat': 'Czynny'}}})

    monkeypatch.setattr('requests.get', fake_get)
    yield
