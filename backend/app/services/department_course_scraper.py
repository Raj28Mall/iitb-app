import json
import pandas as pd
from bs4 import BeautifulSoup
import os
from app.db.session import db

departments_names_to_codes = {
    "Chemical Engineering": "CL", 
    "Aerospace Engineering": "AE",
    "Civil Engineering": "CE",
    "Computer Science and Engineering": "CS",
    "Electrical Engineering": "EE",
    "Energy Science and Engineering": "EN",
    "Engineering Physics": "EP",
    "Metallurgical Engineering and Materials Science": "MM",
    # "Physics": "PH",
    "Environmental Science and Engineering":"ES",
    "Mechanical Engineering":"ME",
    "Industrial Engineering and Operations Research":"IE",
    "Economics":"EC",
    "Chemistry":"CH",
    "Mathematics":"MA"
}

departments_to_skip = ["Physics", "Humanities and Social Sciences", "Centre for Liberal Education (CLEdu)"]

departments_names_to_divisions={
    "Chemical Engineering": "D4", 
    "Aerospace Engineering": "D2",
    "Civil Engineering": "D2",
    "Computer Science and Engineering": "D3",
    "Electrical Engineering": "D4",
    "Energy Science and Engineering": "D1",
    "Engineering Physics": "D2",
    "Metallurgical Engineering and Materials Science": "D3",
    # "Physics": "PH",
    "Environmental Science and Engineering":"D1",
    "Mechanical Engineering":"D1",
    "Industrial Engineering and Operations Research":"D2",
    "Economics":"D3",
    "Chemistry":"D1",
    "Mathematics":"D1"
}

def scrape_course_data(html_content, isFirstYear):
    """
    Parses HTML content to extract department course details.

    Args:
        html_content (str): The HTML source code of the page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a course.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    department_courses: dict[str, set[str]] = {}

    table = soup.find('table', id='example')
    if table is None:
        print("Error: Table with id 'example' not found.")
        return []
    
    DEPARTMENT_COLUMN_INDEX = 4
    CODE_COLUMN_INDEX = 8 if not isFirstYear else 9
    DIVISION_COLUMN_INDEX = 8

    table_body = table.find('tbody') or table

    for row in table_body.find_all('tr'):
        cols = row.find_all('td')
        if not cols:
            print("Empty columns, skipping....")
            continue 

        if len(cols) <= 8:
            print("Less than 8 columns, skipping....")
            continue
        
        department= cols[DEPARTMENT_COLUMN_INDEX].get_text(strip=True)

        if not department:
            print("Department is empty, skipping....")
            continue
        
        if isFirstYear:
            if department not in departments_names_to_divisions:
                print(f"Unknown department '{department}', skipping...")
                continue

            division = departments_names_to_divisions[department]
            division_asc = cols[DIVISION_COLUMN_INDEX].get_text(strip=True)
            if division != division_asc:
                # print(f"Division mismatch for {department}: {division} != {division_asc}, skipping...")
                # break
                continue


        code = cols[CODE_COLUMN_INDEX].get_text(strip=True)
        if not code:
            continue
        
        if department in departments_to_skip:
            continue

        if department not in departments_names_to_codes:
            print(f"Unknown department '{department}', skipping...")
            continue
        
        #To convert from branch name to branch code
        # department = departments_names_to_codes[department]

        if department not in department_courses:
            department_courses[department] = set()
        department_courses[department].add(code)

    return department_courses

def load_and_scrape_html_file(file_path, semester: int):
    """
    Loads an HTML file and scrapes course data from it.
    
    Args:
        file_path (str): Path to the HTML file
        
    Returns:
        list: A list of dictionaries containing course data
    """
    isFirstYear = True if semester/2 <= 1 else False
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            return scrape_course_data(html_content, isFirstYear)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def uploadDataToFireStore(departments_data, semesters):
    """
    Uploads scraped course data to Firestore.

    Args:
        scraped_data (list): List of scraped course data.
        semesters (list): List of semesters corresponding to the data.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    departments_data={}
    for semester_num, semester_data_list in zip(semesters, scraped_data):
        for department_group_dict in semester_data_list:
            for department_name, courses in department_group_dict.items():
                
                if department_name not in departments_data:
                    departments_data[department_name] = {}
                
                unique_courses = sorted(list(set(courses)))
                departments_data[department_name][str(semester_num)] = unique_courses
    collection_ref = db.collection('department_courses')

    print("Starting data upload to Firestore...")

    for department_name, semesters in departments_data.items():
        try:
            doc_ref = collection_ref.document(department_name)
            doc_ref.set(semesters)
            
            print(f"✅ Successfully uploaded data for: {department_name}")
        except Exception as e:
            print(f"❌ Error uploading data for {department_name}: {e}")


if __name__ == "__main__":
    semesters= [1,  2, 3, 4, 5, 6, 7, 8]
    # semesters= [1]

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_base = os.path.join(base_dir, "api", "v1", "endpoints", "department_courses_raw")
    processed_base = os.path.join(base_dir, "api", "v1", "endpoints", "department_courses_processed")

    scraped_data=[]

    for semester in semesters:
        streams =["btech", "bs"]
        all_semester_courses=[]

        for stream in streams:
            html_file_path = os.path.join(raw_base, f"sem_{semester}_{stream}.html")

            try:
                scraped_courses_from_stream = load_and_scrape_html_file(html_file_path, semester)
                
                if scraped_courses_from_stream:
                    all_semester_courses.append(scraped_courses_from_stream)

            except FileNotFoundError:
                print(f"  > Warning: File not found, skipping: {html_file_path}")
            except Exception as e:
                # Catch other potential errors during scraping
                print(f"  > Error processing {html_file_path}: {e}")
            # all_semester_courses.append((load_and_scrape_html_file(html_file_path)))
        
        if all_semester_courses:
            # print(f"SEMESTER{semester}: ",all_semester_courses)
            scraped_data.append(all_semester_courses)
        else:
            print(f"No course data found for in semester {semester}")
    # print(scraped_data)
    uploadStats = uploadDataToFireStore(scraped_data, semesters)

    # departments_data = {}

    # for semester_num, list_of_department_groups in zip(semesters, scraped_data):
    #     for department_group in list_of_department_groups:
    #         for department_name, courses in department_group.items():
    #             if department_name not in departments_data:
    #                 departments_data[department_name] = {}
    #             # **Data Cleaning Step**: Remove duplicates from the course list by converting to a set, then back to a sorted list.
    #             unique_courses = sorted(list(set(courses)))
                
    #             departments_data[department_name][str(semester_num)] = unique_courses # Use string for semester key in JSON

    # output_filename = "courses_by_department.json"

    # with open(output_filename, 'w') as json_file:
    #     json.dump(departments_data, json_file, indent=4)

    # print(f"✅ Successfully created JSON file: {output_filename}")
    # print(f"File saved in: {os.path.abspath(output_filename)}")
