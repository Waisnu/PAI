#!/usr/bin/env python3
"""
COVID-19 Activities Runner (npm-style)
Usage: python run.py <command>

Commands:
  activity1    - Run Activity 1: Data Loading and Basic Analysis
  activity2    - Run Activity 2: Data Cleaning and Feature Engineering  
  activity3    - Run Activity 3: Worldwide COVID-19 Overview
  activity4    - Run Activity 4: Regional Analysis
  activity5    - Run Activity 5: Time Series Analysis
  activity6    - Run Activity 6: Country Analysis
  activity7    - Run Activity 7: Summary Dashboard
  all          - Run all activities in sequence
  setup        - Setup virtual environment and install dependencies
  clean        - Clean all generated images and processed data
  help         - Show this help message
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a system command and handle errors"""
    print(f">> {description}")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def setup_environment():
    """Setup virtual environment and dependencies"""
    print("=" * 60)
    print("SETTING UP COVID-19 ANALYSIS ENVIRONMENT")
    print("=" * 60)
    
    # Check Python version
    try:
        python_version = subprocess.run(['python', '--version'], capture_output=True, text=True, check=True)
        print(f"[SETUP] Python found: {python_version.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("[ERROR] Python not found or not in PATH")
        print("Please install Python 3.8+ from https://python.org")
        return False
    
    # Create venv if it doesn't exist
    if not os.path.exists('venv'):
        print("[SETUP] Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            print("[ERROR] Failed to create virtual environment")
            print("Make sure you have permissions to create folders in this directory")
            return False
    else:
        print("[SETUP] Virtual environment already exists")
    
    # Upgrade pip and install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\python.exe -m pip install --upgrade pip"
        install_cmd = "venv\\Scripts\\python.exe -m pip install -r requirements.txt"
    else:  # Linux/Mac
        pip_cmd = "venv/bin/python -m pip install --upgrade pip"
        install_cmd = "venv/bin/python -m pip install -r requirements.txt"
    
    print("[SETUP] Upgrading pip...")
    if not run_command(pip_cmd, "Upgrading pip"):
        print("[WARNING] Pip upgrade failed, continuing anyway...")
    
    print("[SETUP] Installing dependencies from requirements.txt...")
    if not run_command(install_cmd, "Installing dependencies"):
        print("[ERROR] Failed to install dependencies")
        print("Check if requirements.txt exists and contains valid packages")
        return False
    
    print("[OK] Setup complete!")
    print("\n" + "="*50)
    print("ENVIRONMENT READY!")
    print("="*50)
    print("Next steps:")
    if os.name == 'nt':
        print("1. Activate: venv\\Scripts\\activate")
    else:
        print("1. Activate: source venv/bin/activate")
    print("2. Run all activities: python run.py all")
    print("3. Or run individual: python run.py activity1")
    print("\nYou can also just run 'python run.py all' directly!")
    return True

def clean_outputs():
    """Clean all generated files"""
    print("[CLEAN] Cleaning generated files...")
    
    # Remove image folders
    image_folders = [f"activity{i}_images" for i in range(1, 8)]
    for folder in image_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  [OK] Removed {folder}/")
    
    # Remove processed data files
    data_files = ['covid_data_cleaned.csv', 'covid_data_processed.csv']
    for file in data_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"  [OK] Removed {file}")
    
    print("[OK] Cleanup complete!")

def run_activity(activity_num):
    """Run a specific activity"""
    activity_file = f"activities/activity-{activity_num}/activity-{activity_num}.py"
    
    if not os.path.exists(activity_file):
        print(f"[ERROR] Activity {activity_num} not found: {activity_file}")
        return False
    
    print("=" * 60)
    print(f"RUNNING ACTIVITY {activity_num}")
    print("=" * 60)
    
    return run_command(f"python {activity_file}", f"Activity {activity_num}")

def run_all_activities():
    """Run all activities in sequence"""
    print("=" * 60)
    print("RUNNING ALL COVID-19 ACTIVITIES")
    print("=" * 60)
    
    success_count = 0
    total_activities = 7
    
    for i in range(1, total_activities + 1):
        print(f"\n{'='*20} ACTIVITY {i} {'='*20}")
        if run_activity(i):
            success_count += 1
            print(f"[OK] Activity {i} completed successfully!")
        else:
            print(f"[ERROR] Activity {i} failed!")
            print("Continuing with next activity...")
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"[OK] Completed: {success_count}/{total_activities} activities")
    
    if success_count == total_activities:
        print("*** ALL ACTIVITIES COMPLETED SUCCESSFULLY! ***")
        print("\nGenerated folders:")
        for i in range(1, total_activities + 1):
            folder = f"activity{i}_images"
            if os.path.exists(folder):
                file_count = len([f for f in os.listdir(folder) if f.endswith('.png')])
                print(f"  >> {folder}/ ({file_count} images)")
    else:
        print(f"[WARNING] {total_activities - success_count} activities had issues")

def show_help():
    """Show help message"""
    print(__doc__)

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <command>")
        print("Run 'python run.py help' for available commands")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Command mapping
    commands = {
        'activity1': lambda: run_activity(1),
        'activity2': lambda: run_activity(2),
        'activity3': lambda: run_activity(3),
        'activity4': lambda: run_activity(4),
        'activity5': lambda: run_activity(5),
        'activity6': lambda: run_activity(6),
        'activity7': lambda: run_activity(7),
        'all': run_all_activities,
        'setup': setup_environment,
        'clean': clean_outputs,
        'help': show_help,
        '--help': show_help,
        '-h': show_help
    }
    
    if command in commands:
        try:
            commands[command]()
        except KeyboardInterrupt:
            print("\n[WARNING] Operation cancelled by user")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Available commands:", ", ".join(sorted(commands.keys())))
        sys.exit(1)

if __name__ == "__main__":
    main() 