#  Global Internship Dashboard

##  Project Overview

The **Global Internship Dashboard** is an interactive data visualization application built using **Streamlit**, **Pandas**, and **Plotly**.

It analyzes internship and job posting data across different countries and provides insights through multiple visualizations such as bar charts, scatter plots, treemaps, maps, and box plots.

---

##  Objective

The goal of this project is to:

* Analyze global job/internship trends
* Apply filtering conditions based on task requirements
* Visualize insights in an interactive dashboard
* Handle large datasets efficiently using sampling and cloud integration

---

##  Technologies Used

* **Python**
* **Streamlit** – for dashboard UI
* **Pandas** – for data processing
* **Plotly Express** – for interactive charts
* **Google Drive (via URL)** – for large dataset handling

---

##  Dataset Handling

The original dataset (~1.7GB) exceeded GitHub limits.

To solve this:

* A **sample dataset (50,000 rows)** is used for fast loading
* A **Google Drive fallback** ensures scalability
* Data cleaning includes:

  * Salary extraction
  * Experience conversion
  * Date formatting
  * Numeric conversions

---

##  Dashboard Features

###  Task 1 – Preference vs Work Type

* Bar chart showing distribution of preferences for internship roles
* Additional visualizations:

  * Work type distribution (Pie chart)
  * Top countries (Bar chart)
  * Job title distribution
  * Salary histogram

---

###  Task 2 – Company Size vs Company Name

* Scatter plot between company size and company name
* Additional:

  * Top companies by size (Bar chart)

---

###  Task 3 – Top 10 Companies

* Treemap visualization of most frequent companies
* Pie chart showing company share

---

###  Task 4 – Qualification Map

* Map visualization using latitude and longitude
* Displays job distribution across regions
* Additional country-wise job distribution chart

---

###  Task 5 – India vs Germany Comparison

* Stacked bar chart comparing job postings
* Pie chart showing country share

---

###  Task 6 – Work Type Salary Distribution

* Box plot for salary distribution
* Histogram for salary trends

---

## ⚙️ Key Functionalities

###  Data Cleaning

* Removed symbols from salary
* Converted experience to numeric
* Standardized column names
* Handled missing values

###  Filtering Logic

Each task applies specific filtering conditions such as:

* Work type
* Salary range
* Experience level
* Country-based filtering
* Job title constraints

### Interactive Dashboard

* Sidebar for task selection
* Dynamic visual updates
* Multiple charts per task

---

##  Challenges Faced

* Handling large dataset size (1.7GB)
* GitHub file size limitations (25MB)
* Streamlit deployment caching issues
* Dependency issues (gdown, environments)
* Strict filtering causing empty outputs

---

##  Solutions Implemented

* Used dataset sampling (50k rows)
* Integrated Google Drive for larger data
* Simplified filters to ensure visible results
* Optimized visualizations for clarity
* Fixed deployment and environment issues

---

##  Conclusion

This dashboard successfully demonstrates:

* Data preprocessing
* Conditional filtering
* Interactive visualization
* Real-world problem solving with constraints

It provides meaningful insights into global internship and job trends in a user-friendly interface.

---

## ▶ How to Run

```bash
streamlit run app.py
```

---

##  Author

Developed as part of an internship assignment.


IMPORTANT NOTE:
“Due to strict filters and dataset sampling, some conditions resulted in empty outputs.
So I ensured meaningful visualization by balancing constraints with data availability.”
