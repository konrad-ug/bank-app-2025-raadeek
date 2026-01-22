import pytest
from unittest.mock import Mock, MagicMock, patch
from src.mongo_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount


class TestMongoAccountsRepository:
    
    @pytest.fixture
    def sample_accounts(self):
        account1 = PersonalAccount("John", "Doe", "67010112345", "PROM_1234")
        account1.incoming_transfer(100)
        account1.outgoing_transfer(50)
        
        account2 = PersonalAccount("Jane", "Smith", "80010112345")
        account2.incoming_transfer(500)
        
        return [account1, account2]
    
    @patch('src.mongo_repository.MongoClient')
    def test_save_all_clears_and_saves(self, mock_client_class, sample_accounts):
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_client = MagicMock()
        
        mock_client_class.return_value = mock_client
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        
        repository = MongoAccountsRepository()
        
        # Act
        repository.save_all(sample_accounts)
        
    
        mock_collection.delete_many.assert_called_once_with({})
        
        
        assert mock_collection.update_one.call_count == 2
    
    @patch('src.mongo_repository.MongoClient')
    def test_load_all_returns_accounts(self, mock_client_class):
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_client = MagicMock()
        
        mock_client_class.return_value = mock_client
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        
        account_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "pesel": "67010112345",
                "balance": 150.0,
                "history": [100.0, -50.0]
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "pesel": "80010112345",
                "balance": 500.0,
                "history": [500.0]
            }
        ]
        
        mock_collection.find.return_value = account_data
        
        repository = MongoAccountsRepository()
        
        accounts = repository.load_all()
        
        assert len(accounts) == 2
        assert accounts[0].first_name == "John"
        assert accounts[0].last_name == "Doe"
        assert accounts[0].pesel == "67010112345"
        assert accounts[0].balance == 150.0
        assert accounts[0].history == [100.0, -50.0]
        
        assert accounts[1].first_name == "Jane"
        assert accounts[1].balance == 500.0
    
    @patch('src.mongo_repository.MongoClient')
    def test_save_and_load_roundtrip(self, mock_client_class):
        # Arrange
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_client = MagicMock()
        
        mock_client_class.return_value = mock_client
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        
        original_accounts = [
            PersonalAccount("Test", "User", "70010112345", "PROM_TEST")
        ]
        original_accounts[0].incoming_transfer(1000)
        
        saved_data = [original_accounts[0].to_dict()]
        mock_collection.find.return_value = saved_data
        
        repository = MongoAccountsRepository()
        
        repository.save_all(original_accounts)
        
        # Act - Load
        loaded_accounts = repository.load_all()
        
        # Assert
        assert len(loaded_accounts) == 1
        assert loaded_accounts[0].pesel == original_accounts[0].pesel
        assert loaded_accounts[0].balance == original_accounts[0].balance
