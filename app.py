import streamlit as st
import pandas as pd
from utils import check_missing, detect_duplicates, detect_outliers, detect_jumps

st.set_page_config(page_title="Financial Data Checker", layout="wide")

st.title("📊 Financial Time Series Data Quality Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert 'Date' column to datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
    else:
        st.error("Your CSV must include a 'Date' column.")

    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("🧼 1. Missing Data Check")
    st.write(check_missing(df))

    st.subheader("🪞 2. Duplicate Dates")
    st.write(detect_duplicates(df))

    st.subheader("📈 3. Outliers")
    column = st.selectbox("Choose column for outlier detection", df.columns)
    st.write(detect_outliers(df, column))

    st.subheader("⚡ 4. Sudden Price Jumps")
    st.write(detect_jumps(df, column))

    st.subheader("📉 Price Chart")
    st.line_chart(df.set_index("Date")[column])
