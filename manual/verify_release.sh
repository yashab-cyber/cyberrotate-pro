#!/bin/bash

# CyberRotate Pro Manual - Release Verification Script
# This script verifies that all manual files are present and properly formatted

echo "🔍 CyberRotate Pro Manual - Release Verification"
echo "================================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Function to print status
print_status() {
    local message="$1"
    local status="$2"
    
    printf "%-60s" "$message"
    if [ "$status" = "PASS" ]; then
        echo -e "[${GREEN}PASS${NC}]"
        ((PASSED_CHECKS++))
    elif [ "$status" = "FAIL" ]; then
        echo -e "[${RED}FAIL${NC}]"
        ((FAILED_CHECKS++))
    elif [ "$status" = "WARN" ]; then
        echo -e "[${YELLOW}WARN${NC}]"
    else
        echo -e "[${BLUE}INFO${NC}]"
    fi
    ((TOTAL_CHECKS++))
}

# Check if we're in the manual directory
if [ ! -f "README.md" ]; then
    echo -e "${RED}Error: Please run this script from the manual directory${NC}"
    exit 1
fi

echo -e "${BLUE}📁 Checking file structure...${NC}"
echo

# Define required files
CORE_FILES=(
    "README.md"
    "01-installation.md"
    "02-quick-start.md" 
    "03-configuration.md"
    "04-gui-guide.md"
    "05-cli-guide.md"
    "06-api-reference.md"
    "07-vpn-setup.md"
    "08-proxy-management.md"
    "09-tor-integration.md"
    "10-security.md"
    "11-performance.md"
    "12-analytics.md"
    "13-automation.md"
    "14-troubleshooting.md"
    "15-debugging.md"
    "16-faq.md"
    "17-support.md"
    "18-developer.md"
    "19-api-examples.md"
    "20-enterprise.md"
)

RELEASE_FILES=(
    "RELEASE_NOTES.md"
    "CONTRIBUTING.md"
    "TABLE_OF_CONTENTS.md"
    "QUICK_REFERENCE.md"
    "CHANGELOG.md"
)

# Check core manual files
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status "Core file: $file" "PASS"
    else
        print_status "Core file: $file" "FAIL"
    fi
done

echo

# Check release files
for file in "${RELEASE_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status "Release file: $file" "PASS"
    else
        print_status "Release file: $file" "FAIL"
    fi
done

echo
echo -e "${BLUE}📝 Checking file content structure...${NC}"
echo

# Function to check if file has required sections
check_file_structure() {
    local file="$1"
    local required_sections=("$@")
    
    if [ ! -f "$file" ]; then
        print_status "Content check: $file" "FAIL"
        return
    fi
    
    local missing_sections=0
    for section in "${required_sections[@]:1}"; do
        if ! grep -q "$section" "$file"; then
            ((missing_sections++))
        fi
    done
    
    if [ $missing_sections -eq 0 ]; then
        print_status "Content check: $file" "PASS"
    else
        print_status "Content check: $file (missing $missing_sections sections)" "WARN"
    fi
}

# Check main README structure
check_file_structure "README.md" "Manual Contents" "Quick Navigation" "System Requirements"

# Check a few key files for proper structure
check_file_structure "01-installation.md" "Table of Contents" "Windows Installation" "Linux Installation"
check_file_structure "06-api-reference.md" "Authentication" "Endpoints" "Examples"
check_file_structure "20-enterprise.md" "Licensing Options" "Enterprise Features" "Deployment"

echo
echo -e "${BLUE}🔗 Checking internal links...${NC}"
echo

# Check for broken internal links in README
INTERNAL_LINKS=$(grep -o '\[.*\]([0-9][0-9]-.*\.md)' README.md | grep -o '[0-9][0-9]-.*\.md')

for link in $INTERNAL_LINKS; do
    if [ -f "$link" ]; then
        print_status "Internal link: $link" "PASS"
    else
        print_status "Internal link: $link" "FAIL"
    fi
done

echo
echo -e "${BLUE}📊 File statistics...${NC}"
echo

# Count files and get statistics
TOTAL_FILES=$(ls -1 *.md | wc -l)
TOTAL_SIZE=$(du -sh . | cut -f1)
WORD_COUNT=$(wc -w *.md | tail -n 1 | awk '{print $1}')

print_status "Total markdown files: $TOTAL_FILES" "INFO"
print_status "Total directory size: $TOTAL_SIZE" "INFO" 
print_status "Total word count: $WORD_COUNT" "INFO"

echo
echo -e "${BLUE}🎯 Release readiness check...${NC}"
echo

# Check version consistency
VERSION_FILES=("README.md" "RELEASE_NOTES.md" "CHANGELOG.md")
VERSION_PATTERN="1\.0\.0"

for file in "${VERSION_FILES[@]}"; do
    if [ -f "$file" ] && grep -q "$VERSION_PATTERN" "$file"; then
        print_status "Version check: $file" "PASS"
    else
        print_status "Version check: $file" "FAIL"
    fi
done

# Check date consistency  
RELEASE_DATE="2025-06-24"
for file in "${VERSION_FILES[@]}"; do
    if [ -f "$file" ] && grep -q "$RELEASE_DATE" "$file"; then
        print_status "Date check: $file" "PASS"
    else
        print_status "Date check: $file" "WARN"
    fi
done

echo
echo "================================================="
echo -e "${BLUE}📋 Verification Summary${NC}"
echo "================================================="
echo -e "Total checks: ${BLUE}$TOTAL_CHECKS${NC}"
echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC}"
echo -e "Failed: ${RED}$FAILED_CHECKS${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo
    echo -e "${GREEN}✅ All checks passed! Manual is ready for release.${NC}"
    echo
    echo -e "${BLUE}🚀 Release checklist:${NC}"
    echo "   ✓ All 20 core manual files present"
    echo "   ✓ All release documentation files present" 
    echo "   ✓ File structure and content verified"
    echo "   ✓ Internal links validated"
    echo "   ✓ Version information consistent"
    echo
    echo -e "${GREEN}The CyberRotate Pro manual is ready for distribution!${NC}"
    exit 0
else
    echo
    echo -e "${RED}❌ $FAILED_CHECKS checks failed. Please review and fix issues before release.${NC}"
    exit 1
fi
