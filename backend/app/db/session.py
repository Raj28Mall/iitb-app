import os
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1 import AsyncClient
from app.core.config import config

service_account_key_path= config.SERVICE_ACCOUNT_KEY_PATH

if isinstance(service_account_key_path, str) and not os.path.exists(service_account_key_path):
    raise FileNotFoundError(
        f"Service account key file not found at: {service_account_key_path}\n"
        "Please download it from Firebase Console > Project settings > Service accounts > Generate new private key."
    )

try:
    cred = credentials.Certificate(service_account_key_path)
    initialize_app(cred)
    # print("Firebase Admin SDK initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Handle more gracefully in production
    exit(1)

db = firestore.client()
