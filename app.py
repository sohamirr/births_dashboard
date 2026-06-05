import streamlit as st
import datetime
import pandas as pd

# 1. IMPORT CUSTOM DATA ENGINE & VISUALIZATION BLOCKS
from filters import load_data, db_filters, calculate_kpis
import charts

# 2. PAGE CONFIGURATION SETUP
st.set_page_config(page_title="US Births Command Center", layout="wide")

# PREMIUM SPIDER-MAN UI DESIGN ENGINE INJECTION
st.markdown("""
    <style>
    /* Global Page Context & Clean Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #08090c !important;
        color: #f1f3f9 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Elegant Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0c0e14 !important;
        border-right: 1px solid rgba(193, 18, 31, 0.25) !important;
    }
    
    /* Smooth Transition Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container, .stMarkdown, .stContainer {
        animation: fadeInUp 0.4s ease-out forwards;
    }
    
    /* Hero Banner Custom Card */
    .hero-banner {
        background: linear-gradient(135deg, #001f3f 0%, #050b14 100%);
        border-left: 5px solid #C1121F;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Premium KPI Card Restyling */
    div[data-testid="stMetricContent"] {
        background-color: #0c0e14 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 3px solid #003049 !important; /* Elegant Navy Trim */
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    /* Soft Red Accent on Metric Hover */
    div[data-testid="stMetricContent"]:hover {
        transform: translateY(-4px);
        border-top: 3px solid #C1121F !important; /* Swaps to Spidey Red on hover */
        box-shadow: 0 8px 24px rgba(193, 18, 31, 0.15) !important;
    }
    
    /* Metric Labels Typography */
    div[data-testid="stMetricLabel"] > div {
        color: #8d99ae !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Chart Display Container Cards */
    .chart-card {
        background-color: #0c0e14 !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 20px;
    }
    
    /* Clean Forms & Filters Inputs */
    .stMultiSelect, .stSlider, .stDateInput {
        margin-bottom: 15px !important;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. HERO BANNER HEADER
st.markdown("""
    <div class="hero-banner">
        <p style="color: #C1121F; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 5px; font-size: 0.85rem;">
            ✦ Macro-Trend Demographic Analysis Engine ✦
        </p>
        <h1 style="color: #ffffff; margin: 0; font-weight: 700; font-size: 2.5rem;">US Births Tracker & Explorer</h1>
        <p style="color: #8d99ae; margin-top: 8px; font-size: 1rem; max-width: 800px;">
            Analyzing vital statistics records spanning a decade of CDC/NCHS data. Use the control panel on the left to seamlessly filter across chronological sequences, seasonal variances, and volumetric boundaries.
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. PERFORMANCE OPTIMIZED DATA LOADING PIPELINE
@st.cache_data
def get_cached_data():
    return load_data()

try:
    df_base = get_cached_data()
except Exception as e:
    st.error(f"❌ Could not load dataset file. Error: {e}")
    st.stop()

# 5. SIDEBAR FILTERING CONTROLS USER INTERFACE
st.sidebar.markdown("<h2 style='color:#C1121F; font-size: 1.3rem; font-weight:700; margin-bottom:20px;'>CONTROL PANEL</h2>", unsafe_allow_html=True)

available_years = sorted(df_base['year'].unique())
selected_yrs = st.sidebar.multiselect("Year Selection", options=available_years, default=[])

month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
selected_months = st.sidebar.multiselect("Month Filter", options=month_order, default=[])

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_days = st.sidebar.multiselect("Weekday Filter", options=day_order, default=[])

min_b, max_b = int(df_base['births'].min()), int(df_base['births'].max())
birth_range = st.sidebar.slider("Daily Volumetric Scope", min_value=min_b, max_value=max_b, value=(min_b, max_b))

min_date = df_base['date'].min().to_pydatetime()
max_date = df_base['date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Precise Date Boundary", value=(min_date, max_date), min_value=min_date, max_value=max_date)

search_query = st.sidebar.text_input("🔍 Keyword Pattern Search")

if len(date_range) != 2:
    st.warning("Please select a complete start and end date range.")
    st.stop()

# 6. TRIGGER BACKEND FILTER SYNC ENGINE
df_filtered = db_filters(df_base, selected_yrs, selected_days, selected_months, birth_range, date_range, search_query)

# 7. DISPLAY KPI SUMMARY METRIC CARDS SECTION
kpis = calculate_kpis(df_filtered)

st.markdown("<h3 style='color:#FFFFFF; font-size:1.2rem; font-weight:600; margin-bottom:15px;'>VITAL STATISTICS SUMMARY</h3>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Observed Days", f"{kpis['total_records']:,}")
col2.metric("Aggregate Births", f"{kpis['total_births']:,}")
col3.metric("Daily Average", f"{kpis['avg_births']:,}")
col4.metric("Single-Day Peak", f"{kpis['max_births']:,}")
col5.metric("Single-Day Valley", f"{kpis['min_births']:,}")
st.markdown("<br>", unsafe_allow_html=True)

# 8. DASHBOARD RENDERING PIPELINE (ORGANIZED INTO INDENTED TABS)
if df_filtered.empty:
    st.error("⚠️ No records match the selected filter configurations. Please broaden your scope constraints.")
else:
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.2rem; font-weight:600; margin-bottom:25px;'>📈 GRAPHIC SUITE PORTFOLIO</h3>", unsafe_allow_html=True)
    
    # Structural clean grid tabs allocation
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Macro Trends", "📅 Calendar & Week Analysis", "🎻 Distributions", "🌟 Advanced Matrix"])
    
    with tab1:
        st.markdown("<p style='color:#8d99ae; margin-bottom: 20px;'>Long-term volumetric trends across months and years.</p>", unsafe_allow_html=True)
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_line_chart(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
        with row1_col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_area_chart(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(charts.plot_bar_chart(df_filtered))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("<p style='color:#8d99ae; margin-bottom: 20px;'>Analysis of how delivery rates change based on the days of the week and seasons.</p>", unsafe_allow_html=True)
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_box_plot(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
        with row2_col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_pie_chart(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("<p style='color:#8d99ae; margin-bottom: 20px;'>Density spreads pointing out statistical frequencies and outlier spikes.</p>", unsafe_allow_html=True)
        row3_col1, row3_col2 = st.columns(2)
        with row3_col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_histogram(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
        with row3_col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_violin_plot(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(charts.plot_scatter_plot(df_filtered))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("<p style='color:#8d99ae; margin-bottom: 20px;'>Advanced relational coordinate maps and structural source row verification.</p>", unsafe_allow_html=True)
        row4_col1, row4_col2 = st.columns(2)
        with row4_col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_heatmap(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
        with row4_col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.pyplot(charts.plot_count_plot(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<h4 style='color:#C1121F; font-size:1.1rem; font-weight:600; margin-top:10px; margin-bottom:15px;'>🌟 BONUS: DATE MATRIX GRID</h4>", unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(charts.plot_calendar_heatmap(df_filtered))
        st.markdown('</div>', unsafe_allow_html=True)