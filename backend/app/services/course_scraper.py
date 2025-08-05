import os
import glob
import pandas as pd
from bs4 import BeautifulSoup

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
        # Get all the columns (td elements) in the current row
        columns = row.find_all('td')
        
        # Ensure the row has the expected number of columns to avoid errors
        if len(columns) > 8:
            try:
                # --- Extract the required data based on column position ---
                
                # Course Code is in the 3rd column (index 2)
                # .get_text(strip=True) cleans up whitespace
                course_code = columns[2].get_text(strip=True)

                # Course Name is in the 4th column (index 3)
                course_name = columns[3].get_text(strip=True)
                course_type = columns[4].get_text(strip=True)

                # Slot information is in the 9th column (index 8)
                # We use .get_text with a separator to handle <br> and <hr> tags gracefully
                slot_details = columns[8].get_text(separator='\n', strip=True)

                scraped_data.append({
                    'Course Code': course_code,
                    'Course Name': course_name,
                    'Course Type': course_type,
                    # 'Slot': slot_details
                    'Slot': (slot_details.split('\n'))[0]
                })
                # print(scraped_data[-1]) 
            except IndexError:
                # This will skip any rows that don't have the expected structure
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


# --- Main execution part of the script ---

# IMPORTANT: Place your .html files into a folder named 'html_files'
# or change the path below to where your files are located.
# directory_path = 'html_files'
# all_html_files = glob.glob(os.path.join(directory_path, '*.html'))

# if not all_html_files:
#     print(f"Error: No .html files found in the '{directory_path}' directory.")
#     print("Please create the directory, place your files inside, and run the script again.")
# else:
#     all_courses = []
#     print(f"Found {len(all_html_files)} HTML files to process...")

#     for file_path in all_html_files:
#         print(f"Processing file: {file_path}")
#         with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
#             content = f.read()
#             courses_from_file = scrape_course_data(content)
#             all_courses.extend(courses_from_file)

#     if all_courses:
#         # Convert the list of dictionaries into a pandas DataFrame for easy viewing
#         df = pd.DataFrame(all_courses)

#         print("\n--- Scraping Complete ---")
#         print(df)

#         # Save the results to a CSV file for use in Excel or other programs
#         output_filename = 'scraped_courses.csv'
#         df.to_csv(output_filename, index=False, encoding='utf-8')
        
#         print(f"\nSuccessfully saved all data to '{output_filename}'")
#     else:
#         print("\nCould not find any course data in the provided files.")


if __name__ == "__main__":
    # Example: Load and scrape the asc_chemical.html file
    # departments =["chemical", "electrical", "metallurgy"]
    departments =["chemical"]
    for branch in departments:
        html_file_path = os.path.join(os.path.dirname(__file__), f"asc_{branch}.html")
        
        courses = load_and_scrape_html_file(html_file_path)
        
        if courses:
            print(f"Found {len(courses)} courses for {branch}")
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(courses)
            print(df)
            
            # Optionally save to CSV
            # output_file = "chemical_courses.csv"
            # df.to_csv(output_file, index=False, encoding='utf-8')
            # print(f"\nData saved to {output_file}")
        else:
            print("No course data found.")
