# COVID-19 Analysis - Deployment Guide for Instructors

## 🎯 **Purpose**
This project provides a complete COVID-19 data analysis system that automatically:
- Sets up Python environment
- Processes 358k+ COVID data records  
- Generates 29 professional visualizations
- Creates comprehensive pandemic analysis (2020-2023)

## ⚡ **Quick Deploy (30 seconds)**

### **Step 1: Clone Repository**
```bash
git clone <repository-url>
cd python-scripts
```

### **Step 2: Run Setup**
```bash
bash setup.sh
```

**That's it!** The script handles everything automatically.

---

## 🖥️ **Platform-Specific Instructions**

### **Windows Users**
```bash
# Option 1: Git Bash (Recommended)
bash setup.sh

# Option 2: Double-click
setup.bat

# Option 3: PowerShell
.\setup.ps1
```

### **macOS/Linux Users**
```bash
# Make executable (optional)
chmod +x setup.sh

# Run setup
./setup.sh
```

---

## 📊 **Expected Results**

### **Processing Time**
- **First run**: 5-10 minutes
- **Subsequent runs**: 30 seconds (smart skip)

### **Generated Output**
```
📁 Project will create:
├── activity1_images/     (4 data exploration plots)
├── activity2_images/     (3 data processing plots)
├── activity3_images/     (4 global analysis plots)
├── activity4_images/     (4 regional analysis plots)
├── activity5_images/     (5 time series plots)
├── activity6_images/     (6 country comparison plots)
├── activity7_images/     (2 executive dashboards)
├── covid_data_cleaned.csv      (87MB processed data)
└── covid_data_processed.csv    (180MB final dataset)
```

### **Data Coverage**
- **358,838 data records** across 255 countries
- **January 2020 - November 2023** timeline
- **601+ million COVID cases** analyzed
- **High-resolution PNG plots** (300 DPI)

---

## ✅ **Success Indicators**

When setup completes, you'll see:
```
🎉 COVID-19 Analysis Environment Ready!
📊 Total Visualizations: 29 images
📄 Cleaned Dataset: 87M
📄 Processed Dataset: 180M
```

---

## 🔧 **Requirements Check**

### **Before Running**
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed (for cloning)
- [ ] Internet connection available
- [ ] 500MB+ free disk space

### **Install Python (if needed)**
- **Windows**: [python.org](https://python.org) - Check "Add to PATH"
- **macOS**: `brew install python3` or [python.org](https://python.org)
- **Linux**: `sudo apt install python3 python3-pip`

---

## 🚨 **Common Issues & Solutions**

### **"bash: command not found" (Windows)**
```bash
# Solution: Install Git for Windows (includes Git Bash)
# Alternative: Use setup.bat instead
```

### **"Python not found"**
```bash
# Solution: Install Python from python.org
# Make sure "Add Python to PATH" is checked
```

### **"Permission denied"**
```powershell
# Windows PowerShell: Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **"Virtual environment failed"**
```bash
# Solution: Ensure write permissions in directory
# Try running as administrator if needed
```

---

## 🎯 **Testing the Deployment**

### **Quick Verification**
1. Check folders exist: `ls activity*_images/`
2. Count files: Should see 29 total PNG files
3. Check data files: `ls *.csv` (should show 2 files)
4. Verify sizes: Cleaned ~87MB, Processed ~180MB

### **Individual Activity Testing**
```bash
# After setup, you can run individual parts:
python run.py activity1    # Test data loading
python run.py activity2    # Test data processing  
python run.py activity7    # Test summary dashboard
```

---

## 🧹 **Reset/Clean**

### **Start Fresh**
```bash
# Remove all generated files and restart
python run.py clean
bash setup.sh
```

### **Remove Virtual Environment**
```bash
# Complete clean slate
rm -rf venv/
rm -rf activity*_images/
rm -f covid_data_*.csv
bash setup.sh
```

---

## 📞 **Support Escalation**

If automatic setup fails:

1. **Try manual setup**: See README.md Section "Manual Setup"
2. **Check logs**: Script shows detailed error messages
3. **Verify requirements**: Python 3.8+, pip, internet access
4. **Alternative runners**: `python run.py setup` then `python run.py all`

---

## 🎉 **Success!**

Once deployed successfully:
- Open any `activity*_images/` folder to view visualizations
- Review COVID-19 trends across multiple dimensions
- Use data files for further analysis if needed
- Project is self-contained and requires no additional setup

**Total deployment time: 5-10 minutes for complete COVID-19 analysis system!** 