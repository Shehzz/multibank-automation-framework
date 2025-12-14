#!/bin/bash
# Helper script to view Allure reports

echo "📊 Allure Report Viewer"
echo ""

# Check if allure is installed
if ! command -v allure &> /dev/null; then
    echo "❌ Allure is not installed!"
    echo ""
    echo "Install Allure:"
    echo "  macOS:   brew install allure"
    echo "  Linux:   sudo apt-get install allure"
    echo "  Manual:  https://github.com/allure-framework/allure2/releases"
    exit 1
fi

# Check if results exist
if [ ! -d "reports/allure-results" ] || [ -z "$(ls -A reports/allure-results)" ]; then
    echo "❌ No Allure results found!"
    echo ""
    echo "Run tests first to generate results:"
    echo "  ./run_tests.sh tests/"
    exit 1
fi

# Serve Allure report
echo "🚀 Starting Allure report server..."
echo "📁 Results directory: reports/allure-results"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

allure serve reports/allure-results