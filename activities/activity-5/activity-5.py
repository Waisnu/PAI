#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 5: Time Series Analysis
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 5 REQUIREMENTS (Project Brief):
1. Line plots: Daily new cases and deaths
2. Average daily cases and deaths (using 7-day rolling average)
3. Vaccination trend over time
4. Testing and positive rate trend

OUTPUTS:
- 3 time series analysis visualizations (activity5_images/)
- Daily trend analysis with rolling averages
- Vaccination and testing insights over time

USAGE: python activities/activity-5/activity-5.py

PREREQUISITES: Run Activities 1-2 first to generate covid_data_processed.csv

DATA SOURCE: covid_data_processed.csv (complete dataset with imputed values)
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
    print("=" * 60)
    print("ACTIVITY 5: TIME SERIES ANALYSIS")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity5_images', exist_ok=True)
    
    # Load processed dataset from Activities 1-2
    print("\n1. Loading processed dataset...")
    try:
        df = pd.read_csv('covid_data_processed.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
    
    except FileNotFoundError:
        print("[ERROR] covid_data_processed.csv not found!")
        print("Please run activities 1-2 first.")
        return
    
    print("\nCreating time series analysis visualizations...")
    
    # Task 1 & 2: Daily trends and rolling averages for cases and deaths
    print("\n2. Task 1 & 2: Plotting daily trends and averages for cases & deaths...")
    if 'date' in df.columns and 'new_cases' in df.columns and 'new_deaths' in df.columns:
        global_daily = df.groupby('date').agg({
            'new_cases': 'sum',
            'new_deaths': 'sum'
        }).reset_index()
        
        # Calculate 7-day rolling average
        global_daily['cases_7day_avg'] = global_daily['new_cases'].rolling(window=7, center=True).mean()
        global_daily['deaths_7day_avg'] = global_daily['new_deaths'].rolling(window=7, center=True).mean()
        
        fig, axes = plt.subplots(2, 1, figsize=(16, 12), sharex=True)
        fig.suptitle('Global Daily COVID-19 Trends with 7-Day Rolling Average', fontsize=16, fontweight='bold')
        
        # Cases plot
        axes[0].plot(global_daily['date'], global_daily['new_cases'], alpha=0.3, color='lightblue', label='Daily Cases')
        axes[0].plot(global_daily['date'], global_daily['cases_7day_avg'], color='darkblue', linewidth=2, label='7-Day Average Cases')
        axes[0].set_title('Global Daily Cases')
        axes[0].set_ylabel('New Cases')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Deaths plot
        axes[1].plot(global_daily['date'], global_daily['new_deaths'], alpha=0.3, color='lightcoral', label='Daily Deaths')
        axes[1].plot(global_daily['date'], global_daily['deaths_7day_avg'], color='darkred', linewidth=2, label='7-Day Average Deaths')
        axes[1].set_title('Global Daily Deaths')
        axes[1].set_ylabel('New Deaths')
        axes[1].set_xlabel('Date')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout(rect=(0, 0.03, 1, 0.95))
        plt.savefig('activity5_images/5.1_daily_trends_and_averages.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 5.1_daily_trends_and_averages.png")
    else:
        print("[WARNING] Could not generate daily trends plot. Required columns missing.")

    # Task 3: Global vaccination coverage trends
    print("\n3. Task 3: Visualizing global vaccination trends...")
    if 'date' in df.columns and 'new_vaccinations' in df.columns:
        global_vaccinations = df.groupby('date').agg({'new_vaccinations': 'sum'}).reset_index()
        global_vaccinations['vaccinations_7day_avg'] = global_vaccinations['new_vaccinations'].rolling(window=7, center=True).mean()

        plt.figure(figsize=(16, 8))
        plt.plot(global_vaccinations['date'], global_vaccinations['new_vaccinations'], alpha=0.3, color='lightgreen', label='Daily Vaccinations')
        plt.plot(global_vaccinations['date'], global_vaccinations['vaccinations_7day_avg'], color='darkgreen', linewidth=2, label='7-Day Average Vaccinations')
        plt.title('Global COVID-19 Vaccination Trends', fontsize=16, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('New Vaccinations')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('activity5_images/5.2_global_vaccination_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 5.2_global_vaccination_trends.png")
    else:
        print("[WARNING] No vaccination data found to generate plot.")

    # Task 4: Global trends in testing and positivity rates
    print("\n4. Task 4: Analyzing testing and positivity rate trends...")
    if 'date' in df.columns and 'new_tests' in df.columns and 'new_cases' in df.columns:
        global_testing = df.groupby('date').agg({
            'new_tests': 'sum',
            'new_cases': 'sum'
        }).reset_index()
        
        # Calculate daily positivity rate
        global_testing['positivity_rate'] = (global_testing['new_cases'] / global_testing['new_tests']) * 100
        
        # Calculate rolling averages
        global_testing['tests_7day_avg'] = global_testing['new_tests'].rolling(window=7, center=True).mean()
        global_testing['positivity_7day_avg'] = global_testing['positivity_rate'].rolling(window=7, center=True).mean()
        
        fig, ax1 = plt.subplots(figsize=(16, 8))
        fig.suptitle('Global COVID-19 Testing and Positivity Rate Trends', fontsize=16, fontweight='bold')

        # Plotting new tests
        ax1.plot(global_testing['date'], global_testing['tests_7day_avg'], color='purple', linewidth=2, label='7-Day Avg Tests')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('New Tests (7-Day Average)', color='purple')
        ax1.tick_params(axis='y', labelcolor='purple')
        ax1.legend(loc='upper left')

        # Creating a second y-axis for positivity rate
        ax2 = ax1.twinx()
        ax2.plot(global_testing['date'], global_testing['positivity_7day_avg'], color='orange', linewidth=2, label='7-Day Avg Positivity Rate')
        ax2.set_ylabel('Positivity Rate (%) (7-Day Average)', color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')
        ax2.legend(loc='upper right')
        
        fig.tight_layout(rect=(0, 0.03, 1, 0.95))
        plt.savefig('activity5_images/5.3_testing_and_positivity_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 5.3_testing_and_positivity_trends.png")
    else:
        print("[WARNING] Could not generate testing trends plot. Required columns missing.")

    print(f"\n*** Activity 5 Complete! Check 'activity5_images' folder for plots. ***")

if __name__ == "__main__":
    main() 