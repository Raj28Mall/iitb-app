import sys
import types
from unittest.mock import Mock
import pytest

fake_fb = types.ModuleType("firebase_admin")
fake_credentials = types.ModuleType("firebase_admin.credentials")
fake_firestore = types.ModuleType("firebase_admin.firestore")

mock_db = Mock(name="firestore_db")
setattr(fake_credentials, "Certificate", Mock(name="Certificate"))
setattr(fake_firestore, "client", Mock(name="firestore.client", return_value=mock_db))

setattr(fake_fb, "credentials", fake_credentials)
setattr(fake_fb, "firestore", fake_firestore)
fake_fb.__dict__["initialize_app"] = Mock(name="initialize_app")
fake_fb.__dict__['_apps'] = [] 
sys.modules["firebase_admin"] = fake_fb
sys.modules["firebase_admin.credentials"] = fake_credentials
sys.modules["firebase_admin.firestore"] = fake_firestore

@pytest.fixture(scope="module")
def client():
    from main import app
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c