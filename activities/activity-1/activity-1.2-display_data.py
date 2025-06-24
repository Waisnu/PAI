import pandas as pd
import os
# python activities/activity-1/activity-1.2-display_data.py

def display_ultra_clean_head_tail():
    """
    This script loads the COVID-19 dataset and displays the first and last 5 rows
    of a minimal set of key columns to ensure a clean, single-line output.
    """
    print("=" * 80)
    print("Activity 1.2: Display Core Data Snapshot")
    print("=" * 80)

    file_path = os.path.join("data", "owid-covid-data.csv")

    try:
        print(f"[*] Loading dataset from: {file_path}...")
        df = pd.read_csv(file_path)
        print("[OK] Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"[ERROR] The file was not found at: {file_path}")
        return

    # A minimal, core set of columns guaranteed to fit on one line.
    core_columns = [
        'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths'
    ]
    
    df_core = df[core_columns]

    print("\n" + "-" * 35)
    print("  First 5 Rows (Core Columns)")
    print("-" * 35)
    print(df_core.head().to_string())

    print("\n\n" + "*" * 80)
    print("*" + " " * 29 + "Last 5 Rows (Core Columns)" + " " * 29 + "*")
    print("*" * 80 + "\n")
    
    print(df_core.tail().to_string())
    
    print("\n" + "=" * 80)
    print("Script finished. If you see this line, the entire script has run.")
    print("=" * 80)


if __name__ == "__main__":
    pd.set_option('display.width', 200) 
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.max_colwidth', 15)
    display_ultra_clean_head_tail() 