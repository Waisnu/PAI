#!/usr/bin/env python3
"""
COVID-19 Activity 1: Data Loading and Basic Analysis
Run: python activities/activity-1/activity-1.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("ACTIVITY 1: COVID-19 DATA LOADING AND EXPLORATION")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity1_images', exist_ok=True)
    
    # Load data
    print("\nLoading dataset...")
    try:
        df = pd.read_csv("data/owid-covid-data.csv")
        print(f"[OK] Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        print("[ERROR] data/owid-covid-data.csv not found!")
        return
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Clean data - drop columns with >90% missing data
    missing_pct = (df.isnull().sum() / len(df)) * 100
    cols_to_drop = missing_pct[missing_pct > 90].index.tolist()
    df_clean = df.drop(columns=cols_to_drop)
    print(f"[OK] Cleaned data: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
    print(f"[OK] Dropped {len(cols_to_drop)} columns with >90% missing data")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # 1. Missing values heatmap for key columns
    key_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'population']
    available_cols = [col for col in key_cols if col in df_clean.columns]
    
    if available_cols:
        plt.figure(figsize=(12, 8))
        sns.heatmap(df_clean[available_cols].isnull(), cbar=True, yticklabels=False)
        plt.title('Missing Values in Key Columns')
        plt.tight_layout()
        plt.savefig('activity1_images/1.1_missing_values_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] missing_values_heatmap.png")
    
    # 2. Top 10 countries by total cases
    if 'total_cases' in df_clean.columns and 'location' in df_clean.columns:
        latest_data = df_clean.groupby('location')['total_cases'].max().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(12, 6))
        latest_data.plot(kind='bar', color='steelblue')
        plt.title('Top 10 Countries by Total COVID-19 Cases')
        plt.xticks(rotation=45)
        plt.ylabel('Total Cases')
        plt.tight_layout()
        plt.savefig('activity1_images/top_countries_cases.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] top_countries_cases.png")
    
    # 3. Global daily new cases timeline
    if 'new_cases' in df_clean.columns:
        global_daily = df_clean.groupby('date')['new_cases'].sum()
        
        plt.figure(figsize=(14, 6))
        plt.plot(global_daily.index, global_daily.values, color='darkblue', linewidth=2)
        plt.title('Global Daily New COVID-19 Cases Over Time')
        plt.xlabel('Date')
        plt.ylabel('New Cases')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('activity1_images/global_daily_cases.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] global_daily_cases.png")
    
    # 4. Data coverage by country
    country_coverage = df_clean.groupby('location').size().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    country_coverage.plot(kind='bar', color='green')
    plt.title('Data Coverage by Country (Number of Records)')
    plt.xticks(rotation=45)
    plt.ylabel('Number of Records')
    plt.tight_layout()
    plt.savefig('activity1_images/data_coverage.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] data_coverage.png")
    
    # Save cleaned dataset for next activities
    df_clean.to_csv('covid_data_cleaned.csv', index=False)
    print("\n[OK] Cleaned dataset saved as 'covid_data_cleaned.csv'")
    
    print(f"\n*** Activity 1 Complete! Check 'activity1_images' folder for plots. ***")

if __name__ == "__main__":
    main() 