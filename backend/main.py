import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, firestore, initialize_app

app = FastAPI() 

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json" 

if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
    raise FileNotFoundError(
        f"Service account key file not found at: {SERVICE_ACCOUNT_KEY_PATH}\n"
        "Please download it from Firebase Console > Project settings > Service accounts > Generate new private key."
    )

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    initialize_app(cred)
    print("Firebase Admin SDK initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Handle more gracefully in production
    exit(1)

db = firestore.client()

@app.get("/")
def test():
    return {"message": "Hello World"}

@app.post("/add_document/{collection_name}")
async def add_document(collection_name: str, data: dict):
    """
    Adds a new document to the specified Firestore collection.
    Example: POST to /add_document/my_important_docs with JSON body:
             {"title": "My First Doc", "content": "This is important info."}
    """
    try:
        doc_ref = db.collection(collection_name).add(data)
        return {"message": "Document added successfully!", "document_id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {e}")

@app.get("/get_documents/{collection_name}")
async def get_documents(collection_name: str):
    """
    Retrieves all documents from the specified Firestore collection.
    Example: GET from /get_documents/my_important_docs
    """
    try:
        docs = db.collection(collection_name).stream()
        results = []
        for doc in docs:
            results.append({"id": doc.id, **doc.to_dict()})
        return {"collection": collection_name, "documents": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents: {e}")