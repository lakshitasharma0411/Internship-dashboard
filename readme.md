\# Internship Dashboard – Task 1



-----Project Overview

This project builds an interactive dashboard analyzing job posting data.  

The goal is to visualize \*\*Preference vs Work Type (Intern)\*\* using specific filtering conditions.



--------------- Dataset

CSV dataset containing job posting information such as:

\- Experience

\- Salary Range

\- Job Title

\- Company Size

\- Location

\- Job Posting Date

\- Preference

\- Work Type



\## Filters Applied

The dashboard applies the following rules:



\- Work Type = Intern

\- Latitude < 10

\- Country name does not start with A, B, C, or D

\- Job Title must be a single word with fewer than 10 characters

\- Company Size < 50,000

\- Salary above $9,000

\- Experience must be an even number

\- Job Posting month must be odd-numbered



\## Visualization

A bar chart showing the count of \*\*Preference vs Work Type (Intern)\*\*.



The chart is sorted in descending order by count.



\## Tools Used

\- Python

\- Streamlit

\- Pandas

\- Plotly



\## How to Run the Project



Install required libraries:



pip install -r requirements.txt



Run the dashboard:



streamlit run app.py

