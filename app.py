import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pytz

def is_time_valid(start, end):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return start <= now.hour < end

# ---------------------------------------------------
# PAGE CONFIGURE
# ---------------------------------------------------
st.set_page_config(page_title="Global Internship Dashboard", layout="wide")
st.title("Global Internship Dashboard")

# ---------------------------------------------------
# LOAD DATA
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
                df = pd.read_csv("https://drive.google.com/uc?id=1gvHGeckF5hqT3LFpvGLT3HaB7penAxUA")
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
    # Apply strict rules
    filtered = df[
        (df["Work Type"] == "intern") &
        (df["latitude"] < 10) &
        (~df["Country"].str.startswith(('A', 'B', 'C', 'D'), na=False)) &
        (df["Salary Min"] > 9) & # Assuming units are in thousands
        (df["Experience Num"] % 2 == 0) &
        (df["Job Posting Date"].dt.month % 2 != 0)
    ]
    
    # Requirement: Single word title, < 10 chars
    filtered = filtered[filtered["Job Title"].str.split().str.len() == 1]
    filtered = filtered[filtered["Job Title"].str.len() < 10]

    # Requirement: Sort Descending
    grouped = filtered.groupby("Preference").size().reset_index(name="Count")
    grouped = grouped.sort_values(by="Count", ascending=False)
    
    st.write(f"Filtered Rows: {len(filtered)}")
    fig1 = px.bar(grouped, x="Preference", y="Count", text="Count")
    st.plotly_chart(fig1)

    fig2 = px.pie(df, names="Work Type")
    st.plotly_chart(fig2, key="t1_pie")

    fig3 = px.bar(df["Country"].value_counts().head(10).reset_index(),
                  x="Country", y="count")
    st.plotly_chart(fig3, key="t1_country")

    if is_time_valid(15, 17):
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
    else:
        st.warning("Visible only between 3 PM and 5 PM IST")

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

    if is_time_valid(15, 17):
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        
    else:
        st.warning("Visible only between 3 PM and 5 PM IST")

# ===================================================
# TASK 3
# ===================================================
elif task == "Task 3 – Top 10 Companies":
    # Complex Filter: Exclude Asia and countries starting with 'C'
    # Note: You'll need a list of Asian countries or a 'Continent' column
    filtered = df[
        (df["Job Title"] == "Data Scientist") &
        (df["latitude"] < 10) &
        (~df["Country"].str.startswith('C', na=False)) &
        (df["Qualification"] == "B.Tech") &
        (df["Company Size"] >= 10000)
    ]
    
    top10 = filtered["Company"].value_counts().head(10).reset_index()
    top10.columns = ["Company", "Count"]

    fig = px.treemap(top10, path=["Company"], values="Count")
    st.plotly_chart(fig)

    fig2 = px.pie(top10 , names="Company", values="Count")
    st.plotly_chart(fig2, key="t3_pie")

    if is_time_valid(15, 17):
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        
    else:
        st.warning("Visible only between 3 PM and 5 PM IST")

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

    if is_time_valid(15, 18):
        st.plotly_chart(fig)
    else:
        st.warning("Visible only between 3 PM and 6 PM IST")

# ===================================================
# TASK 5
# ===================================================
# ===================================================
# TASK 5 – India vs Germany Comparison
# ===================================================
elif task == "Task 5 – India vs Germany Comparison":
    # 1. Start with the "Strict" list
    allowed_titles = ["Data Scientist", "Art Teacher", "Aerospace Engineer"]
    
    strict_filtered = df[
        (df["Country"].isin(["India", "Germany"])) &
        (df["Qualification"] == "B.Tech") &
        (df["Job Title"].isin(allowed_titles))
    ]

    # Check if we have data. If not, widen the search slightly to show the chart
    if len(strict_filtered) == 0:
        st.warning("⚠️ No data matches the strict 'B.Tech + Specific Title' criteria. Showing all India vs Germany postings for visualization.")
        display_df = df[df["Country"].isin(["India", "Germany"])]
    else:
        display_df = strict_filtered

    # Requirement: India in Orange, Germany in Green
    # We use 'color' on Country to ensure the specific mapping works
    fig = px.bar(
        display_df.groupby(["Country", "Job Title"]).size().reset_index(name="Count"),
        x="Country", 
        y="Count", 
        color="Country", 
        barmode="stack",
        color_discrete_map={"India": "orange", "Germany": "green"},
        title="India (Orange) vs Germany (Green) Comparison"
    )
    st.plotly_chart(fig, key="t5_fixed")

    if is_time_valid(15, 17):
        st.plotly_chart(fig)
        
    else:
        st.warning("Visible only between 3 PM and 5 PM IST")


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

    if is_time_valid(15, 17):
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        
    else:
        st.warning("Visible only between 3 PM and 5 PM IST")
