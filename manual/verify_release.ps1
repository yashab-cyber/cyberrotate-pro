# CyberRotate Pro Manual Release Verification Script (PowerShell)
# This script verifies that all manual files are present and ready for release

Write-Host "CyberRotate Pro Manual Release Verification" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

$manualPath = $PSScriptRoot
$errors = 0
$warnings = 0

# Define required files
$requiredFiles = @(
    "README.md",
    "01-installation.md",
    "02-quick-start.md", 
    "03-configuration.md",
    "04-gui-guide.md",
    "05-cli-guide.md",
    "06-api-reference.md",
    "07-vpn-setup.md",
    "08-proxy-management.md",
    "09-tor-integration.md",
    "10-security.md",
    "11-performance.md",
    "12-analytics.md",
    "13-automation.md",
    "14-troubleshooting.md",
    "15-debugging.md",
    "16-faq.md",
    "17-support.md",
    "18-developer.md",
    "19-api-examples.md",
    "20-enterprise.md",
    "RELEASE_NOTES.md",
    "CONTRIBUTING.md",
    "TABLE_OF_CONTENTS.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md"
)

# Function to check file existence and basic content
function Test-ManualFile {
    param([string]$fileName)
    
    $filePath = Join-Path $manualPath $fileName
    
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        $wordCount = ($content -split '\s+').Count
        
        if ($wordCount -lt 50) {
            Write-Host "⚠️  WARNING: $fileName appears to have minimal content ($wordCount words)" -ForegroundColor Yellow
            $script:warnings++
        } else {
            Write-Host "✅ $fileName ($('{0:N0}' -f $wordCount) words)" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ MISSING: $fileName" -ForegroundColor Red
        $script:errors++
    }
}

# Check all required files
Write-Host "Checking Manual Files:" -ForegroundColor White
Write-Host ""

foreach ($file in $requiredFiles) {
    Test-ManualFile $file
}

Write-Host ""

# Check for broken internal links in README
Write-Host "Checking Internal Links in README.md:" -ForegroundColor White
$readmePath = Join-Path $manualPath "README.md"

if (Test-Path $readmePath) {
    $readmeContent = Get-Content $readmePath -Raw
    $linkPattern = '\[([^\]]+)\]\(([^)]+\.md)\)'
    $matches = [regex]::Matches($readmeContent, $linkPattern)
    
    foreach ($match in $matches) {
        $linkTarget = $match.Groups[2].Value
        $linkPath = Join-Path $manualPath $linkTarget
        
        if (Test-Path $linkPath) {
            Write-Host "✅ Link to $linkTarget" -ForegroundColor Green
        } else {
            Write-Host "❌ BROKEN LINK: $linkTarget" -ForegroundColor Red
            $errors++
        }
    }
} else {
    Write-Host "❌ README.md not found" -ForegroundColor Red
    $errors++
}

Write-Host ""

# File size analysis
Write-Host "Manual Statistics:" -ForegroundColor White
$totalSize = 0
$totalFiles = 0

Get-ChildItem $manualPath -Filter "*.md" | ForEach-Object {
    $totalSize += $_.Length
    $totalFiles++
}

$totalSizeKB = [math]::Round($totalSize / 1024, 2)
Write-Host "📊 Total Files: $totalFiles" -ForegroundColor Cyan
Write-Host "📊 Total Size: $totalSizeKB KB" -ForegroundColor Cyan

# Release readiness check
Write-Host ""
Write-Host "Release Readiness Summary:" -ForegroundColor White
Write-Host "=" * 30 -ForegroundColor White

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "🎉 READY FOR RELEASE!" -ForegroundColor Green
    Write-Host "All files are present and appear complete." -ForegroundColor Green
    exit 0
} elseif ($errors -eq 0) {
    Write-Host "⚠️  READY WITH WARNINGS" -ForegroundColor Yellow
    Write-Host "No critical errors found, but $warnings warning(s) to review." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "❌ NOT READY FOR RELEASE" -ForegroundColor Red
    Write-Host "Found $errors error(s) and $warnings warning(s) that must be fixed." -ForegroundColor Red
    exit 2
}
