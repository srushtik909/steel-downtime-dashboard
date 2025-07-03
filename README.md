# Steel Plant Production Downtime Analysis & Optimization

## Project Overview
This project analyzes simulated downtime events in a steel manufacturing plant to uncover inefficiencies and recommend actionable improvements. Using Python, data analytics, and interactive dashboards, it provides insights into downtime causes, trends, and their impact on productivity.

## Features
- Simulated dataset generation for downtime events
- Interactive dashboard (Streamlit + Plotly) with:
  - Filters for Department, Month, Machine, and Shift
  - Visualizations: downtime by machine, shift, reason, and department
  - Time-series analysis
  - Downtime duration distribution (histogram)
  - Modern UI with gradient background (no green), light blur, and all fonts/axes in black for maximum readability

## Dataset Description
- **Timestamp**: Date and time of downtime event
- **Machine_ID**: Unique machine identifier
- **Shift**: Shift during which downtime occurred
- **Downtime_Minutes**: Duration of downtime
- **Downtime_Reason**: Reason for stoppage (e.g., Maintenance)
- **Department**: Functional area (e.g., Melting, Rolling)
- **Operator_Name**: Operator responsible during the event
- **Production_Loss**: Estimated loss in output (tons/₹)

## Setup & Execution Steps

### 1. Clone or Download the Repository

### 2. Install Required Python Packages
Open a terminal in the project directory and run:
```bash
pip install pandas numpy Faker streamlit plotly statsmodels
```

### 3. Generate the Simulated Dataset
Run the following command to create `steel_downtime_data.csv`:
```bash
python generate_steel_downtime_data.py
```

### 4. Launch the Interactive Dashboard
Start the Streamlit app with:
```bash
streamlit run steel_downtime_dashboard.py
```

### 5. Explore the Dashboard
- Use the sidebar filters to analyze downtime by department, machine, shift, and month.
- View KPIs, bar charts, pie charts, time-series, and the downtime duration histogram.
- All chart and axis labels are in black for maximum visibility.

## Notes
- All data is simulated for demonstration purposes.
- The dashboard UI uses a gradient background (orange/yellow/pink), light blur, and black font for readability.

## Requirements
- Python 3.8+
- The above listed Python packages
