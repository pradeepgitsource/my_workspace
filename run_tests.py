#!/usr/bin/env python3
"""
Comprehensive test runner for Flight Check-in Application
Runs all tests with coverage reporting and generates detailed reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, description=""):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out after 5 minutes")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False, "", str(e)

def main():
    """Main test runner function."""
    print("🚀 Starting Comprehensive Test Suite for Flight Check-in Application")
    
    # Get project root directory
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    # Test results tracking
    test_results = {
        "backend_unit": False,
        "backend_integration": False,
        "backend_coverage": False,
        "frontend_unit": False,
        "frontend_coverage": False,
        "docker_build": False
    }
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Backend directory: {backend_dir}")
    print(f"📁 Frontend directory: {frontend_dir}")
    
    # 1. Backend Unit Tests
    print("\n🧪 Running Backend Unit Tests...")
    success, stdout, stderr = run_command(
        "python -m pytest tests/ -v --tb=short",
        cwd=backend_dir,
        description="Backend Unit Tests"
    )
    test_results["backend_unit"] = success
    
    # 2. Backend Integration Tests
    print("\n🔗 Running Backend Integration Tests...")
    success, stdout, stderr = run_command(
        "python -m pytest tests/test_integration_comprehensive.py -v --tb=short",
        cwd=backend_dir,
        description="Backend Integration Tests"
    )
    test_results["backend_integration"] = success
    
    # 3. Backend Coverage Report
    print("\n📊 Generating Backend Coverage Report...")
    success, stdout, stderr = run_command(
        "python -m pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=95",
        cwd=backend_dir,
        description="Backend Coverage Analysis"
    )
    test_results["backend_coverage"] = success
    
    # 4. Frontend Unit Tests
    print("\n🎨 Running Frontend Unit Tests...")
    success, stdout, stderr = run_command(
        "npm test -- --coverage --watchAll=false --verbose",
        cwd=frontend_dir,
        description="Frontend Unit Tests"
    )
    test_results["frontend_unit"] = success
    
    # 5. Frontend Coverage Report
    print("\n📈 Generating Frontend Coverage Report...")
    success, stdout, stderr = run_command(
        "npm test -- --coverage --coverageReporters=html --coverageReporters=text --watchAll=false",
        cwd=frontend_dir,
        description="Frontend Coverage Analysis"
    )
    test_results["frontend_coverage"] = success
    
    # 6. Docker Build Test
    print("\n🐳 Testing Docker Build...")
    success, stdout, stderr = run_command(
        "docker-compose build --no-cache",
        cwd=project_root,
        description="Docker Build Test"
    )
    test_results["docker_build"] = success
    
    # Generate Summary Report
    print("\n" + "="*80)
    print("📋 TEST SUMMARY REPORT")
    print("="*80)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Application is ready for deployment.")
        coverage_report_path = backend_dir / "htmlcov" / "index.html"
        if coverage_report_path.exists():
            print(f"📊 Backend Coverage Report: {coverage_report_path}")
        
        frontend_coverage_path = frontend_dir / "coverage" / "lcov-report" / "index.html"
        if frontend_coverage_path.exists():
            print(f"📊 Frontend Coverage Report: {frontend_coverage_path}")
        
        return 0
    else:
        print("❌ Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)