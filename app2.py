import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")
st.title("📊 Credit Risk Analysis Dashboard")

# -------------------- MONGO CONNECTION --------------------
connection_url = 'mongodb+srv://anakalasurya7_db_user:iQZTULVdCi1AyBZu@cluster0.i1aaffi.mongodb.net/?appName=Cluster0'

client = MongoClient(connection_url)
db = client["Credit_Risk-2"]
collection = db["Credit_risk_data-2"]

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    data = list(collection.find())
    df = pd.DataFrame(data)
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)
    return df

df = load_data()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("🔍 Filters")

state_filter = st.sidebar.multiselect("Select State", df["state"].unique())
loan_type_filter = st.sidebar.multiselect("Loan Type", df["loan_type"].unique())

filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["state"].isin(state_filter)]

if loan_type_filter:
    filtered_df = filtered_df[filtered_df["loan_type"].isin(loan_type_filter)]

# -------------------- KPI METRICS --------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_loans = len(filtered_df)
avg_income = int(filtered_df["income"].mean())
default_rate = round(filtered_df["default"].mean() * 100, 2)
avg_credit_score = int(filtered_df["credit_score"].mean())

col1.metric("Total Loans", total_loans)
col2.metric("Avg Income", f"₹{avg_income}")
col3.metric("Default Rate", f"{default_rate}%")
col4.metric("Avg Credit Score", avg_credit_score)

# -------------------- CHARTS --------------------

# Loan Status
st.subheader("📉 Default Distribution")
fig1 = px.pie(filtered_df, names="default", title="Default vs Non-Default")
st.plotly_chart(fig1, use_container_width=True)

# Credit Score Distribution
st.subheader("📊 Credit Score Distribution")
fig2 = px.histogram(filtered_df, x="credit_score", nbins=30)
st.plotly_chart(fig2, use_container_width=True)

# Income vs Loan Amount
st.subheader("💰 Income vs Loan Amount")
fig3 = px.scatter(
    filtered_df,
    x="income",
    y="loan_amount",
    color="default",
    size="credit_score",
    hover_data=["cust_id"]
)
st.plotly_chart(fig3, use_container_width=True)

# Loan Purpose Analysis
st.subheader("📌 Loan Purpose Analysis")
fig4 = px.bar(
    filtered_df,
    x="loan_purpose",
    color="default",
    title="Loan Purpose vs Default"
)
st.plotly_chart(fig4, use_container_width=True)

# Delinquency Analysis
st.subheader("⚠️ Delinquency vs Default")
fig5 = px.box(
    filtered_df,
    x="default",
    y="delinquent_months"
)
st.plotly_chart(fig5, use_container_width=True)

# -------------------- ADVANCED INSIGHT --------------------
st.subheader("📈 Risk Analysis")

fig6 = px.scatter(
    filtered_df,
    x="loan_to_income",
    y="credit_score",
    color="default",
    title="Risk Segmentation"
)
st.plotly_chart(fig6, use_container_width=True)

# -------------------- DATA TABLE --------------------
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)