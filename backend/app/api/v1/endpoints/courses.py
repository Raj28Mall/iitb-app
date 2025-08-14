from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from pydantic import ValidationError
import asyncio
# from google.cloud.firestore_v1.client import Client
from app.db.session import db
from app.api.v1.schemas import Department, Course
from app.services.department_course_scraper import departments_names_to_codes

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

@router.get("/courses/{department_code}/{semester}", response_model=List[str])
async def get_courses_for_department(department_code: str, semester: int) -> List[str] | str:
    """Returns the core courses running for the given department"""
    if semester < 1 or semester > 8:
        raise HTTPException(status_code=400, detail="Invalid semester")
    
    available_departments = await get_departments()
    for department in available_departments:
        if department.code == department_code:
            doc_ref = db.collection('department_courses').document(department.name)
            doc = (doc_ref.get()).to_dict()
            if doc:
                courses = doc.get(str(semester), [])
                return courses 
            else:
                raise HTTPException(status_code=404, detail=f"No courses found for department: {department_code} in semester {semester}")
    
    raise HTTPException(status_code=400, detail="Invalid department code")
    
async def get_all_department_data():
    """Fetches all data from the department_courses collection."""
    all_department_courses = {}
    try:
        docs = db.collection('department_courses').stream()
                
        for doc in docs:
            # doc.id is the department name (e.g., "Civil Engineering")
            all_department_courses[doc.id] = doc.to_dict()
        
        print(f"✅ Successfully fetched {len(all_department_courses)} departments.")
        return all_department_courses
    except Exception as e:
        print(f"🔥 An error occurred: {e}")
        return None

# async def print_available_departments():
#     available_departments = await get_departments()
#     print(f"Available Departments: {(available_departments[0]).name}")
    
# if __name__ == "__main__":
    # asyncio.run(print_available_departments())
    # pass