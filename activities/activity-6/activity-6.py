#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 6: In-Depth Country Analysis
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 6 REQUIREMENTS (Project Brief):
1. Plot: Total cases and deaths over time (specific country)
2. User input: Country and metric, plot line chart (simulated via hardcoded choice)
3. Box plot: Total cases by continent
4. Line plot: Year-wise monthly new cases for selected country

OUTPUTS:
- 3 country-specific analysis visualizations (activity6_images/)
- Individual country performance analysis

USAGE: python activities/activity-6/activity-6.py

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

# ==========================================================================
# CONFIGURATION: CHOOSE A COUNTRY FOR ANALYSIS
# Change this variable to analyze a different country.
# ==========================================================================
CHOSEN_COUNTRY = 'United States'
# ==========================================================================

def main():
    print("=" * 60)
    print("ACTIVITY 6: IN-DEPTH COUNTRY ANALYSIS")
    print(f"Analyzing: {CHOSEN_COUNTRY}")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity6_images', exist_ok=True)
    
    # Load processed dataset
    print("\n1. Loading processed dataset...")
    try:
        df = pd.read_csv('covid_data_processed.csv')
        df['date'] = pd.to_datetime(df['date'])
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        print("[ERROR] covid_data_processed.csv not found!")
        print("Please run activities 1-2 first.")
        return
        
    # Filter data for the chosen country
    country_df = df[df['location'] == CHOSEN_COUNTRY].copy()
    if country_df.empty:
        print(f"[ERROR] No data found for the chosen country: '{CHOSEN_COUNTRY}'")
        print(f"Please choose a valid country from the 'location' column.")
        return
    
    print(f"\nCreating visualizations for {CHOSEN_COUNTRY}...")

    # Task 1 & 2: Evolution of total cases and deaths for a chosen country
    print(f"\n2. Task 1: Plotting total cases and deaths for {CHOSEN_COUNTRY}...")
    if 'total_cases' in country_df.columns and 'total_deaths' in country_df.columns:
        plt.figure(figsize=(16, 8))
        plt.plot(country_df['date'], country_df['total_cases'], label='Total Cases', color='blue', linewidth=2)
        plt.plot(country_df['date'], country_df['total_deaths'], label='Total Deaths', color='red', linewidth=2)
        plt.title(f'COVID-19 Evolution: Total Cases and Deaths in {CHOSEN_COUNTRY}', fontsize=16, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.yscale('log')
        plt.legend()
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(f'activity6_images/6.1_country_evolution_{CHOSEN_COUNTRY.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] Saved: 6.1_country_evolution_{CHOSEN_COUNTRY.replace(' ', '_')}.png")
    else:
        print("[WARNING] Could not generate country evolution plot.")

    # Task 3: Box plot of total cases by continent
    print("\n3. Task 3: Creating box plot of total cases by continent...")
    continent_col = 'continent'
    if continent_col in df.columns:
        # Use the latest data for each country for a meaningful box plot
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        latest_df = latest_df.dropna(subset=[continent_col, 'total_cases'])
        
        plt.figure(figsize=(14, 8))
        sns.boxplot(data=latest_df, x=continent_col, y='total_cases', palette='viridis')
        plt.title('Distribution of Total COVID-19 Cases by Continent', fontsize=16, fontweight='bold')
        plt.xlabel('Continent')
        plt.ylabel('Total Cases (Log Scale)')
        plt.yscale('log')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('activity6_images/6.2_cases_by_continent_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 6.2_cases_by_continent_boxplot.png")
    else:
        print("[WARNING] Continent column not found for box plot analysis.")

    # Task 4: Monthly trend analysis of new cases for the selected country, grouped by year
    print(f"\n4. Task 4: Analyzing monthly new cases by year for {CHOSEN_COUNTRY}...")
    if 'new_cases' in country_df.columns:
        country_df['year'] = country_df['date'].dt.year
        country_df['month'] = country_df['date'].dt.month
        monthly_trends = country_df.groupby(['year', 'month'])['new_cases'].sum().unstack(level=0)
        
        plt.figure(figsize=(16, 8))
        monthly_trends.plot(kind='line', marker='o', figsize=(16, 8))
        plt.title(f'Monthly New Cases in {CHOSEN_COUNTRY} by Year', fontsize=16, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('New Cases')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.legend(title='Year')
        plt.grid(True, alpha=0.5)
        plt.tight_layout()
        plt.savefig(f'activity6_images/6.3_monthly_trend_{CHOSEN_COUNTRY.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] Saved: 6.3_monthly_trend_{CHOSEN_COUNTRY.replace(' ', '_')}.png")
    else:
        print("[WARNING] Could not generate monthly trend plot.")

    print(f"\n*** Activity 6 Complete! Check 'activity6_images' folder for plots. ***")

if __name__ == "__main__":
    main() 