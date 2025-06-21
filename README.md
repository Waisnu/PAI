# COVID-19 Data Analysis Project

**A comprehensive COVID-19 data analysis system with automated setup for Windows, macOS, and Linux.**

---

## 🚀 **QUICK START (One Command)**

### **Universal Setup (All Operating Systems)**
```bash
bash setup.sh
```

**That's it!** The script will:
- ✅ Auto-detect your operating system
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Run complete COVID-19 analysis
- ✅ Generate 25+ visualizations
- ✅ Skip regeneration if outputs already exist

---

## 📋 **Requirements**

- **Python 3.8+** ([Download here](https://python.org))
- **Git Bash** (Windows users - comes with Git)
- **Internet connection** (for package installation)

---

## 🎯 **Setup Options**

### **Option 1: Universal Script (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd python-scripts

# Run setup (works on all platforms)
bash setup.sh
```

### **Option 2: Platform-Specific**

#### **Windows**
```batch
# Double-click method
setup.bat

# Or PowerShell
.\setup.ps1

# Or Git Bash
bash setup.sh
```

#### **macOS/Linux**
```bash
# Make executable (optional)
chmod +x setup.sh

# Run setup
./setup.sh
```

#### **Manual Setup (Any Platform)**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows Git Bash:
source venv/Scripts/activate
# Windows CMD:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run analysis
python run.py all
```

---

## 📊 **What You'll Get**

### **Generated Output**
```
📁 activity1_images/     ← Data loading & exploration (4 plots)
📁 activity2_images/     ← Data cleaning & features (3 plots)  
📁 activity3_images/     ← Global overview (4 plots)
📁 activity4_images/     ← Regional analysis (4 plots)
📁 activity5_images/     ← Time series analysis (5 plots)
📁 activity6_images/     ← Country comparisons (6 plots)
📁 activity7_images/     ← Summary dashboards (2 plots)

📄 covid_data_cleaned.csv      ← Cleaned dataset (87MB)
📄 covid_data_processed.csv    ← Feature-engineered dataset (180MB)
```

### **Analysis Coverage**
- **358,838 data records** from January 2020 to November 2023
- **255 countries/regions** analyzed
- **601+ million COVID cases** processed
- **29 visualizations** generated automatically

---

## ⚡ **Performance & Optimization**

### **Smart Skip System**
- **First run**: 5-10 minutes (full setup + processing)
- **Subsequent runs**: 30 seconds (skips existing outputs)
- **Partial runs**: Only regenerates missing files

### **File Size Expectations**
- Total output: ~300MB (datasets + images)
- Individual images: 1-5MB each (high-resolution PNG)
- Processing datasets: 87MB + 180MB

---

## 🎯 **Available Commands**

| Command | Description | Time |
|---------|-------------|------|
| `bash setup.sh` | Complete setup + run all | 5-10 min |
| `python run.py all` | Run all 7 activities | 3-5 min |
| `python run.py activity1` | Data loading only | 30-60 sec |
| `python run.py activity2` | Data processing only | 30-60 sec |
| `python run.py activity3` | Global analysis only | 30-60 sec |
| `python run.py activity4` | Regional analysis only | 30-60 sec |
| `python run.py activity5` | Time series analysis only | 30-60 sec |
| `python run.py activity6` | Country analysis only | 30-60 sec |
| `python run.py activity7` | Summary dashboards only | 30-60 sec |
| `python run.py clean` | Remove all generated files | 5 sec |
| `python run.py setup` | Setup environment only | 2-3 min |

---

## 🔧 **Virtual Environment Management**

### **Activation Commands**
```bash
# Windows (Git Bash)
source venv/Scripts/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### **Deactivation**
```bash
deactivate
```

---

## 🆘 **Troubleshooting**

### **Common Issues**

#### **"Python not found"**
```bash
# Install Python from python.org
# Windows: Check "Add Python to PATH" during installation
# macOS: brew install python3
# Linux: sudo apt install python3 python3-pip
```

#### **"bash: command not found" (Windows)**
```bash
# Install Git for Windows (includes Git Bash)
# Or use alternative methods:
setup.bat          # Double-click
.\setup.ps1         # PowerShell
python run.py setup # Direct Python
```

#### **"Permission denied" (Windows)**
```powershell
# Run in PowerShell as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **"Virtual environment failed"**
```bash
# Ensure you have write permissions in the directory
# Try running as administrator/sudo if needed
# Check available disk space (needs ~500MB)
```

#### **"Dependencies installation failed"**
```bash
# Check internet connection
# Try upgrading pip first:
python -m pip install --upgrade pip
# Then retry:
pip install -r requirements.txt
```

#### **"Images not generating"**
```bash
# Check if matplotlib backend is available
# On Linux, may need: sudo apt-get install python3-tk
# On macOS, ensure XQuartz is installed
```

---

## 📈 **Project Structure**

```
covid-analysis/
├── 🚀 setup.sh              ← Universal setup script
├── 🪟 setup.bat             ← Windows batch file
├── 🪟 setup.ps1             ← PowerShell script
├── ⚙️  run.py               ← Main runner (npm-style commands)
├── 📄 requirements.txt      ← Python dependencies
├── 📊 README.md             ← This file
├── ⚡ QUICK_START.txt       ← Ultra-quick reference
│
├── 📁 data/                 ← Raw COVID-19 datasets
│   ├── owid-covid-data.csv
│   └── owid-covid-data-backup-clean.csv
│
├── 📁 activities/           ← Analysis modules
│   ├── activity-1/          ← Data loading & exploration
│   ├── activity-2/          ← Data cleaning & feature engineering
│   ├── activity-3/          ← Global trends analysis
│   ├── activity-4/          ← Regional comparisons
│   ├── activity-5/          ← Time series analysis
│   ├── activity-6/          ← Country-specific analysis
│   └── activity-7/          ← Executive summary dashboards
│
└── 📁 [Generated Output]    ← Created after running
    ├── activity1_images/    ← (4 visualizations)
    ├── activity2_images/    ← (3 visualizations)
    ├── activity3_images/    ← (4 visualizations)
    ├── activity4_images/    ← (4 visualizations)
    ├── activity5_images/    ← (5 visualizations)
    ├── activity6_images/    ← (6 visualizations)
    ├── activity7_images/    ← (2 visualizations)
    ├── covid_data_cleaned.csv
    ├── covid_data_processed.csv
    └── venv/               ← Python virtual environment
```

---

## 📚 **Activity Descriptions**

| Activity | Purpose | Outputs | Key Insights |
|----------|---------|---------|--------------|
| **Activity 1** | Data loading & basic exploration | 4 plots + cleaned CSV | Data quality, coverage, missing values |
| **Activity 2** | Data cleaning & feature engineering | 3 plots + processed CSV | New features, CFR, rates per million |
| **Activity 3** | Global COVID-19 overview | 4 plots | Worldwide patterns, peak periods |
| **Activity 4** | Regional analysis | 4 plots | Continental comparisons, regional trends |
| **Activity 5** | Time series analysis | 5 plots | Seasonal patterns, rolling averages |
| **Activity 6** | Country-specific analysis | 6 plots | Top performers, population correlations |
| **Activity 7** | Executive summary | 2 dashboards | High-level insights, final report |

---

## 🔬 **Technical Details**

### **Dependencies**
- **numpy** ≥1.20.0 - Numerical computations
- **pandas** ≥1.3.0 - Data manipulation  
- **matplotlib** ≥3.3.0 - Plotting
- **seaborn** ≥0.11.0 - Statistical visualizations

### **Data Source**
- **Our World in Data COVID-19 dataset**
- Updated through November 2023
- 67 original columns, 73 after feature engineering
- Global coverage: 255 countries/regions

### **Output Specifications**
- **Image format**: PNG (high-resolution, 300 DPI)
- **File naming**: Numbered for easy organization
- **Color scheme**: Professional, colorblind-friendly
- **Size optimization**: Balanced quality vs. file size

---

## 🚦 **Deployment Checklist**

### **Before Sharing**
- [ ] Python 3.8+ installed
- [ ] Git installed (for cloning)
- [ ] Internet connection available
- [ ] ~500MB free disk space

### **After Cloning**
- [ ] Navigate to project directory
- [ ] Run `bash setup.sh`
- [ ] Wait for completion (5-10 minutes)
- [ ] Check generated folders
- [ ] Review visualizations

### **Success Indicators**
- [ ] 7 activity image folders created
- [ ] 2 CSV files generated
- [ ] No error messages
- [ ] Setup completion message displayed

---

## 📞 **Support**

If you encounter any issues:

1. **Check Requirements**: Ensure Python 3.8+ is installed
2. **Try Alternative**: Use `setup.bat` (Windows) or `python run.py setup`
3. **Clean Start**: Run `python run.py clean` then restart
4. **Manual Setup**: Follow the manual installation steps above
5. **Check Logs**: Error messages usually indicate missing dependencies

---

## 🎉 **Success!**

When setup completes successfully, you should see:
```
🎉 COVID-19 Analysis Environment Ready!
📊 Total Visualizations: 29 images
📄 Cleaned Dataset: 87M
📄 Processed Dataset: 180M
```

The project is now ready for analysis and review! 