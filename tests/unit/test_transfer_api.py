import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.api import app, registry


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_registry():
    registry.accounts = []
    yield
    registry.accounts = []


@pytest.fixture
def account_with_balance(client):
    client.post("/api/accounts", json={
        "name": "james",
        "surname": "hetfield",
        "pesel": "89092909825"
    })
    account = registry.find_by_pesel("89092909825")
    account.balance = 1000.0
    return "89092909825"


class TestTransferIncoming:
    
    def test_incoming_transfer_success(self, client, account_with_balance):
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance + 500
    
    def test_incoming_transfer_to_nonexistent_account(self, client):
        response = client.post("/api/accounts/99999999999/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        
        assert response.status_code == 404
        assert "Account not found" in response.get_json()["error"]
    
    def test_incoming_transfer_multiple(self, client, account_with_balance):
        pesel = account_with_balance
        
        for i in range(3):
            response = client.post(f"/api/accounts/{pesel}/transfer", json={
                "amount": 100,
                "type": "incoming"
            })
            assert response.status_code == 200
        
        # Verify final balance
        final_response = client.get(f"/api/accounts/{pesel}")
        final_balance = final_response.get_json()["balance"]
        assert final_balance == 1000 + 300  # 3 * 100


class TestTransferOutgoing:
    
    def test_outgoing_transfer_success(self, client, account_with_balance):
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 300,
            "type": "outgoing"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance - 300
    
    def test_outgoing_transfer_insufficient_funds(self, client, account_with_balance):
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 5000,  # More than balance
            "type": "outgoing"
        })
        
        assert response.status_code == 422
        assert "Insufficient funds" in response.get_json()["error"]
        
        get_response = client.get(f"/api/accounts/{pesel}")
        balance = get_response.get_json()["balance"]
        assert balance == 1000.0  # Unchanged
    
    def test_outgoing_transfer_to_nonexistent_account(self, client):
        response = client.post("/api/accounts/99999999999/transfer", json={
            "amount": 100,
            "type": "outgoing"
        })
        
        assert response.status_code == 404


class TestTransferExpress:
    
    def test_express_transfer_success(self, client, account_with_balance):
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 200,
            "type": "express"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance - 200 - 1.0  # amount + fee
    
    def test_express_transfer_insufficient_funds(self, client, account_with_balance):
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 5000,  # More than balance
            "type": "express"
        })
        
        assert response.status_code == 422
        assert "Insufficient funds" in response.get_json()["error"]


class TestTransferValidation:
    
    def test_transfer_missing_fields(self, client, account_with_balance):
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 100
        })
        assert response.status_code == 400
        
        # Missing amount
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "type": "incoming"
        })
        assert response.status_code == 400
    
    def test_transfer_unknown_type(self, client, account_with_balance):
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 100,
            "type": "unknown_type"
        })
        
        assert response.status_code == 400
        assert "Unknown transfer type" in response.get_json()["error"]
    
    def test_transfer_empty_body(self, client, account_with_balance):
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={})
        
        assert response.status_code == 400
