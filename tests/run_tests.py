#!/usr/bin/env python3
"""
CyberRotate Pro Test Runner
Simple script to run all tests
"""

import os
import sys
import subprocess
import argparse

def run_tests(test_type="all", verbose=False):
    """Run tests with specified parameters"""
    
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    
    # Add project root to Python path
    sys.path.insert(0, project_root)
    
    print("CyberRotate Pro Test Runner")
    print("=" * 40)
    print(f"Test directory: {test_dir}")
    print(f"Project root: {project_root}")
    print(f"Test type: {test_type}")
    print(f"Verbose: {verbose}")
    print()
    
    # Run tests based on type
    if test_type == "all":
        return run_all_tests(verbose)
    elif test_type == "unit":
        return run_unit_tests(verbose)
    elif test_type == "integration":
        return run_integration_tests(verbose)
    else:
        print(f"Unknown test type: {test_type}")
        return False

def run_all_tests(verbose=False):
    """Run all tests"""
    try:
        import unittest
        
        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover(os.path.dirname(__file__), pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(suite)
        
        print(f"\nTests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
                if verbose:
                    print(f"    {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
                if verbose:
                    print(f"    {traceback}")
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_unit_tests(verbose=False):
    """Run only unit tests"""
    print("Running unit tests...")
    # Implementation would filter for unit tests specifically
    return run_all_tests(verbose)

def run_integration_tests(verbose=False):
    """Run only integration tests"""
    print("Running integration tests...")
    # Implementation would filter for integration tests specifically
    return run_all_tests(verbose)

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking test dependencies...")
    
    required_modules = [
        'unittest',
        'unittest.mock',
        'tempfile',
        'json',
        'os',
        'sys'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Missing required modules: {', '.join(missing_modules)}")
        return False
    
    print("All test dependencies available.")
    return True

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='CyberRotate Pro Test Runner')
    parser.add_argument('--type', choices=['all', 'unit', 'integration'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose output')
    parser.add_argument('--check-deps', action='store_true',
                       help='Check dependencies only')
    
    args = parser.parse_args()
    
    if args.check_deps:
        success = check_dependencies()
        sys.exit(0 if success else 1)
    
    # Check dependencies first
    if not check_dependencies():
        print("Dependency check failed. Cannot run tests.")
        sys.exit(1)
    
    # Run tests
    success = run_tests(args.type, args.verbose)
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
