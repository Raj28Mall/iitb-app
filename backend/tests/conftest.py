# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import os
from main import app

# Mock Firebase for testing
@pytest.fixture(scope="session", autouse=True)
def mock_firebase():
    if os.getenv("GITHUB_ACTIONS") or os.getenv("CI"):
        # Mock Firebase components during CI
        with patch("app.db.session.firestore") as mock_firestore, \
             patch("app.db.session.initialize_app") as mock_init, \
             patch("app.db.session.credentials"):
            
            mock_db = Mock()
            mock_firestore.client.return_value = mock_db
            
            # Mock collection methods for your tests
            mock_collection = Mock()
            mock_db.collection.return_value = mock_collection
            
            yield mock_db
    else:
        yield None

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c