import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import datetime
import gdown
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Global Internship Dashboard", layout="wide")
st.title("🌍 Global Internship Dashboard")

# ---------------------------------------------------
# LOAD DATA (GITHUB + DRIVE FALLBACK)
# ---------------------------------------------------
@st.cache_data
def load_data():
    try:
        # ✅ Load small dataset (GitHub)
        df = pd.read_csv("dataset.csv")
        st.sidebar.success("Loaded GitHub dataset (fast)")
    
    except:
        # ✅ Fallback to Google Drive
        file_id = "1gvHGeckF5hqT3LFpvGLT3HaB7penAxUA"
        url = f"https://drive.google.com/uc?id=1gvHGeckF5hqT3LFpvGLT3HaB7penAxUA"
        output = "data.csv"

        if not os.path.exists(output):
            with st.spinner("Downloading dataset from Google Drive..."):
                gdown.download(url, output, quiet=False)

        df = pd.read_csv(output, nrows=50000)
        st.sidebar.warning("Loaded large dataset (Drive)")

    # ---------------- CLEANING ----------------
    df.columns = df.columns.str.strip()

    df.rename(columns={
        "Qualifications": "Qualification",
        "location": "Location"
    }, inplace=True)

    # Salary
    df["Salary Min"] = (
        df["Salary Range"]
        .str.replace(r"[\$,K]", "", regex=True)
        .str.split("-")
        .str[0]
    )
    df["Salary Min"] = pd.to_numeric(df["Salary Min"], errors="coerce")

    # Experience
    df["Experience Num"] = (
        df["Experience"]
        .str.extract(r"(\d+)")
    )
    df["Experience Num"] = pd.to_numeric(df["Experience Num"], errors="coerce")

    # Numeric
    df["Company Size"] = pd.to_numeric(df["Company Size"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    # Date fix
    df["Job Posting Date"] = pd.to_datetime(
        df["Job Posting Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # Normalize text
    df["Work Type"] = df["Work Type"].str.lower()
    df["Preference"] = df["Preference"].str.capitalize()

    return df


df = load_data()

st.sidebar.write("Total Rows:", len(df))

# ---------------------------------------------------
# SIDEBAR
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
# TIME
# ---------------------------------------------------
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)

# ===================================================
# TASK 1
# ===================================================
if task == "Task 1 – Preference vs Work Type":

    filtered = df.copy()

    filtered = filtered[filtered["Work Type"] == "intern"]
    filtered = filtered[filtered["Salary Min"] > 5]
    filtered = filtered[filtered["Company Size"] < 100000]

    st.write("Filtered Rows:", len(filtered))

    if len(filtered) > 0:
        grouped = filtered.groupby("Preference").size().reset_index(name="Count")

        fig = px.bar(grouped, x="Preference", y="Count", text="Count")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")

    pref_counts = df["Work Type"].value_counts().reset_index()
    pref_counts.columns = ["Work Type", "Count"]

    fig = px.pie(
        pref_counts,
        names="Work Type",
        values="Count",
        title="Work Type Distribution"
    )
    st.plotly_chart(fig)
    
    country_counts = df["Country"].value_counts().head(10).reset_index()
    country_counts.columns = ["Country", "Count"]
    fig = px.bar(
        country_counts,
        x="Country",
        y="Count",
        title="Top 10 Countries",
        text="Count"
    )
    st.plotly_chart(fig)

    pref_counts = df["Preference"].value_counts().reset_index()
    pref_counts.columns = ["Preference", "Count"]

    fig = px.pie(
        pref_counts,
        names="Preference",
        values="Count",
        title="Preference Distribution"
    )
    st.plotly_chart(fig)
    
    job_counts = df["Job Title"].value_counts().head(10).reset_index()
    job_counts.columns = ["Job Title", "Count"]

    fig = px.bar(
        job_counts,
        x="Job Title",
        y="Count",
        title="Top Job Titles",
        text="Count"
    )
    st.plotly_chart(fig)
    fig = px.histogram(
        df,
        x="Salary Min",
        nbins=30,
        title="Salary Distribution"
    )
    st.plotly_chart(fig)
    pref_counts = df["Preference"].value_counts().reset_index()
    pref_counts.columns = ["Preference", "Count"]

    fig = px.pie(
        pref_counts,
        names="Preference",
        values="Count",
        title="Preference Distribution"
    )
    st.plotly_chart(fig)

# ===================================================
# TASK 2
# ===================================================
elif task == "Task 2 – Company Size vs Company Name":

    filtered = df.copy()

    filtered = filtered[filtered["Company Size"] < 50000]
    filtered = filtered[filtered["Salary Min"] > 20]

    st.write("Filtered Rows:", len(filtered))

    if len(filtered) > 0:
        fig = px.scatter(filtered, x="Company Size", y="Company")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")

    top_companies = (
    filtered.groupby("Company")["Company Size"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        top_companies,
        x="Company",
        y="Company Size",
        title="Top Companies by Size",
        text="Company Size"
    )

    st.plotly_chart(fig)
        

# ===================================================
# TASK 3
# ===================================================
elif task == "Task 3 – Top 10 Companies":

    filtered = df.copy()

    if len(filtered) > 0:
        top = filtered["Company"].value_counts().head(10).reset_index()
        top.columns = ["Company", "Count"]

        fig = px.treemap(top, path=["Company"], values="Count")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")
        
    fig = px.pie(
         filtered,
         names="Company",
         title="Company Share Distribution"
    )
    st.plotly_chart(fig)

# ===================================================
# TASK 4
# ===================================================
elif task == "Task 4 – Qualification Map":

    filtered = df.copy()

    filtered = filtered[filtered["Salary Min"] > 20]

    st.write("Filtered Rows:", len(filtered))

    if len(filtered) > 0:
        fig = px.scatter_mapbox(
            filtered,
            lat="latitude",
            lon="longitude",
            hover_name="Company",
            zoom=2
        )

        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")
        
    country_counts = filtered["Country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]
    fig = px.bar(
        country_counts,
        x="Country",
        y="Count",
        title="Jobs by Country"
    )
    st.plotly_chart(fig)

# ===================================================
# TASK 5
# ===================================================
elif task == "Task 5 – India vs Germany Comparison":

    filtered = df.copy()

    filtered = filtered[filtered["Country"].isin(["India", "Germany"])]
    filtered = filtered[filtered["Salary Min"] > 10]

    st.write("Filtered Rows:", len(filtered))

    if len(filtered) > 0:
        grouped = filtered.groupby(["Country", "Job Title"]).size().reset_index(name="Count")

        fig = px.bar(grouped, x="Country", y="Count", color="Job Title", barmode="stack")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")
        
    fig = px.pie(
        filtered,
        names="Country",
        title="India vs Germany Share"
    )
    st.plotly_chart(fig)

# ===================================================
# TASK 6
# ===================================================
elif task == "Task 6 – Work Type Salary Distribution":

    filtered = df.copy()

    filtered = filtered[filtered["Work Type"] == "intern"]
    filtered = filtered[filtered["Salary Min"] > 5]

    st.write("Filtered Rows:", len(filtered))

    if len(filtered) > 0:
        fig = px.box(filtered, x="Work Type", y="Salary Min")
        st.plotly_chart(fig)
    else:
        st.warning("No data available")

    fig = px.histogram(
        filtered,
        x="Salary Min",
        nbins=30,
        title="Salary Distribution"
    )

    st.plotly_chart(fig)
