# Data-Quality-Dashboard-for-Financial-Time-Series

# Financial Data Quality Dashboard

A Streamlit application for analyzing financial time series data quality.

## Features
- Missing data detection
- Duplicate date identification
- Outlier detection using IQR method
- Price jump detection
- Interactive price charts

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python -m streamlit run app.py
```

## Data Format
Your CSV file should contain:
- A 'Date' column (will be converted to datetime)
- At least one numeric column for analysis

## Requirements
- Python 3.8+
- Streamlit
- Pandas
- NumPy
