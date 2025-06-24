const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Colors for better output
const colors = {
    cyan: '\x1b[36m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    reset: '\x1b[0m'
};

const printStatus = (msg) => console.log(`${colors.cyan}[SETUP]${colors.reset} ${msg}`);
const printSuccess = (msg) => console.log(`${colors.green}[OK]${colors.reset} ${msg}`);
const printWarning = (msg) => console.log(`${colors.yellow}[WARNING]${colors.reset} ${msg}`);
const printError = (msg) => console.log(`${colors.red}[ERROR]${colors.reset} ${msg}`);

const printHeader = () => {
    console.log(`${colors.cyan}===============================================${colors.reset}`);
    console.log(`${colors.cyan}  COVID-19 Analysis Project - Auto Setup${colors.reset}`);
    console.log(`${colors.cyan}===============================================${colors.reset}`);
    console.log('');
};

const runCommand = (command) => {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                printError(`Failed to execute: ${command}`);
                console.error(stderr);
                reject(error);
                return;
            }
            resolve(stdout.trim());
        });
    });
};

async function checkPython() {
    printStatus('Checking for Python...');
    try {
        await runCommand('python --version');
        printSuccess('Python found.');
        return 'python';
    } catch (e) {
        try {
            await runCommand('python3 --version');
            printSuccess('Python3 found.');
            return 'python3';
        } catch (e2) {
            printError('Python is not installed or not in PATH.');
            console.log('Please install Python 3.8+ from https://python.org');
            process.exit(1);
        }
    }
}

async function createVenv(pythonCmd) {
    printStatus('Creating virtual environment...');
    if (fs.existsSync('venv')) {
        printStatus('Virtual environment already exists.');
        return;
    }
    try {
        await runCommand(`${pythonCmd} -m venv venv`);
        printSuccess('Virtual environment created.');
    } catch (e) {
        printError('Failed to create virtual environment.');
        process.exit(1);
    }
}

function getVenvPython() {
    const platform = process.platform;
    if (platform === 'win32') {
        return path.join('venv', 'Scripts', 'python.exe');
    }
    return path.join('venv', 'bin', 'python');
}

async function installDependencies(venvPython) {
    printStatus('Installing dependencies...');
    if (!fs.existsSync('requirements.txt')) {
        printError('requirements.txt not found.');
        process.exit(1);
    }

    try {
        printStatus('Upgrading pip...');
        await runCommand(`${venvPython} -m pip install --upgrade pip`);
        printStatus('Installing from requirements.txt...');
        await runCommand(`${venvPython} -m pip install -r requirements.txt`);
        printSuccess('✅ Dependencies installed successfully.');
    } catch (e) {
        printError('Failed to install dependencies.');
        process.exit(1);
    }
}

// async function runAnalysis(venvPython) {
//     printStatus('Running COVID-19 Analysis Activities...');
//     try {
//         await runCommand(`${venvPython} run.py all`);
//         printSuccess('All activities completed successfully!');
//     } catch (e) {
//         printError('Failed to run analysis script.');
//         process.exit(1);
//     }
// }


async function main() {
    printHeader();
    const pythonCmd = await checkPython();
    await createVenv(pythonCmd);
    const venvPython = getVenvPython();
    await installDependencies(venvPython);
    // await runAnalysis(venvPython);
    printSuccess(' Setup complete! You can re-run the analysis anytime with `npm run all`.');
    printSuccess(' Or you can run the specific activity with: ');
    printSuccess('🔥 `npm run activity-1`');
    printSuccess('🔥 `npm run activity-2`');
    printSuccess('🔥 `npm run activity-3`');
    printSuccess('🔥 `npm run activity-4`');
    printSuccess('🔥 `npm run activity-5`');
    printSuccess('🔥 `npm run activity-6`');
    printSuccess('🔥 `npm run activity-7`');
}

main(); 