#!/usr/bin/env python3
"""
COVID-19 Activity 6: Country Analysis
Run: python activities/activity-6/activity-6.py
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
    print("ACTIVITY 6: COUNTRY ANALYSIS")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity6_images', exist_ok=True)
    
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
    
    print("\nCreating country-specific analysis visualizations...")
    
    # 1. Top 20 Countries by Total Cases
    if 'location' in df.columns and 'total_cases' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        top_cases = latest_df.nlargest(20, 'total_cases')[['location', 'total_cases']]
        
        plt.figure(figsize=(14, 10))
        bars = plt.barh(top_cases['location'], top_cases['total_cases'], color='steelblue', alpha=0.8)
        plt.title('Top 20 Countries by Total COVID-19 Cases')
        plt.xlabel('Total Cases')
        plt.ylabel('Country')
        
        # Add value labels
        for bar, value in zip(bars, top_cases['total_cases']):
            plt.text(bar.get_width() + value*0.01, bar.get_y() + bar.get_height()/2.,
                     f'{value:,.0f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('activity6_images/6.1_top_countries_cases.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] top_countries_cases.png")
    
    # 2. Top 20 Countries by Deaths Per Million
    if 'deaths_per_million' in df.columns and 'location' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        # Filter out very small populations or extreme values
        filtered_df = latest_df[latest_df['population'] > 100000]  # At least 100k population
        top_deaths_pm = filtered_df.nlargest(20, 'deaths_per_million')[['location', 'deaths_per_million']]
        
        plt.figure(figsize=(14, 10))
        bars = plt.barh(top_deaths_pm['location'], top_deaths_pm['deaths_per_million'], 
                        color='darkred', alpha=0.8)
        plt.title('Top 20 Countries by COVID-19 Deaths Per Million Population')
        plt.xlabel('Deaths Per Million')
        plt.ylabel('Country')
        
        # Add value labels
        for bar, value in zip(bars, top_deaths_pm['deaths_per_million']):
            plt.text(bar.get_width() + value*0.01, bar.get_y() + bar.get_height()/2.,
                     f'{value:,.0f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('activity6_images/6.2_top_countries_deaths_per_million.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] top_countries_deaths_per_million.png")
    
    # 3. Case Fatality Rate Comparison
    if 'case_fatality_rate' in df.columns and 'location' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        # Filter countries with at least 1000 total cases to avoid small number artifacts
        filtered_df = latest_df[(latest_df['total_cases'] >= 1000) & (latest_df['case_fatality_rate'] <= 20)]
        top_cfr = filtered_df.nlargest(20, 'case_fatality_rate')[['location', 'case_fatality_rate']]
        
        plt.figure(figsize=(14, 10))
        bars = plt.barh(top_cfr['location'], top_cfr['case_fatality_rate'], color='orange', alpha=0.8)
        plt.title('Top 20 Countries by Case Fatality Rate (Min 1000 cases)')
        plt.xlabel('Case Fatality Rate (%)')
        plt.ylabel('Country')
        
        # Add value labels
        for bar, value in zip(bars, top_cfr['case_fatality_rate']):
            plt.text(bar.get_width() + value*0.01, bar.get_y() + bar.get_height()/2.,
                     f'{value:.2f}%', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('activity6_images/6.3_top_countries_cfr.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] top_countries_cfr.png")
    
    # 4. Population vs Cases Scatter Plot
    if 'population' in df.columns and 'total_cases' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        scatter_df = latest_df[(latest_df['population'] > 1000000) & (latest_df['total_cases'] > 1000)]
        
        plt.figure(figsize=(14, 10))
        plt.scatter(scatter_df['population'], scatter_df['total_cases'], 
                   alpha=0.6, s=60, color='purple')
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Population (Log Scale)')
        plt.ylabel('Total Cases (Log Scale)')
        plt.title('Population vs Total COVID-19 Cases (Countries > 1M population)')
        plt.grid(True, alpha=0.3)
        
        # Add trend line
        x_vals = np.log10(scatter_df['population'])
        y_vals = np.log10(scatter_df['total_cases'])
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        plt.plot(scatter_df['population'], 10**p(x_vals), "r--", alpha=0.8, linewidth=2, label='Trend Line')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('activity6_images/6.4_population_vs_cases.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] population_vs_cases.png")
    
    # 5. Country Performance Dashboard (Top 5 by each metric)
    if all(col in df.columns for col in ['location', 'total_cases', 'total_deaths', 'cases_per_million']):
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('COVID-19 Country Performance Dashboard', fontsize=16)
        
        # Top 5 by total cases
        top5_cases = latest_df.nlargest(5, 'total_cases')
        axes[0, 0].bar(top5_cases['location'], top5_cases['total_cases'], 
                       color='steelblue', alpha=0.8)
        axes[0, 0].set_title('Top 5 Countries - Total Cases')
        axes[0, 0].set_ylabel('Total Cases')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Top 5 by total deaths
        if 'total_deaths' in df.columns:
            top5_deaths = latest_df.nlargest(5, 'total_deaths')
            axes[0, 1].bar(top5_deaths['location'], top5_deaths['total_deaths'], 
                           color='darkred', alpha=0.8)
            axes[0, 1].set_title('Top 5 Countries - Total Deaths')
            axes[0, 1].set_ylabel('Total Deaths')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Top 5 by cases per million
        if 'cases_per_million' in df.columns:
            filtered_cpm = latest_df[latest_df['population'] > 100000]
            top5_cpm = filtered_cpm.nlargest(5, 'cases_per_million')
            axes[1, 0].bar(top5_cpm['location'], top5_cpm['cases_per_million'], 
                           color='green', alpha=0.8)
            axes[1, 0].set_title('Top 5 Countries - Cases Per Million')
            axes[1, 0].set_ylabel('Cases Per Million')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Top 5 by deaths per million
        if 'deaths_per_million' in df.columns:
            filtered_dpm = latest_df[latest_df['population'] > 100000]
            top5_dpm = filtered_dpm.nlargest(5, 'deaths_per_million')
            axes[1, 1].bar(top5_dpm['location'], top5_dpm['deaths_per_million'], 
                           color='purple', alpha=0.8)
            axes[1, 1].set_title('Top 5 Countries - Deaths Per Million')
            axes[1, 1].set_ylabel('Deaths Per Million')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('activity6_images/6.5_country_performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] country_performance_dashboard.png")
    
    # 6. Regional Country Comparison
    region_col = None
    for col in ['continent', 'who_region', 'region']:
        if col in df.columns:
            region_col = col
            break
    
    if region_col and 'location' in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        
        # Get top 3 countries per region by total cases
        regional_top = latest_df.groupby(region_col).apply(
            lambda x: x.nlargest(3, 'total_cases')
        ).reset_index(drop=True)
        
        # Select a few major regions for cleaner visualization
        major_regions = regional_top.groupby(region_col)['total_cases'].sum().nlargest(4).index
        regional_top_filtered = regional_top[regional_top[region_col].isin(major_regions)]
        
        plt.figure(figsize=(16, 10))
        
        # Create grouped bar chart
        regions = regional_top_filtered[region_col].unique()
        x_pos = np.arange(len(regions))
        width = 0.25
        
        for i in range(3):  # Top 3 per region
            country_data = []
            labels = []
            
            for region in regions:
                region_countries = regional_top_filtered[
                    regional_top_filtered[region_col] == region
                ].nlargest(3, 'total_cases')
                
                if len(region_countries) > i:
                    country_data.append(region_countries.iloc[i]['total_cases'])
                    if i == 0:  # Only add region labels once
                        labels.append(region_countries.iloc[i]['location'])
                else:
                    country_data.append(0)
                    if i == 0:
                        labels.append('')
            
            plt.bar(x_pos + i*width, country_data, width, 
                   label=f'{"1st" if i==0 else "2nd" if i==1 else "3rd"} in Region', 
                   alpha=0.8)
        
        plt.xlabel('Region')
        plt.ylabel('Total Cases')
        plt.title('Top 3 Countries by Total Cases in Major Regions')
        plt.xticks(x_pos + width, regions, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig('activity6_images/6.6_regional_country_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[SAVED] regional_country_comparison.png")
    
    print(f"\n*** Activity 6 Complete! Check 'activity6_images' folder for plots. ***")

if __name__ == "__main__":
    main() 