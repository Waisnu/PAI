#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 1: Data Loading and Exploration
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 1 REQUIREMENTS (Project Brief):
1. Load dataset using Pandas
2. Show first and last 5 rows  
3. Check and handle missing values
4. Drop columns with >90% missing values
5. Convert 'date' column to datetime

OUTPUTS:
- Cleaned dataset (covid_data_cleaned.csv) 
- 2 exploration visualizations (activity1_images/)
- Missing value analysis and data overview

USAGE: python activities/activity-1/activity-1.py

NOTE: This activity ONLY cleans structure and explores data.
      Missing value IMPUTATION is handled in Activity 2.
      
DATA FLOW: 
data/owid-covid-data.csv → Activity 1 → covid_data_cleaned.csv → Activity 2
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 70)
    print("ACTIVITY 1: DATA LOADING AND EXPLORATION")
    print("Following Project Brief Requirements")
    print("=" * 70)
    
    # Create output folder
    os.makedirs('activity1_images', exist_ok=True)
    
    # 1. Load dataset using Pandas
    print("\n1. LOADING DATASET FROM /data DIRECTORY")
    print("-" * 50)
    try:
        df = pd.read_csv("data/owid-covid-data.csv")
        print(f"✅ Dataset loaded successfully from data/owid-covid-data.csv")
        print(f"✅ Original Shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
        print(f"✅ Memory usage: ~{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    except FileNotFoundError:
        print("❌ ERROR: data/owid-covid-data.csv not found!")
        return
    
    # 2. Show first and last 5 rows
    print("\n2. DISPLAYING FIRST AND LAST 5 ROWS")
    print("-" * 50)
    print("\n📊 FIRST 5 ROWS:")
    print(df.head().to_string())
    print("\n📊 LAST 5 ROWS:")
    print(df.tail().to_string())
    
    # Show basic info about the dataset
    print(f"\n📈 DATASET OVERVIEW:")
    print(f"   • Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   • Countries/Regions: {df['location'].nunique()}")
    print(f"   • Total records: {len(df):,}")
    
    # 3. Check and handle missing values (ANALYSIS ONLY)
    print("\n3. CHECKING FOR MISSING VALUES")
    print("-" * 50)
    
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100
    
    missing_summary = pd.DataFrame({
        'Column': missing_count.index,
        'Missing_Count': missing_count.values,
        'Missing_Percentage': missing_percentage.values
    }).sort_values('Missing_Percentage', ascending=False)
    
    total_missing = missing_count.sum()
    cols_with_missing = (missing_count > 0).sum()
    
    print(f"📊 MISSING VALUES ANALYSIS:")
    print(f"   • Total missing values: {total_missing:,}")
    print(f"   • Columns with missing data: {cols_with_missing}/{len(df.columns)}")
    print(f"   • Dataset completeness: {((1 - total_missing/(len(df)*len(df.columns)))*100):.1f}%")
    
    # Show top columns with missing values
    print(f"\n🔍 TOP 10 COLUMNS WITH MOST MISSING VALUES:")
    top_missing = missing_summary.head(10)
    for _, row in top_missing.iterrows():
        print(f"   • {row['Column']}: {row['Missing_Count']:,} ({row['Missing_Percentage']:.1f}%)")
    
    # 4. Drop columns with >90% missing values
    print("\n4. DROPPING COLUMNS WITH >90% MISSING VALUES")
    print("-" * 50)
    
    cols_to_drop = missing_summary[missing_summary['Missing_Percentage'] > 90]['Column'].tolist()
    
    print(f"🗑️  COLUMNS TO BE DROPPED ({len(cols_to_drop)} columns):")
    if cols_to_drop:
        for col in cols_to_drop:
            pct = missing_summary[missing_summary['Column'] == col]['Missing_Percentage'].iloc[0]
            print(f"   • {col}: {pct:.1f}% missing")
    else:
        print("   • No columns have >90% missing data")
    
    # Apply the column dropping
    df_cleaned = df.drop(columns=cols_to_drop)
    print(f"\n✅ STRUCTURE CLEANED:")
    print(f"   • Before: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"   • After:  {df_cleaned.shape[0]:,} rows × {df_cleaned.shape[1]} columns")
    print(f"   • Removed: {len(cols_to_drop)} unnecessary columns")
    
    # 5. Convert 'date' column to datetime
    print("\n5. CONVERTING DATE COLUMN TO DATETIME")
    print("-" * 50)
    
    if 'date' in df_cleaned.columns:
        print(f"📅 Before: {df_cleaned['date'].dtype}")
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
        print(f"📅 After:  {df_cleaned['date'].dtype}")
        print(f"✅ Date range: {df_cleaned['date'].min()} to {df_cleaned['date'].max()}")
        print(f"✅ Total days: {(df_cleaned['date'].max() - df_cleaned['date'].min()).days}")
    else:
        print("❌ ERROR: 'date' column not found!")
    
    # Create visualizations
    print("\n6. CREATING EXPLORATION VISUALIZATIONS")
    print("-" * 50)
    
    # Visualization 1: Missing values overview
    plt.figure(figsize=(15, 10))
    
    # Top subplot: Bar chart of missing percentages
    plt.subplot(2, 1, 1)
    top_15_missing = missing_summary.head(15)
    bars = plt.bar(range(len(top_15_missing)), top_15_missing['Missing_Percentage'], 
                   color=['red' if x > 90 else 'orange' if x > 50 else 'yellow' if x > 10 else 'green' 
                          for x in top_15_missing['Missing_Percentage']])
    plt.title('Missing Value Analysis - Top 15 Columns', fontsize=14, fontweight='bold')
    plt.xlabel('Columns')
    plt.ylabel('Missing Percentage (%)')
    plt.xticks(range(len(top_15_missing)), top_15_missing['Column'], rotation=45, ha='right')
    
    # Add percentage labels
    for bar, pct in zip(bars, top_15_missing['Missing_Percentage']):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Add 90% threshold line
    plt.axhline(y=90, color='red', linestyle='--', alpha=0.8, label='90% Threshold (Drop Line)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Bottom subplot: Data coverage by location
    plt.subplot(2, 1, 2)
    location_counts = df_cleaned['location'].value_counts().head(15)
    plt.bar(range(len(location_counts)), location_counts.values, color='steelblue', alpha=0.8)
    plt.title('Data Coverage - Top 15 Locations by Record Count', fontsize=14, fontweight='bold')
    plt.xlabel('Countries/Regions')
    plt.ylabel('Number of Records')
    plt.xticks(range(len(location_counts)), location_counts.index, rotation=45, ha='right')
    
    # Add value labels
    for i, v in enumerate(location_counts.values):
        plt.text(i, v + 20, str(v), ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('activity1_images/1_data_exploration_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved: data_exploration_overview.png")
    
    # Visualization 2: Dataset timeline
    plt.figure(figsize=(12, 6))
    daily_records = df_cleaned.groupby('date').size()
    plt.plot(daily_records.index, daily_records.values, linewidth=2, color='darkblue')
    plt.title('Daily Record Count Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Number of Records per Day')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('activity1_images/2_dataset_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved: dataset_timeline.png")
    
    # Save CLEANED dataset (structure cleaned, missing values NOT imputed yet)
    output_file = 'covid_data_cleaned.csv'
    df_cleaned.to_csv(output_file, index=False)
    
    # Check file size
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n7. SAVING CLEANED DATASET")
    print("-" * 50)
    print(f"✅ Saved as: {output_file}")
    print(f"✅ File size: {file_size_mb:.1f} MB")
    print(f"✅ Note: Missing values NOT imputed yet (Activity 2 task)")
    
    # Final summary
    print(f"\n" + "="*70)
    print("ACTIVITY 1 COMPLETE - SUMMARY")
    print(f"="*70)
    print(f"✅ Dataset loaded from data/owid-covid-data.csv")
    print(f"✅ First/last 5 rows displayed")
    print(f"✅ Missing values analyzed: {total_missing:,} total missing")
    print(f"✅ Dropped {len(cols_to_drop)} columns with >90% missing data")
    print(f"✅ Date column converted to datetime")
    print(f"✅ 2 exploration visualizations created")
    print(f"✅ Cleaned dataset saved: {df_cleaned.shape[0]:,} rows × {df_cleaned.shape[1]} columns")
    print(f"\n🎯 NEXT: Run Activity 2 for missing value imputation and feature engineering")

if __name__ == "__main__":
    main() 