from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import db
app = FastAPI() 

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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