#!/usr/bin/env python3
"""
COVID-19 Activity 3: Worldwide COVID-19 Overview
Run: python activities/activity-3/activity-3.py
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
    
    # Load processed dataset
    print("\nLoading processed dataset...")
    try:
        df = pd.read_csv('covid_data_processed.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
    
    except FileNotFoundError:
        print("[ERROR] covid_data_processed.csv not found!")
        print("Please run activity-2 first.")
        return
    
    print("\nCreating worldwide overview visualizations...")
    
    # 1. Total Cases and Deaths by Region/Continent
    region_col = None
    for col in ['continent', 'who_region', 'region']:
        if col in df.columns:
            region_col = col
            break
    
    if region_col:
        # Get latest data for each location
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        regional_data = latest_df.groupby(region_col).agg({
            'total_cases': 'sum',
            'total_deaths': 'sum'
        }).reset_index()
        regional_data = regional_data.dropna(subset=[region_col])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Total cases by region
        bars1 = ax1.bar(regional_data[region_col], regional_data['total_cases'], 
                        color='steelblue', alpha=0.8)
        ax1.set_title('Total COVID-19 Cases by Region')
        ax1.set_xlabel('Region')
        ax1.set_ylabel('Total Cases')
        ax1.tick_params(axis='x', rotation=45)
        
        # Total deaths by region
        bars2 = ax2.bar(regional_data[region_col], regional_data['total_deaths'], 
                        color='crimson', alpha=0.8)
        ax2.set_title('Total COVID-19 Deaths by Region')
        ax2.set_xlabel('Region')
        ax2.set_ylabel('Total Deaths')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('activity3_images/3.1_regional_cases_deaths.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] regional_cases_deaths.png")
    
    # 2. Monthly Worldwide Cases
    if 'date' in df.columns and 'new_cases' in df.columns:
        df['year_month'] = df['date'].dt.to_period('M')
        monthly_cases = df.groupby('year_month')['new_cases'].sum().reset_index()
        monthly_cases['year_month'] = monthly_cases['year_month'].dt.to_timestamp()
        
        plt.figure(figsize=(14, 8))
        plt.plot(monthly_cases['year_month'], monthly_cases['new_cases'], 
                 marker='o', linewidth=2, markersize=6, color='darkblue')
        
        plt.title('Monthly Worldwide COVID-19 New Cases')
        plt.xlabel('Month')
        plt.ylabel('New Cases')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add peak annotation
        max_cases_idx = monthly_cases['new_cases'].idxmax()
        max_cases = monthly_cases.loc[max_cases_idx, 'new_cases']
        max_date = monthly_cases.loc[max_cases_idx, 'year_month']
        
        plt.annotate(f'Peak: {max_cases:,.0f} cases\n{max_date.strftime("%B %Y")}',
                    xy=(max_date, max_cases), xytext=(10, 10), 
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        plt.savefig('activity3_images/3.2_monthly_worldwide_cases.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] monthly_worldwide_cases.png")
        print(f"[OK] Peak month: {max_date.strftime('%B %Y')} with {max_cases:,} cases")
    
    # 3. Correlation Heatmap
    correlation_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
    if 'total_tests' in df.columns:
        correlation_cols.append('total_tests')
    if 'population' in df.columns:
        correlation_cols.append('population')
    
    available_cols = [col for col in correlation_cols if col in df.columns]
    
    if len(available_cols) >= 2:
        correlation_matrix = df[available_cols].corr()
        
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                    vmin=-1, vmax=1, center=0, fmt='.2f', 
                    square=True, cbar_kws={"shrink": .8})
        
        plt.title('Correlation Matrix: COVID-19 Key Metrics')
        plt.tight_layout()
        plt.savefig('activity3_images/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] correlation_heatmap.png")
    
    # 4. Global Daily Timeline
    if 'date' in df.columns and 'new_cases' in df.columns and 'new_deaths' in df.columns:
        global_daily = df.groupby('date').agg({
            'new_cases': 'sum',
            'new_deaths': 'sum'
        }).reset_index()
        
        fig, ax1 = plt.subplots(figsize=(16, 8))
        
        # New cases
        color1 = 'steelblue'
        ax1.fill_between(global_daily['date'], global_daily['new_cases'], 
                         alpha=0.3, color=color1, label='Daily New Cases')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('New Cases', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.tick_params(axis='x', rotation=45)
        
        # New deaths on secondary axis
        ax2 = ax1.twinx()
        color2 = 'darkred'
        ax2.fill_between(global_daily['date'], global_daily['new_deaths'], 
                         alpha=0.3, color=color2, label='Daily New Deaths')
        ax2.set_ylabel('New Deaths', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        plt.title('Global COVID-19 Daily Cases and Deaths Timeline')
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        plt.savefig('activity3_images/3.4_global_daily_timeline.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] global_daily_timeline.png")
    
    print(f"\n*** Activity 3 Complete! Check 'activity3_images' folder for plots. ***")

if __name__ == "__main__":
    main() 