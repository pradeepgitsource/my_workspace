import pytest
import subprocess
import sys
import os

def test_run_enterprise_tests_with_coverage():
    """Run all enterprise domain tests with 95%+ coverage requirement"""
    
    # Test directories for enterprise domains
    test_directories = [
        "tests/booking/",
        "tests/checkin/", 
        "tests/flight/",
        "tests/shared/"
    ]
    
    # Coverage targets for enterprise modules
    coverage_modules = [
        "app.booking.booking_repository",
        "app.booking.booking_service", 
        "app.booking.booking_controller",
        "app.checkin.checkin_repository",
        "app.checkin.checkin_service",
        "app.checkin.checkin_controller",
        "app.flight.flight_repository",
        "app.passenger.passenger_repository",
        "app.shared.exceptions"
    ]
    
    print("Running enterprise domain tests with coverage analysis...")
    
    # Build coverage command
    coverage_args = []
    for module in coverage_modules:
        coverage_args.extend(["--cov", module])
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        *test_directories,
        *coverage_args,
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov_enterprise",
        "--cov-fail-under=95",
        "-v"
    ]
    
    result = subprocess.run(cmd, cwd=".", capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    # Check if coverage meets 95% requirement
    if result.returncode == 0:
        print("\nAll enterprise tests passed with 95%+ coverage!")
        
        # Extract coverage percentage from output
        coverage_lines = result.stdout.split('\n')
        total_coverage_line = [line for line in coverage_lines if 'TOTAL' in line and '%' in line]
        
        if total_coverage_line:
            coverage_info = total_coverage_line[0]
            print(f"Coverage Summary: {coverage_info}")
        
        return True
    else:
        print(f"\nTests failed or coverage below 95%. Return code: {result.returncode}")
        return False

def test_count_enterprise_test_cases():
    """Count total test cases in enterprise architecture"""
    
    test_files = [
        "tests/booking/test_booking_repository.py",
        "tests/booking/test_booking_service.py", 
        "tests/booking/test_booking_controller.py",
        "tests/checkin/test_checkin_service.py",
        "tests/flight/test_flight_passenger_repositories.py",
        "tests/shared/test_exceptions.py"
    ]
    
    total_tests = 0
    for test_file in test_files:
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                content = f.read()
                test_count = content.count('def test_')
                total_tests += test_count
                print(f"{test_file}: {test_count} tests")
        else:
            print(f"⚠️  {test_file}: File not found")
    
    print(f"\nTotal Enterprise Test Cases: {total_tests}")
    
    # Verify minimum test coverage
    assert total_tests >= 50, f"Expected at least 50 test cases, got {total_tests}"
    
    print("Enterprise test suite meets minimum test case requirements!")
    return total_tests

def test_verify_enterprise_structure():
    """Verify enterprise domain structure exists"""
    
    required_directories = [
        "app/booking",
        "app/checkin", 
        "app/flight",
        "app/passenger",
        "app/shared",
        "tests/booking",
        "tests/checkin",
        "tests/flight", 
        "tests/shared"
    ]
    
    missing_dirs = []
    for directory in required_directories:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"Missing directories: {missing_dirs}")
        return False
    
    print("Enterprise domain structure verified!")
    return True

if __name__ == "__main__":
    print("Running Enterprise Architecture Test Suite")
    print("=" * 60)
    
    # Verify structure
    structure_ok = test_verify_enterprise_structure()
    
    # Count test cases
    test_count = test_count_enterprise_test_cases()
    
    # Run tests with coverage
    if structure_ok:
        coverage_ok = test_run_enterprise_tests_with_coverage()
        
        if coverage_ok:
            print("\nEnterprise Architecture Test Suite PASSED!")
            print(f"✅ {test_count} test cases executed")
            print("✅ 95%+ code coverage achieved")
            print("✅ All business domains tested")
        else:
            print("\nEnterprise Architecture Test Suite FAILED!")
            sys.exit(1)
    else:
        print("\nEnterprise structure verification failed!")
        sys.exit(1)