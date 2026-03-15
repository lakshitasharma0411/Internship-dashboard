import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import datetime

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------

st.title("Global Internship Dashboard")

# ---------------------------------------------------
# SIDEBAR TASK SELECTOR
# ---------------------------------------------------

task = st.sidebar.selectbox(
    "Select Task",
    [
        "Task 1 – Preference vs Work Type",
        "Task 2 – Company Size vs Company Name",
        "Task 3 – Top 10 Companies",
        "Task 4 – Qualification Map",
        "Task 5 – India vs Germany Comparison",
        "Task 6 – Work Type Salary Distribution"
    ]
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("dataset_sample.csv")
df.columns = df.columns.str.strip()

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

df["Salary Min"] = (
    df["Salary Range"]
    .str.replace("$", "", regex=False)
    .str.replace("K", "", regex=False)
    .str.split("-")
    .str[0]
)

df["Salary Min"] = pd.to_numeric(df["Salary Min"], errors="coerce")

df["Experience Num"] = df["Experience"].str.extract(r"(\d+)")
df["Experience Num"] = pd.to_numeric(df["Experience Num"], errors="coerce")

df["Company Size"] = pd.to_numeric(df["Company Size"], errors="coerce")

df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

df["Job Posting Date"] = pd.to_datetime(df["Job Posting Date"], errors="coerce")

# ---------------------------------------------------
# TIME
# ---------------------------------------------------
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)


# ===================================================
# TASK 1 – BAR CHART
# ===================================================

if task == "Task 1 – Preference vs Work Type":

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
    grouped = (
    filtered.groupby("Preference")
    .size()
    .reset_index(name="Count")
    )
    fig = px.bar(
        grouped,
        x="Preference",
        y="Count",
        text="Count",
        title="Preference vs Intern Work Type"
    )
    st.plotly_chart(fig)
    # -----------------------------
# WORK TYPE DISTRIBUTION
# ----------------------------
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
    st.subheader("Top 10 Countries")
    country_counts = filtered["Country"].value_counts().head(10).reset_index()
    country_counts.columns = ["Country","Count"]
    fig3 = px.bar(
        country_counts,
        x="Country",
        y="Count",
        color="Country"
    )
    st.plotly_chart(fig3)
    st.subheader("Top 10 Job Titles")
    job_counts = filtered["Job Title"].value_counts().head(10).reset_index()
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

    st.subheader("Filtered Task Data")

    st.write("Rows after task filters:", len(filtered))

    st.dataframe(filtered[["Preference","Work Type","Country","Job Title"]])

    st.subheader("Interactive Filter Data")

    st.write("Rows after sidebar filters:", len(filtered))

    st.dataframe(filtered.head(50))



# ===================================================
# TASK 2 – SCATTER PLOT
# ===================================================

elif task == "Task 2 – Company Size vs Company Name":

    filtered = df.copy()

    filtered = filtered[filtered["Company Size"] < 50000]
    filtered = filtered[filtered["Job Title"] == "Mechanical Engineer"]
    filtered = filtered[filtered["Experience Num"] > 5]
    filtered = filtered[filtered["Salary Min"] > 50]

    filtered = filtered[
        filtered["Work Type"].isin(["Full-Time","Part-Time"])
    ]

    filtered = filtered[filtered["Preference"] == "Male"]
    filtered = filtered[filtered["Job Portal"] == "Idealist"]

    asia = [
        "China","Japan","South Korea","Saudi Arabia","UAE",
        "Thailand","Malaysia","Singapore","Pakistan",
        "Bangladesh","Nepal","Sri Lanka","Philippines","Vietnam"
    ]

    filtered = filtered[filtered["Country"].isin(asia)]
    filtered = filtered[~filtered["Country"].str.startswith("I", na=False)]

    def vowel_check(name):
        vowels = "aeiouAEIOU"
        return sum(c in vowels for c in str(name)) >= 2

    filtered = filtered[filtered["Company"].apply(vowel_check)]

    if 15 <= current_time.hour < 17:

        fig = px.scatter(
            filtered,
            x="Company Size",
            y="Company",
            title="Company Size vs Company Name"
        )

        st.plotly_chart(fig)

    else:
        st.warning("Chart visible only between 3 PM and 5 PM IST")

# ===================================================
# TASK 3 – TREEMAP
# ===================================================

elif task == "Task 3 – Top 10 Companies":

    filtered = df.copy()

    filtered = filtered[filtered["Role"] == "Data Engineer"]
    filtered = filtered[filtered["Job Title"] == "Data Scientist"]

    filtered = filtered[~filtered["Country"].str.contains("Asia", na=False)]
    filtered = filtered[~filtered["Country"].str.startswith("C", na=False)]

    filtered = filtered[filtered["latitude"] < 10]
    filtered = filtered[filtered["Preference"] == "Female"]
    filtered = filtered[filtered["Qualification"] == "B.Tech"]

    filtered = filtered[
        (filtered["Job Posting Date"] >= "2023-01-01") &
        (filtered["Job Posting Date"] <= "2023-01-06")
    ]

    filtered = filtered[filtered["Job Portal"] == "LinkedIn"]
    filtered = filtered[filtered["Company Size"] >= 10000]

    filtered = filtered[
        filtered["Contact Person"].str.endswith(
            ("a","e","i","o","u"), na=False
        )
    ]

    if 15 <= current_time.hour < 17:

        top = (
            filtered["Company"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top.columns = ["Company","Count"]

        fig = px.treemap(
            top,
            path=["Company"],
            values="Count",
            title="Top 10 Companies"
        )

        st.plotly_chart(fig)

    else:
        st.warning("Chart visible only between 3 PM and 5 PM IST")

# ===================================================
# TASK 4 – MAP
# ===================================================

elif task == "Task 4 – Qualification Map":

    filtered = df.copy()

    filtered = filtered[
        filtered["Qualification"].isin(["B.Tech","M.Tech","PhD"])
    ]

    filtered = filtered[filtered["Work Type"] == "Full-Time"]
    filtered = filtered[filtered["Preference"] == "Male"]

    filtered = filtered[filtered["Company Size"] > 80000]
    filtered = filtered[filtered["Job Portal"] == "Indeed"]

    filtered = filtered[filtered["Job Title"].str.startswith("D", na=False)]
    filtered = filtered[filtered["Contact Person"].str.startswith("A", na=False)]

    filtered = filtered[filtered["Salary Min"] > 20]

    africa = [
        "Nigeria","Kenya","Egypt","South Africa",
        "Morocco","Ghana","Ethiopia"
    ]

    filtered = filtered[filtered["Country"].isin(africa)]

    if 15 <= current_time.hour < 18:

        fig = px.scatter_mapbox(
            filtered,
            lat="latitude",
            lon="longitude",
            hover_name="Company",
            zoom=2,
            height=500
        )

        fig.update_layout(mapbox_style="open-street-map")

        st.plotly_chart(fig)

    else:
        st.warning("Chart visible only between 3 PM and 6 PM IST")

# ===================================================
# TASK 5 – STACKED BAR
# ===================================================

elif task == "Task 5 – India vs Germany Comparison":

    filtered = df.copy()

    filtered = filtered[
        filtered["Country"].isin(["India","Germany"])
    ]

    filtered = filtered[filtered["Qualification"] == "B.Tech"]
    filtered = filtered[filtered["Work Type"] == "Full-Time"]

    filtered = filtered[filtered["Experience Num"] > 2]

    filtered = filtered[
        filtered["Job Title"].isin(
            ["Data Scientist","Art Teacher","Aerospace Engineer"]
        )
    ]

    filtered = filtered[filtered["Salary Min"] > 10]
    filtered = filtered[filtered["Job Portal"] == "Indeed"]
    filtered = filtered[filtered["Preference"] == "Female"]

    filtered = filtered[
        filtered["Job Posting Date"] < "2023-01-08"
    ]

    filtered = filtered[filtered["Location"].notna()]
    filtered = filtered[filtered["Company"].str.len() > 8]

    if 15 <= current_time.hour < 17:

        grouped = (
            filtered.groupby(["Country","Job Title"])
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            grouped,
            x="Country",
            y="Count",
            color="Job Title",
            title="India vs Germany Job Postings",
            barmode="stack"
        )

        st.plotly_chart(fig)

    else:
        st.warning("Chart visible only between 3 PM and 5 PM IST")

# ===================================================
# TASK 6 – BOX PLOT
# ===================================================

elif task == "Task 6 – Work Type Salary Distribution":

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
    filtered = filtered[filtered["Salary Min"] > 8]

    filtered = filtered[filtered["Experience Num"] % 2 == 0]

    filtered = filtered[
        filtered["Job Posting Date"].dt.year.between(2021,2023)
    ]

    filtered = filtered[
        filtered["Contact Person"].str.contains("e", case=False, na=False)
    ]

    if 15 <= current_time.hour < 17:

        fig = px.box(
            filtered,
            x="Work Type",
            y="Salary Min",
            title="Work Type Salary Distribution"
        )

        st.plotly_chart(fig)

    else:
        st.warning("Chart visible only between 3 PM and 5 PM IST")
