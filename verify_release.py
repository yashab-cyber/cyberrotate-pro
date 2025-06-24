#!/usr/bin/env python3
"""
CyberRotate Pro - Release Verification Script
Verifies that the project is ready for production release
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ReleaseVerifier:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        
    def print_header(self):
        """Print the release verification header"""
        print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}🚀 CyberRotate Pro - Release Verification System 🚀{Colors.END}")
        print(f"{Colors.CYAN}Created by Yashab Alam - Founder & CEO of ZehraSec{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")
    
    def print_status(self, message: str, status: str, details: str = ""):
        """Print status message with color coding"""
        self.total_checks += 1
        
        if status == "PASS":
            icon = "✅"
            color = Colors.GREEN
            self.success_count += 1
        elif status == "FAIL":
            icon = "❌"
            color = Colors.RED
        elif status == "WARN":
            icon = "⚠️ "
            color = Colors.YELLOW
        else:
            icon = "ℹ️ "
            color = Colors.BLUE
        
        print(f"{icon} {color}{message:<50}{Colors.END} [{status}]")
        if details:
            print(f"   {Colors.WHITE}{details}{Colors.END}")
    
    def check_file_exists(self, file_path: str, description: str) -> bool:
        """Check if a file exists"""
        full_path = self.project_root / file_path
        exists = full_path.exists()
        
        if exists:
            self.print_status(f"File: {description}", "PASS", f"Found: {file_path}")
        else:
            self.print_status(f"File: {description}", "FAIL", f"Missing: {file_path}")
            self.errors.append(f"Missing file: {file_path}")
        
        return exists
    
    def check_directory_exists(self, dir_path: str, description: str) -> bool:
        """Check if a directory exists"""
        full_path = self.project_root / dir_path
        exists = full_path.exists() and full_path.is_dir()
        
        if exists:
            self.print_status(f"Directory: {description}", "PASS", f"Found: {dir_path}")
        else:
            self.print_status(f"Directory: {description}", "FAIL", f"Missing: {dir_path}")
            self.errors.append(f"Missing directory: {dir_path}")
        
        return exists
    
    def check_python_syntax(self, file_path: str) -> bool:
        """Check Python file syntax"""
        full_path = self.project_root / file_path
        
        if not full_path.exists():
            return False
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                compile(f.read(), str(full_path), 'exec')
            self.print_status(f"Python Syntax: {file_path}", "PASS")
            return True
        except SyntaxError as e:
            self.print_status(f"Python Syntax: {file_path}", "FAIL", f"Syntax error: {e}")
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            self.print_status(f"Python Syntax: {file_path}", "WARN", f"Check failed: {e}")
            self.warnings.append(f"Could not check {file_path}: {e}")
            return False
    
    def check_version_consistency(self) -> bool:
        """Check version consistency across files"""
        try:
            # Check _version.py
            version_file = self.project_root / "_version.py"
            setup_file = self.project_root / "setup.py"
            
            # Extract version from _version.py
            spec = importlib.util.spec_from_file_location("_version", version_file)
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)
            version_py = version_module.__version__
            
            # Extract version from setup.py
            with open(setup_file, 'r', encoding='utf-8') as f:
                setup_content = f.read()
                import re
                version_match = re.search(r'version="([^"]+)"', setup_content)
                version_setup = version_match.group(1) if version_match else None
            
            if version_py == version_setup == "1.0.0":
                self.print_status("Version Consistency", "PASS", f"Version: {version_py}")
                return True
            else:
                self.print_status("Version Consistency", "FAIL", 
                                f"Mismatch: _version.py={version_py}, setup.py={version_setup}")
                self.errors.append(f"Version mismatch: _version.py={version_py}, setup.py={version_setup}")
                return False
                
        except Exception as e:
            self.print_status("Version Consistency", "FAIL", f"Error: {e}")
            self.errors.append(f"Version check failed: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if core dependencies are installable"""
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_status("Dependencies Check", "FAIL", "requirements.txt not found")
            return False
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            critical_deps = ['requests', 'colorama', 'psutil', 'stem', 'pysocks']
            missing_critical = []
            
            for dep in critical_deps:
                if not any(dep in line for line in deps):
                    missing_critical.append(dep)
            
            if missing_critical:
                self.print_status("Dependencies Check", "FAIL", 
                                f"Missing critical deps: {missing_critical}")
                self.errors.append(f"Missing critical dependencies: {missing_critical}")
                return False
            else:
                self.print_status("Dependencies Check", "PASS", 
                                f"Found {len(deps)} dependencies")
                return True
                
        except Exception as e:
            self.print_status("Dependencies Check", "FAIL", f"Error: {e}")
            self.errors.append(f"Dependencies check failed: {e}")
            return False
    
    def check_manual_completeness(self) -> bool:
        """Check if manual documentation is complete"""
        manual_dir = self.project_root / "manual"
        
        if not manual_dir.exists():
            self.print_status("Manual Completeness", "FAIL", "manual/ directory not found")
            return False
        
        expected_files = [
            "README.md",
            "01-installation.md", "02-quick-start.md", "03-configuration.md",
            "04-gui-guide.md", "05-cli-guide.md", "06-api-reference.md",
            "07-vpn-setup.md", "08-proxy-management.md", "09-tor-integration.md",
            "10-security.md", "11-performance.md", "12-analytics.md",
            "13-automation.md", "14-troubleshooting.md", "15-debugging.md",
            "16-faq.md", "17-support.md", "18-developer.md",
            "19-api-examples.md", "20-enterprise.md"
        ]
        
        missing_files = []
        for file in expected_files:
            if not (manual_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.print_status("Manual Completeness", "FAIL", 
                            f"Missing {len(missing_files)} files: {missing_files[:3]}...")
            self.errors.append(f"Missing manual files: {missing_files}")
            return False
        else:
            self.print_status("Manual Completeness", "PASS", 
                            f"All {len(expected_files)} manual files present")
            return True
    
    def check_executable_permissions(self) -> bool:
        """Check executable file permissions"""
        executable_files = [
            "install.sh",
            "start_gui.sh"
        ]
        
        issues = []
        for file in executable_files:
            file_path = self.project_root / file
            if file_path.exists():
                if os.name != 'nt':  # Not Windows
                    if not os.access(file_path, os.X_OK):
                        issues.append(f"{file} not executable")
            else:
                issues.append(f"{file} missing")
        
        if issues:
            self.print_status("Executable Permissions", "WARN", f"Issues: {issues}")
            self.warnings.extend(issues)
            return False
        else:
            self.print_status("Executable Permissions", "PASS", 
                            f"Checked {len(executable_files)} files")
            return True
    
    def check_license_and_legal(self) -> bool:
        """Check license and legal files"""
        legal_files = {
            "LICENSE": "MIT License file",
            "SECURITY.md": "Security policy",
            "CONTRIBUTING.md": "Contribution guidelines"
        }
        
        all_present = True
        for file, desc in legal_files.items():
            if not self.check_file_exists(file, desc):
                all_present = False
        
        return all_present
    
    def run_verification(self) -> bool:
        """Run complete release verification"""
        self.print_header()
        
        print(f"{Colors.BOLD}{Colors.BLUE}🔍 Starting Release Verification...{Colors.END}\n")
        
        # Core file checks
        print(f"{Colors.PURPLE}📁 Core Files Verification{Colors.END}")
        core_files = {
            "ip_rotator.py": "Main application",
            "setup.py": "Installation script",
            "_version.py": "Version information",
            "requirements.txt": "Core dependencies",
            "requirements-full.txt": "Full dependencies",
            "README.md": "Project documentation"
        }
        
        for file, desc in core_files.items():
            self.check_file_exists(file, desc)
        
        print()
        
        # Directory structure checks
        print(f"{Colors.PURPLE}📁 Directory Structure Verification{Colors.END}")
        directories = {
            "core": "Core modules",
            "config": "Configuration files",
            "ui": "User interface",
            "utils": "Utility modules",
            "manual": "Documentation manual",
            "docs": "Additional documentation"
        }
        
        for dir_name, desc in directories.items():
            self.check_directory_exists(dir_name, desc)
        
        print()
        
        # Python syntax checks
        print(f"{Colors.PURPLE}🐍 Python Syntax Verification{Colors.END}")
        python_files = [
            "ip_rotator.py",
            "setup.py",
            "_version.py",
            "gui_launcher.py"
        ]
        
        for py_file in python_files:
            self.check_python_syntax(py_file)
        
        print()
        
        # Version and dependency checks
        print(f"{Colors.PURPLE}📦 Package Configuration Verification{Colors.END}")
        self.check_version_consistency()
        self.check_dependencies()
        print()
        
        # Documentation checks
        print(f"{Colors.PURPLE}📚 Documentation Verification{Colors.END}")
        self.check_manual_completeness()
        print()
        
        # Legal and permissions
        print(f"{Colors.PURPLE}⚖️  Legal and Permissions Verification{Colors.END}")
        self.check_license_and_legal()
        self.check_executable_permissions()
        print()
        
        # Final summary
        self.print_summary()
        
        return len(self.errors) == 0
    
    def print_summary(self):
        """Print verification summary"""
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}📊 RELEASE VERIFICATION SUMMARY{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}")
        
        success_rate = (self.success_count / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print(f"\n📈 {Colors.BOLD}Success Rate: {success_rate:.1f}% ({self.success_count}/{self.total_checks}){Colors.END}")
        print(f"✅ {Colors.GREEN}Passed Checks: {self.success_count}{Colors.END}")
        print(f"❌ {Colors.RED}Failed Checks: {len(self.errors)}{Colors.END}")
        print(f"⚠️  {Colors.YELLOW}Warnings: {len(self.warnings)}{Colors.END}")
        
        if self.errors:
            print(f"\n{Colors.RED}❌ CRITICAL ISSUES:{Colors.END}")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}⚠️  WARNINGS:{Colors.END}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        print()
        
        if len(self.errors) == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 RELEASE STATUS: READY FOR PRODUCTION! 🎉{Colors.END}")
            print(f"{Colors.GREEN}CyberRotate Pro v1.0.0 passes all critical checks and is ready for release.{Colors.END}")
            print(f"{Colors.GREEN}Quality Grade: ⭐⭐⭐⭐⭐ (Production Ready){Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}🚫 RELEASE STATUS: NOT READY - ISSUES FOUND{Colors.END}")
            print(f"{Colors.RED}Please fix the critical issues before proceeding with release.{Colors.END}")
        
        print(f"\n{Colors.CYAN}Verification completed by: Yashab Alam - ZehraSec{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")

def main():
    """Main verification function"""
    verifier = ReleaseVerifier()
    success = verifier.run_verification()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
