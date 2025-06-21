#!/usr/bin/env python3
"""
COVID-19 Activity 2: Data Cleaning and Feature Engineering
Run: python activities/activity-2/activity-2.py
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("ACTIVITY 2: DATA CLEANING AND FEATURE ENGINEERING")
    print("=" * 60)
    
    # Load cleaned dataset from Activity 1
    print("\nLoading cleaned dataset...")
    try:
        df = pd.read_csv('covid_data_cleaned.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
    
    except FileNotFoundError:
        print("[ERROR] covid_data_cleaned.csv not found!")
        print("Please run activity-1 first.")
        return
    
    # Missing values imputation
    print("\nHandling missing values...")
    
    # Get numerical and categorical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Remove date from categorical if present
    if 'date' in categorical_cols:
        categorical_cols.remove('date')
    
    missing_before = df.isnull().sum().sum()
    
    # Impute numerical columns with median
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Impute categorical columns with mode
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_series = df[col].mode()
            mode_value = mode_series.iloc[0] if len(mode_series) > 0 else 'Unknown'
            df[col].fillna(mode_value, inplace=True)
    
    missing_after = df.isnull().sum().sum()
    print(f"[OK] Missing values: {missing_before} -> {missing_after}")
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates()
    duplicates_after = df.duplicated().sum()
    print(f"[OK] Duplicates removed: {duplicates_before}")
    print(f"[OK] Final shape: {df.shape}")
    
    # Feature engineering
    print("\nCreating new features...")
    
    if 'date' in df.columns:
        # Date-based features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['month_name'] = df['date'].dt.month_name()
        df['day_name'] = df['date'].dt.day_name()
        
        # Seasonal features
        season_map = {
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
        }
        df['season'] = df['month'].map(season_map)
        
        df['quarter'] = df['date'].dt.quarter
        print("[OK] Date-based features created")
    
    # COVID-specific calculated features
    if 'total_deaths' in df.columns and 'total_cases' in df.columns:
        df['case_fatality_rate'] = np.where(
            df['total_cases'] > 0,
            (df['total_deaths'] / df['total_cases']) * 100,
            0
        )
        print("[OK] Case fatality rate calculated")
    
    if 'total_cases' in df.columns and 'total_tests' in df.columns:
        df['test_positivity_rate'] = np.where(
            df['total_tests'] > 0,
            (df['total_cases'] / df['total_tests']) * 100,
            0
        )
        print("[OK] Test positivity rate calculated")
    
    if 'total_cases' in df.columns and 'population' in df.columns:
        df['cases_per_million'] = np.where(
            df['population'] > 0,
            (df['total_cases'] / df['population']) * 1000000,
            0
        )
        print("[OK] Cases per million calculated")
    
    if 'total_deaths' in df.columns and 'population' in df.columns:
        df['deaths_per_million'] = np.where(
            df['population'] > 0,
            (df['total_deaths'] / df['population']) * 1000000,
            0
        )
        print("[OK] Deaths per million calculated")
    
    # Save processed dataset
    df.to_csv('covid_data_processed.csv', index=False)
    print(f"\n[OK] Processed dataset saved as 'covid_data_processed.csv'")
    print(f"[OK] Features added: {df.shape[1] - len(numerical_cols) - len(categorical_cols) - 1}")  # -1 for date
    
    # Summary
    if 'location' in df.columns:
        unique_locations = df['location'].nunique()
        print(f"[OK] Total locations: {unique_locations}")
    
    print(f"\n*** Activity 2 Complete! Dataset ready for analysis. ***")

if __name__ == "__main__":
    main() 