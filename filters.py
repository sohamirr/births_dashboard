import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns            
import streamlit as st

def load_data(f_path="US_births_1994-2003_CDC_NCHS.csv"):
    df = pd.read_csv(f_path) 
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y') 
    df['day_of_year'] = df['date'].dt.dayofyear 

    day_mapping = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 
        5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    month_mapping = {
        1: "January", 2: "February", 3: "March", 4: "April", 
        5: "May", 6: "June", 7: "July", 8: "August", 
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    
    df['day_name'] = df['day_of_week'].map(day_mapping)
    df['month_name'] = df['month'].map(month_mapping)

    # Defined helper function
    def getseason(x):
        if x in [12, 1, 2]: return 'Winter'
        if x in [6, 7, 8]: return 'Summer'
        if x in [3, 4, 5]: return 'Spring'
        else: return 'Autumn'

    # FIXED: Added this line so the season column actually gets built!
    df['season'] = df['month'].apply(getseason)

    return df

def db_filters(df, selected_yrs, selected_days, selected_months, birth_range, date_range, query=None):
    df_filtered = df.copy()
    
    if selected_yrs:
        df_filtered = df_filtered[df_filtered['year'].isin(selected_yrs)]
    
    # FIXED: Sourced from text column 'month_name' instead of numerical 'month'
    if selected_months:
        df_filtered = df_filtered[df_filtered['month_name'].isin(selected_months)]

    # FIXED: Sourced from 'day_name' to match what you declared in load_data
    if selected_days:
        df_filtered = df_filtered[df_filtered['day_name'].isin(selected_days)]

    # FIXED: Fixed the broken structural indentations here
    df_filtered = df_filtered[
        (df_filtered['births'] >= birth_range[0]) & 
        (df_filtered['births'] <= birth_range[1])
    ]

    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered['date'] >= pd.to_datetime(start_date)) & 
        (df_filtered['date'] <= pd.to_datetime(end_date))
    ]
    
    # Text search implementation wrapper
    if query:
        q = str(query).strip().lower()
        mask = (
            df_filtered['day_name'].str.lower().str.contains(q) |
            df_filtered['month_name'].str.lower().str.contains(q) |
            df_filtered['season'].str.lower().str.contains(q)
        )
        df_filtered = df_filtered[mask]
    
    return df_filtered

def calculate_kpis(df_filtered): 
    # FIXED: Changed 'filtered_df' variables to match your function input 'df_filtered'
    if df_filtered.empty:
        return {"total_records": 0, "total_births": 0, "avg_births": 0, "max_births": 0, "min_births": 0}
        
    return {
        "total_records": len(df_filtered),
        "total_births": int(df_filtered['births'].sum()),
        "avg_births": round(df_filtered['births'].mean(), 1),
        "max_births": int(df_filtered['births'].max()),
        "min_births": int(df_filtered['births'].min())
    }