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
                terms = [li.text.strip() for li in course_offerings.find_all('li')]
                return terms
    return []

# Main function to process courses and save the output
def process_courses(input_excel, output_excel):
    # Read the Excel file, skipping the header row
    df = pd.read_excel(input_excel, skiprows=1, header=None, names=['Department', 'Number'])
    
    # Prepare the output data
    output_data = []

    for _, row in df.iterrows():
        department_abbr = row['Department']
        course_num = row['Number']
        
        # Scrape data for each course
        terms_offered = scrape_course_data(department_abbr, course_num)
        output_data.append([department_abbr, course_num] + terms_offered)
    
    # Convert to DataFrame and save as Excel
    max_terms = max(len(row) for row in output_data)
    columns = ['Department', 'Number'] + [f'Term {i}' for i in range(1, max_terms - 1)]
    output_df = pd.DataFrame(output_data, columns=columns)
    output_df.to_excel(output_excel, index=False)

# Example usage
process_courses('courses.xlsx', 'uiuc_courses_semesters.xlsx')
