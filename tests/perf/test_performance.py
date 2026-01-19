import pytest
import requests
import time


class TestAccountCreationDeletion:
    """Performance tests for account creation and deletion"""
    
    MAX_RESPONSE_TIME = 0.5  # seconds
    NUM_ITERATIONS = 100
    
    def test_create_and_delete_100_accounts(self, api_client):
        """
        Test creating and deleting 100 accounts sequentially.
        Each request should respond within 0.5 seconds.
        """
        base_url = api_client
        
        for i in range(self.NUM_ITERATIONS):
            pesel = f"{80000000000 + i}"  # Generate unique PESEL
            
            # Test account creation
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/accounts",
                json={
                    "name": f"TestUser{i}",
                    "surname": f"TestSurname{i}",
                    "pesel": pesel
                },
                timeout=1.0
            )
            response_time = time.time() - start_time
            
            # Assert response code
            assert response.status_code == 201, f"Iteration {i}: Expected 201, got {response.status_code}"
            
            # Assert response time
            assert response_time < self.MAX_RESPONSE_TIME, \
                f"Iteration {i}: Account creation took {response_time:.3f}s, max allowed is {self.MAX_RESPONSE_TIME}s"
            
            # Test account deletion
            start_time = time.time()
            response = requests.delete(
                f"{base_url}/api/accounts/{pesel}",
                timeout=1.0
            )
            response_time = time.time() - start_time
            
            # Assert response code
            assert response.status_code == 200, f"Iteration {i}: Expected 200 for delete, got {response.status_code}"
            
            # Assert response time
            assert response_time < self.MAX_RESPONSE_TIME, \
                f"Iteration {i}: Account deletion took {response_time:.3f}s, max allowed is {self.MAX_RESPONSE_TIME}s"


class TestIncomingTransfers:
    """Performance tests for incoming transfers"""
    
    MAX_RESPONSE_TIME = 0.5  # seconds
    NUM_TRANSFERS = 100
    TRANSFER_AMOUNT = 10.0
    
    def test_create_account_and_100_incoming_transfers(self, api_client):
        """
        Test creating an account and executing 100 incoming transfers.
        Each request should respond within 0.5 seconds.
        Final balance should be 50 (initial) + 100 * 10 = 1050.
        """
        base_url = api_client
        pesel = "85010112345"
        
        # Create account
        response = requests.post(
            f"{base_url}/api/accounts",
            json={
                "name": "John",
                "surname": "Doe",
                "pesel": pesel
            },
            timeout=1.0
        )
        assert response.status_code == 201
        
        # Get initial balance
        response = requests.get(
            f"{base_url}/api/accounts/{pesel}",
            timeout=1.0
        )
        assert response.status_code == 200
        initial_balance = response.json()["balance"]
        assert initial_balance == 50.0, "Initial balance should be 50"
        
        # Execute 100 incoming transfers
        for i in range(self.NUM_TRANSFERS):
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/transfers/incoming",
                json={
                    "pesel": pesel,
                    "amount": self.TRANSFER_AMOUNT
                },
                timeout=1.0
            )
            response_time = time.time() - start_time
            
            # Assert response code
            assert response.status_code == 200, \
                f"Transfer {i}: Expected 200, got {response.status_code}"
            
            # Assert response time
            assert response_time < self.MAX_RESPONSE_TIME, \
                f"Transfer {i}: Request took {response_time:.3f}s, max allowed is {self.MAX_RESPONSE_TIME}s"
        
        # Verify final balance
        response = requests.get(
            f"{base_url}/api/accounts/{pesel}",
            timeout=1.0
        )
        assert response.status_code == 200
        final_balance = response.json()["balance"]
        expected_balance = initial_balance + (self.NUM_TRANSFERS * self.TRANSFER_AMOUNT)
        assert final_balance == expected_balance, \
            f"Final balance should be {expected_balance}, got {final_balance}"
        
        # Cleanup
        requests.delete(f"{base_url}/api/accounts/{pesel}", timeout=1.0)


class TestBulkAccountCreation:
    """Performance test for bulk account creation and deletion"""
    
    MAX_RESPONSE_TIME = 0.5  # seconds
    NUM_ACCOUNTS = 1000
    
    def test_create_1000_accounts_then_delete(self, api_client):
        """
        Test creating 1000 accounts first, then deleting them all.
        This tests how the system handles bulk operations and if memory/data structures
        impact performance over time. Key difference from create-delete pairs:
        - Sequential pairs: test if individual operations remain fast
        - Bulk then delete: tests if performance degrades as registry grows
        Each request should respond within 0.5 seconds.
        """
        base_url = api_client
        pesels = []
        
        # Phase 1: Create all accounts
        for i in range(self.NUM_ACCOUNTS):
            pesel = f"{70000000000 + i}"
            pesels.append(pesel)
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/accounts",
                json={
                    "name": f"BulkUser{i}",
                    "surname": f"BulkSurname{i}",
                    "pesel": pesel
                },
                timeout=1.0
            )
            response_time = time.time() - start_time
            
            # Assert response code
            assert response.status_code == 201, \
                f"Creation {i}: Expected 201, got {response.status_code}"
            
            # Assert response time
            assert response_time < self.MAX_RESPONSE_TIME, \
                f"Creation {i}: Request took {response_time:.3f}s, max allowed is {self.MAX_RESPONSE_TIME}s"
        
        # Phase 2: Delete all accounts
        for i, pesel in enumerate(pesels):
            start_time = time.time()
            response = requests.delete(
                f"{base_url}/api/accounts/{pesel}",
                timeout=1.0
            )
            response_time = time.time() - start_time
            
            # Assert response code
            assert response.status_code == 200, \
                f"Deletion {i}: Expected 200, got {response.status_code}"
            
            # Assert response time
            assert response_time < self.MAX_RESPONSE_TIME, \
                f"Deletion {i}: Request took {response_time:.3f}s, max allowed is {self.MAX_RESPONSE_TIME}s"
