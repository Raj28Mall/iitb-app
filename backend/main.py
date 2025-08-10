from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.cloud.firestore_v1.client import Client
from google.api_core.exceptions import GoogleAPICallError
from app.api.deps import get_db
from app.api.v1.endpoints.courses import router as courses_router

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

# @app.get("/health", tags=["System"])
# def health_check(db: Client = Depends(get_db)):
    """
    Performs a health check of the API and its connection to the database.
    Returns a 200 OK status if healthy, otherwise a 503 Service Unavailable.
    """
    try:
        # Perform a simple, low-cost read operation on the database.
        # We try to get a document that doesn't exist to confirm connectivity
        # without retrieving any data.
        db.collection("health_check").document("ping").get(timeout=5)
        
        return {"status": "ok", "database": "healthy"}
    
    except GoogleAPICallError as e:
        # This catches issues like permissions, network problems, etc.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "database": "unhealthy", "reason": str(e)},
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "database": "unhealthy", "reason": str(e)},
        )
    
app.include_router(courses_router, prefix="/api/v1", tags=["Courses"])
