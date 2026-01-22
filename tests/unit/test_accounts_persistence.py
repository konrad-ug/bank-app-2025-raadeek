import pytest
import sys
import os
from unittest.mock import Mock, patch

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
def mock_db_repository(monkeypatch):
    """Mock the database repository"""
    mock_repo = Mock()
    mock_repo.save_all.return_value = None
    mock_repo.load_all.return_value = []
    monkeypatch.setattr('src.api.db_repository', mock_repo)
    return mock_repo


class TestSaveAccountsEndpoint:
    
    def test_save_accounts_success(self, client, mock_db_repository):
        
        client.post("/api/accounts", json={
            "name": "john",
            "surname": "doe",
            "pesel": "85010112345"
        })
        client.post("/api/accounts", json={
            "name": "jane",
            "surname": "smith",
            "pesel": "90010112345"
        })
        
        # Save to database
        response = client.post("/api/accounts/save")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Accounts saved successfully"
        assert data["count"] == 2
    
    def test_save_empty_registry(self, client, mock_db_repository):
        
        response = client.post("/api/accounts/save")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 0


class TestLoadAccountsEndpoint:
    
    def test_load_accounts_success(self, client, mock_db_repository):
       
        client.post("/api/accounts", json={
            "name": "test",
            "surname": "user",
            "pesel": "88010112345"
        })
        
        save_response = client.post("/api/accounts/save")
        assert save_response.status_code == 200
        
       
        registry.accounts = []
        
        
        load_response = client.post("/api/accounts/load")
        
        assert load_response.status_code == 200
        data = load_response.get_json()
        assert data["message"] == "Accounts loaded successfully"
        assert data["count"] >= 0
    
    def test_load_clears_existing_accounts(self, client, mock_db_repository):
        # Create first account
        client.post("/api/accounts", json={
            "name": "first",
            "surname": "account",
            "pesel": "75010112345"
        })
        
        client.post("/api/accounts/save")
        
        client.post("/api/accounts", json={
            "name": "second",
            "surname": "account",
            "pesel": "76010112345"
        })
        
        response = client.post("/api/accounts/load")
        
        assert response.status_code == 200
        
        check_response = client.get("/api/accounts/76010112345")
        assert check_response.status_code == 404
