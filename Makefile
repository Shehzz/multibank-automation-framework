# Makefile for MultiBank Automation Framework
# Build automation and common commands

.PHONY: help install install-dev test test-all test-bonus test-smoke test-regression test-navigation \
        test-trading test-accessibility test-performance test-content test-parallel test-firefox \
        test-chromium test-webkit test-cross-browser coverage allure-serve allure-generate \
        allure-open clean lint format type-check build browsers check run-string-frequency \
        ci-test ci-coverage dev-setup quick-test setup

# Default target
help:
	@echo "MultiBank Automation Framework - Build Automation"
	@echo ""
	@echo "🚀 Setup Commands:"
	@echo "  install          Install framework and dependencies"
	@echo "  install-dev      Install with dev dependencies"
	@echo "  setup            Complete setup (install + browsers + permissions)"
	@echo "  dev-setup        Development setup (install-dev + .env + permissions)"
	@echo ""
	@echo "🧪 Test Commands:"
	@echo "  test             Run all tests"
	@echo "  test-all         Run comprehensive test suite"
	@echo "  test-bonus       Run bonus features (accessibility + performance)"
	@echo "  test-smoke       Run smoke tests only"
	@echo "  test-regression  Run regression tests"
	@echo "  test-navigation  Run navigation tests"
	@echo "  test-trading     Run trading tests"
	@echo "  test-accessibility  Run accessibility tests (WCAG)"
	@echo "  test-performance Run performance tests"
	@echo "  test-content     Run content tests"
	@echo "  test-parallel    Run tests in parallel"
	@echo ""
	@echo "🌐 Browser Commands:"
	@echo "  test-firefox     Run tests in Firefox"
	@echo "  test-chromium    Run tests in Chromium"
	@echo "  test-webkit      Run tests in WebKit"
	@echo "  test-cross-browser  Run cross-browser tests"
	@echo ""
	@echo "📊 Reporting Commands:"
	@echo "  coverage         Run tests with coverage report"
	@echo "  allure-serve     View Allure report (interactive)"
	@echo "  allure-generate  Generate static Allure report"
	@echo "  allure-open      Open generated Allure report"
	@echo ""
	@echo "🔧 Code Quality:"
	@echo "  lint             Run code linting"
	@echo "  format           Format code with black"
	@echo "  type-check       Run type checker"
	@echo ""
	@echo "🏗️  Build Commands:"
	@echo "  clean            Clean build artifacts and reports"
	@echo "  build            Build distribution package"
	@echo ""
	@echo "💡 Quick Tips:"
	@echo "  • Use './run_tests.sh tests/' to auto-read PARALLEL_WORKERS from .env"
	@echo "  • Use './view_allure_report.sh' for quick Allure report viewing"
	@echo "  • Run 'make dev-setup' for complete development environment setup"

# Installation targets
install:
	@echo "Installing framework..."
	pip install -r requirements.txt
	playwright install

install-dev:
	@echo "Installing with dev dependencies..."
	pip install -e ".[dev]"
	playwright install

setup: install
	@echo "Setting up script permissions..."
	@chmod +x run_tests.sh
	@chmod +x view_allure_report.sh
	@echo "✓ Setup complete!"
	@echo "Run './run_tests.sh' or 'make test' to verify installation"

# Testing targets
test:
	@echo "Running all tests..."
	pytest -v

test-smoke:
	@echo "Running smoke tests..."
	pytest -m smoke -v

test-regression:
	@echo "Running regression tests..."
	pytest -m regression -v

test-navigation:
	@echo "Running navigation tests..."
	pytest -m navigation -v

test-trading:
	@echo "Running trading tests..."
	pytest -m trading -v

test-accessibility:
	@echo "Running accessibility tests..."
	pytest -m accessibility -v

test-performance:
	@echo "Running performance tests..."
	pytest -m performance -v

test-content:
	@echo "Running content tests..."
	pytest -m content -v

test-all:
	@echo "Running comprehensive test suite..."
	@echo "This includes: navigation, trading, content, accessibility, performance"
	pytest tests/ -v

test-bonus:
	@echo "Running bonus feature tests (accessibility + performance)..."
	pytest -m "accessibility or performance" -v

test-parallel:
	@echo "Running tests in parallel..."
	@if [ -f .env ]; then \
		export $$(cat .env | grep PARALLEL_WORKERS | xargs) && \
		pytest -n $${PARALLEL_WORKERS:-auto} -v; \
	else \
		pytest -n auto -v; \
	fi

test-firefox:
	@echo "Running tests in Firefox..."
	pytest --browser firefox -v

test-chromium:
	@echo "Running tests in Chromium..."
	pytest --browser chromium -v

test-webkit:
	@echo "Running tests in WebKit..."
	pytest --browser webkit -v

test-cross-browser:
	@echo "Running cross-browser tests..."
	pytest --browser chromium --browser firefox -v

# Coverage
coverage:
	@echo "Running tests with coverage..."
	pytest --cov=pages --cov=utils --cov=config --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

# Allure reporting
allure-serve:
	@echo "Serving Allure report..."
	@if command -v allure >/dev/null 2>&1; then \
		allure serve reports/allure-results; \
	else \
		echo "❌ Allure CLI not installed!"; \
		echo "Install: brew install allure (macOS) or see docs/ALLURE_SETUP.md"; \
	fi

allure-generate:
	@echo "Generating Allure report..."
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure-results -o reports/allure-report --clean; \
		echo "✓ Report generated: reports/allure-report/index.html"; \
	else \
		echo "❌ Allure CLI not installed!"; \
		echo "Install: brew install allure (macOS) or see docs/ALLURE_SETUP.md"; \
	fi

allure-open:
	@echo "Opening Allure report..."
	@if [ -f reports/allure-report/index.html ]; then \
		open reports/allure-report/index.html 2>/dev/null || \
		xdg-open reports/allure-report/index.html 2>/dev/null || \
		echo "Please open reports/allure-report/index.html manually"; \
	else \
		echo "❌ Report not found. Run 'make allure-generate' first"; \
	fi

# Code quality
lint:
	@echo "Running linters..."
	flake8 pages utils config tests --max-line-length=100

format:
	@echo "Formatting code..."
	black pages utils config tests

type-check:
	@echo "Running type checker..."
	mypy pages utils config

# Build targets
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf reports/*.html
	rm -rf reports/allure-results/*
	rm -rf reports/allure-report/*
	rm -rf screenshots/*.png
	rm -rf videos/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	@echo "✓ Cleaned all build artifacts and test reports"

build: clean
	@echo "Building distribution package..."
	python setup.py sdist bdist_wheel

# Utility targets
browsers:
	@echo "Installing Playwright browsers..."
	playwright install

check:
	@echo "Checking installation..."
	python --version
	playwright --version
	pytest --version

run-string-frequency:
	@echo "Running string frequency script..."
	python utils/string_frequency.py

# CI/CD targets
ci-test:
	@echo "Running CI tests..."
	pytest --browser chromium --browser firefox -v --html=reports/ci-report.html

ci-coverage:
	@echo "Running CI with coverage..."
	pytest --cov=pages --cov=utils --cov-report=xml --cov-report=term

# Development workflow
dev-setup: install-dev
	@echo "Setting up development environment..."
	cp .env.example .env
	@chmod +x run_tests.sh
	@chmod +x view_allure_report.sh
	@echo "✓ Dev setup complete! Edit .env file as needed."
	@echo "Run './run_tests.sh tests/' to run tests with parallel workers from .env"

quick-test:
	@echo "Quick test run (string frequency only)..."
	pytest tests/test_string_frequency.py -v