#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 3: Worldwide COVID-19 Overview
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 3 REQUIREMENTS (Project Brief):
1. Bar plot: WHO regions with total cases and deaths
2. Line plot: Worldwide monthly trend  
3. Heatmap: Correlation between total cases and deaths
4. Time evolution for a country (e.g., India)

OUTPUTS:
- 4 worldwide analysis visualizations (activity3_images/)
- Global COVID-19 trend analysis
- Regional comparison and correlation insights

USAGE: python activities/activity-3/activity-3.py

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
    print("ACTIVITY 3: WORLDWIDE COVID-19 OVERVIEW")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity3_images', exist_ok=True)
    
    # Load cleaned dataset
    print("\nLoading cleaned dataset...")
    try:
        df = pd.read_csv('covid_data_processed.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
            
            # Create month/year features on-the-fly
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['month_name'] = df['date'].dt.month_name()
            df['year_month'] = df['date'].dt.to_period('M')
    
    except FileNotFoundError:
        print("[ERROR] covid_data_processed.csv not found!")
        print("Please run activity-1 and activity-2 first.")
        return
    
    print("\nCreating worldwide overview visualizations...")
    
    # 1. WHO Regions with total COVID-19 cases and deaths (bar plots)
    print("\n1. Visualizing WHO Regions with total cases and deaths...")
    
    # Look for WHO region column
    who_region_col = None
    for col in ['who_region', 'continent', 'region']:
        if col in df.columns:
            who_region_col = col
            print(f"[OK] Using region column: {col}")
            break
    
    if who_region_col:
        # Get latest data for each location to avoid double counting
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        
        # Group by WHO region
        regional_data = latest_df.groupby(who_region_col).agg({
            'total_cases': 'sum',
            'total_deaths': 'sum'
        }).reset_index()
        regional_data = regional_data.dropna(subset=[who_region_col])
        regional_data = regional_data.sort_values('total_cases', ascending=False)
        
        # Create bar plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Total cases by WHO region
        bars1 = ax1.bar(regional_data[who_region_col], regional_data['total_cases'], 
                        color='steelblue', alpha=0.8)
        ax1.set_title('Total COVID-19 Cases by WHO Region')
        ax1.set_xlabel('WHO Region')
        ax1.set_ylabel('Total Cases')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars1, regional_data['total_cases']):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + value*0.01,
                    f'{value/1e6:.1f}M', ha='center', va='bottom', fontsize=9)
        
        # Total deaths by WHO region
        bars2 = ax2.bar(regional_data[who_region_col], regional_data['total_deaths'], 
                        color='crimson', alpha=0.8)
        ax2.set_title('Total COVID-19 Deaths by WHO Region')
        ax2.set_xlabel('WHO Region')
        ax2.set_ylabel('Total Deaths')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars2, regional_data['total_deaths']):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + value*0.01,
                    f'{value/1e3:.0f}K', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('activity3_images/3.1_who_regions_cases_deaths.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: who_regions_cases_deaths.png")
        
        # Print summary
        print(f"WHO Regions summary:")
        for _, row in regional_data.iterrows():
            print(f"- {row[who_region_col]}: {row['total_cases']:,.0f} cases, {row['total_deaths']:,.0f} deaths")
    else:
        print("[ERROR] No WHO region column found in dataset!")
    
    # 2. Worldwide monthly trend of COVID-19 cases (line plot)
    print("\n2. Exploring worldwide monthly trend of COVID-19 cases...")
    
    if 'date' in df.columns and 'new_cases' in df.columns:
        # Group by year-month for monthly trend
        monthly_cases = df.groupby('year_month')['new_cases'].sum().reset_index()
        monthly_cases['year_month_date'] = monthly_cases['year_month'].dt.to_timestamp()
        
        plt.figure(figsize=(16, 8))
        plt.plot(monthly_cases['year_month_date'], monthly_cases['new_cases'], 
                 marker='o', linewidth=3, markersize=8, color='darkblue', 
                 markerfacecolor='lightblue', markeredgecolor='darkblue')
        
        plt.title('Worldwide Monthly Trend of COVID-19 Cases', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('New Cases', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add peak annotation
        max_cases_idx = monthly_cases['new_cases'].idxmax()
        max_cases = monthly_cases.loc[max_cases_idx, 'new_cases']
        max_date = monthly_cases.loc[max_cases_idx, 'year_month_date']
        
        plt.annotate(f'Peak: {max_cases:,.0f} cases\n{max_date.strftime("%B %Y")}',
                    xy=(max_date, max_cases), xytext=(50, 50), 
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', lw=2))
        
        # Add trend phases
        plt.axvline(x=pd.to_datetime('2020-03-01'), color='red', linestyle='--', alpha=0.7, label='WHO Pandemic Declaration')
        plt.axvline(x=pd.to_datetime('2021-01-01'), color='green', linestyle='--', alpha=0.7, label='Vaccine Rollout Begins')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('activity3_images/3.2_monthly_worldwide_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: monthly_worldwide_trend.png")
        print(f"[OK] Peak month: {max_date.strftime('%B %Y')} with {max_cases:,} cases")
        print(f"[OK] Total months analyzed: {len(monthly_cases)}")
    else:
        print("[ERROR] Required columns 'date' or 'new_cases' not found!")
    
    # 3. Correlation between total cases and total deaths (heatmap)
    print("\n3. Investigating correlation between total cases and total deaths...")
    
    # Focus on the specific correlation requested: total cases vs total deaths
    correlation_cols = ['total_cases', 'total_deaths']
    
    # Add other relevant metrics for comprehensive analysis
    extended_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
    if 'total_tests' in df.columns:
        extended_cols.append('total_tests')
    if 'population' in df.columns:
        extended_cols.append('population')
    
    available_cols = [col for col in extended_cols if col in df.columns]
    
    if len(available_cols) >= 2:
        # Filter out rows with null values for cleaner correlation
        correlation_df = df[available_cols].dropna()
        correlation_matrix = correlation_df.corr()
        
        plt.figure(figsize=(12, 10))
        
        # Create a mask for upper triangle
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        # Create heatmap
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', 
                    vmin=-1, vmax=1, center=0, fmt='.3f', 
                    square=True, cbar_kws={"shrink": .8, "label": "Correlation Coefficient"},
                    annot_kws={"fontsize": 12})
        
        plt.title('Correlation Matrix: Total Cases vs Total Deaths\n(and other COVID-19 metrics)', 
                 fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('activity3_images/3_correlation_heatmap_cases_deaths.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Correlation heatmap saved.")
        
        # Print key correlations
        cases_deaths_corr = correlation_matrix.loc['total_cases', 'total_deaths']
        print(f"[OK] Correlation between total cases and total deaths: {cases_deaths_corr:.3f}")
        
        if cases_deaths_corr > 0.8:
            print("     -> Very strong positive correlation")
        elif cases_deaths_corr > 0.6:
            print("     -> Strong positive correlation")
        elif cases_deaths_corr > 0.4:
            print("     -> Moderate positive correlation")
        else:
            print("     -> Weak correlation")
    else:
        print("[ERROR] Required columns for correlation analysis not found!")
    
    # 4. Total cases evolution over time for India (specific location analysis)
    print("\n4. Analyzing total cases evolution over time for India...")
    
    if 'location' in df.columns and 'total_cases' in df.columns:
        # Filter data for India
        india_data = df[df['location'] == 'India'].copy()
        
        if len(india_data) > 0:
            india_data = india_data.sort_values('date')
            
            plt.figure(figsize=(16, 8))
            plt.plot(india_data['date'], india_data['total_cases'], 
                     linewidth=3, color='orange', marker='o', markersize=4,
                     markerfacecolor='red', markeredgecolor='orange')
            
            plt.title('COVID-19 Total Cases Evolution Over Time - India', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Total Cases', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Annotate major waves
            wave1_peak = india_data[india_data['date'] == pd.to_datetime('2021-05-08')]
            if not wave1_peak.empty:
                plt.annotate('Second Wave Peak (Delta)', 
                             xy=(wave1_peak['date'].iloc[0], wave1_peak['total_cases'].iloc[0]),
                             xytext=(wave1_peak['date'].iloc[0] - pd.Timedelta(days=200), wave1_peak['total_cases'].iloc[0] * 0.8),
                             arrowprops=dict(facecolor='black', shrink=0.05),
                             bbox=dict(boxstyle="round,pad=0.3", fc="cyan", ec="b", lw=2))

            wave2_peak = india_data[india_data['date'] == pd.to_datetime('2022-01-21')]
            if not wave2_peak.empty:
                plt.annotate('Third Wave Peak (Omicron)',
                             xy=(wave2_peak['date'].iloc[0], wave2_peak['total_cases'].iloc[0]),
                             xytext=(wave2_peak['date'].iloc[0] - pd.Timedelta(days=200), wave2_peak['total_cases'].iloc[0] * 1.05),
                             arrowprops=dict(facecolor='black', shrink=0.05),
                             bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="orange", lw=2))
            
            plt.tight_layout()
            plt.savefig('activity3_images/3.3_evolution_total_cases_india.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("[OK] India total cases evolution plot saved.")
            
            # Print India summary
            print("[OK] India Summary:")
            print(f" - Latest Total Cases: {india_data['total_cases'].iloc[-1]:,.0f}")
            print(f" - Latest Total Deaths: {india_data['total_deaths'].iloc[-1]:,.0f}")
        else:
            print("[WARNING] No data found for India")
    else:
        print("[ERROR] Required columns not found for India analysis!")
    
    print("\n" + "="*60)
    print("ACTIVITY 3 COMPLETE!")
    print("Check 'activity3_images' folder for visualizations.")
    print("="*60)

if __name__ == "__main__":
    main() 