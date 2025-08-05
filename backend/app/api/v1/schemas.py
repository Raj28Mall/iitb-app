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
    name: str
    code: Optional[str] = None
    type: str
    department_id: str
    slot: List[str] # I dont know if this is the best