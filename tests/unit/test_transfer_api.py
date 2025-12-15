import pytest
import sys
import os

# Dodaj src do path żeby móc importować moduły
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.api import app, registry


@pytest.fixture
def client():
    """Create Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before and after each test"""
    registry.accounts = []
    yield
    registry.accounts = []


@pytest.fixture
def account_with_balance(client):
    """Create account with some initial balance"""
    client.post("/api/accounts", json={
        "name": "james",
        "surname": "hetfield",
        "pesel": "89092909825"
    })
    # Manually add balance for testing
    account = registry.find_by_pesel("89092909825")
    account.balance = 1000.0
    return "89092909825"


class TestTransferIncoming:
    """Test incoming transfers"""
    
    def test_incoming_transfer_success(self, client, account_with_balance):
        """Test successful incoming transfer"""
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        # Verify balance increased
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance + 500
    
    def test_incoming_transfer_to_nonexistent_account(self, client):
        """Test incoming transfer to account that doesn't exist"""
        response = client.post("/api/accounts/99999999999/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        
        assert response.status_code == 404
        assert "Account not found" in response.get_json()["error"]
    
    def test_incoming_transfer_multiple(self, client, account_with_balance):
        """Test multiple incoming transfers"""
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
    """Test outgoing transfers"""
    
    def test_outgoing_transfer_success(self, client, account_with_balance):
        """Test successful outgoing transfer"""
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 300,
            "type": "outgoing"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        # Verify balance decreased
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance - 300
    
    def test_outgoing_transfer_insufficient_funds(self, client, account_with_balance):
        """Test outgoing transfer with insufficient funds returns 422"""
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 5000,  # More than balance
            "type": "outgoing"
        })
        
        assert response.status_code == 422
        assert "Insufficient funds" in response.get_json()["error"]
        
        # Verify balance didn't change
        get_response = client.get(f"/api/accounts/{pesel}")
        balance = get_response.get_json()["balance"]
        assert balance == 1000.0  # Unchanged
    
    def test_outgoing_transfer_to_nonexistent_account(self, client):
        """Test outgoing transfer to account that doesn't exist"""
        response = client.post("/api/accounts/99999999999/transfer", json={
            "amount": 100,
            "type": "outgoing"
        })
        
        assert response.status_code == 404


class TestTransferExpress:
    """Test express transfers"""
    
    def test_express_transfer_success(self, client, account_with_balance):
        """Test successful express transfer"""
        pesel = account_with_balance
        initial_response = client.get(f"/api/accounts/{pesel}")
        initial_balance = initial_response.get_json()["balance"]
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 200,
            "type": "express"
        })
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        # Verify balance decreased by amount + fee (1.0)
        updated_response = client.get(f"/api/accounts/{pesel}")
        new_balance = updated_response.get_json()["balance"]
        assert new_balance == initial_balance - 200 - 1.0  # amount + fee
    
    def test_express_transfer_insufficient_funds(self, client, account_with_balance):
        """Test express transfer with insufficient funds returns 422"""
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 5000,  # More than balance
            "type": "express"
        })
        
        assert response.status_code == 422
        assert "Insufficient funds" in response.get_json()["error"]


class TestTransferValidation:
    """Test transfer validation"""
    
    def test_transfer_missing_fields(self, client, account_with_balance):
        """Test transfer with missing required fields"""
        pesel = account_with_balance
        
        # Missing type
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
        """Test transfer with unknown type returns 400"""
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={
            "amount": 100,
            "type": "unknown_type"
        })
        
        assert response.status_code == 400
        assert "Unknown transfer type" in response.get_json()["error"]
    
    def test_transfer_empty_body(self, client, account_with_balance):
        """Test transfer with empty body"""
        pesel = account_with_balance
        
        response = client.post(f"/api/accounts/{pesel}/transfer", json={})
        
        assert response.status_code == 400
