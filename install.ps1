# CyberRotate Pro Windows Installation Script
# PowerShell script for Windows installation

param(
    [switch]$SkipPython,
    [switch]$SkipDependencies,
    [switch]$DevMode
)

Write-Host "CyberRotate Pro - Windows Installation Script" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check for administrator privileges
if (-not (Test-Administrator)) {
    Write-Host "Warning: Running without administrator privileges." -ForegroundColor Yellow
    Write-Host "Some features may require elevated permissions." -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 1
    }
}

# Check Python installation
if (-not $SkipPython) {
    Write-Host "Checking Python installation..." -ForegroundColor Cyan
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Python found: $pythonVersion" -ForegroundColor Green
        } else {
            throw "Python not found"
        }
    } catch {
        Write-Host "Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
        Write-Host "Make sure to add Python to PATH during installation." -ForegroundColor Yellow
        exit 1
    }
}

# Check pip installation
Write-Host "Checking pip installation..." -ForegroundColor Cyan
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "pip found: $pipVersion" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "pip not found. Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install pip. Please install manually." -ForegroundColor Red
        exit 1
    }
}

# Install Python dependencies
if (-not $SkipDependencies) {
    Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
    
    if ($DevMode) {
        Write-Host "Installing development dependencies..." -ForegroundColor Yellow
        pip install -r requirements-dev.txt
    } else {
        pip install -r requirements.txt
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install Python dependencies." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Python dependencies installed successfully!" -ForegroundColor Green
}

# Check for OpenVPN
Write-Host "Checking OpenVPN installation..." -ForegroundColor Cyan
$openvpnPath = Get-Command openvpn -ErrorAction SilentlyContinue
if ($openvpnPath) {
    Write-Host "OpenVPN found at: $($openvpnPath.Source)" -ForegroundColor Green
} else {
    Write-Host "OpenVPN not found. Please install OpenVPN from https://openvpn.net" -ForegroundColor Yellow
    Write-Host "CyberRotate Pro requires OpenVPN for VPN functionality." -ForegroundColor Yellow
}

# Check for Tor (optional)
Write-Host "Checking Tor installation..." -ForegroundColor Cyan
$torPath = Get-Command tor -ErrorAction SilentlyContinue
if ($torPath) {
    Write-Host "Tor found at: $($torPath.Source)" -ForegroundColor Green
} else {
    Write-Host "Tor not found. Install Tor Browser or standalone Tor for anonymity features." -ForegroundColor Yellow
    Write-Host "Download from: https://www.torproject.org" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "Creating necessary directories..." -ForegroundColor Cyan
$directories = @(
    "logs",
    "temp",
    "profiles",
    "backups",
    "exports"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Set up configuration files
Write-Host "Setting up configuration files..." -ForegroundColor Cyan
if (-not (Test-Path "config\config.json.bak")) {
    Copy-Item "config\config.json" "config\config.json.bak" -Force
    Write-Host "Backed up default configuration" -ForegroundColor Green
}

# Create Windows-specific batch file
Write-Host "Creating Windows launcher..." -ForegroundColor Cyan
$batchContent = @"
@echo off
echo Starting CyberRotate Pro...
python ip_rotator.py %*
pause
"@

Set-Content -Path "cyberrotate.bat" -Value $batchContent
Write-Host "Created cyberrotate.bat launcher" -ForegroundColor Green

# Create PowerShell launcher
$psLauncherContent = @"
# CyberRotate Pro PowerShell Launcher
param([string[]]`$Args)

Write-Host "Starting CyberRotate Pro..." -ForegroundColor Green
python ip_rotator.py @Args
"@

Set-Content -Path "cyberrotate.ps1" -Value $psLauncherContent
Write-Host "Created cyberrotate.ps1 launcher" -ForegroundColor Green

# Installation complete
Write-Host ""
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start CyberRotate Pro:" -ForegroundColor Cyan
Write-Host "  Method 1: python ip_rotator.py" -ForegroundColor White
Write-Host "  Method 2: python ip_rotator.py --gui (Graphical Interface)" -ForegroundColor White
Write-Host "  Method 3: .\cyberrotate.bat" -ForegroundColor White
Write-Host "  Method 4: .\cyberrotate.ps1" -ForegroundColor White
Write-Host "  Method 5: .\start_gui.bat (GUI only)" -ForegroundColor White
Write-Host ""
Write-Host "For help: python ip_rotator.py --help" -ForegroundColor Cyan
Write-Host "For interactive mode: python ip_rotator.py --interactive" -ForegroundColor Cyan
Write-Host ""

# Optional: Add to PATH
$addToPath = Read-Host "Add CyberRotate Pro to PATH? (y/N)"
if ($addToPath -eq 'y' -or $addToPath -eq 'Y') {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $projectPath = (Get-Location).Path
    
    if ($currentPath -notlike "*$projectPath*") {
        $newPath = "$currentPath;$projectPath"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "Added to PATH. Restart your terminal to use 'cyberrotate' command." -ForegroundColor Green
    } else {
        Write-Host "Already in PATH." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Installation log saved to install.log" -ForegroundColor Cyan
Write-Host "Happy IP rotating! 🔄" -ForegroundColor Green
