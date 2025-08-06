import os
import pandas as pd
from bs4 import BeautifulSoup
import re

VALID_COURSE_TYPES = ["Theory", "Lab", "Non-Credit"]

def scrape_course_data(html_content):
    """
    Parses HTML content to extract course details.

    Args:
        html_content (str): The HTML source code of the page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a course.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    scraped_data = []

    course_rows = soup.find_all('tr', bgcolor="#CCCC99")

    from bs4 import Tag
    for row in course_rows:
        if not isinstance(row, Tag):
            continue
        columns = row.find_all('td')
        
        if len(columns) > 8:
            try:
                course_code = columns[2].get_text(strip=True)
                course_name = columns[3].get_text(strip=True)


                # course_code = "".join([char for char in course_code_raw if char.isalnum() and char != ' '])
                # course_code = course_code_raw
                # if len(course_code) == 6 and course_code.find(' ') == -1:
                    # course_code = course_code[:3] + ' ' + course_code[3:]
                    # print(course_code)


                course_type = columns[4].get_text(strip=True)
                if course_type not in VALID_COURSE_TYPES:
                    continue
                
                slot_details = columns[8].get_text(separator='\n', strip=True)
                if course_type == "Lab":
                    matches = re.findall('L[1-6]', slot_details)
                    if matches:
                        slot_details = matches[0]
                    else:
                        #Skipping cause invalid slot
                        continue
                
                slot_details = slot_details.split('\n')[0]
                
                if not slot_details:
                    #Skipping cause no slot details (Maybe i shouldnt be skipping, rather keep it and later update when get to know the slot)
                    continue

                if course_type == "Theory" and not slot_details.isdigit():
                    #Skipping cause invalid slot, why does theory slot have a Lab slot
                    continue

                scraped_data.append({
                    'course_name' : course_name,
                    'course_code': course_code,
                    'course_type': course_type,
                    # 'Slot': slot_details
                    'slot': slot_details
                })
            except IndexError:
                print(f"Skipping a malformed row...")
                continue

    return scraped_data

def load_and_scrape_html_file(file_path):
    """
    Loads an HTML file and scrapes course data from it.
    
    Args:
        file_path (str): Path to the HTML file
        
    Returns:
        list: A list of dictionaries containing course data
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            return scrape_course_data(html_content)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

if __name__ == "__main__":
    departments =["chemical", "electrical", "metallurgy", "civil", "computer_science", "aerospace", "economics", "energy"]
    # departments =["aerospace"]
    for branch in departments:
        html_file_path = os.path.join(os.path.dirname(__file__), f"department_data/{branch}.html")
        
        courses = load_and_scrape_html_file(html_file_path)
        
        if courses:
            print(f"Found {len(courses)} courses for {branch}")
            
            # print(courses[0])
            df = pd.DataFrame(courses, index=None)
            df = df.drop_duplicates(subset=['course_code'])
            # Optionally save to CSV
            df.to_csv(os.path.join(os.path.dirname(__file__), f"{branch}_data.csv"), index=False)
        else:
            print("No course data found.")
