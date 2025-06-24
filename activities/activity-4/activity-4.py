#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 4: Regional Analysis
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 4 REQUIREMENTS (Project Brief):
1. Grouped bar chart: New cases by continent and month
2. Box plot: Total cases by year
3. Bar plot: Deaths by continent  
4. Bar plot: Monthly total cases

OUTPUTS:
- 4 regional analysis visualizations (activity4_images/)
- Continental comparison insights
- Temporal analysis by year and month

USAGE: python activities/activity-4/activity-4.py

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
    print("ACTIVITY 4: REGIONAL ANALYSIS")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity4_images', exist_ok=True)
    
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
    
    # Find region column
    region_col = None
    for col in ['continent', 'who_region', 'region']:
        if col in df.columns:
            region_col = col
            break
    
    if not region_col:
        print("[ERROR] No region column found!")
        return
    
    print(f"[OK] Using region column: {region_col}")
    print("\nCreating regional analysis visualizations...")
    
    # 1. New Cases by Region/Month
    if 'new_cases' in df.columns and 'month_name' in df.columns:
        df_filtered = df.dropna(subset=[region_col])
        monthly_regional = df_filtered.groupby([region_col, 'month_name'])['new_cases'].sum().reset_index()
        monthly_pivot = monthly_regional.pivot(index='month_name', columns=region_col, values='new_cases')
        monthly_pivot = monthly_pivot.fillna(0)
        
        # Reorder months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_pivot = monthly_pivot.reindex([m for m in month_order if m in monthly_pivot.index])
        
        plt.figure(figsize=(16, 8))
        monthly_pivot.plot(kind='bar', width=0.8, figsize=(16, 8))
        plt.title('New COVID-19 Cases by Region and Month')
        plt.xlabel('Month')
        plt.ylabel('New Cases')
        plt.xticks(rotation=45)
        plt.legend(title=region_col.title(), bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('activity4_images/4.1_new_cases_by_region_month.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: new_cases_by_region_month.png")
    
    # 2. Total Cases by Year (Box Plot)
    if 'total_cases' in df.columns and 'year' in df.columns:
        df_year = df.dropna(subset=['total_cases', 'year'])
        df_year = df_year[df_year['total_cases'] > 0]
        
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=df_year, x='year', y='total_cases')
        plt.yscale('log')
        plt.title('Distribution of Total COVID-19 Cases by Year')
        plt.xlabel('Year')
        plt.ylabel('Total Cases (Log Scale)')
        plt.tight_layout()
        plt.savefig('activity4_images/4.2_total_cases_by_year_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: total_cases_by_year_boxplot.png")
    
    # 3. Total Deaths by Region
    if 'total_deaths' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        deaths_by_region = latest_df.groupby(region_col)['total_deaths'].sum().sort_values(ascending=False)
        deaths_by_region = deaths_by_region.dropna()
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(deaths_by_region.index, deaths_by_region.values, 
                       color='darkred', alpha=0.8)
        plt.title('Total COVID-19 Deaths by Region')
        plt.xlabel('Region')
        plt.ylabel('Total Deaths')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, deaths_by_region.values):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + value*0.01,
                    f'{value:,.0f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('activity4_images/4.3_total_deaths_by_region.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: total_deaths_by_region.png")
    
    # 4. Monthly Analysis (Multiple Metrics)
    if 'month_name' in df.columns:
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Monthly COVID-19 Analysis', fontsize=16)
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        
        # New cases by month
        if 'new_cases' in df.columns:
            monthly_cases = df.groupby('month_name')['new_cases'].sum()
            monthly_cases = monthly_cases.reindex([m for m in month_order if m in monthly_cases.index])
            axes[0, 0].bar(monthly_cases.index, monthly_cases.values, color='steelblue', alpha=0.8)
            axes[0, 0].set_title('New Cases by Month')
            axes[0, 0].set_ylabel('New Cases')
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # New deaths by month
        if 'new_deaths' in df.columns:
            monthly_deaths = df.groupby('month_name')['new_deaths'].sum()
            monthly_deaths = monthly_deaths.reindex([m for m in month_order if m in monthly_deaths.index])
            axes[0, 1].bar(monthly_deaths.index, monthly_deaths.values, color='darkred', alpha=0.8)
            axes[0, 1].set_title('New Deaths by Month')
            axes[0, 1].set_ylabel('New Deaths')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Case fatality rate by month
        if 'total_cases' in df.columns and 'total_deaths' in df.columns:
            # Recalculate CFR monthly
            monthly_totals = df.groupby('month_name').agg({'new_cases': 'sum', 'new_deaths': 'sum'})
            monthly_totals['case_fatality_rate'] = (monthly_totals['new_deaths'] / monthly_totals['new_cases'] * 100)
            monthly_cfr = monthly_totals['case_fatality_rate'].reindex([m for m in month_order if m in monthly_totals.index])
            axes[1, 0].bar(monthly_cfr.index, monthly_cfr.values, color='orange', alpha=0.8)
            axes[1, 0].set_title('Average Case Fatality Rate by Month')
            axes[1, 0].set_ylabel('CFR (%)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Vaccinations by month (if available)
        if 'new_vaccinations' in df.columns:
            monthly_vacc = df.groupby('month_name')['new_vaccinations'].sum()
            monthly_vacc = monthly_vacc.reindex([m for m in month_order if m in monthly_vacc.index])
            axes[1, 1].bar(monthly_vacc.index, monthly_vacc.values, color='green', alpha=0.8)
            axes[1, 1].set_title('New Vaccinations by Month')
            axes[1, 1].set_ylabel('New Vaccinations')
            axes[1, 1].tick_params(axis='x', rotation=45)
        elif 'new_tests' in df.columns:
            monthly_tests = df.groupby('month_name')['new_tests'].sum()
            monthly_tests = monthly_tests.reindex([m for m in month_order if m in monthly_tests.index])
            axes[1, 1].bar(monthly_tests.index, monthly_tests.values, color='purple', alpha=0.8)
            axes[1, 1].set_title('New Tests by Month')
            axes[1, 1].set_ylabel('New Tests')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('activity4_images/4.4_monthly_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: monthly_analysis.png")
    
    # 5. Regional Summary Table
    latest_df = df.loc[df.groupby('location')['date'].idxmax()]
    regional_summary = latest_df.groupby(region_col).agg({
        'total_cases': 'sum',
        'total_deaths': 'sum',
        'population': 'sum',
        'location': 'count'
    }).round(2)
    
    regional_summary.columns = ['Total_Cases', 'Total_Deaths', 'Total_Population', 'Num_Locations']
    regional_summary['Cases_Per_Million'] = (regional_summary['Total_Cases'] / regional_summary['Total_Population'] * 1000000).round(2)
    regional_summary['Deaths_Per_Million'] = (regional_summary['Total_Deaths'] / regional_summary['Total_Population'] * 1000000).round(2)
    regional_summary['Case_Fatality_Rate'] = (regional_summary['Total_Deaths'] / regional_summary['Total_Cases'] * 100).round(2)
    regional_summary = regional_summary.sort_values('Total_Cases', ascending=False)
    
    print("\nRegional Summary:")
    print("=" * 80)
    for region, row in regional_summary.iterrows():
        print(f"{region}: {row['Total_Cases']:,.0f} cases, {row['Total_Deaths']:,.0f} deaths, CFR: {row['Case_Fatality_Rate']:.2f}%")
    
    print(f"\n*** Activity 4 Complete! Check 'activity4_images' folder for plots. ***")

if __name__ == "__main__":
    main() 