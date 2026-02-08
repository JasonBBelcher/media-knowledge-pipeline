#!/usr/bin/env python3
"""
Test Runner for CLI Frontend Components
This script runs all CLI frontend tests and generates reports.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """Run all CLI frontend tests."""
    print("=" * 60)
    print("CLI FRONTEND TEST SUITE")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run pytest with verbose output
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/cli_frontend/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print("TEST OUTPUT:")
        print("-" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("ERRORS/WARNINGS:")
            print("-" * 40)
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    """Main test runner function."""
    print("Starting CLI Frontend Test Suite...")
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        print("CLI Frontend components are working correctly!")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the output above and fix issues.")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())