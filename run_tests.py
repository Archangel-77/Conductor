#!/usr/bin/env python3
"""
Simple test runner for Conductor.
"""

import sys
import subprocess

def run_tests():
    """Run all tests."""
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--cov=conductor",
            "--cov-report=term-missing"
        ], check=True)
        
        print("All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
