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
- About Us → Why MultiLink page content

## ✨ Key Features

- **Modern Framework**: Built with Playwright 1.57.0 for fast, reliable automation
- **Page Object Model**: Clean separation of test logic and page interactions
- **External Locator Management**: All locators stored in JSON files (production-ready approach)
- **XPath Locators**: Reliable XPath-based element identification
- **Cross-Browser Support**: Tests run on Chromium, Firefox, and WebKit
- **Build Automation**: setup.py, pyproject.toml, and Makefile (like Maven/Gradle)
- **Data-Driven**: External test data management (no hard-coded assertions)
- **Smart Waits**: Auto-waiting with Playwright (no flaky time.sleep())
- **Rich Reporting**: HTML reports + Allure reports with screenshots on failure
- **Accessibility Testing**: WCAG 2.1 compliance checks using axe-core
- **Performance Testing**: Automated page load and resource optimization metrics
- **CI/CD Ready**: GitHub Actions workflow included
- **Parallel Execution**: Configurable parallel test execution via .env
- **Professional Logging**: Comprehensive logging for debugging
- **Type Hints**: Python type annotations throughout

## 📁 Project Structure

```
multibank-automation-framework/
├── .github/                    # CI/CD configuration
│   └── workflows/
│       └── test-automation.yml # GitHub Actions workflow
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

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd multibank-automation-framework
```

### Step 2: Choose Installation Method

#### Option A: Using Makefile (Recommended)

```bash
# Complete setup (install + browsers)
make setup

# Run tests
make test

# See all available commands
make help
```

#### Option B: Manual Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Install Allure (Optional - for advanced reporting)**
   ```bash
   # macOS
   brew install allure
   
   # Linux
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   
   # Or download binary from:
   # https://github.com/allure-framework/allure2/releases
   ```
   
   > **Note:** `allure-pytest` (Python package) is already in `requirements.txt`.  
   > The `allure` CLI tool is needed only to **view** the reports.

5. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

6. **Verify installation**
   ```bash
   pytest tests/test_string_frequency.py -v
   ```

## 🔧 Build Automation

This framework includes **build automation** similar to Maven/Gradle/npm:

### Using Makefile Commands

```bash
# Testing
make test              # Run all tests
make test-smoke        # Run smoke tests only
make test-regression   # Run regression tests
make test-parallel     # Run tests in parallel
make test-firefox      # Run tests in Firefox
make test-chromium     # Run tests in Chromium
make test-cross-browser # Run on multiple browsers

# Code Quality
make lint              # Run code linting
make format            # Format code with black
make coverage          # Generate test coverage report

# Build & Install
make install           # Install dependencies
make install-dev       # Install with dev dependencies
make build             # Build distribution package
make clean             # Clean build artifacts

# Utilities
make browsers          # Install Playwright browsers
make check             # Verify installation
```

### Using setup.py

```bash
# Install framework
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Build distribution
python setup.py sdist bdist_wheel
```

## 🧪 Running Tests

### Using Test Runner Script (Recommended for Parallel Execution)
```bash
# Uses PARALLEL_WORKERS from .env automatically
./run_tests.sh tests/test_navigation.py

# Run all tests with parallel workers from .env
./run_tests.sh

# Pass any pytest arguments
./run_tests.sh tests/ -v -k "navigation"
```

### Using Makefile
```bash
make test                    # All tests
make test-smoke             # Smoke tests only
make test-navigation        # Navigation tests
make test-parallel          # Parallel execution (uses .env PARALLEL_WORKERS)
make quick-test             # Quick verification
```

### Using pytest Directly

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_navigation.py

# Run specific test
pytest tests/test_navigation.py::TestNavigation::test_navigation_menu_displays

# Run by marker
pytest -m smoke
pytest -m regression
pytest -m navigation

# Run in specific browser
pytest --browser firefox
pytest --browser chromium
pytest --browser webkit

# Run cross-browser
pytest --browser chromium --browser firefox

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

## 📊 Advanced Reporting with Allure

### Setup Allure (One-Time)

The `allure-pytest` Python package is already installed via `requirements.txt`. You just need the Allure CLI tool:

```bash
# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Verify installation
allure --version
```

### Make Scripts Executable (First Time Only)

```bash
chmod +x run_tests.sh
chmod +x view_allure_report.sh
```

### Viewing Allure Reports

**Option 1: Automatic (Recommended)**
```bash
# Run tests and view report
./run_tests.sh tests/
./view_allure_report.sh
# Opens interactive report in browser automatically
```

**Option 2: Manual**
```bash
# Run tests (generates JSON results)
./run_tests.sh tests/

# Serve interactive report
allure serve reports/allure-results

# OR generate static HTML
allure generate reports/allure-results -o reports/allure-report --clean
open reports/allure-report/index.html
```

### Allure Report Features

- 📈 **Test execution trends** - Track pass/fail rates over time
- ⏱️ **Duration metrics** - See which tests are slowest
- 📸 **Screenshots & videos** - Attached to failed tests automatically
- 🏷️ **Categorization** - Tests grouped by markers and features
- 📊 **Beautiful graphs** - Visual analytics and timelines
- 🔍 **Detailed logs** - Step-by-step execution details

**Full documentation:** `docs/ALLURE_SETUP.md`

## ♿ Accessibility Testing

The framework includes automated accessibility testing using **axe-core** for WCAG 2.1 compliance:

```bash
# Run all accessibility tests
./run_tests.sh -m accessibility

# Run specific test
./run_tests.sh tests/test_accessibility.py::TestAccessibility::test_home_page_accessibility
```

**What it checks:**
- ✅ Color contrast ratios
- ✅ Keyboard navigation
- ✅ Screen reader compatibility
- ✅ ARIA labels and roles
- ✅ Form accessibility
- ✅ Image alt text
- ✅ Heading structure

**Example output:**
```
Accessibility Results:
  ✓ Passed checks: 47
  ⚠️ Violations: 2
  [MODERATE] Images must have alternate text
    More info: https://dequeuniversity.com/rules/axe/4.8/image-alt
```

## ⚡ Performance Testing

Automated performance metrics and assertions:

```bash
# Run all performance tests
./run_tests.sh -m performance

# Run specific test
./run_tests.sh tests/test_performance.py::TestPerformance::test_home_page_load_time
```

**Metrics measured:**
- ⏱️ Page load time (< 10s)
- 🚀 Time to Interactive (< 6s)
- 🌐 DNS lookup time
- 🔌 TCP connection time
- 📥 Request/response time
- 📦 Resource counts (scripts, images, etc.)

**Example output:**
```
Performance Metrics:
  DNS Lookup: 45ms
  TCP Connect: 67ms
  Request Time: 123ms
  Response Time: 234ms
  DOM Load: 456ms
  Page Load: 2341ms
  Time to Interactive: 1876ms
  
✓ Homepage loaded in 2.34s
```

**Full documentation:** `docs/BONUS_FEATURES.md`

### Using Environment Variables

```bash
# Browser selection (.env file takes precedence)
BROWSER=firefox pytest

# Headless mode
HEADLESS=true pytest

# Slow motion (for debugging)
SLOW_MO=500 pytest
```

## 🎨 Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.smoke` - Quick smoke tests for critical paths
- `@pytest.mark.regression` - Full regression test suite
- `@pytest.mark.navigation` - Navigation-related tests
- `@pytest.mark.trading` - Trading functionality tests
- `@pytest.mark.content` - Content validation tests
- `@pytest.mark.cross_browser` - Cross-browser compatibility tests
- `@pytest.mark.accessibility` - Accessibility compliance tests (WCAG 2.1)
- `@pytest.mark.performance` - Performance and load time tests

**Run tests by marker:**
```bash
# Accessibility tests
./run_tests.sh -m accessibility

# Performance tests
./run_tests.sh -m performance

# Both accessibility and performance
./run_tests.sh -m "accessibility or performance"
```

## ⚙️ Configuration

### Environment Variables

Configure the framework by setting environment variables in `.env` file:

```bash
# Application
BASE_URL=https://trade.multibank.io/

# Browser Settings
BROWSER=firefox          # chromium, firefox, webkit (from .env or --browser flag)
HEADLESS=false          # true for CI/CD
SLOW_MO=0              # Slow down by milliseconds
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Timeouts (milliseconds)
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=30000

# Test Execution
MAX_RETRIES=2

# Screenshots
SCREENSHOT_ON_FAILURE=true

# Logging
LOG_LEVEL=INFO
```

**Note**: Command line `--browser` flag overrides `.env` setting.

### Locator Management (Production Approach)

**All locators are stored externally in JSON files** for easy maintenance:

#### locators.json
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

#### home_locators.py
```python
class HomeLocators:
    def __init__(self):
        locators = LOCATORS["Home Page"]
        self.nav_menu = locators["nav_menu"]["locator"]
```

#### Usage in Page Objects
```python
class HomePage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page)
        self.locators = HomeLocators()  # Load from JSON
    
    def is_navigation_displayed(self):
        return self.is_visible(self.locators.nav_menu)  # Use locator
```

**Benefits**:
- ✅ No hardcoded locators in code
- ✅ Easy to update (edit JSON file only)
- ✅ Non-technical team members can update locators
- ✅ Version control friendly
- ✅ Production-ready approach

### Test Data

Edit `config/test_data.json` to update expected values:

```json
{
  "navigation": {
    "expected_menu_items": ["Markets", "Trading", "About"]
  }
}
```

## 📊 Reporting

### HTML Report

After test execution, view the HTML report:
```bash
open reports/report.html  # macOS
start reports/report.html # Windows
xdg-open reports/report.html # Linux
```

### Coverage Report

Generate test coverage:
```bash
make coverage
# View: htmlcov/index.html
```

### Screenshots

Failed tests automatically capture screenshots in `screenshots/` directory.

### Logs

Detailed execution logs are saved in `reports/test_execution.log`.

## 🏗️ Architecture & Design Decisions

### Page Object Model (POM) with External Locators

The framework implements **production-grade POM** with:

1. **BasePage**: Common methods for all pages (click, fill, wait, etc.)
2. **Specific Page Classes**: HomePage, TradingPage inherit from BasePage
3. **External Locator Files**: All locators stored in `resources/locators/locators.json`
4. **Locator Classes**: Type-safe access to locators (e.g., `HomeLocators`)
5. **Separation of Concerns**: Test logic → Page Objects → Locators (3 layers)

**Traditional POM** (hardcoded):
```python
class HomePage:
    NAV_MENU = "//nav"  # ❌ Hardcoded
```

**Our Approach** (externalized):
```python
class HomePage:
    def __init__(self):
        self.locators = HomeLocators()  # ✅ From JSON
```

### Why XPath Over CSS?

- **Reliability**: More robust for complex DOM structures
- **Text-based selection**: Can locate by visible text
- **Flexibility**: Better handling of dynamic elements
- **Industry standard**: Widely used in enterprise automation

### Why Playwright?

1. **Auto-waiting**: Built-in smart waits eliminate flaky tests
2. **Speed**: Faster execution compared to Selenium
3. **Modern**: Supports modern web features (WebSockets, SPA)
4. **Cross-Browser**: Single API for Chromium, Firefox, WebKit
5. **Developer Experience**: Excellent debugging tools (trace viewer)

### Design Patterns Used

- **Page Object Model**: Encapsulates page elements and interactions
- **Repository Pattern**: Locators stored in external repository (JSON)
- **Fixture Pattern**: Pytest fixtures for setup/teardown
- **Data-Driven Testing**: External JSON for test data
- **Factory Pattern**: Browser and page creation

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
    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.locators = NewPageLocators()
    
    def submit_form(self):
        self.click(self.locators.submit_button)
```

### 4. Add Fixture

```python
@pytest.fixture
def new_page(page):
    from pages.new_page import NewPage
    from config.settings import BASE_URL
    return NewPage(page, BASE_URL)
```

### 5. Write Test

```python
import pytest

@pytest.mark.regression
def test_new_feature(new_page):
    new_page.load()
    new_page.submit_form()
    assert True
```

## 🛠️ Troubleshooting

### Tests fail to start
```bash
# Verify installation
make check

# Reinstall
make install
```

### Element not found errors
- Update locators in `resources/locators/locators.json`
- Increase timeout in settings.py
- Use browser in headed mode: `HEADLESS=false pytest`

### Browser launch fails
```bash
# Install browsers
make browsers
```

### Build errors
```bash
# Clean and rebuild
make clean
make build
```

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
# Run the script
python utils/string_frequency.py

# Run tests
pytest tests/test_string_frequency.py -v

# Or using Makefile
make run-string-frequency
```

## 🚀 CI/CD Integration

### GitHub Actions

Workflow file: `.github/workflows/test-automation.yml`

### CI Commands

```bash
# Run CI tests
make ci-test

# Run with coverage
make ci-coverage
```

## 📦 Building Distribution Package

```bash
# Build package
make build

# Output: dist/multibank-automation-framework-1.0.0.tar.gz
```

## 🎓 Best Practices Implemented

✅ **External Locator Management** - All locators in JSON files  
✅ **XPath Locators** - Reliable element identification  
✅ **Build Automation** - Makefile, setup.py, pyproject.toml  
✅ **Page Object Model** - Clean code organization  
✅ **Smart Waits** - No flaky time.sleep() calls  
✅ **Type Hints** - Better IDE support  
✅ **Comprehensive Logging** - Easy debugging  
✅ **Screenshot on Failure** - Visual debugging  
✅ **Cross-Browser Testing** - Multi-browser support  
✅ **CI/CD Ready** - GitHub Actions integration  
✅ **Allure Reporting** - Advanced test analytics and trends  
✅ **Accessibility Testing** - WCAG 2.1 compliance checks  
✅ **Performance Testing** - Automated performance metrics  
✅ **Parallel Execution** - Configurable parallel test runs  

## 📚 Documentation

- **Getting Started** - This README
- **Allure Setup** - `docs/ALLURE_SETUP.md`
- **Bonus Features** - `docs/BONUS_FEATURES.md` (Accessibility, Performance, CI/CD)
- **Parallel Testing** - `docs/PARALLEL_TESTING_GUIDE.md`
- **Execution Flow** - `docs/PARALLEL_EXECUTION_FLOW.md`

## 🎁 Bonus Features

This framework includes several advanced features:

- **CI/CD Pipeline Integration** - GitHub Actions with multi-browser testing
- **Advanced Reporting** - Allure reports with execution trends and analytics
- **Accessibility Testing** - Automated WCAG 2.1 compliance checks
- **Performance Testing** - Page load time and resource optimization metrics

See `docs/BONUS_FEATURES.md` for detailed documentation.

## 👥 Author

Shehzaan Ansari

**Last Updated**: December 2025
