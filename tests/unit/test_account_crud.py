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


class TestCreateAccount:
    """Test POST /api/accounts"""
    
    def test_create_personal_account_success(self, client):
        """Test successful account creation"""
        account_data = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
        response = client.post("/api/accounts", json=account_data)
        
        assert response.status_code == 201
        assert response.get_json()["message"] == "Account created"
    
    def test_create_account_missing_fields(self, client):
        """Test account creation with missing fields"""
        account_data = {
            "name": "james",
            "surname": "hetfield"
        }
        response = client.post("/api/accounts", json=account_data)
        
        assert response.status_code == 400
    
    def test_create_account_invalid_pesel(self, client):
        """Test account creation with invalid PESEL"""
        account_data = {
            "name": "john",
            "surname": "doe",
            "pesel": "12345"  # Invalid PESEL
        }
        response = client.post("/api/accounts", json=account_data)
        
        # API tworzy konto nawet z invalid PESEL, ale PESEL jest ustawiony na "Invalid"
        assert response.status_code == 201
    
    def test_create_account_duplicate_pesel(self, client):
        """Test account creation with duplicate PESEL returns 409"""
        pesel = "89092909825"
        
        # Create first account
        response1 = client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        assert response1.status_code == 201
        
        # Try to create second account with same PESEL
        response2 = client.post("/api/accounts", json={
            "name": "lars",
            "surname": "ulrich",
            "pesel": pesel
        })
        
        assert response2.status_code == 409
        assert "PESEL already exists" in response2.get_json()["error"]


class TestGetAllAccounts:
    """Test GET /api/accounts"""
    
    def test_get_all_accounts_empty(self, client):
        """Test getting accounts when registry is empty"""
        response = client.get("/api/accounts")
        
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_get_all_accounts_with_data(self, client):
        """Test getting all accounts"""
        # Create two accounts
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        })
        client.post("/api/accounts", json={
            "name": "lars",
            "surname": "ulrich",
            "pesel": "85010112345"
        })
        
        response = client.get("/api/accounts")
        
        assert response.status_code == 200
        accounts = response.get_json()
        assert len(accounts) == 2
        assert accounts[0]["name"] == "james"
        assert accounts[1]["name"] == "lars"


class TestGetAccountCount:
    """Test GET /api/accounts/count"""
    
    def test_get_account_count_empty(self, client):
        """Test account count when registry is empty"""
        response = client.get("/api/accounts/count")
        
        assert response.status_code == 200
        assert response.get_json()["count"] == 0
    
    def test_get_account_count_with_accounts(self, client):
        """Test account count with multiple accounts"""
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        })
        client.post("/api/accounts", json={
            "name": "lars",
            "surname": "ulrich",
            "pesel": "85010112345"
        })
        client.post("/api/accounts", json={
            "name": "kirk",
            "surname": "hammett",
            "pesel": "82111412345"
        })
        
        response = client.get("/api/accounts/count")
        
        assert response.status_code == 200
        assert response.get_json()["count"] == 3


class TestGetAccountByPesel:
    """Test GET /api/accounts/<pesel>"""
    
    def test_get_account_by_pesel_success(self, client):
        """Test getting account by PESEL"""
        pesel = "89092909825"
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        
        response = client.get(f"/api/accounts/{pesel}")
        
        assert response.status_code == 200
        account = response.get_json()
        assert account["name"] == "james"
        assert account["surname"] == "hetfield"
        assert account["pesel"] == pesel
        assert account["balance"] == 0.0
    
    def test_get_account_by_pesel_not_found(self, client):
        """Test getting account that doesn't exist"""
        response = client.get("/api/accounts/99999999999")
        
        assert response.status_code == 404
        assert "error" in response.get_json()


class TestUpdateAccount:
    """Test PATCH /api/accounts/<pesel>"""
    
    def test_update_account_name(self, client):
        """Test updating account name"""
        pesel = "89092909825"
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        
        response = client.patch(f"/api/accounts/{pesel}", json={
            "name": "james_updated"
        })
        
        assert response.status_code == 200
        
        # Verify update
        get_response = client.get(f"/api/accounts/{pesel}")
        account = get_response.get_json()
        assert account["name"] == "james_updated"
        assert account["surname"] == "hetfield"  # Surname unchanged
    
    def test_update_account_surname(self, client):
        """Test updating account surname"""
        pesel = "89092909825"
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        
        response = client.patch(f"/api/accounts/{pesel}", json={
            "surname": "hetfield_updated"
        })
        
        assert response.status_code == 200
        
        # Verify update
        get_response = client.get(f"/api/accounts/{pesel}")
        account = get_response.get_json()
        assert account["name"] == "james"  # Name unchanged
        assert account["surname"] == "hetfield_updated"
    
    def test_update_account_both_fields(self, client):
        """Test updating both name and surname"""
        pesel = "89092909825"
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        
        response = client.patch(f"/api/accounts/{pesel}", json={
            "name": "james_new",
            "surname": "hetfield_new"
        })
        
        assert response.status_code == 200
        
        # Verify update
        get_response = client.get(f"/api/accounts/{pesel}")
        account = get_response.get_json()
        assert account["name"] == "james_new"
        assert account["surname"] == "hetfield_new"
    
    def test_update_account_not_found(self, client):
        """Test updating account that doesn't exist"""
        response = client.patch("/api/accounts/99999999999", json={
            "name": "john"
        })
        
        assert response.status_code == 404


class TestDeleteAccount:
    """Test DELETE /api/accounts/<pesel>"""
    
    def test_delete_account_success(self, client):
        """Test successful account deletion"""
        pesel = "89092909825"
        client.post("/api/accounts", json={
            "name": "james",
            "surname": "hetfield",
            "pesel": pesel
        })
        
        response = client.delete(f"/api/accounts/{pesel}")
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f"/api/accounts/{pesel}")
        assert get_response.status_code == 404
    
    def test_delete_account_not_found(self, client):
        """Test deleting account that doesn't exist"""
        response = client.delete("/api/accounts/99999999999")
        
        assert response.status_code == 404
