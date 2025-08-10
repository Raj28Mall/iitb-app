import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

# Make sure this import points to your main FastAPI application instance
from main import app 

@pytest.fixture(autouse=True)
def mock_firebase_admin():
    """
    Mocks the Firebase Admin SDK for all tests.
    """
    with patch('app.db.session.credentials.Certificate') as mock_cert, \
         patch('app.db.session.initialize_app') as mock_init, \
         patch('app.db.session.firestore.client') as mock_firestore_client:
        
        mock_db = Mock()
        mock_firestore_client.return_value = mock_db
        yield mock_db

# ADD THIS FIXTURE
@pytest.fixture(scope="module")
def client():
    """
    Provides a TestClient instance for the FastAPI app.
    It's created once per test module.
    """
    with TestClient(app) as c:
        yield c