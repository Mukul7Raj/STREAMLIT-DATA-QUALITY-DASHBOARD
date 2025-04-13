import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    check_missing, detect_duplicates, detect_outliers, detect_jumps,
    validate_dataframe, preprocess_data, analyze_data_distribution,
    detect_trends, check_data_consistency
)

# Page configuration
st.set_page_config(
    page_title="Financial Data Quality Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    outlier_threshold = st.slider("Outlier Detection Threshold (IQR multiplier)", 1.0, 3.0, 1.5, 0.1)
    jump_threshold = st.slider("Price Jump Threshold (%)", 0.05, 0.50, 0.10, 0.01)
    ma_window = st.slider("Moving Average Window", 5, 100, 30, 5)

# Main content
st.title("📊 Financial Time Series Data Quality Dashboard")
st.markdown("""
    This dashboard helps you analyze and validate your financial time series data.
    Upload your CSV file to get started.
""")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validate data
        is_valid, message = validate_dataframe(df)
        if not is_valid:
            st.error(message)
            st.stop()
        
        # Preprocess data
        df = preprocess_data(df)
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Data Overview", "🔍 Quality Checks", "📊 Analysis", "📥 Export"])
        
        with tab1:
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("Data Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Dataset Shape:", df.shape)
                st.write("Date Range:", df["Date"].min(), "to", df["Date"].max())
            with col2:
                st.write("Columns:", ", ".join(df.columns))
                st.write("Memory Usage:", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        with tab2:
            st.subheader("Data Quality Checks")
            
            # Missing Data
            st.write("### 🧼 Missing Data Analysis")
            missing_data = check_missing(df)
            if not missing_data.empty:
                st.warning("Missing values detected!")
                st.dataframe(missing_data)
            else:
                st.success("No missing values found!")
            
            # Duplicates
            st.write("### 🪞 Duplicate Analysis")
            duplicates = detect_duplicates(df)
            if isinstance(duplicates, str):
                st.info(duplicates)
            else:
                st.warning("Duplicate dates found!")
                st.dataframe(duplicates)
            
            # Column selection for detailed analysis
            column = st.selectbox("Select column for detailed analysis", df.select_dtypes(include=[np.number]).columns)
            
            # Outliers
            st.write("### 📊 Outlier Analysis")
            outliers = detect_outliers(df, column)
            if isinstance(outliers, str):
                st.info(outliers)
            else:
                st.warning("Outliers detected!")
                st.dataframe(outliers)
            
            # Data Consistency
            st.write("### ✅ Data Consistency Check")
            consistency = check_data_consistency(df, column)
            if "error" in consistency:
                st.error(consistency["error"])
            else:
                st.write(consistency)
        
        with tab3:
            st.subheader("Data Analysis")
            
            # Distribution Analysis
            st.write("### 📈 Distribution Analysis")
            dist_stats = analyze_data_distribution(df, column)
            if "error" in dist_stats:
                st.error(dist_stats["error"])
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{dist_stats['mean']:.2f}")
                    st.metric("Median", f"{dist_stats['median']:.2f}")
                with col2:
                    st.metric("Std Dev", f"{dist_stats['std']:.2f}")
                    st.metric("Skewness", f"{dist_stats['skewness']:.2f}")
                with col3:
                    st.metric("Min", f"{dist_stats['min']:.2f}")
                    st.metric("Max", f"{dist_stats['max']:.2f}")
            
            # Trend Analysis
            st.write("### 📈 Trend Analysis")
            trends = detect_trends(df, column, window=ma_window)
            if "error" in trends.columns:
                st.error(trends["error"].iloc[0])
            else:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=trends["Date"], y=trends[column], name="Original Data"))
                fig.add_trace(go.Scatter(x=trends["Date"], y=trends["MA"], name=f"{ma_window}-day MA"))
                fig.update_layout(title=f"{column} Price and Moving Average", xaxis_title="Date", yaxis_title="Value")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("Export Options")
            
            # Export processed data
            if st.button("Export Processed Data"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="processed_data.csv",
                    mime="text/csv"
                )
            
            # Export analysis results
            if st.button("Export Analysis Report"):
                report = f"""
                Data Quality Analysis Report
                ===========================
                
                Dataset Information:
                - Shape: {df.shape}
                - Date Range: {df["Date"].min()} to {df["Date"].max()}
                - Columns: {", ".join(df.columns)}
                
                Missing Values:
                {check_missing(df).to_string()}
                
                Distribution Statistics for {column}:
                {pd.Series(analyze_data_distribution(df, column)).to_string()}
                """
                
                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="analysis_report.txt",
                    mime="text/plain"
                )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()
