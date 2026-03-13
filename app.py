import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import datetime

st.title("Global Job Preference Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("dataset_sample.csv")

df.columns = df.columns.str.strip()

st.write("Total rows loaded:", len(df))

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

work_type_filter = st.sidebar.selectbox(
    "Select Work Type",
    df["Work Type"].dropna().unique()
)

country_filter = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["Country"].dropna().unique())
)

job_filter = st.sidebar.selectbox(
    "Select Job Title",
    ["All"] + list(df["Job Title"].dropna().unique())
)

# -----------------------------
# DATA CLEANING
# -----------------------------

# Salary cleaning
df["Salary Min"] = (
    df["Salary Range"]
    .str.replace("$", "", regex=False)
    .str.replace("K", "", regex=False)
    .str.split("-")
    .str[0]
)

df["Salary Min"] = pd.to_numeric(df["Salary Min"], errors="coerce")

# Experience cleaning
df["Experience Num"] = df["Experience"].str.extract(r"(\d+)")
df["Experience Num"] = pd.to_numeric(df["Experience Num"], errors="coerce")

# Company Size
df["Company Size"] = pd.to_numeric(df["Company Size"], errors="coerce")

# Latitude
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")

# Date
df["Job Posting Date"] = pd.to_datetime(df["Job Posting Date"], errors="coerce")

# -----------------------------
# APPLY FILTERS
# -----------------------------

filtered_df = df[df["Work Type"] == work_type_filter]

if country_filter != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country_filter]

if job_filter != "All":
    filtered_df = filtered_df[filtered_df["Job Title"] == job_filter]

# -----------------------------
# TASK FILTERS
# -----------------------------

filtered = df.copy()

filtered = filtered[filtered["Work Type"] == "Intern"]
filtered = filtered[filtered["latitude"] < 10]

filtered = filtered[
    ~filtered["Country"].str.startswith(("A","B","C","D"), na=False)
]

filtered = filtered[
    (filtered["Job Title"].str.split().str.len() == 1) &
    (filtered["Job Title"].str.len() < 10)
]

filtered = filtered[filtered["Company Size"] < 50000]
filtered = filtered[filtered["Salary Min"] > 9]

filtered = filtered[filtered["Experience Num"] % 2 == 0]

filtered = filtered[
    filtered["Job Posting Date"].dt.month % 2 == 1
]

# -----------------------------
# PREFERENCE CHART
# -----------------------------

grouped = (
    filtered.groupby("Preference")
    .size()
    .reset_index(name="Count")
)

st.subheader("Preference vs Work Type (Intern)")

fig = px.bar(
    grouped,
    x="Preference",
    y="Count",
    text="Count",
    color="Preference"
)

st.plotly_chart(fig)

# -----------------------------
# WORK TYPE DISTRIBUTION
# -----------------------------

st.subheader("Work Type Distribution")

work_counts = df["Work Type"].value_counts().reset_index()
work_counts.columns = ["Work Type","Count"]

fig2 = px.bar(
    work_counts,
    x="Work Type",
    y="Count",
    color="Work Type"
)

st.plotly_chart(fig2)

# -----------------------------
# TOP COUNTRIES
# -----------------------------

st.subheader("Top 10 Countries")

country_counts = filtered_df["Country"].value_counts().head(10).reset_index()
country_counts.columns = ["Country","Count"]

fig3 = px.bar(
    country_counts,
    x="Country",
    y="Count",
    color="Country"
)

st.plotly_chart(fig3)

# -----------------------------
# TOP JOB TITLES
# -----------------------------

st.subheader("Top 10 Job Titles")

job_counts = filtered_df["Job Title"].value_counts().head(10).reset_index()
job_counts.columns = ["Job Title","Count"]

fig4 = px.bar(
    job_counts,
    x="Job Title",
    y="Count",
    color="Job Title"
)

st.plotly_chart(fig4)

# -----------------------------
# PREFERENCE PIE CHART
# -----------------------------

st.subheader("Preference Distribution")

pref_counts = filtered_df["Preference"].value_counts().reset_index()
pref_counts.columns = ["Preference","Count"]

fig5 = px.pie(
    pref_counts,
    names="Preference",
    values="Count"
)

st.plotly_chart(fig5)

# -----------------------------
# DATA TABLES
# -----------------------------

st.subheader("Filtered Task Data")

st.write("Rows after task filters:", len(filtered))

st.dataframe(filtered[["Preference","Work Type","Country","Job Title"]])

st.subheader("Interactive Filter Data")

st.write("Rows after sidebar filters:", len(filtered_df))

st.dataframe(filtered_df.head(50))

# TIME CONDITION (3PM–5PM IST)
# -----------------------------
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)

if 15 <= current_time.hour < 17:

    grouped = (
        filtered.groupby("Preference")
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
    )

    if not grouped.empty:
        fig = px.bar(
            grouped,
            x="Preference",
            y="Count",
            text="Count",
            title="Preference vs Intern Work Type"
        )
        st.plotly_chart(fig)
    else:
        st.warning("No data available after applying all filters.")

else:
    st.warning("Chart visible only between 3 PM and 5 PM IST.")

# Local URL: http://localhost:8501

#  Network URL: http://192.168.0.21:8501



