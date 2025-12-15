# MultiBank Trading Platform - Test Automation Framework

**Version**: 1.0.0  
**Framework**: Playwright 1.57.0 + Python 3.8+  
**Pattern**: Page Object Model with External Locator Management

A production-grade web automation framework for testing the MultiBank trading platform (https://trade.multibank.io/) using Python and Playwright.

## 🎯 Project Overview

This framework implements the Page Object Model (POM) design pattern with **externalized locator management** to provide maintainable, scalable, and reliable automated tests for critical user flows including:

- Navigation and Layout validation
- Trading functionality (spot trading, trading pairs, categories)
- Content validation (marketing banners, download links)
- About Us → Why MultiBank page content

## ✨ Key Features

- **Modern Framework**: Built with Playwright 1.57.0 for fast, reliable automation
- **Page Object Model**: Clean separation of test logic and page interactions
- **External Locator Management**: All locators stored in JSON files (production-ready approach)
- **XPath Locators**: Reliable XPath-based element identification
- **Cross-Browser Support**: Tests run on Chromium, Firefox, and WebKit
- **Data-Driven**: External test data management (no hard-coded assertions)
- **Smart Waits**: Auto-waiting with Playwright (no flaky time.sleep())
- **Rich Reporting**: Allure reports with screenshots on failure
- **Accessibility Testing**: WCAG 2.1 compliance checks using axe-core
- **Performance Testing**: Automated page load and resource optimization metrics
- **Parallel Execution**: Configurable parallel test execution
- **Professional Logging**: Comprehensive logging for debugging
- **Type Hints**: Python type annotations throughout

## 📁 Project Structure

```
multibank-automation-framework/
├── Makefile                    # Build commands (make test, make build)
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── run_tests.sh                # Bash script to run tests
├── view_allure_report.sh      # Allure report viewer script
├── .env.example               # Environment variables template
├── config/                     # Configuration files
│   ├── settings.py            # Framework settings
│   ├── test_data.json         # External test data
│   └── __init__.py
├── pages/                      # Page Object Model classes
│   ├── base_page.py           # Base page with common methods
│   ├── home_page.py           # Home page object
│   ├── why_multibank_page.py  # Why Multibank page object
│   └── __init__.py
├── resources/                  # External resources
│   └── locators/              # ⭐ Locators stored separately (PROD-ready)
│       ├── locators.json      # All page locators (XPath)
│       ├── home_locators.py   # Home page locator class
│       └── why_multibank_locators.py  # Why Multibank page locator class
├── tests/                      # Test cases
│   ├── conftest.py            # Pytest fixtures
│   ├── test_navigation.py     # Navigation tests
│   ├── test_content.py        # Content validation tests
│   ├── test_trading.py        # Trade tests
│   ├── test_accessibility.py  # Accessibility (WCAG) tests
│   ├── test_performance.py    # Performance & load time tests
│   ├── test_string_frequency.py # Unit tests for Task 2
│   └── __init__.py
├── utils/                      # Utility functions
│   ├── string_frequency.py    # String frequency counter (Task 2)
│   ├── locator_reader.py      # Locator JSON reader
│   ├── test_data_reader.py      # Test data JSON reader
│   ├── accessibility.py       # Accessibility testing utilities
│   ├── performance.py         # Performance testing utilities
│   └── __init__.py
├── reports/                    # Test execution reports
│   ├── allure-results/        # Allure JSON results
│   └── allure-report/         # Allure HTML reports
└── screenshots/                # Screenshots on failure
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation (4 Simple Steps)

```bash
# 1. Clone the repository
git clone https://github.com/Shehzz/multibank-automation-framework
cd multibank-automation-framework

# 2. Run setup (installs dependencies + browsers)
make setup

# 3. Configure environment variables
cp .env.example .env
# Edit .env file with your settings (browser, headless mode, etc.)

# 4. Verify installation
./run_tests.sh tests/test_string_frequency.py -v
```

✅ **Installation complete!** You're ready to run tests.


## 🧪 Running Tests

### ⚠️ IMPORTANT: Always use `./run_tests.sh`

**Do NOT use `pytest` directly** - the test runner script handles parallel execution, Allure reporting, and proper configuration.

### Basic Usage

```bash
# Run all tests
./run_tests.sh

# Run specific test file
./run_tests.sh tests/test_navigation.py

# Run with verbose output
./run_tests.sh tests/test_content.py -v

# Run specific test
./run_tests.sh tests/test_navigation.py::TestNavigation::test_navigation_menu_displays

# Run by marker
./run_tests.sh -m smoke
./run_tests.sh -m regression
./run_tests.sh -m accessibility
```

### Browser Selection

```bash
# Run in specific browser (overrides .env setting)
./run_tests.sh --browser firefox
./run_tests.sh --browser chromium
./run_tests.sh --browser webkit

# Run in multiple browsers
./run_tests.sh --browser chromium --browser firefox
```

### Parallel Execution

Parallel execution is **automatically configured** via the `.env` file:

```bash
# In .env file:
PARALLEL_WORKERS=4

# Then just run normally - parallelization happens automatically:
./run_tests.sh tests/
```

---

## 📊 Viewing Test Reports

### Allure Reports (Recommended)

```bash
# After running tests, view the interactive Allure report:
./view_allure_report.sh
```

This opens a beautiful interactive report in your browser with:
- 📈 Test execution trends
- ⏱️ Duration metrics
- 📸 Screenshots attached to failed tests
- 🏷️ Test categorization
- 📊 Visual analytics

### HTML Report (Alternative)

The test runner also generates a simple HTML report:
```bash
open reports/report.html  # macOS
start reports/report.html # Windows
xdg-open reports/report.html # Linux
```

---

## ⚙️ Configuration

### Environment Variables (.env)

After running `cp .env.example .env`, configure these settings:

```bash
# Application
BASE_URL=https://trade.multibank.io/

# Browser Settings
BROWSER=chromium           # chromium, firefox, webkit
HEADLESS=false            # true for headless mode
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Timeouts (milliseconds)
DEFAULT_TIMEOUT=30000

# Test Execution
PARALLEL_WORKERS=4        # Number of parallel test workers
MAX_RETRIES=2

# Screenshots
SCREENSHOT_ON_FAILURE=true

# Logging
LOG_LEVEL=INFO
```

### Test Data

Edit `config/test_data.json` to update expected values:

```json
{
  "navigation": {
    "expected_menu_items": [
      "Dashboard",
      "Markets",
      "Trade",
      "Features",
      "About Us",
      "Support"
    ]
  },
  "why_multibank": {
    "content": {
      "hero_slides": {
        "slide_1": "Master the Market with a Champion's Mindset"
      }
    }
  }
}
```

---

## 🎨 Test Markers

Tests are organized using pytest markers:

| Marker | Description |
|--------|-------------|
| `smoke` | Quick smoke tests for critical paths |
| `regression` | Full regression test suite |
| `navigation` | Navigation-related tests |
| `trading` | Trading functionality tests |
| `content` | Content validation tests |
| `accessibility` | WCAG 2.1 accessibility tests |
| `performance` | Performance and load time tests |

**Example:**
```bash
# Run only accessibility tests
./run_tests.sh -m accessibility

# Run smoke + regression tests
./run_tests.sh -m "smoke or regression"
```

---

## 🏗️ Architecture

### Page Object Model with External Locators

This framework uses a **production-ready approach** with 3 separate layers:

#### 1. **Locators (JSON)** - `resources/locators/locators.json`
```json
{
  "Home Page": {
    "nav_menu": {
      "name": "Navigation Menu",
      "locator": "//nav",
      "type": "xpath"
    }
  }
}
```

#### 2. **Locator Classes** - `resources/locators/home_locators.py`
```python
class HomeLocators:
    def __init__(self):
        locators = LOCATORS["Home Page"]
        self.nav_menu = locators["nav_menu"]["locator"]
```

#### 3. **Page Objects** - `pages/home_page.py`
```python
class HomePage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page)
        self.locators = HomeLocators()
    
    def is_navigation_displayed(self):
        return self.is_visible(self.locators.nav_menu)
```

#### 4. **Tests** - `tests/test_navigation.py`
```python
def test_navigation_menu(home_page):
    home_page.load()
    assert home_page.is_navigation_displayed()
```

**Benefits:**
- ✅ No hardcoded locators in code
- ✅ Easy to update (edit JSON file only)
- ✅ Non-technical team members can update locators
- ✅ Production-ready architecture

---

## 📝 Task 2: String Character Frequency

### Implementation

Located in `utils/string_frequency.py`:

```python
from utils.string_frequency import count_character_frequency

result = count_character_frequency("hello world")
print(result)  # Output: h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1
```

### Running

```bash
# Run the function directly
python utils/string_frequency.py

# Run unit tests
./run_tests.sh tests/test_string_frequency.py -v
```

---

## 🎁 Bonus Features

### Accessibility Testing

Automated WCAG 2.1 compliance checks using **axe-core**:

```bash
# Run all accessibility tests
./run_tests.sh -m accessibility
```

**Checks for:**
- ✅ Color contrast ratios
- ✅ Keyboard navigation
- ✅ Screen reader compatibility
- ✅ ARIA labels and roles
- ✅ Form accessibility
- ✅ Image alt text

### Performance Testing

Automated performance metrics and assertions:

```bash
# Run all performance tests
./run_tests.sh -m performance
```

**Metrics measured:**
- ⏱️ Page load time
- 🚀 Time to Interactive
- 🌐 DNS lookup time
- 📥 Request/response time
- 📦 Resource counts

---

## 🔍 Adding New Tests

### 1. Add Locators to JSON

```json
{
  "New Page": {
    "submit_button": {
      "name": "Submit Button",
      "locator": "//button[@type='submit']",
      "type": "xpath"
    }
  }
}
```

### 2. Create Locator Class

```python
# resources/locators/new_page_locators.py
from utils.locator_reader import LOCATORS

class NewPageLocators:
    def __init__(self):
        locators = LOCATORS["New Page"]
        self.submit_button = locators["submit_button"]["locator"]
```

### 3. Create Page Object

```python
# pages/new_page.py
from pages.base_page import BasePage
from resources.locators.new_page_locators import NewPageLocators

class NewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.locators = NewPageLocators()
    
    def submit_form(self):
        self.click(self.locators.submit_button)
```

### 4. Write Test

```python
# tests/test_new_page.py
import pytest

@pytest.mark.regression
def test_new_feature(new_page):
    new_page.load()
    new_page.submit_form()
    assert True
```

---

## 🛠️ Troubleshooting

### Installation Issues

```bash
# If make setup fails, try manual installation:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### Tests Fail to Start

```bash
# Verify .env file exists
ls -la .env

# If missing, copy from example
cp .env.example .env
```

### Element Not Found Errors

1. Check if locators in `resources/locators/locators.json` are correct
2. Run in headed mode to see what's happening: `HEADLESS=false` in `.env`
3. Increase timeout in `.env`: `DEFAULT_TIMEOUT=60000`

### Browser Launch Fails

```bash
# Reinstall browsers
playwright install
```

---

## 🎓 Best Practices Implemented

✅ **External Locator Management** - All locators in JSON files  
✅ **XPath Locators** - Reliable element identification  
✅ **Page Object Model** - Clean code organization  
✅ **Smart Waits** - No flaky time.sleep() calls  
✅ **Type Hints** - Better IDE support and code clarity  
✅ **Comprehensive Logging** - Easy debugging  
✅ **Screenshot on Failure** - Attached to Allure reports  
✅ **Cross-Browser Testing** - Multi-browser support  
✅ **Allure Reporting** - Advanced test analytics  
✅ **Accessibility Testing** - WCAG 2.1 compliance  
✅ **Performance Testing** - Automated performance metrics  
✅ **Parallel Execution** - Fast test execution  

---

## 👥 Author

Shehzaan Ansari

**Last Updated**: December 2025