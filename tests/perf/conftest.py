import pytest
import requests
import time

# Wait for Flask to be ready
@pytest.fixture(scope="session", autouse=True)
def wait_for_flask():
    """Wait for Flask server to be ready"""
    base_url = "http://localhost:5000"
    max_retries = 30
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{base_url}/api/accounts/count", timeout=1)
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    raise RuntimeError(f"Flask server not ready after {max_retries * retry_delay} seconds")

@pytest.fixture
def api_client():
    """Provide base URL for API client"""
    return "http://localhost:5000"
