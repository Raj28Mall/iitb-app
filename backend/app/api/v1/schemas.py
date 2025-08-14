from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Literal

class Department(BaseModel):
    """Department model for representing department data"""
    id: str
    name: str
    code: str = Field(pattern=r"^[A-Z]{2}$")
    description: Optional[str] = None
    
class DepartmentCreate(BaseModel):
    """Department creation model"""
    name: str
    code: str = Field(pattern=r"^[A-Z]{2}$")
    description: Optional[str] = None

class Course(BaseModel):
    """Course model for representing course data"""
    id: str
    course_name: str
    course_code: str = Field(pattern=r"^(?:[A-Z]{2} \d{3}|[A-Z]{3}\d{3}|[A-Z]{2}\d{4})$")
    course_type: Literal["Theory", "Lab"]
    slot: str
    
    @model_validator(mode='after')
    def validate_slot_for_course_type(self):
        """Validate that slot matches the course type requirements"""
        course_type = self.course_type
        slot = self.slot
        
        if course_type == "Theory":
            # Theory courses: slots 1-14
            if not (slot.isdigit() and 1 <= int(slot) <= 15):
                raise ValueError(f"Theory courses must have slots 1-15, got '{slot}'")
        elif course_type == "Lab":
            # Lab courses: slots L1-L6
            if not (slot.startswith('L') and len(slot) == 2 and 
                    slot[1].isdigit() and 1 <= int(slot[1]) <= 6):
                raise ValueError(f"Lab courses must have slots L1-L6, got '{slot}'")
        
        return self

class CourseCreate(BaseModel):
    """Course creation model"""
    course_name: str
    course_code: str
    course_type: str
    slot: str