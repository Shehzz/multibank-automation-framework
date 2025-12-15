"""
Accessibility Tests:
Tests for WCAG compliance and accessibility standards.
"""
import pytest
import logging
from pages.home_page import HomePage
from utils.accessibility import AccessibilityChecker

logger = logging.getLogger(__name__)


@pytest.mark.accessibility
@pytest.mark.regression
class TestAccessibility:
    """Test suite for accessibility compliance."""

    def test_home_page_accessibility(self, loaded_home_page: HomePage):
        """
        Test homepage for accessibility violations.

        Test Steps:
        1. Load home page
        2. Run axe-core accessibility checks
        3. Assert no critical/serious violations
        """
        logger.info("Test: Checking homepage accessibility")

        loaded_home_page.wait_until_page_fully_loads()
        # Initialize accessibility checker
        a11y = AccessibilityChecker(loaded_home_page.page)

        # Run accessibility checks
        results = a11y.check_page("Home Page")

        # Get violations
        violations = results.get('violations', [])
        passes = results.get('passes', 0)

        # Log summary
        logger.info(f"Accessibility Results:")
        logger.info(f"  ✓ Passed checks: {passes}")
        logger.info(f"  ⚠️ Violations: {len(violations)}")

        # Assert no critical violations
        critical_violations = [
            v for v in violations
            if v.get('impact') in ['critical', 'serious']
        ]

        assert len(critical_violations) == 0, \
            f"❌ Found {len(critical_violations)} critical/serious accessibility violations"

        logger.info("✓ No critical accessibility violations found")

    def test_why_multibank_page_accessibility(self, loaded_home_page: HomePage):
        """
        Test Why Multibank page for accessibility violations.

        Test Steps:
        1. Navigate to Why Multibank page
        2. Run axe-core accessibility checks
        3. Verify accessibility compliance
        """
        logger.info("Test: Checking trading section accessibility")

        # Navigate to Why Multibank page
        loaded_home_page.navigate_to_why_multibank()

        # Initialize accessibility checker
        a11y = AccessibilityChecker(loaded_home_page.page)

        # Run accessibility checks and assert no critical violations
        a11y.assert_no_critical_violations()

        logger.info("✓ Why Multibank page accessibility verified")