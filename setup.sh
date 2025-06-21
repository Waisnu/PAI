#!/bin/bash
# COVID-19 Analysis Project - Universal Setup Script
# Works on Windows (Git Bash), Mac, and Linux

set -e  # Exit on any error

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${CYAN}[SETUP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}===============================================${NC}"
    echo -e "${CYAN}  COVID-19 Analysis Project - Auto Setup${NC}"
    echo -e "${CYAN}===============================================${NC}"
    echo ""
}

# Detect operating system
detect_os() {
    # Check for Windows first by looking for common Windows indicators
    if [[ -n "$WINDIR" ]] || [[ -n "$windir" ]] || [[ "$OS" == "Windows_NT" ]] || [[ -f "/c/Windows/System32/cmd.exe" ]]; then
        OS="windows"
        print_status "Detected: Windows (Git Bash/MSYS/WSL)"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="mac"
        print_status "Detected: macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_status "Detected: Linux"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        OS="windows"
        print_status "Detected: Windows (Cygwin/MSYS)"
    else
        # Default to checking if we can find Windows-style paths
        if [ -d "/c/" ] || [ -d "/mnt/c/" ]; then
            OS="windows"
            print_status "Detected: Windows (WSL/Git Bash) - fallback detection"
        else
            OS="linux"
            print_warning "Unknown OS: $OSTYPE - defaulting to Linux-style commands"
        fi
    fi
}

# Check if Python is installed
check_python() {
    if ! command -v python &> /dev/null; then
        if ! command -v python3 &> /dev/null; then
            print_error "Python is not installed or not in PATH"
            echo "Please install Python 3.8+ from https://python.org"
            if [[ "$OS" == "mac" ]]; then
                echo "On macOS, you can also use: brew install python"
            elif [[ "$OS" == "linux" ]]; then
                echo "On Linux, try: sudo apt install python3 python3-pip"
            fi
            exit 1
        else
            PYTHON_CMD="python3"
        fi
    else
        PYTHON_CMD="python"
    fi
    
    print_status "Python found: $($PYTHON_CMD --version)"
}

# Create virtual environment
create_venv() {
    if [ -d "venv" ]; then
        print_status "Virtual environment already exists"
    else
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        if [ $? -ne 0 ]; then
            print_error "Failed to create virtual environment"
            exit 1
        fi
        print_success "Virtual environment created"
    fi
}

# Activate virtual environment and set paths
activate_venv() {
    # Try to find the correct Python executable in the virtual environment
    VENV_PYTHON=""
    VENV_PIP=""
    
    # Possible paths to check (in order of preference)
    PYTHON_PATHS=(
        "venv/Scripts/python.exe"  # Windows
        "venv/Scripts/python"      # Windows (no .exe)
        "venv/bin/python"          # Unix-like
        "venv/bin/python3"         # Unix-like with python3
    )
    
    PIP_PATHS=(
        "venv/Scripts/pip.exe"     # Windows
        "venv/Scripts/pip"         # Windows (no .exe)
        "venv/bin/pip"             # Unix-like
        "venv/bin/pip3"            # Unix-like with pip3
    )
    
    # Find Python executable
    for path in "${PYTHON_PATHS[@]}"; do
        if [ -f "$path" ]; then
            VENV_PYTHON="$path"
            break
        fi
    done
    
    # Find pip executable
    for path in "${PIP_PATHS[@]}"; do
        if [ -f "$path" ]; then
            VENV_PIP="$path"
            break
        fi
    done
    
    # Verify we found Python
    if [ -z "$VENV_PYTHON" ] || [ ! -f "$VENV_PYTHON" ]; then
        print_error "Virtual environment activation failed - Python executable not found"
        print_error "Checked paths: ${PYTHON_PATHS[*]}"
        exit 1
    fi
    
    print_success "Virtual environment paths set: $VENV_PYTHON"
}

# Install dependencies
install_deps() {
    print_status "Upgrading pip..."
    $VENV_PYTHON -m pip install --upgrade pip
    
    print_status "Installing dependencies from requirements.txt..."
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    $VENV_PYTHON -m pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Check if activities have already been run
check_existing_outputs() {
    print_status "Checking for existing outputs..."
    
    ACTIVITY_FOLDERS=(
        "activity1_images"
        "activity2_images" 
        "activity3_images"
        "activity4_images"
        "activity5_images"
        "activity6_images"
        "activity7_images"
    )
    
    DATA_FILES=(
        "covid_data_cleaned.csv"
        "covid_data_processed.csv"
    )
    
    existing_folders=0
    existing_files=0
    
    # Check image folders
    for folder in "${ACTIVITY_FOLDERS[@]}"; do
        if [ -d "$folder" ] && [ "$(ls -A $folder 2>/dev/null | wc -l)" -gt 0 ]; then
            existing_folders=$((existing_folders + 1))
            print_success "Found: $folder/ ($(ls $folder/*.png 2>/dev/null | wc -l) images)"
        fi
    done
    
    # Check data files
    for file in "${DATA_FILES[@]}"; do
        if [ -f "$file" ]; then
            existing_files=$((existing_files + 1))
            file_size=$(ls -lh "$file" | awk '{print $5}')
            print_success "Found: $file ($file_size)"
        fi
    done
    
    total_folders=${#ACTIVITY_FOLDERS[@]}
    total_files=${#DATA_FILES[@]}
    
    if [ $existing_folders -eq $total_folders ] && [ $existing_files -eq $total_files ]; then
        echo ""
        print_success "All outputs already exist! Skipping data processing."
        echo -e "${YELLOW}To regenerate everything, run: $VENV_PYTHON run.py clean && $VENV_PYTHON run.py all${NC}"
        return 1  # Skip processing
    elif [ $existing_folders -gt 0 ] || [ $existing_files -gt 0 ]; then
        echo ""
        print_warning "Some outputs exist ($existing_folders/$total_folders folders, $existing_files/$total_files files)"
        print_status "Running activities to complete missing outputs..."
        return 0  # Continue processing
    else
        echo ""
        print_status "No existing outputs found. Running full analysis..."
        return 0  # Continue processing
    fi
}

# Run the project
run_project() {
    echo ""
    echo -e "${CYAN}===============================================${NC}"
    echo -e "${CYAN}  Checking Project Status...${NC}"
    echo -e "${CYAN}===============================================${NC}"
    echo ""
    
    # Check if we need to run activities
    if check_existing_outputs; then
        echo ""
        echo -e "${CYAN}===============================================${NC}"
        echo -e "${CYAN}  Running COVID-19 Analysis Activities...${NC}"
        echo -e "${CYAN}===============================================${NC}"
        echo ""
        
        $VENV_PYTHON run.py all
        
        if [ $? -eq 0 ]; then
            print_success "All activities completed successfully!"
        else
            print_warning "Some activities may have had issues"
        fi
    fi
}

# Show final summary and exit message
show_completion_summary() {
    echo ""
    echo -e "${CYAN}===============================================${NC}"
    echo -e "${CYAN}       COVID-19 ANALYSIS SETUP COMPLETE!${NC}"
    echo -e "${CYAN}===============================================${NC}"
    echo ""
    
    # Count final outputs
    total_images=0
    if [ -d "activity1_images" ]; then total_images=$((total_images + $(ls activity1_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity2_images" ]; then total_images=$((total_images + $(ls activity2_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity3_images" ]; then total_images=$((total_images + $(ls activity3_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity4_images" ]; then total_images=$((total_images + $(ls activity4_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity5_images" ]; then total_images=$((total_images + $(ls activity5_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity6_images" ]; then total_images=$((total_images + $(ls activity6_images/*.png 2>/dev/null | wc -l))); fi
    if [ -d "activity7_images" ]; then total_images=$((total_images + $(ls activity7_images/*.png 2>/dev/null | wc -l))); fi
    
    echo -e "${GREEN}✅ Project Status:${NC}"
    echo -e "   📊 Total Visualizations: ${YELLOW}$total_images images${NC}"
    if [ -f "covid_data_cleaned.csv" ]; then
        cleaned_size=$(ls -lh covid_data_cleaned.csv | awk '{print $5}')
        echo -e "   📄 Cleaned Dataset: ${YELLOW}$cleaned_size${NC}"
    fi
    if [ -f "covid_data_processed.csv" ]; then
        processed_size=$(ls -lh covid_data_processed.csv | awk '{print $5}')
        echo -e "   📄 Processed Dataset: ${YELLOW}$processed_size${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🚀 Next Steps:${NC}"
    echo -e "   ${YELLOW}• View images in the activity*_images/ folders${NC}"
    echo -e "   • Run individual activities: ${BLUE}$VENV_PYTHON run.py activity1${NC}"
    echo -e "   • Clean and regenerate: ${BLUE}$VENV_PYTHON run.py clean && $VENV_PYTHON run.py all${NC}"
    
    echo ""
    echo -e "${BLUE}🔧 Virtual Environment:${NC}"
    if [[ "$OS" == "windows" ]]; then
        echo -e "   Activate: ${YELLOW}source venv/Scripts/activate${NC} ${CYAN}(Git Bash)${NC}"
        echo -e "            ${YELLOW}venv\\Scripts\\activate.bat${NC} ${CYAN}(Command Prompt)${NC}"
    else
        echo -e "   Activate: ${YELLOW}source venv/bin/activate${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 COVID-19 Analysis Environment Ready!${NC}"
    echo -e "${CYAN}===============================================${NC}"
}

# Main execution
main() {
    print_header
    
    detect_os
    check_python
    create_venv
    activate_venv
    install_deps
    run_project
    
    show_completion_summary
    
    # Keep terminal open on Windows
    if [[ "$OS" == "windows" ]]; then
        echo ""
        echo -e "${YELLOW}Press Enter to exit...${NC}"
        read
    fi
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${YELLOW}[WARNING]${NC} Setup interrupted by user"; exit 1' INT

# Run main function
main "$@" 