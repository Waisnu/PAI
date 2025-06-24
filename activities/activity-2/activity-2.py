#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 2: Data Cleaning and Feature Engineering
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 2 REQUIREMENTS (Project Brief):
1. Impute missing values
2. Remove duplicate rows
3. Create features (e.g., extract year/month from date)
4. Count unique countries

OUTPUTS:
- Final processed dataset (covid_data_processed.csv)
- 2 feature engineering visualizations (activity2_images/)
- Complete dataset ready for analysis (Activities 3-7)

USAGE: python activities/activity-2/activity-2.py

NOTE: This activity creates the FINAL processed dataset used by Activities 3-7.
      All missing values are imputed and new date features are added.
      
DATA FLOW: 
covid_data_cleaned.csv → Activity 2 → covid_data_processed.csv → Activities 3-7
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
    print("ACTIVITY 2: DATA CLEANING AND FEATURE ENGINEERING")
    print("Following Project Brief Requirements")
    print("=" * 70)
    
    # Create output folder
    os.makedirs('activity2_images', exist_ok=True)
    
    # Load cleaned dataset from Activity 1
    print("\n1. LOADING CLEANED DATASET FROM ACTIVITY 1")
    print("-" * 50)
    try:
        df = pd.read_csv('covid_data_cleaned.csv')
        print(f"[OK] Loaded cleaned dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
        
        # Check file size
        file_size_mb = os.path.getsize('covid_data_cleaned.csv') / (1024 * 1024)
        print(f"[OK] Input file size: {file_size_mb:.1f} MB")
    
    except FileNotFoundError:
        print("[ERROR] covid_data_cleaned.csv not found!")
        print("   Please run Activity 1 first.")
        return
    
    # 1. Impute missing values in dataset columns
    print("\n2. IMPUTING MISSING VALUES")
    print("-" * 50)
    
    # Show current missing values status
    missing_before = df.isnull().sum().sum()
    missing_by_col = df.isnull().sum()
    cols_with_missing = missing_by_col[missing_by_col > 0]
    
    print(f"BEFORE IMPUTATION:")
    print(f"- Total missing values: {missing_before:,}")
    print(f"- Columns with missing values: {len(cols_with_missing)}")
    
    if len(cols_with_missing) > 0:
        print(f"\nTOP 10 COLUMNS WITH MISSING VALUES:")
        for col, count in cols_with_missing.head(10).items():
            pct = (count / len(df)) * 100
            print(f"- {col}: {count:,} ({pct:.1f}%)")
    
    # Get numerical and categorical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Remove date from categorical if present
    if 'date' in categorical_cols:
        categorical_cols.remove('date')
    
    # Imputation strategy
    print(f"\nIMPUTATION STRATEGY:")
    print(f"- Numerical columns ({len(numerical_cols)}): Median imputation")
    print(f"- Categorical columns ({len(categorical_cols)}): Mode imputation")
    
    # Track imputation statistics
    imputation_stats = []
    
    # Impute numerical columns with median
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            missing_count = df[col].isnull().sum()
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            imputation_stats.append({
                'column': col,
                'type': 'numerical',
                'missing_count': missing_count,
                'fill_value': median_val
            })
    
    # Impute categorical columns with mode
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            missing_count = df[col].isnull().sum()
            mode_series = df[col].mode()
            mode_value = mode_series.iloc[0] if len(mode_series) > 0 else 'Unknown'
            df[col].fillna(mode_value, inplace=True)
            imputation_stats.append({
                'column': col,
                'type': 'categorical',
                'missing_count': missing_count,
                'fill_value': mode_value
            })
    
    missing_after = df.isnull().sum().sum()
    print(f"\nIMPUTATION COMPLETE:")
    print(f"- Missing values: {missing_before:,} -> {missing_after:,}")
    print(f"- Imputed {len(imputation_stats)} columns")
    
    # 2. Remove duplicate rows from DataFrame
    print("\n3. REMOVING DUPLICATE ROWS")
    print("-" * 50)
    
    duplicates_before = df.duplicated().sum()
    print(f"Duplicate rows found: {duplicates_before:,}")
    
    if duplicates_before > 0:
        # Show some example duplicates
        duplicate_rows = df[df.duplicated()]
        print(f"Example duplicate rows (first 3):")
        example_cols = ['location', 'date', 'total_cases', 'total_deaths']
        available_cols = [col for col in example_cols if col in duplicate_rows.columns]
        if len(available_cols) > 0:
            print(duplicate_rows[available_cols].head(3).to_string(index=False))
        
        df = df.drop_duplicates()
        print(f"Removed {duplicates_before:,} duplicate rows")
    else:
        print(f"No duplicate rows found - data is already unique")
    
    print(f"Final shape after deduplication: {df.shape}")
    
    # 3. Create new features (extract year and month from date column)
    print("\n4. CREATING NEW FEATURES FROM DATE")
    print("-" * 50)
    
    if 'date' in df.columns:
        # Extract basic date components as requested
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        
        # Additional useful features
        df['quarter'] = df['date'].dt.quarter
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        print(f"CREATED NEW FEATURES:")
        print(f"- year: {df['year'].min()} to {df['year'].max()}")
        print(f"- month: {df['month'].min()} to {df['month'].max()}")
        print(f"- month_name: {df['month_name'].nunique()} unique month names")
        print(f"- quarter: {df['quarter'].nunique()} quarters")
        print(f"- day_of_year: 1 to 366")
        print(f"- week_of_year: 1 to 53")
        
        # Show sample of new features
        print(f"\nSAMPLE OF NEW DATE FEATURES:")
        sample_cols = ['date', 'year', 'month', 'month_name', 'quarter']
        print(df[sample_cols].head().to_string(index=False))
    else:
        print("ERROR: 'date' column not found!")
    
    # 4. Explore unique countries and count total
    print("\n5. EXPLORING UNIQUE COUNTRIES")
    print("-" * 50)
    
    if 'location' in df.columns:
        unique_countries = df['location'].unique()
        total_countries = len(unique_countries)
        
        print(f"COUNTRY ANALYSIS:")
        print(f"- Total countries/locations: {total_countries}")
        
        # Show some examples
        print(f"\nFIRST 15 COUNTRIES/LOCATIONS:")
        for i, country in enumerate(unique_countries[:15], 1):
            print(f"   {i:2d}. {country}")
        
        if total_countries > 15:
            print(f"   ... and {total_countries - 15} more")
        
        # Show data coverage per country
        country_coverage = df['location'].value_counts().head(10)
        print(f"\nTOP 10 COUNTRIES BY RECORD COUNT:")
        for country, count in country_coverage.items():
            records_per_day = count / ((df['date'].max() - df['date'].min()).days + 1)
            print(f"- {country}: {count:,} records ({records_per_day:.1f}/day avg)")
    else:
        print("ERROR: 'location' column not found!")
    
    # Create visualizations for Activity 2
    print("\n6. CREATING FEATURE ENGINEERING VISUALIZATIONS")
    print("-" * 50)
    
    # Visualization 1: Before/After Missing Values
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Before imputation (reconstruct from stats)
    if imputation_stats:
        cols = [stat['column'] for stat in imputation_stats[:15]]
        missing_counts = [stat['missing_count'] for stat in imputation_stats[:15]]
        
        ax1.bar(range(len(cols)), missing_counts, color='red', alpha=0.7)
        ax1.set_title('Missing Values BEFORE Imputation\n(Top 15 Columns)', fontweight='bold')
        ax1.set_xlabel('Columns')
        ax1.set_ylabel('Missing Count')
        ax1.set_xticks(range(len(cols)))
        ax1.set_xticklabels(cols, rotation=45, ha='right')
        
        # After imputation (should be all zeros)
        ax2.bar(range(len(cols)), [0] * len(cols), color='green', alpha=0.7)
        ax2.set_title('Missing Values AFTER Imputation\n(All Columns Complete)', fontweight='bold')
        ax2.set_xlabel('Columns')
        ax2.set_ylabel('Missing Count')
        ax2.set_xticks(range(len(cols)))
        ax2.set_xticklabels(cols, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('activity2_images/1_missing_values_before_after.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: missing_values_before_after.png")
    
    # Visualization 2: New Features Overview
    if 'year' in df.columns and 'month' in df.columns:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Bar chart for records per year
        year_counts = df['year'].value_counts().sort_index()
        ax1.bar(year_counts.index, year_counts.values, color='skyblue')
        ax1.set_title('Data Distribution by Year', fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Number of Records')
        ax1.set_xticks(year_counts.index)
        
        # Line chart for records per month
        month_counts = df.groupby('month')['date'].count()
        ax2.plot(month_counts.index, month_counts.values, marker='o', linestyle='-', color='salmon')
        ax2.set_title('Data Distribution by Month (Across All Years)', fontweight='bold')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Number of Records')
        ax2.set_xticks(range(1, 13))
        
        fig.suptitle('Overview of New Date-Based Features', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('activity2_images/2_new_features_overview.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: new_features_overview.png")
    
    # Save the FINAL processed dataset for Activities 3-7
    output_file = 'covid_data_processed.csv'
    
    print(f"\n7. SAVING FINAL PROCESSED DATASET")
    print("-" * 50)
    df.to_csv(output_file, index=False)
    
    # Check file size
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"[OK] Saved as: {output_file}")
    print(f"[OK] File size: {file_size_mb:.1f} MB")
    print(f"[OK] Final dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"[OK] Ready for Activities 3-7")
    
    # Final summary
    print(f"\n" + "="*70)
    print("ACTIVITY 2 COMPLETE - SUMMARY")
    print(f"="*70)
    print(f"- Missing values imputed: {missing_before:,} -> {missing_after:,}")
    print(f"- Duplicate rows removed: {duplicates_before:,}")
    print(f"- New features created: 6 date-based features")
    print(f"- Countries explored: {df['location'].nunique() if 'location' in df.columns else 'N/A'}")
    print(f"- 2 visualizations created")
    print(f"- Final processed dataset saved for Activities 3-7")
    print(f"\nNEXT: Run Activities 3-7 for analysis and visualization")

if __name__ == "__main__":
    main() 