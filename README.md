## 🔢 DataBuddy - A Data Profiling App
**Automated Data Auditing & Cleaning Roadmap for Analysts**

DataProfiler Pro is a high-performance Streamlit application designed to bridge the gap between raw data and actionable insights. It automates the tedious process of initial data exploration, sanitization, and effort estimation.

### 🚀 Key Features
- **Smart Sanitization:** Automatically filters out noise by identifying and removing ID-related columns across all data types.
- **Performance Optimized:** Implements Streamlit caching and dynamic sampling to handle datasets up to 200MB with near-instant interaction.
- **Health & Effort Metrics:** A custom heuristic engine that calculates a "Data Health Score" and estimates the manual cleaning time required (in minutes/days).
- **Format Auditing:** Regex-based pattern matching to identify inconsistent date and string formats.
- **Interactive Visuals:** Dynamic correlation heatmaps and statistical summaries to spot trends at a glance.

### 🛠️ Technical Stack
- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly (WebGL enabled)
- **Reporting:** FPDF (Automated PDF Report Generation)

### 🔬 Methodology
The tool uses a weighted heuristic to estimate cleaning effort:
`Total Minutes = 15m (Base) + (Null% * 3) + (Duplicates * 1)`
This provides a "Business ROI" perspective on data quality, helping analysts advocate for better data entry validation.
