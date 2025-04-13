import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

def check_missing(df):
    """Check for missing values in the dataframe."""
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    result = pd.DataFrame({
        'Missing Values': missing_data,
        'Percentage (%)': missing_percentage.round(2)
    })
    return result[result['Missing Values'] > 0]

def detect_duplicates(df):
    """Detect duplicate dates in the dataframe."""
    if "Date" not in df.columns:
        return "No 'Date' column found in the dataframe"
    
    duplicates = df[df.duplicated(subset=['Date'], keep=False)]
    if duplicates.empty:
        return "No duplicate dates found"
    else:
        return duplicates.sort_values('Date')

def detect_outliers(df, column):
    """Detect outliers using the IQR method."""
    if column not in df.columns:
        return f"Column '{column}' not found in dataframe"
    
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    if outliers.empty:
        return f"No outliers found in column '{column}'"
    else:
        return outliers

def detect_jumps(df, column, threshold=0.1):
    """Detect sudden price jumps in the data."""
    if column not in df.columns:
        return f"Column '{column}' not found in dataframe"
    
    # Calculate percentage change
    df['pct_change'] = df[column].pct_change()
    
    # Find significant jumps (both positive and negative)
    jumps = df[abs(df['pct_change']) > threshold]
    
    if jumps.empty:
        return f"No significant price jumps detected in column '{column}' (threshold: {threshold*100}%)"
    else:
        return jumps[['Date', column, 'pct_change']].sort_values('Date')

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate the input dataframe structure and content."""
    if df.empty:
        return False, "The uploaded file is empty"
    
    if "Date" not in df.columns:
        return False, "The file must contain a 'Date' column"
    
    try:
        pd.to_datetime(df["Date"])
    except:
        return False, "The 'Date' column contains invalid date formats"
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) == 0:
        return False, "The file must contain at least one numeric column"
    
    return True, "Data validation successful"

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the dataframe for analysis."""
    df = df.copy()
    
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by date
    df = df.sort_values("Date")
    
    # Remove any duplicate indices
    df = df.reset_index(drop=True)
    
    return df

def analyze_data_distribution(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Analyze the distribution of data in a column."""
    if column not in df.columns:
        return {"error": f"Column '{column}' not found in dataframe"}
    
    stats = {
        "mean": df[column].mean(),
        "median": df[column].median(),
        "std": df[column].std(),
        "min": df[column].min(),
        "max": df[column].max(),
        "skewness": df[column].skew(),
        "kurtosis": df[column].kurtosis()
    }
    
    return stats

def detect_trends(df: pd.DataFrame, column: str, window: int = 30) -> pd.DataFrame:
    """Detect trends in the data using moving averages."""
    if column not in df.columns:
        return pd.DataFrame({"error": [f"Column '{column}' not found in dataframe"]})
    
    df = df.copy()
    df['MA'] = df[column].rolling(window=window).mean()
    df['MA_std'] = df[column].rolling(window=window).std()
    
    # Calculate trend direction
    df['Trend'] = np.where(df['MA'] > df['MA'].shift(1), 'Upward', 'Downward')
    
    return df[['Date', column, 'MA', 'MA_std', 'Trend']].dropna()

def check_data_consistency(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Check for data consistency issues."""
    if column not in df.columns:
        return {"error": f"Column '{column}' not found in dataframe"}
    
    issues = {
        "zero_values": (df[column] == 0).sum(),
        "negative_values": (df[column] < 0).sum(),
        "constant_values": (df[column].nunique() == 1),
        "gaps": df[column].isnull().sum()
    }
    
    return issues
