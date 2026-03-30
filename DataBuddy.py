import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
import re

# Page Configuration
st.set_page_config(page_title="DataBuddy", layout="wide", page_icon="🔢")

# --- 1. Optimized Data Engine (Caching) ---
@st.cache_data(show_spinner="Analyzing large dataset...")
def load_and_sanitize_data(file):
    # Load File
    if file.name.endswith('.csv'):
        raw_df = pd.read_csv(file)
    else:
        raw_df = pd.read_excel(file)
    
    # Global Filter: Remove any column containing 'id' (case-insensitive)
    cols_to_keep = [col for col in raw_df.columns if 'id' not in col.lower()]
    removed = [col for col in raw_df.columns if 'id' in col.lower()]
    
    return raw_df[cols_to_keep], removed

# --- Helper: Identify Formats ---
def get_format(value):
    if pd.isnull(value): return "Null"
    val_str = str(value).strip()
    if re.match(r'\d{2}/\d{2}/\d{4}', val_str): return "DD/MM/YYYY"
    if re.match(r'\d{4}-\d{2}-\d{2}', val_str): return "YYYY-MM-DD"
    if re.match(r'\d{2} [A-Za-z]+', val_str): return "DD Month"
    if val_str.replace('.','',1).isdigit(): return "Numeric String"
    return "Text/Mixed"

# --- Main UI ---
st.title("🔢 DataBuddy - A Data Profiling App")
st.markdown("Automated Data Auditing & Cleaning Roadmap for Analysts")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])

if uploaded_file:
    # Use cached loader to handle large files smoothly
    df, removed_cols = load_and_sanitize_data(uploaded_file)
    
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(exclude=['number']).columns

    # 2. Performance-Aware Calculations
    total_nulls = df.isnull().sum().sum()
    null_pct = (total_nulls / (df.size if df.size > 0 else 1)) * 100
    health_score = max(0, int(100 - null_pct))
    
    # Cleaning Time Heuristic
    total_mins = 15 + (null_pct * 3) + (df.duplicated().sum() * 1)
    time_str = f"{int(total_mins)} Mins" if total_mins < 100 else f"{round(total_mins/60, 1)} Days"

    # --- Section 1: Health Status ---
    st.header("1. Data Health Status")
    k1, k2, k3 = st.columns(3)
    k1.metric("Health Score", f"{health_score}%")
    t_status = "✅ Low Effort" if total_mins < 45 else "⚠️ Moderate" if total_mins < 120 else "🚨 High Effort"
    k2.metric("Cleaning Workload", time_str, delta=t_status)
    k3.metric("Total Records", f"{df.shape[0]:,}")

    if removed_cols:
        st.info(f"🛡️ **Sanitization Active:** {len(removed_cols)} ID columns filtered out.")

    # --- Section 2: Variable Correlation Heatmap ---
    st.header("2. Variable Correlation Heatmap")
    if len(num_cols) >= 2:
        top_n = num_cols[:10]
        corr_matrix = df[top_n].corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient numerical data for a heatmap.")

    # --- Section 3: Detailed Data Profile ---
    st.header("3. Detailed Data Profile")
    t1, t2 = st.tabs(["🔢 Numerical Details", "🔠 Categorical Audit"])
    
    with t1:
        if not num_cols.empty:
            st.dataframe(df[num_cols].describe().T, use_container_width=True)
            
    with t2:
        if not cat_cols.empty:
            cat_data = []
            for c in cat_cols:
                # FIX: Drop nulls first to prevent 'sample size > population' error
                clean_col = df[c].dropna()
                pop_size = len(clean_col)
                
                if pop_size > 0:
                    current_sample = min(1000, pop_size)
                    formats = ", ".join(list(clean_col.sample(current_sample).apply(get_format).unique())[:3])
                else:
                    formats = "Empty/All Null"

                cat_data.append({
                    "Column": c, "Formats": formats, "Unique": df[c].nunique(), 
                    "Duplicates": df[c].duplicated().sum(), "Nulls": df[c].isnull().sum()
                })
            st.table(pd.DataFrame(cat_data))

    # --- Section 4: Methodology ---
    with st.expander("🔬 Methodology"):
        st.write(f"**Health Score:** Calculated as [1-(null cells/total cells)*100].")
        st.write(f"**Cleaning Estimate:** Base 15m + {int(null_pct*3)}m for missing data + {df.duplicated().sum()}m for duplicates.")

    # --- Section 5: Recommended Projects ---
    st.header("💡 Recommendations")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.subheader("Analysis")
        top_cat = cat_cols[0] if not cat_cols.empty else "Category"
        top_num = num_cols[0] if not num_cols.empty else "Metric"
        st.write(f"**Segmented Performance:** Analyze how `{top_num}` varies across `{top_cat}` groups to find hidden outliers.")
    with p2:
        st.subheader("Engineering")
        st.write("**Auto-Clean Pipeline:** Build a robust Python script to standardize the inconsistent formats identified in the audit.")
    with p3:
        st.subheader("Strategy")
        st.write(f"**Business Case:** Use the **{time_str}** cleaning estimate to advocate for better automated validation at the data source.")

    # --- 6. Footer / Branding ---
    st.divider()
    st.markdown(
        f"""
        <div style="text-align: center; color: grey; padding: 10px;">
            <p>Built with ❤️ by <strong>Ruchita</strong> | March 2026</p>
            <p style="font-size: 0.8em;">DataProfiler Pro v1.4 | Performance Optimized</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Ready for upload. Automated ID-filtering and performance caching enabled.")