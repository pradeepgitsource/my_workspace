@echo off
echo 🚀 Flight Check-in Application - Comprehensive Test Suite
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    exit /b 1
)

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not in PATH
    exit /b 1
)

echo ✅ All prerequisites are available

REM Install backend dependencies
echo.
echo 📦 Installing Backend Dependencies...
cd backend
pip install fastapi uvicorn sqlalchemy asyncpg "pydantic[email]" alembic
pip install pytest pytest-asyncio pytest-cov httpx
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    exit /b 1
)

REM Install frontend dependencies
echo.
echo 📦 Installing Frontend Dependencies...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    exit /b 1
)

REM Go back to project root
cd ..

REM Run the comprehensive test suite
echo.
echo 🧪 Running Comprehensive Test Suite...
cd backend
set PYTHONPATH=%CD%
pytest tests/test_schemas_comprehensive.py tests/test_utils_comprehensive.py tests/test_services.py tests/test_api_endpoints_mocked.py -v --cov=app --cov-report=html --cov-report=term-missing
cd ..

if %errorlevel% equ 0 (
    echo.
    echo 🎉 All tests completed successfully!
    echo 📊 Check the coverage reports in:
    echo    - Backend: backend\htmlcov\index.html
    echo    - Frontend: frontend\coverage\lcov-report\index.html
) else (
    echo.
    echo ❌ Some tests failed. Please check the output above.
)

pause