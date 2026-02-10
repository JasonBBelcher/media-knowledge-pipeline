#!/usr/bin/env python3
"""
Test runner for CLI frontend tests
"""
import subprocess
import sys
import os

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

def run_tests():
    """Run all CLI frontend tests."""
    print("🚀 Running CLI Frontend Tests")
    print("=" * 50)
    
    test_files = [
        "test_cli_commands.py",
        "test_interactive_options.py", 
        "test_wizard_components.py"
    ]
    
    results = []
    
    for test_file in test_files:
        print(f"\n📋 Running {test_file}...")
        print("-" * 40)
        
        result = subprocess.run(
            ["python", "-m", "pytest", f"tests/cli_frontend/{test_file}", "-v"],
            capture_output=True,
            text=True
        )
        
        results.append({
            'file': test_file,
            'exit_code': result.returncode,
            'output': result.stdout + result.stderr
        })
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Exit code: {result.returncode}")
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for result in results:
        status = "✅ PASSED" if result['exit_code'] == 0 else "❌ FAILED"
        if result['exit_code'] == 0:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {result['file']}")
        if result['exit_code'] != 0:
            # Show first few lines of error output
            lines = result['output'].split('\n')
            error_lines = [line for line in lines if 'FAILED' in line or 'ERROR' in line]
            if error_lines:
                print("    ", error_lines[0])
    
    print(f"\n📈 Total: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed - check above for details")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())