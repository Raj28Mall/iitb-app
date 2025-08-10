from app.db.session import db
from pathlib import Path
import csv
from typing import Dict, Any, Iterable
import os

def validate_course_data(course_data: Dict[str, str]) -> bool:
    """Validates the course data against predefined rules."""
    required_fields = ['course_code', 'course_name', 'course_type', 'slot']
    missing = [k for k in required_fields if k not in course_data]
    if missing:
        # print(f"Missing required fields: {', '.join(missing)}")
        return False
    return True

def clean_course_data(course_data):
    """Cleans the course data by removing whitespaces."""
    for field in ['course_code', 'course_name', 'course_type', 'slot']:
        course_data[field] = course_data[field].strip()

    return course_data

def upload_course_data(course_data):
    """Uploads the cleaned and validated course data to the database."""
    try:
        db.collection("courses").add(course_data)
        print(f"{course_data['course_name']} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading course data: {e}")

if __name__ == "__main__":
    
    departments =["chemical", "electrical", "metallurgy", "civil", "computer_science", "aerospace", "economics", "energy", "digital_health", "data_science", "ent", "ieor", "environmental", "math", "mechanical", "physics", "chemistry", "biology", "climate_studies", "educational_tech", "gnr", "earth_sciences", "humanities", "idc", "management", "syscon", "policy_studies", "technology_alternatives", "liberal_education"]


    courses_data = []
    for branch in departments:
        file_path = os.path.join(os.path.dirname(__file__), f"department_data_processed/{branch}_data.csv")
        with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                courses_data.append(dict(row))
        
    for raw_course in courses_data:
        if validate_course_data(raw_course):
            course = clean_course_data(raw_course)
            upload_course_data(course)
        else:
            print(f"Invalid course data: {raw_course}")
    print("All course data upload completed.")
