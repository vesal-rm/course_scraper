# UIUC Course Offering Scraper

This Python script scrapes the past semester offerings for courses at the University of Illinois at Urbana-Champaign (UIUC) from the UIUC Course Catalog website. It reads a list of course codes from a text file, accesses the relevant course pages, and extracts the information about which semesters each course has been offered. The data is then saved into a CSV file for easy reference.

## Requirements

Before running the script, ensure you have the following Python packages installed:

```
pip install requests beautifulsoup4 pandas
```

## How it Works

### 1. Input Course List

The script reads a list of course codes from a text file (e.g., `courses.txt`). Each course code should be in the format `[DepartmentAbbreviation][CourseNumber]` (e.g., `CS101`, `MATH221`).

### 2. Building the URL

The script constructs a URL for each course, based on the UIUC course catalog's URL structure:
	```
	https://course.illinois.edu/schedule/terms/DEPT/NUMBER
	```
	For example, for `CS101`, the URL would be:
	```
	https://courses.illinois.edu/schedule/terms/CS/101
	```

### 3. Scraping the Webpage

The script sends a request to each course page and then locates the HTML section `<div id="app-content" role="main">`, which contains the list of semesters the course was offered. It then extracts the semesters and years from the `<ul class="list-unstyled">` within this section.

### 4. Output to CSV

The script compiles the extracted data into a CSV file where each row contains a course code and the semesters it was offered.

## How to Use

### 1. Prepare the Course List

Create a `.txt` file called `courses.txt` containing the course codes you want to scrape. Each course should be on a new line. For example, `courses.txt` may look like this:
```
CS101
MATH221
STAT403
PHYS280
```

### 2. Run the Script

You can run the script by executing it in your Python environment:
```
python scrape_courses.py
```
Make sure to update the script with the correct file paths for your input and output files if necessary.

### 3. Output

The output will be a CSV file, named by default, `uiuc_courses_offered.csv`.

## Troubleshooting

### 1. No Data Found

If the script outputs `No data found` for a course, this could mean:
Markup: * The course has no semesters listed in the catalog.
	* The course page structure might have changed, in which case you may need to inspect the HTML to ensure that the correct elements are targeted.

### 2. Failed to Retrive Data

This indicates that the request to the UIUC course catalog webpage failed. Ensure that you have a working internet connection and that the UIUC course catalog URL is correct.

## Ownership

This script was developed for use by the Program in Arms Control Domestic and International Security (ACDIS) at the University of Illinois Urbana-Champaign (UIUC).
