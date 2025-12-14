"""
Configuration settings for the automation framework.
Centralizes all configuration values for easy management.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
TEST_RESULTS_DIR = BASE_DIR / "test-results"

# Application Under Test
BASE_URL = os.getenv("BASE_URL", "https://trade.multibank.io/")

# Browser Configuration
BROWSER_TYPE = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
HEADLESS =  os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down operations by ms
VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

# Timeout Configuration (in milliseconds)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

# Test Execution
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "1"))

# Screenshots
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create directories if they don't exist
REPORTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
TEST_RESULTS_DIR.mkdir(exist_ok=True)