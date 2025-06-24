# COVID-19 Data Analysis Project

**A comprehensive COVID-19 data analysis system with automated setup for Windows, macOS, and Linux.**

---

## 🚀 **QUICK START**

### **Clone & Setup (One Command)**
```bash
git clone <repository-url>
cd python-scripts
npm run setup
```

**That's it!** The setup script will:
- ✅ Auto-detect your operating system  
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Ready to run activities

---

## 📋 **Requirements**

- **Python 3.8+** ([Download here](https://python.org))
- **Git** (for cloning)
- **npm** (optional - for npm-style commands)

---

## 🎯 **Run Activities**

### **NPM-Style Commands (Recommended)**
```bash
npm run setup          # Initial setup
npm run activity-1     # Data loading & exploration
npm run activity-2     # Data cleaning & features  
npm run activity-3     # Global overview
npm run activity-4     # Regional analysis
npm run activity-5     # Time series analysis
npm run activity-6     # Country comparisons
npm run activity-7     # Additional insights
npm run all           # Run all activities
npm run clean         # Remove generated files
```

### **Python Commands (Alternative)**
```bash
python run.py setup    # Initial setup
python run.py activity1 # Individual activities
python run.py all      # Run all activities
python run.py clean    # Clean outputs
```

### **Manual Setup (Any Platform)**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/Scripts/activate     # Windows Git Bash
# OR
venv\Scripts\activate.bat        # Windows CMD  
# OR  
source venv/bin/activate         # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run analysis
python run.py all
```

---

## 📊 **What You'll Get**

### **Activity Outputs**
```
📁 activity1_images/    ← Data loading & exploration (4 plots)
📁 activity2_images/    ← Data cleaning & features (3 plots)  
📁 activity3_images/    ← Global overview (4 plots)
📁 activity4_images/    ← Regional analysis (4 plots)
📁 activity5_images/    ← Time series analysis (5 plots)
📁 activity6_images/    ← Country comparisons (6 plots)
📁 activity7_images/    ← Additional insights (4 plots)

📄 covid_data_cleaned.csv      ← Cleaned dataset
📄 covid_data_processed.csv    ← Feature-engineered dataset
```

### **Analysis Coverage**
- **300K+ data records** from 2020-2023
- **200+ countries/regions** analyzed  
- **600M+ COVID cases** processed
- **28 visualizations** generated automatically

---

## ⚡ **Performance**

- **First run**: 5-10 minutes (setup + processing)
- **Subsequent runs**: 30 seconds (skips existing outputs)
- **Individual activities**: 30-60 seconds each

---

## 🔧 **Available Commands**

| Command | Description | Time |
|---------|-------------|------|
| `npm run setup` | Complete environment setup | 2-3 min |
| `npm run all` | Run all 7 activities | 3-5 min |
| `npm run activity-1` | Data loading only | 30-60 sec |
| `npm run activity-2` | Data cleaning only | 30-60 sec |
| `npm run activity-3` | Global analysis only | 30-60 sec |
| `npm run activity-4` | Regional analysis only | 30-60 sec |
| `npm run activity-5` | Time series analysis only | 30-60 sec |
| `npm run activity-6` | Country analysis only | 30-60 sec |
| `npm run activity-7` | Additional insights only | 30-60 sec |
| `npm run clean` | Remove all generated files | 5 sec |

---

## 🆘 **Troubleshooting**

### **"Python not found"**
```bash
# Install Python from python.org
# Windows: Check "Add Python to PATH" during installation
# macOS: brew install python3
# Linux: sudo apt install python3 python3-pip
```

### **"npm not found"**
```bash
# Use Python commands instead:
python run.py setup
python run.py all
```

### **"Permission denied" (Windows)**
```powershell
# Run PowerShell as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Virtual environment issues**
```bash
# Manual activation:
# Windows: venv\Scripts\activate.bat
# macOS/Linux: source venv/bin/activate
```

---

## 📋 **Project Brief Alignment**

This project implements all requirements from the BDSE PAI Module:

### **Activity 1: Data Loading and Exploration**
- ✅ Load COVID-19 DataFrame  
- ✅ Display first/last 5 rows
- ✅ Check missing values & handle them
- ✅ Remove columns >90% missing
- ✅ Convert date column to datetime

### **Activity 2: Data Cleaning and Feature Engineering**  
- ✅ Impute missing values
- ✅ Remove duplicate rows
- ✅ Create new features (year/month extraction)
- ✅ Explore unique countries

### **Activity 3: Worldwide COVID-19 Overview**
- ✅ WHO Regions with cases/deaths (bar plots)
- ✅ Worldwide monthly trend (line plot)
- ✅ Correlation heatmap (cases vs deaths)
- ✅ Time evolution for specific location

### **Activity 4: Regional Analysis**
- ✅ Grouped bar chart (new cases by continent/month)
- ✅ Distribution by year (box plot)
- ✅ Deaths across continents (bar plot)
- ✅ Month-by-month cases analysis

### **Activity 5: Time Series Analysis**
- ✅ Daily trend of new cases/deaths (line plots)
- ✅ Daily averages globally  
- ✅ Vaccination coverage over time
- ✅ Tests and positive rate analysis

### **Activity 6: In-Depth Country Analysis**
- ✅ Specific country cases/deaths over time
- ✅ User input for country/metric selection
- ✅ Continental distribution (box plot)
- ✅ Year-wise monthly trends by country

### **Activity 7: Additional Insights**  
- ✅ Fatality rate over time globally
- ✅ Positivity rate vs total tests (log scale)
- ✅ Fatality rate relationship with smoking
- ✅ Heatmap: Hospital beds vs fatality rate

---

## 📝 **Notes**

- Virtual environments (`venv/`, `covid_analysis_env/`) are excluded from git
- Generated images and processed data are excluded from git  
- All outputs are regenerated automatically when needed
- Use `npm run clean` to reset and start fresh 