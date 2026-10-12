import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Indian Tech Job Market Tracker", layout="wide")

st.title("📊 Freshers Tech Market Analytics Dashboard")
st.markdown("Evaluating demand for Software Engineer & Data roles across India.")
st.caption("Data: simulated sample data (randomly generated for demonstration)")


@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect("tech_jobs.db")
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    df["date_added"] = pd.to_datetime(df["date_added"])
    return df


try:
    df = load_data()
    if df.empty:
        raise ValueError("empty")
except Exception:
    st.error("Database is empty or missing! Run `python scraper.py` first.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
locations = st.sidebar.multiselect("Location", sorted(df["location"].unique()),
                                   default=sorted(df["location"].unique()))
roles = st.sidebar.multiselect("Job Role", sorted(df["title"].unique()),
                               default=sorted(df["title"].unique()))
df = df[df["location"].isin(locations) & df["title"].isin(roles)]

if df.empty:
    st.warning("No jobs match the selected filters.")
    st.stop()

# --- KPIs ---
c1, c2, c3 = st.columns(3)
c1.metric("Total Jobs Indexed", len(df))
c2.metric("Companies Hiring", df["company"].nunique())
c3.metric("Top Location", df["location"].value_counts().idxmax())

st.write("---")

# --- ROW 1: roles + locations ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top Job Roles in Demand")
    role_counts = df["title"].value_counts().reset_index()
    role_counts.columns = ["Job Title", "Openings"]
    fig1 = px.bar(role_counts, x="Job Title", y="Openings",
                  color="Openings", color_continuous_scale="Blues")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📍 Hiring by Location")
    loc_counts = df["location"].value_counts().reset_index()
    loc_counts.columns = ["Location", "Count"]
    fig2 = px.pie(loc_counts, values="Count", names="Location", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# --- ROW 2: skills + trend ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("🧠 Most In-Demand Skills")
    skills = df["skills"].str.split(", ").explode()
    skills = skills[skills != "Not specified"].value_counts().reset_index()
    skills.columns = ["Skill", "Mentions"]
    fig3 = px.bar(skills.head(10), x="Mentions", y="Skill", orientation="h",
                  color="Mentions", color_continuous_scale="Teal")
    fig3.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📈 Postings Over Time")
    trend = df.groupby("date_added").size().reset_index(name="Postings")
    fig4 = px.line(trend, x="date_added", y="Postings", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

# --- RAW DATA ---
st.write("---")
st.subheader("🔍 Explore Raw Listings")
st.dataframe(df[["title", "company", "skills", "location", "date_added"]]
             .sort_values("date_added", ascending=False),
             use_container_width=True)