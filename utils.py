import pandas as pd
import numpy as np

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
