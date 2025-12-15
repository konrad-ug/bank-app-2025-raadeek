import pytest
from src.company_account import Company_Account


class DummyResp:
    def __init__(self, json_data):
        self._json = json_data
        self.text = str(json_data)

    def json(self):
        return self._json


@pytest.fixture(autouse=True)
def mock_mf_active(monkeypatch):
    """Default: mock MF API to report NIP as active ('Czynny')."""

    def fake_get(url, timeout=10):
        return DummyResp({'result': {'subject': {'statusVat': 'Czynny'}}})

    monkeypatch.setattr('requests.get', fake_get)
    yield


class Test_Company_Account:

    def test_company_nip_invalid(self):
        account = Company_Account("Nokia", "1234567")
        assert account.nip == "Invalid"

    def test_company_account_valid_nip(self):
        account = Company_Account("Nokia", "1234567890")
        assert account.company_name == "Nokia"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_company_account(self):
        account = Company_Account("Nokia", "1234567890")
        assert account.company_name == "Nokia"
        assert account.nip == "1234567890"

    def test_company_incoming_transfer(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0

    def test_company_outgoing_transfer(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(100.0)

        result = account.outgoing_transfer(60.0)

        assert result is True
        assert account.balance == 40.0

    def test_company_outgoing_transfer_insufficient_balance(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(50.0)

        result = account.outgoing_transfer(100.0)

        assert result is False
        assert account.balance == 50.0


def test_company_nip_not_registered(monkeypatch):
    """When MF reports non-active status, constructor should raise ValueError."""

    def fake_get_inactive(url, timeout=10):
        return DummyResp({'result': {'subject': {'statusVat': 'Zawieszony'}}})

    monkeypatch.setattr('requests.get', fake_get_inactive)

    with pytest.raises(ValueError):
        Company_Account("Nokia", "1234567890")