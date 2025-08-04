from app.db.session import db 
from google.cloud.firestore_v1.client import Client

def get_db() -> Client:
    """
    Dependency function that yields the Firestore client.
    """
    try:
        yield db
    finally:
        # In a traditional SQL DB, you might close the session here.
        # For Firestore's client, it's managed globally, so there's
        # often no explicit close needed per request. The try/finally
        # block is good practice for future-proofing.
        pass