from fastapi import APIRouter, HTTPException
from typing import List
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


@router.get("/courses/{department_id}", response_model=List[Course])
async def get_courses_by_department(department_id: str) -> List[Course]:
    """
    Retrieves courses for a specific department by its id.
    """
    collection_name = "courses"
    try:
        # Filter courses by department_id
        docs = db.collection(collection_name).where("department_id", "==", department_id).stream()
        results = []
        for doc in docs:
            doc_data = doc.to_dict()
            try:
                course = Course(
                    id=doc.id,
                    name=doc_data.get('name'),
                    code=doc_data.get('code'),
                    type=doc_data.get('type', ''), 
                    department_id=doc_data.get('department_id', ''),  
                    slot=doc_data.get('slot', []) 
                )
                results.append(course)
            except ValidationError as ve:
                print(f"Validation error for document {doc.id}: {ve}")
                continue
                
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve courses for department: {department_id} {e}")
    
# TODO: Figure out what to use, department id or department name
@router.post("/courses", response_model=Course)
async def create_course(course: Course) -> Course:
    """
    Creates a new course in the database.
    """
    collection_name = "courses"
    try:
        doc_ref = db.collection(collection_name)
        _, doc_ref = doc_ref.add(course.dict())
        return course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create course: {e}")