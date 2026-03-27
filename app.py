import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import os
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIGURE
# ---------------------------------------------------
st.set_page_config(page_title="Global Internship Dashboard", layout="wide")
st.title("🌍 Global Internship Dashboard")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset.csv")
        st.sidebar.success("Loaded GitHub dataset")
    except:
        file_id = "1gvHGeckF5hqT3LFpvGLT3HaB7penAxUA"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = "data.csv"

        if not os.path.exists(output):
            with st.spinner("Downloading dataset..."):
                gdown.download(url, output, quiet=False)

        df = pd.read_csv(output, nrows=50000)
        st.sidebar.warning("Loaded Drive dataset")

    # CLEANING
    df.columns = df.columns.str.strip()

    df.rename(columns={
        "Qualifications": "Qualification",
        "location": "Location"
    }, inplace=True)

    df["Salary Min"] = (
        df["Salary Range"]
        .str.replace(r"[\$,K]", "", regex=True)
        .str.split("-")
        .str[0]
    )
    df["Salary Min"] = pd.to_numeric(df["Salary Min"], errors="coerce")

    df["Experience Num"] = (
        df["Experience"].str.extract(r"(\d+)")
    )
    df["Experience Num"] = pd.to_numeric(df["Experience Num"], errors="coerce")

    df["Company Size"] = pd.to_numeric(df["Company Size"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df["Job Posting Date"] = pd.to_datetime(
        df["Job Posting Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    df["Work Type"] = df["Work Type"].str.lower()
    df["Preference"] = df["Preference"].str.capitalize()

    return df


df = load_data()
st.sidebar.write("Total Rows:", len(df))

# ---------------------------------------------------
# SIDEBAR (TASK SELECTOR FIRST)
# ---------------------------------------------------
st.sidebar.title("📊 Dashboard Controls")

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
# OPTIONAL FILTERS
# ---------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("Filters")

work_type_filter = st.sidebar.selectbox(
    "Work Type",
    ["All"] + sorted(df["Work Type"].dropna().unique().tolist())
)

country_filter = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["Country"].dropna().unique().tolist())
)

job_filter = st.sidebar.selectbox(
    "Job Title",
    ["All"] + sorted(df["Job Title"].dropna().unique().tolist())
)

# ---------------------------------------------------
# APPLY FILTER FUNCTION
# ---------------------------------------------------
def apply_filters(data):
    filtered = data.copy()

    if work_type_filter != "All":
        filtered = filtered[filtered["Work Type"] == work_type_filter]

    if country_filter != "All":
        filtered = filtered[filtered["Country"] == country_filter]

    if job_filter != "All":
        filtered = filtered[filtered["Job Title"] == job_filter]

    return filtered

# ===================================================
# TASK 1
# ===================================================
if task == "Task 1 – Preference vs Work Type":

    filtered = apply_filters(df)

    filtered = filtered[filtered["Work Type"] == "intern"]
    filtered = filtered[filtered["Salary Min"] > 5]

    st.write("Filtered Rows:", len(filtered))

    grouped = filtered.groupby("Preference").size().reset_index(name="Count")
    fig1 = px.bar(grouped, x="Preference", y="Count", text="Count")
    st.plotly_chart(fig1, key="t1_bar")

    fig2 = px.pie(df, names="Work Type")
    st.plotly_chart(fig2, key="t1_pie")

    fig3 = px.bar(df["Country"].value_counts().head(10).reset_index(),
                  x="Country", y="count")
    st.plotly_chart(fig3, key="t1_country")

# ===================================================
# TASK 2
# ===================================================
elif task == "Task 2 – Company Size vs Company Name":

    filtered = apply_filters(df)
    filtered = filtered[filtered["Company Size"] < 50000]

    st.write("Filtered Rows:", len(filtered))

    fig = px.scatter(filtered, x="Company Size", y="Company")
    st.plotly_chart(fig, key="t2_scatter")

    top = (
        filtered.groupby("Company")["Company Size"]
        .mean().sort_values(ascending=False).head(10).reset_index()
    )

    fig2 = px.bar(top, x="Company", y="Company Size")
    st.plotly_chart(fig2, key="t2_bar")

# ===================================================
# TASK 3
# ===================================================
elif task == "Task 3 – Top 10 Companies":

    filtered = apply_filters(df)

    top = filtered["Company"].value_counts().head(10).reset_index()
    top.columns = ["Company", "Count"]

    fig1 = px.treemap(top, path=["Company"], values="Count")
    st.plotly_chart(fig1, key="t3_tree")

    fig2 = px.pie(top, names="Company", values="Count")
    st.plotly_chart(fig2, key="t3_pie")

# ===================================================
# TASK 4
# ===================================================
elif task == "Task 4 – Qualification Map":

    filtered = apply_filters(df)
    filtered = filtered.dropna(subset=["latitude", "longitude"])

    fig = px.scatter_mapbox(
        filtered,
        lat="latitude",
        lon="longitude",
        hover_name="Company",
        zoom=2
    )

    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, key="t4_map")

# ===================================================
# TASK 5
# ===================================================
elif task == "Task 5 – India vs Germany Comparison":

    filtered = apply_filters(df)
    filtered = filtered[filtered["Country"].isin(["India", "Germany"])]

    grouped = filtered.groupby(["Country", "Job Title"]).size().reset_index(name="Count")

    fig = px.bar(grouped, x="Country", y="Count", color="Job Title", barmode="stack")
    st.plotly_chart(fig, key="t5_bar")

    fig2 = px.pie(filtered, names="Country")
    st.plotly_chart(fig2, key="t5_pie")

# ===================================================
# TASK 6
# ===================================================
elif task == "Task 6 – Work Type Salary Distribution":

    filtered = apply_filters(df)
    filtered = filtered[filtered["Work Type"] == "intern"]

    fig = px.box(filtered, x="Work Type", y="Salary Min")
    st.plotly_chart(fig, key="t6_box")

    fig2 = px.histogram(filtered, x="Salary Min")
    st.plotly_chart(fig2, key="t6_hist")
