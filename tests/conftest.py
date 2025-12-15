"""
Pytest configuration and fixtures for the test suite.
Contains shared fixtures used across all tests.
"""
import pytest
import logging
from playwright.sync_api import Page, Browser
from config.settings import (
    BASE_URL,
    BROWSER_TYPE,
    HEADLESS,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    SCREENSHOT_ON_FAILURE
)
from pages.home_page import HomePage
from pages.why_multibank_page import WhyMultibankPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Browser launch arguments."""
    import platform

    args = []

    # Add maximize in headed mode
    if not HEADLESS:
        args.append("--start-fullscreen")

    return {
        "headless": HEADLESS,
        "args": args
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context arguments."""
    return {
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }


@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args) -> Page:
    """
    Create a new page for each test.
    Automatically handles cleanup and screenshots on failure.
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    yield page

    # Cleanup
    page.close()
    context.close()

@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    """
    Fixture for HomePage object.

    Args:
        page: Playwright Page fixture

    Returns:
        HomePage instance
    """
    logger.info(f"Creating HomePage object")
    return HomePage(page, BASE_URL)

@pytest.fixture(scope="function")
def why_multibank_page(page: Page) -> WhyMultibankPage:
    """
    Fixture for WhyMultibankPage object.

    Args:
        page: Playwright Page fixture

    Returns:
        WhyMultibankPage instance
    """
    logger.info(f"Creating WhyMultibankPage object")
    return WhyMultibankPage(page)

@pytest.fixture(scope="function")
def loaded_home_page(home_page):
    """
    Fixture for HomePage object that's already loaded.

    Args:
        home_page: HomePage fixture

    Returns:
        HomePage instance with page already loaded
    """
    logger.info("Auto-loading home page")
    home_page.load()
    return home_page

@pytest.fixture(scope="session")
def test_data():
    """
    Provide test data from centralized test_data_reader.

    Returns:
        Dictionary containing test data
    """
    from utils.test_data_reader import TEST_DATA
    return TEST_DATA


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """Automatically log test start and end information."""
    logger.info(f"\n{'=' * 80}")
    logger.info(f"Starting test: {request.node.name}")
    logger.info(f"{'=' * 80}")

    yield

    logger.info(f"\n{'=' * 80}")
    logger.info(f"Finished test: {request.node.name}")
    logger.info(f"{'=' * 80}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test failures and take screenshots.
    Attaches screenshots to Allure reports.
    """
    outcome = yield
    rep = outcome.get_result()

    # Only capture screenshot on test failure during call phase
    if rep.when == "call" and rep.failed:
        if SCREENSHOT_ON_FAILURE:
            # Get the page fixture if it exists
            if "page" in item.funcargs:
                page = item.funcargs["page"]
                screenshot_name = f"FAILED_{item.name}"

                try:
                    from config.settings import SCREENSHOTS_DIR
                    import allure

                    screenshot_path = SCREENSHOTS_DIR / f"{screenshot_name}.png"
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"Screenshot saved: {screenshot_path}")

                    # Attach screenshot to Allure report
                    allure.attach.file(
                        str(screenshot_path),
                        name=screenshot_name,
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Screenshot attached to Allure report: {screenshot_name}")

                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers and browser settings."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "navigation: Navigation tests")
    config.addinivalue_line("markers", "trading: Trading functionality tests")
    config.addinivalue_line("markers", "content: Content validation tests")
    config.addinivalue_line("markers", "cross_browser: Cross-browser tests")
    config.addinivalue_line("markers", "accessibility: Accessibility tests")
    config.addinivalue_line("markers", "performance: Performance tests")

    # Set default browser from .env if not specified via command line
    if not config.option.browser:
        config.option.browser = [BROWSER_TYPE]
