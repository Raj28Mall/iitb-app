from pydantic import BaseModel
from typing import Optional, List

class Department(BaseModel):
    """Department model for representing department data"""
    id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    
class DepartmentCreate(BaseModel):
    """Department creation model"""
    name: str
    code: Optional[str] = None
    description: Optional[str] = None

class Course(BaseModel):
    """Course model for representing course data"""
    id: str
    course_name: str
    course_code: str
    course_type: str
    slot: str
class CourseCreate(BaseModel):
    """Course creation model"""
    course_name: str
    course_code: str
    course_type: str
    slot: str