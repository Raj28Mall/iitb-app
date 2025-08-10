from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from pydantic import ValidationError
# from google.cloud.firestore_v1.client import Client
from app.db.session import db
from app.api.v1.schemas import Department, Course

router = APIRouter()

@router.get("/departments", response_model=List[Department])
async def get_departments() -> List[Department]:
    """
    Retrieves all available supported departments as a list of Department objects
    """
    collection_name = "departments"
    try:
        docs = db.collection(collection_name).stream()
        results = []
        for doc in docs:
            doc_data = doc.to_dict()
            try:
                department = Department(
                    id=doc.id,
                    name=doc_data.get('name', doc.id),  # Fallback to doc.id if name not present
                    code=doc_data.get('code'),
                    description=doc_data.get('description')
                )
                results.append(department)
            except ValidationError as ve:
                print(f"Validation error for document {doc.id}: {ve}")
                continue
                
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve departments: {e}")


@router.get("/courses/", response_model=List[Course])
async def get_courses() -> List[Course]:
    """
    Retrieves all running courses for the current sem
    """
    collection_name = "courses"
    try:
        docs = db.collection(collection_name).stream()
        results: list[Course] = []
        for doc in docs:
            data: Dict[str, Any] = (doc.to_dict() or {})
            try:
                course = Course(id=doc.id, **data) if 'id' in Course.model_fields else Course(**data)
                results.append(course)
            except ValidationError as ve:
                print(f"Validation error for document {doc.id}: {ve}")
                continue
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve courses for department: {e}")

@router.get("/courses/{department_code}", response_model=List[Course])
async def get_courses_for_department(department_code: str) -> List[Course]:
    """Returns the core courses running for the given department"""
    return []