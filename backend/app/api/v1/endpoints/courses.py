from fastapi import APIRouter, HTTPException
from google.cloud.firestore_v1.client import Client
from app.db.session import db

router = APIRouter()

@router.get("/get_documents/{collection_name}")
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