# Makefile for MultiBank Automation Framework
# Build automation and common commands

.PHONY: help install install-dev test test-smoke test-regression test-parallel clean lint format build

# Default target
help:
	@echo "MultiBank Automation Framework - Build Automation"
	@echo ""
	@echo "Available targets:"
	@echo "  install          Install framework and dependencies"
	@echo "  install-dev      Install with dev dependencies"
	@echo "  setup            Complete setup (install + browsers + permissions)"
	@echo "  dev-setup        Development setup (install-dev + .env + permissions)"
	@echo "  test             Run all tests"
	@echo "  test-smoke       Run smoke tests only"
	@echo "  test-regression  Run regression tests"
	@echo "  test-parallel    Run tests in parallel"
	@echo "  test-firefox     Run tests in Firefox"
	@echo "  test-chromium    Run tests in Chromium"
	@echo "  coverage         Run tests with coverage report"
	@echo "  lint             Run code linting"
	@echo "  format           Format code with black"
	@echo "  clean            Clean build artifacts"
	@echo "  build            Build distribution package"
	@echo ""
	@echo "💡 Tip: Use './run_tests.sh tests/' to auto-read PARALLEL_WORKERS from .env"

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
	@echo "Setting up run_tests.sh permissions..."
	@chmod +x run_tests.sh
	@echo "Setup complete!"
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
	rm -rf screenshots/*.png
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

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
	@echo "Dev setup complete! Edit .env file as needed."
	@echo "Run './run_tests.sh tests/' to run tests with parallel workers from .env"

quick-test:
	@echo "Quick test run (string frequency only)..."
	pytest tests/test_string_frequency.py -v