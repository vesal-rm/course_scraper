import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to construct the URL for each course
def construct_url(department_abbr, course_num):
    base_url = "https://courses.illinois.edu/schedule/terms/"
    return f"{base_url}{department_abbr}/{course_num:03d}"

# Function to scrape the webpage for past semesters offered
def scrape_course_data(department_abbr, course_num):
    url = construct_url(department_abbr, course_num)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Navigate to <div id="app-content" role="main">
        app_content = soup.find('div', id='app-content', role='main')
        
        if app_content:
            # Find the <ul> with class "list-unstyled" within the app-content div
            course_offerings = app_content.find('ul', class_='list-unstyled')
            if course_offerings:
                # Extract all <li> elements which contain the terms offered
                terms_list = course_offerings.find_all('li')
                terms = [term.text.strip() for term in terms_list]
                return terms
            else:
                return ["No data found within app content"]
        else:
            return ["App content not found"]
    else:
        return ["Failed to retrieve data"]

# Function to read the course list from the txt file
def read_course_list(file_path):
    with open(file_path, 'r') as f:
        courses = [line.strip() for line in f.readlines()]
    return courses

# Main function to orchestrate the process
def scrape_courses_to_csv(course_file, output_csv):
    course_list = read_course_list(course_file)
    
    # Prepare a list to store the result
    course_data = []
    
    for course in course_list:
        try:
            # Split the course into department abbreviation and course number
            department_abbr, course_num = course[:-3], int(course[-3:])
            semesters_offered = scrape_course_data(department_abbr, course_num)
            course_data.append({
                'Course': course,
                'Semesters Offered': ', '.join(semesters_offered)
            })
        except Exception as e:
            print(f"Error processing course {course}: {e}")
    
    # Convert the result into a DataFrame and save it to CSV
    df = pd.DataFrame(course_data)
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")

# Example usage
scrape_courses_to_csv('courses.txt', 'uiuc_courses_offered.csv')

