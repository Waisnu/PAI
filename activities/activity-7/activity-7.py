#!/usr/bin/env python3
"""
================================================================================
COVID-19 Data Analysis Project - Activity 7: Additional Insights
================================================================================

COURSE: BDSE - Python for AI (PAI) Module
PROJECT: Worldwide COVID-19 Data Analysis for ABC Health Analytics

ACTIVITY 7 REQUIREMENTS (Project Brief):
1. Visualize the fatality rate (total deaths / total cases) over time globally
2. Explore the positivity rate (total_cases / total_tests) versus total tests 
   conducted to analyse testing effectiveness using the x-axis as the logarithmic 
   scale for better visualisation
3. Analyze the fatality rate and its relationship with smoking (Use male_smokers 
   and female_smokers columns)
4. Create a heatmap to analyse the relationship between hospital beds per 
   thousand and fatality rate

OUTPUTS:
- 4 visualizations addressing each requirement
- Analysis of external factors affecting COVID-19 outcomes
- Insights into testing effectiveness and health infrastructure impact

USAGE: python activities/activity-7/activity-7.py

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
from datetime import datetime
warnings.filterwarnings('ignore')

def main():
    print("=" * 80)
    print("ACTIVITY 7: ADDITIONAL INSIGHTS")
    print("=" * 80)
    print("Extracting additional insights, examining the influence of external")
    print("factors, and evaluating regional disparities for a holistic understanding")
    print("of the COVID-19 landscape.")
    
    # Create output folder
    os.makedirs('activity7_images', exist_ok=True)
    
    # Load processed dataset from Activities 1-2
    print("\n1. Loading processed dataset...")
    try:
        df = pd.read_csv('covid_data_processed.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
        
        # Calculate fatality rate where both cases and deaths exist
        df['fatality_rate'] = np.where(
            (df['total_cases'] > 0) & (df['total_deaths'] > 0),
            (df['total_deaths'] / df['total_cases']) * 100,
            np.nan
        )
        
        # Calculate positivity rate where both cases and tests exist
        if 'total_tests' in df.columns:
            df['positivity_rate'] = np.where(
                (df['total_tests'] > 0) & (df['total_cases'] > 0),
                (df['total_cases'] / df['total_tests']) * 100,
                np.nan
            )
        
        print(f"[OK] Calculated rates - Fatality rate and Positivity rate")
    
    except FileNotFoundError:
        print("[ERROR] covid_data_processed.csv not found!")
        print("Please run activities 1-2 first to generate the processed dataset.")
        return
    
    # ==========================================================================
    # TASK 1: Visualize the fatality rate over time globally
    # ==========================================================================
    print("\n2. Task 1: Global Fatality Rate Over Time...")
    
    # Calculate global fatality rate over time
    global_daily = df.groupby('date').agg({
        'total_cases': 'sum',
        'total_deaths': 'sum'
    }).reset_index()
    
    # Calculate cumulative fatality rate
    global_daily['global_fatality_rate'] = np.where(
        global_daily['total_cases'] > 0,
        (global_daily['total_deaths'] / global_daily['total_cases']) * 100,
        np.nan
    )
    
    if not global_daily.empty:
        # Create subplot layout
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [2, 1]})
        
        # Plot 1: Global fatality rate timeline
        ax1.plot(global_daily['date'], global_daily['global_fatality_rate'], 
                 color='darkred', linewidth=2, label='Global Fatality Rate')
        ax1.fill_between(global_daily['date'], global_daily['global_fatality_rate'], 
                         alpha=0.3, color='darkred')
        ax1.set_title('Global COVID-19 Fatality Rate Over Time\n(Total Deaths / Total Cases)', 
                      fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Fatality Rate (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=11)
        
        # Add annotations for key periods
        max_rate_idx = global_daily['global_fatality_rate'].idxmax()
        max_rate_date = global_daily.loc[max_rate_idx, 'date']
        max_rate_value = global_daily.loc[max_rate_idx, 'global_fatality_rate']
        
        ax1.annotate(f'Peak: {max_rate_value:.2f}%\n{max_rate_date.strftime("%b %Y")}',
                     xy=(max_rate_date, max_rate_value),
                     xytext=(max_rate_date, max_rate_value + 0.5),
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                     fontsize=10, ha='center',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
        
        # Plot 2: Total Cases vs Total Deaths
        ax2.plot(global_daily['date'], global_daily['total_cases'], color='blue', label='Total Cases')
        ax2.plot(global_daily['date'], global_daily['total_deaths'], color='red', label='Total Deaths')
        ax2.set_title('Total Cases vs. Total Deaths Over Time', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Count (log scale)')
        ax2.set_yscale('log')
        ax2.legend()
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.tight_layout()
        plt.savefig('activity7_images/7.1_global_fatality_rate_over_time.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 7.1_global_fatality_rate_over_time.png")

    # ==========================================================================
    # TASK 2: Positivity rate vs total tests (logarithmic x-axis)
    # ==========================================================================
    print("\n3. Task 2: Positivity Rate vs Total Tests Analysis...")
    
    if 'positivity_rate' in df.columns:
        # Filter data for meaningful analysis
        test_data = df[(df['total_tests'] > 1000) & 
                       (df['total_cases'] > 100) & 
                       (df['positivity_rate'] <= 100) &
                       (df['positivity_rate'] > 0)].copy()
        
        if len(test_data) > 0:
            plt.figure(figsize=(15, 10))
            scatter = plt.scatter(test_data['total_tests'], test_data['positivity_rate'], 
                                 alpha=0.6, c=test_data['total_cases'], 
                                 cmap='viridis', s=30)
            plt.xscale('log')
            plt.xlabel('Total Tests (log scale)', fontsize=12)
            plt.ylabel('Positivity Rate (%)', fontsize=12)
            plt.title('COVID-19 Testing Effectiveness Analysis\nPositivity Rate vs Total Tests', 
                      fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            
            # Add colorbar
            cbar = plt.colorbar(scatter)
            cbar.set_label('Total Cases', fontsize=10)
            
            plt.tight_layout()
            plt.savefig('activity7_images/7.2_positivity_rate_vs_total_tests.png', 
                        dpi=300, bbox_inches='tight')
            plt.close()
            print("[OK] Saved: 7.2_positivity_rate_vs_total_tests.png")
        else:
            print("[WARNING] Insufficient testing data for positivity rate analysis")
    else:
        print("[WARNING] `positivity_rate` column not available for analysis.")

    # ==========================================================================
    # TASK 3: Fatality rate relationship with smoking
    # ==========================================================================
    print("\n4. Task 3: Fatality Rate vs Smoking Analysis...")
    
    smoking_cols = ['male_smokers', 'female_smokers']
    available_smoking_cols = [col for col in smoking_cols if col in df.columns]
    
    if available_smoking_cols:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        smoking_data = latest_df.dropna(subset=available_smoking_cols + ['fatality_rate'])
        
        if len(smoking_data) > 0:
            fig, axes = plt.subplots(1, len(available_smoking_cols), 
                                     figsize=(8 * len(available_smoking_cols), 6), squeeze=False)
            
            for i, col in enumerate(available_smoking_cols):
                sns.regplot(data=smoking_data, x=col, y='fatality_rate', ax=axes[0, i],
                            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
                axes[0, i].set_title(f'Fatality Rate vs {col.replace("_", " ").title()}', 
                                   fontweight='bold')
                axes[0, i].set_xlabel(f'{col.replace("_", " ").title()} (%)')
                axes[0, i].set_ylabel('Fatality Rate (%)')
                
                corr = smoking_data[[col, 'fatality_rate']].corr().iloc[0,1]
                axes[0, i].text(0.05, 0.95, f'Corr: {corr:.2f}', transform=axes[0, i].transAxes,
                                fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            plt.tight_layout()
            plt.savefig('activity7_images/7.3_fatality_rate_vs_smoking.png', 
                        dpi=300, bbox_inches='tight')
            plt.close()
            print("[OK] Saved: 7.3_fatality_rate_vs_smoking.png")
        else:
            print("[WARNING] Insufficient smoking data for analysis")
    else:
        print("[WARNING] No smoking data columns found in dataset.")

    # ==========================================================================
    # TASK 4: Heatmap: Hospital beds vs fatality rate
    # ==========================================================================
    print("\n5. Task 4: Hospital Beds vs Fatality Rate Analysis...")
    
    hospital_col = 'hospital_beds_per_thousand'
    if hospital_col in df.columns:
        latest_df = df.loc[df.groupby('location')['date'].idxmax()]
        hospital_data = latest_df.dropna(subset=[hospital_col, 'fatality_rate'])
        
        if len(hospital_data) > 10: # Need enough data for heatmap
            hospital_data['hosp_bed_bins'] = pd.qcut(hospital_data[hospital_col], q=5, duplicates='drop')
            hospital_data['fatality_rate_bins'] = pd.qcut(hospital_data['fatality_rate'], q=5, duplicates='drop')

            contingency_table = pd.crosstab(hospital_data['hosp_bed_bins'], hospital_data['fatality_rate_bins'])
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlGnBu')
            plt.title('Heatmap of Hospital Beds per Thousand vs. Fatality Rate', fontweight='bold')
            plt.xlabel('Fatality Rate (Quintiles)')
            plt.ylabel('Hospital Beds per Thousand (Quintiles)')
            plt.tight_layout()
            plt.savefig('activity7_images/7.4_hospital_beds_vs_fatality_rate.png', 
                        dpi=300, bbox_inches='tight')
            plt.close()
            print("[OK] Saved: 7.4_hospital_beds_vs_fatality_rate.png")
        else:
            print("[WARNING] Insufficient hospital beds data for heatmap analysis")
    else:
        print("[WARNING] `hospital_beds_per_thousand` column not found.")

    print("\n" + "="*80)
    print("ACTIVITY 7 COMPLETE!")
    print("Check 'activity7_images' folder for visualizations.")
    print("="*80)

if __name__ == "__main__":
    main() 