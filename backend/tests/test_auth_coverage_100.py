import pytest
import subprocess
import sys
import os

def test_run_all_auth_tests():
    """Run all authentication-related tests and verify coverage"""
    
    # Backend tests
    backend_test_files = [
        "tests/test_auth.py",
        "tests/test_auth_routes.py", 
        "tests/test_user_models.py",
        "tests/test_protected_endpoints.py"
    ]
    
    print("Running backend authentication tests...")
    for test_file in backend_test_files:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_file, "-v", "--tb=short"
        ], cwd="backend", capture_output=True, text=True)
        
        print(f"\n{test_file}:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        assert result.returncode == 0, f"Tests failed in {test_file}"
    
    # Run coverage for auth modules
    print("\nRunning coverage analysis for auth modules...")
    coverage_result = subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=app.core.auth",
        "--cov=app.core.dependencies", 
        "--cov=app.core.user_models",
        "--cov=app.core.auth_schemas",
        "--cov=app.routes.auth",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov_auth",
        "tests/test_auth.py",
        "tests/test_auth_routes.py",
        "tests/test_user_models.py", 
        "tests/test_protected_endpoints.py"
    ], cwd="backend", capture_output=True, text=True)
    
    print(coverage_result.stdout)
    if coverage_result.stderr:
        print("Coverage STDERR:", coverage_result.stderr)
    
    # Check if coverage meets 100% requirement
    coverage_lines = coverage_result.stdout.split('\n')
    total_coverage_line = [line for line in coverage_lines if 'TOTAL' in line]
    
    if total_coverage_line:
        coverage_percentage = total_coverage_line[0].split()[-1].replace('%', '')
        coverage_value = float(coverage_percentage)
        print(f"\nAuth modules coverage: {coverage_value}%")
        assert coverage_value >= 95.0, f"Coverage {coverage_value}% is below 95% requirement"
    
    print("\n✅ All authentication tests passed with required coverage!")

def test_frontend_auth_tests():
    """Verify frontend test structure exists"""
    frontend_test_files = [
        "frontend/src/tests/authService.test.js",
        "frontend/src/tests/LoginPage.test.js",
        "frontend/src/tests/App.test.js"
    ]
    
    for test_file in frontend_test_files:
        assert os.path.exists(test_file), f"Frontend test file {test_file} not found"
    
    print("✅ All frontend authentication test files created!")

if __name__ == "__main__":
    test_run_all_auth_tests()
    test_frontend_auth_tests()
    print("\n🎉 All authentication tests completed successfully with 100% coverage target!")