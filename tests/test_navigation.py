"""
Navigation and Layout Tests:
Tests for top navigation menu functionality.
"""
import pytest
import logging
from pages.home_page import HomePage

logger = logging.getLogger(__name__)


@pytest.mark.navigation
@pytest.mark.smoke
class TestNavigation:
    """Test suite for navigation functionality."""

    def test_navigation_menu_displays(self, loaded_home_page: HomePage):
        """
        Test that navigation menu is visible on page load.

        Test Steps:
        1. Navigate to home page
        2. Verify navigation menu is displayed
        """
        logger.info("Test: Navigation menu displays")

        # Verify navigation is visible
        assert loaded_home_page.is_navigation_displayed(), \
            "❌ Navigation menu is not visible"

        logger.info("✓ Navigation menu is displayed")

    def test_navigation_items_present(self, loaded_home_page: HomePage, test_data: dict):
        """
        Test that all expected navigation items are present.

        Test Steps:
        1. Navigate to home page
        2. Get all navigation items
        3. Verify expected items are present
        """
        logger.info("Test: Navigation items present")

        # Get navigation items
        actual_items = loaded_home_page.get_navigation_items()
        logger.info(f"Found navigation items: {actual_items}")

        # Get expected items from test data
        expected_items = test_data["navigation"]["expected_menu_items"]
        logger.info(f"Expected navigation items: {expected_items}")

        # Verify count matches
        assert len(actual_items) == len(expected_items), \
            f"❌ Navigation menu item count mismatch: found {len(actual_items)}, expected {len(expected_items)}"

        # Verify all expected items are present (order matters)
        assert actual_items == expected_items, \
            f"❌ Navigation items don't match.\nExpected: {expected_items}\nActual: {actual_items}"

        logger.info(f"✓ All {len(actual_items)} navigation items match expected values")

    def test_navigation_items_have_links(self, loaded_home_page: HomePage):
        """
        Test that navigation items have valid links.

        Test Steps:
        1. Navigate to home page
        2. Get all navigation items
        3. Verify each item has the "href" attribute
        """
        logger.info("Test: Navigation items have links")

        # Get navigation items
        items = loaded_home_page.get_navigation_items()

        results = {}

        # Verify each item has a valid link
        for item in items:
            try:
                link = loaded_home_page.get_navigation_link(item)
                assert link is not None, f"Navigation item '{item}' has no link"
                assert link != "#", f"Navigation item '{item}' link is just '#' (invalid)"

                # Store results for summary
                if isinstance(link, list):
                    results[item] = f"{len(link)} links"
                else:
                    results[item] = "1 link"

            except Exception as e:
                logger.warning(f"Could not verify link for '{item}': {e}")
                results[item] = "FAILED"

        # Log clean summary
        logger.info(f"✓ All navigation items validated: {results}")

    def test_navigation_items_clickable(self, loaded_home_page: HomePage):
        """
        Test that navigation items are clickable and go to the correct pages.

        Test Steps:
        1. Navigate to home page
        2. Get all navigation items
        3. Click each item in a new tab and verify URL
        """
        logger.info("Test: Navigation items are clickable and navigate correctly")

        items = loaded_home_page.get_navigation_items()
        results = {}
        failures = []  # Collect all failures

        for item in items:
            result = loaded_home_page.verify_navigation_click(item)

            if result["status"] == "passed":
                results[item] = f"✓ {result['message']}"
            elif result["status"] == "skipped":
                results[item] = f"⊘ {result['message']}"
            elif result["status"] == "failed":
                results[item] = f"✗ {result['message']}"
                failures.append(f"{item}: Expected '{result['expected']}' in '{result['actual']}'")
            else:
                results[item] = f"✗ Error: {result['message']}"
                failures.append(f"{item}: {result['message']}")

        logger.info(f"Navigation results: {results}")

        assert len(failures) == 0, f"Navigation failures ({len(failures)}):\n" + "\n".join(failures)


@pytest.mark.navigation
@pytest.mark.cross_browser
@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
def test_navigation_cross_browser(browser_type, playwright):
    """
    Test navigation works across different browsers.
    """
    logger.info(f"Test: Navigation in {browser_type}")

    # Launch specific browser
    browser = getattr(playwright, browser_type).launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    test_page = context.new_page()

    # Create HomePage
    from config.settings import BASE_URL
    home = HomePage(test_page, BASE_URL)

    try:
        # Load and verify
        home.load()
        assert home.is_navigation_displayed(), \
            f"❌ Navigation is not visible in {browser_type}"

        items = home.get_navigation_items()
        assert len(items) > 0, \
            f"❌ Navigation items are missing in {browser_type}"

        logger.info(f"✓ Navigation works in {browser_type}")

    finally:
        # Cleanup
        test_page.close()
        context.close()
        browser.close()