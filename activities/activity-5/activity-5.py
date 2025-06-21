#!/usr/bin/env python3
"""
COVID-19 Activity 5: Time Series Analysis
Run: python activities/activity-5/activity-5.py
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
    
    print("\nCreating time series analysis visualizations...")
    
    # 1. Global Weekly Rolling Average
    if 'date' in df.columns and 'new_cases' in df.columns:
        global_daily = df.groupby('date').agg({
            'new_cases': 'sum',
            'new_deaths': 'sum' if 'new_deaths' in df.columns else 'sum'
        }).reset_index()
        
        # Calculate 7-day rolling average
        global_daily['cases_7day_avg'] = global_daily['new_cases'].rolling(window=7, center=True).mean()
        if 'new_deaths' in df.columns:
            global_daily['deaths_7day_avg'] = global_daily['new_deaths'].rolling(window=7, center=True).mean()
        
        fig, axes = plt.subplots(2, 1, figsize=(16, 12))
        
        # Cases
        axes[0].plot(global_daily['date'], global_daily['new_cases'], 
                     alpha=0.3, color='lightblue', label='Daily Cases')
        axes[0].plot(global_daily['date'], global_daily['cases_7day_avg'], 
                     color='darkblue', linewidth=2, label='7-Day Average')
        axes[0].set_title('Global COVID-19 Daily Cases with 7-Day Rolling Average')
        axes[0].set_ylabel('New Cases')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Deaths
        if 'new_deaths' in df.columns:
            axes[1].plot(global_daily['date'], global_daily['new_deaths'], 
                         alpha=0.3, color='lightcoral', label='Daily Deaths')
            axes[1].plot(global_daily['date'], global_daily['deaths_7day_avg'], 
                         color='darkred', linewidth=2, label='7-Day Average')
            axes[1].set_title('Global COVID-19 Daily Deaths with 7-Day Rolling Average')
            axes[1].set_ylabel('New Deaths')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('activity5_images/5.1_global_rolling_average.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] global_rolling_average.png")
    
    # 2. Seasonal Trends
    if 'month_name' in df.columns and 'new_cases' in df.columns:
        seasonal_data = df.groupby(['month_name', 'year']).agg({
            'new_cases': 'sum',
            'new_deaths': 'sum' if 'new_deaths' in df.columns else 'sum'
        }).reset_index()
        
        # Average by month across years
        monthly_avg = seasonal_data.groupby('month_name').agg({
            'new_cases': 'mean',
            'new_deaths': 'mean' if 'new_deaths' in df.columns else 'mean'
        }).reset_index()
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_avg['sort_order'] = monthly_avg['month_name'].map({month: i for i, month in enumerate(month_order)})
        monthly_avg = monthly_avg.sort_values('sort_order')
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Cases
        axes[0].bar(monthly_avg['month_name'], monthly_avg['new_cases'], 
                    color='steelblue', alpha=0.8)
        axes[0].set_title('Average Monthly COVID-19 Cases')
        axes[0].set_ylabel('Average New Cases')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Deaths
        if 'new_deaths' in df.columns:
            axes[1].bar(monthly_avg['month_name'], monthly_avg['new_deaths'], 
                        color='darkred', alpha=0.8)
            axes[1].set_title('Average Monthly COVID-19 Deaths')
            axes[1].set_ylabel('Average New Deaths')
            axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('activity5_images/5.2_seasonal_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] seasonal_trends.png")
    
    # 3. Top Countries Time Series
    if 'location' in df.columns and 'total_cases' in df.columns:
        # Get top 10 countries by total cases
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        top_countries = latest_df.nlargest(10, 'total_cases')['location'].tolist()
        
        # Filter data for top countries
        top_countries_data = df[df['location'].isin(top_countries)]
        
        plt.figure(figsize=(16, 10))
        
        for country in top_countries:
            country_data = top_countries_data[top_countries_data['location'] == country]
            country_data = country_data.sort_values('date')
            
            plt.plot(country_data['date'], country_data['total_cases'], 
                     linewidth=2, label=country, alpha=0.8)
        
        plt.title('COVID-19 Total Cases Over Time - Top 10 Countries')
        plt.xlabel('Date')
        plt.ylabel('Total Cases')
        plt.yscale('log')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('activity5_images/5.3_top_countries_timeseries.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] top_countries_timeseries.png")
    
    # 4. Growth Rate Analysis
    if 'date' in df.columns and 'total_cases' in df.columns:
        # Calculate global growth rate
        global_totals = df.groupby('date')['total_cases'].sum().reset_index()
        global_totals = global_totals.sort_values('date')
        
        # Calculate percentage change
        global_totals['growth_rate'] = global_totals['total_cases'].pct_change() * 100
        global_totals['growth_rate_7day'] = global_totals['growth_rate'].rolling(window=7, center=True).mean()
        
        plt.figure(figsize=(16, 8))
        
        plt.plot(global_totals['date'], global_totals['growth_rate'], 
                 alpha=0.3, color='gray', label='Daily Growth Rate')
        plt.plot(global_totals['date'], global_totals['growth_rate_7day'], 
                 color='darkgreen', linewidth=2, label='7-Day Average Growth Rate')
        
        plt.title('Global COVID-19 Cases Growth Rate Over Time')
        plt.xlabel('Date')
        plt.ylabel('Growth Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('activity5_images/5.4_growth_rate_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] growth_rate_analysis.png")
    
    # 5. Quarterly Analysis
    if 'quarter' in df.columns and 'year' in df.columns:
        quarterly_data = df.groupby(['year', 'quarter']).agg({
            'new_cases': 'sum',
            'new_deaths': 'sum' if 'new_deaths' in df.columns else 'sum'
        }).reset_index()
        
        quarterly_data['period'] = quarterly_data['year'].astype(str) + '-Q' + quarterly_data['quarter'].astype(str)
        
        fig, axes = plt.subplots(2, 1, figsize=(16, 12))
        
        # Cases
        axes[0].bar(quarterly_data['period'], quarterly_data['new_cases'], 
                    color='steelblue', alpha=0.8)
        axes[0].set_title('Quarterly COVID-19 Cases')
        axes[0].set_ylabel('New Cases')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Deaths
        if 'new_deaths' in df.columns:
            axes[1].bar(quarterly_data['period'], quarterly_data['new_deaths'], 
                        color='darkred', alpha=0.8)
            axes[1].set_title('Quarterly COVID-19 Deaths')
            axes[1].set_ylabel('New Deaths')
            axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('activity5_images/5.5_quarterly_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] quarterly_analysis.png")
    
    print(f"\n*** Activity 5 Complete! Check 'activity5_images' folder for plots. ***")

if __name__ == "__main__":
    main() 