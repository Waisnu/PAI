#!/usr/bin/env python3
"""
COVID-19 Activity 7: Summary Dashboard
Run: python activities/activity-7/activity-7.py
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
    print("ACTIVITY 7: SUMMARY DASHBOARD")
    print("=" * 60)
    
    # Create output folder
    os.makedirs('activity7_images', exist_ok=True)
    
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
    
    print("\nGenerating comprehensive COVID-19 summary dashboard...")
    
    # Get latest data for summary statistics
    latest_df = df.loc[df.groupby('location')['date'].idxmax()]
    
    # Calculate global totals
    global_totals = {
        'total_cases': latest_df['total_cases'].sum(),
        'total_deaths': latest_df['total_deaths'].sum() if 'total_deaths' in df.columns else 0,
        'total_countries': latest_df['location'].nunique(),
        'avg_cfr': latest_df[latest_df['total_cases'] >= 1000]['case_fatality_rate'].mean() if 'case_fatality_rate' in df.columns else 0
    }
    
    print(f"\n=== GLOBAL SUMMARY ===")
    print(f"Total Cases: {global_totals['total_cases']:,}")
    print(f"Total Deaths: {global_totals['total_deaths']:,}")
    print(f"Countries/Regions: {global_totals['total_countries']}")
    print(f"Average CFR: {global_totals['avg_cfr']:.2f}%" if global_totals['avg_cfr'] > 0 else "")
    
    # 1. Executive Summary Dashboard
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
    
    # Global Timeline (top section)
    ax1 = fig.add_subplot(gs[0, :2])
    if 'date' in df.columns and 'new_cases' in df.columns:
        daily_global = df.groupby('date')['new_cases'].sum()
        daily_global_ma = daily_global.rolling(window=7).mean()
        
        ax1.fill_between(daily_global.index, daily_global.values, alpha=0.3, color='steelblue')
        ax1.plot(daily_global.index, daily_global_ma.values, color='darkblue', linewidth=2)
        ax1.set_title('Global Daily New Cases (7-day MA)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('New Cases')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
    
    # Global Deaths Timeline
    ax2 = fig.add_subplot(gs[0, 2:])
    if 'date' in df.columns and 'new_deaths' in df.columns:
        daily_deaths = df.groupby('date')['new_deaths'].sum()
        daily_deaths_ma = daily_deaths.rolling(window=7).mean()
        
        ax2.fill_between(daily_deaths.index, daily_deaths.values, alpha=0.3, color='darkred')
        ax2.plot(daily_deaths.index, daily_deaths_ma.values, color='darkred', linewidth=2)
        ax2.set_title('Global Daily Deaths (7-day MA)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('New Deaths')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
    
    # Top Countries by Cases
    ax3 = fig.add_subplot(gs[1, :2])
    if 'location' in df.columns and 'total_cases' in df.columns:
        top_cases = latest_df.nlargest(10, 'total_cases')
        bars = ax3.barh(top_cases['location'], top_cases['total_cases'], color='steelblue', alpha=0.8)
        ax3.set_title('Top 10 Countries by Total Cases', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Total Cases')
        
        # Add value labels
        for bar, value in zip(bars, top_cases['total_cases']):
            ax3.text(bar.get_width() + value*0.01, bar.get_y() + bar.get_height()/2.,
                     f'{value/1e6:.1f}M', ha='left', va='center', fontsize=8)
    
    # Regional Distribution Pie Chart
    ax4 = fig.add_subplot(gs[1, 2:])
    region_col = None
    for col in ['continent', 'who_region', 'region']:
        if col in df.columns:
            region_col = col
            break
    
    if region_col:
        regional_cases = latest_df.groupby(region_col)['total_cases'].sum().sort_values(ascending=False)
        ax4.pie(regional_cases.values, labels=regional_cases.index, autopct='%1.1f%%', startangle=90)
        ax4.set_title(f'Cases Distribution by {region_col.title()}', fontsize=12, fontweight='bold')
    
    # Monthly Trend Analysis
    ax5 = fig.add_subplot(gs[2, :2])
    if 'month_name' in df.columns and 'new_cases' in df.columns:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_cases = df.groupby('month_name')['new_cases'].sum()
        monthly_cases = monthly_cases.reindex([m for m in month_order if m in monthly_cases.index])
        
        ax5.bar(monthly_cases.index, monthly_cases.values, color='green', alpha=0.8)
        ax5.set_title('Total Cases by Month (All Years)', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Total New Cases')
        ax5.tick_params(axis='x', rotation=45)
    
    # Case Fatality Rate by Top Countries
    ax6 = fig.add_subplot(gs[2, 2:])
    if 'case_fatality_rate' in df.columns and 'location' in df.columns:
        # Get countries with high case counts for reliable CFR
        high_case_countries = latest_df[latest_df['total_cases'] >= 100000]
        top_cfr = high_case_countries.nlargest(10, 'case_fatality_rate')
        
        bars = ax6.barh(top_cfr['location'], top_cfr['case_fatality_rate'], color='orange', alpha=0.8)
        ax6.set_title('Top 10 CFR (Countries >100k cases)', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Case Fatality Rate (%)')
        
        # Add value labels
        for bar, value in zip(bars, top_cfr['case_fatality_rate']):
            ax6.text(bar.get_width() + value*0.01, bar.get_y() + bar.get_height()/2.,
                     f'{value:.2f}%', ha='left', va='center', fontsize=8)
    
    # Key Statistics Summary
    ax7 = fig.add_subplot(gs[3, :])
    ax7.axis('off')
    
    # Create summary text
    # Get top countries safely
    top_countries = latest_df.nlargest(3, 'total_cases')
    
    summary_text = f"""
GLOBAL COVID-19 PANDEMIC SUMMARY DASHBOARD
==================================================================================================================

[GLOBAL TOTALS]
   * Total Confirmed Cases: {global_totals['total_cases']:,.0f}
   * Total Deaths: {global_totals['total_deaths']:,.0f}
   * Countries/Regions Affected: {global_totals['total_countries']}
   * Global Case Fatality Rate: {global_totals['avg_cfr']:.2f}%

[MOST AFFECTED COUNTRIES] (by total cases):
   1. {top_countries.iloc[0]['location']}: {top_countries.iloc[0]['total_cases']:,.0f} cases
   2. {top_countries.iloc[1]['location']}: {top_countries.iloc[1]['total_cases']:,.0f} cases
   3. {top_countries.iloc[2]['location']}: {top_countries.iloc[2]['total_cases']:,.0f} cases

[DATA INSIGHTS]
   * Peak Daily Cases: {df.groupby('date')['new_cases'].sum().max():,.0f} ({df.groupby('date')['new_cases'].sum().idxmax().strftime('%B %d, %Y')})
   * Data Coverage: {df['date'].min().strftime('%B %Y')} to {df['date'].max().strftime('%B %Y')}
   * Total Data Points: {len(df):,} records
"""
    
    ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    plt.suptitle('COVID-19 GLOBAL PANDEMIC SUMMARY DASHBOARD', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig('activity7_images/7.1_executive_summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] executive_summary_dashboard.png")
    
    # 2. Detailed Analysis Dashboard
    fig, axes = plt.subplots(3, 2, figsize=(18, 15))
    fig.suptitle('COVID-19 DETAILED ANALYSIS DASHBOARD', fontsize=16, fontweight='bold')
    
    # Population vs Cases Correlation
    if 'population' in df.columns and 'total_cases' in df.columns:
        scatter_df = latest_df[(latest_df['population'] > 1000000) & (latest_df['total_cases'] > 1000)]
        axes[0, 0].scatter(scatter_df['population'], scatter_df['total_cases'], alpha=0.6, color='purple')
        axes[0, 0].set_xscale('log')
        axes[0, 0].set_yscale('log')
        axes[0, 0].set_xlabel('Population')
        axes[0, 0].set_ylabel('Total Cases')
        axes[0, 0].set_title('Population vs Total Cases')
        axes[0, 0].grid(True, alpha=0.3)
    
    # Deaths Per Million Distribution
    if 'deaths_per_million' in df.columns:
        filtered_dpm = latest_df[(latest_df['population'] > 100000) & (latest_df['deaths_per_million'] > 0)]
        axes[0, 1].hist(filtered_dpm['deaths_per_million'], bins=30, alpha=0.7, color='darkred')
        axes[0, 1].set_xlabel('Deaths Per Million')
        axes[0, 1].set_ylabel('Number of Countries')
        axes[0, 1].set_title('Distribution of Deaths Per Million')
        axes[0, 1].axvline(filtered_dpm['deaths_per_million'].median(), color='red', 
                          linestyle='--', label=f'Median: {filtered_dpm["deaths_per_million"].median():.0f}')
        axes[0, 1].legend()
    
    # Quarterly Trends
    if 'quarter' in df.columns and 'year' in df.columns:
        quarterly = df.groupby(['year', 'quarter'])['new_cases'].sum().reset_index()
        quarterly['period'] = quarterly['year'].astype(str) + '-Q' + quarterly['quarter'].astype(str)
        axes[1, 0].bar(quarterly['period'], quarterly['new_cases'], color='green', alpha=0.8)
        axes[1, 0].set_title('Quarterly Case Trends')
        axes[1, 0].set_ylabel('New Cases')
        axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Seasonal Analysis
    if 'season' in df.columns and 'new_cases' in df.columns:
        seasonal = df.groupby('season')['new_cases'].sum().sort_values(ascending=True)
        axes[1, 1].barh(seasonal.index, seasonal.values, color=['lightblue', 'lightgreen', 'orange', 'lightcoral'])
        axes[1, 1].set_title('Cases by Season')
        axes[1, 1].set_xlabel('Total New Cases')
    
    # Day of Week Patterns
    if 'day_name' in df.columns and 'new_cases' in df.columns:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_avg = df.groupby('day_name')['new_cases'].mean()
        daily_avg = daily_avg.reindex([d for d in day_order if d in daily_avg.index])
        axes[2, 0].bar(daily_avg.index, daily_avg.values, color='teal', alpha=0.8)
        axes[2, 0].set_title('Average Daily Cases by Day of Week')
        axes[2, 0].set_ylabel('Average New Cases')
        axes[2, 0].tick_params(axis='x', rotation=45)
    
    # Growth Rate Timeline
    if 'date' in df.columns and 'total_cases' in df.columns:
        global_totals_ts = df.groupby('date')['total_cases'].sum().reset_index()
        global_totals_ts['growth_rate'] = global_totals_ts['total_cases'].pct_change() * 100
        axes[2, 1].plot(global_totals_ts['date'], global_totals_ts['growth_rate'].rolling(7).mean(), 
                       color='darkgreen', linewidth=2)
        axes[2, 1].set_title('7-Day Average Growth Rate')
        axes[2, 1].set_ylabel('Growth Rate (%)')
        axes[2, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[2, 1].tick_params(axis='x', rotation=45)
        axes[2, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('activity7_images/7.2_detailed_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("[SAVED] detailed_analysis_dashboard.png")
    
    # 3. Generate Summary Report
    print("\n" + "="*80)
    print("COVID-19 COMPREHENSIVE ANALYSIS REPORT")
    print("="*80)
    
    print(f"\nDATA OVERVIEW:")
    print(f"- Dataset Size: {len(df):,} records")
    print(f"- Countries/Regions: {df['location'].nunique()}")
    print(f"- Date Range: {df['date'].min().strftime('%B %d, %Y')} to {df['date'].max().strftime('%B %d, %Y')}")
    print(f"- Total Days: {(df['date'].max() - df['date'].min()).days} days")
    
    print(f"\nGLOBAL STATISTICS:")
    print(f"- Total Confirmed Cases: {global_totals['total_cases']:,}")
    print(f"- Total Deaths: {global_totals['total_deaths']:,}")
    print(f"- Global Case Fatality Rate: {global_totals['avg_cfr']:.2f}%")
    
    if 'date' in df.columns and 'new_cases' in df.columns:
        peak_day = df.groupby('date')['new_cases'].sum().idxmax()
        peak_cases = df.groupby('date')['new_cases'].sum().max()
        print(f"- Peak Daily Cases: {peak_cases:,} on {peak_day.strftime('%B %d, %Y')}")
    
    print(f"\nTOP PERFORMERS:")
    top5_cases = latest_df.nlargest(5, 'total_cases')
    for i, (_, row) in enumerate(top5_cases.iterrows(), 1):
        print(f"{i}. {row['location']}: {row['total_cases']:,} cases")
    
    if 'deaths_per_million' in df.columns:
        print(f"\nHIGHEST DEATHS PER MILLION (Population >100k):")
        filtered_latest = latest_df[latest_df['population'] > 100000]
        top5_dpm = filtered_latest.nlargest(5, 'deaths_per_million')
        for i, (_, row) in enumerate(top5_dpm.iterrows(), 1):
            print(f"{i}. {row['location']}: {row['deaths_per_million']:,.1f} deaths per million")
    
    print(f"\n*** Activity 7 Complete! Check 'activity7_images' folder for dashboards. ***")
    print("="*80)

if __name__ == "__main__":
    main() 