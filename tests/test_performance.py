"""
Performance Tests:
Tests for page load performance, resource optimization, and speed metrics.
"""
import pytest
import logging
from pages.home_page import HomePage
from utils.performance import PerformanceChecker

logger = logging.getLogger(__name__)


@pytest.mark.performance
@pytest.mark.regression
class TestPerformance:
    """Test suite for performance metrics."""

    def test_home_page_load_time(self, loaded_home_page: HomePage):
        """
        Test homepage loads within acceptable time.

        Test Steps:
        1. Load home page
        2. Measure page load metrics
        3. Assert page loads within 10 seconds
        """
        logger.info("Test: Measuring homepage load time")

        # Initialize performance checker
        perf = PerformanceChecker(loaded_home_page.page)

        # Measure page load
        metrics = perf.measure_page_load()

        # Assert page loads within 10 seconds
        page_load_ms = metrics.get('page_load', 0)
        page_load_seconds = page_load_ms / 1000

        assert page_load_seconds > 0, "❌ Page load time not measured"
        assert page_load_seconds <= 10, \
            f"❌ Page load time {page_load_seconds:.2f}s exceeds 10s limit"

        logger.info(f"✓ Homepage loaded in {page_load_seconds:.2f}s")

    def test_home_page_time_to_interactive(self, loaded_home_page: HomePage):
        """
        Test homepage becomes interactive quickly.

        Test Steps:
        1. Load home page
        2. Measure time to interactive
        3. Assert TTI is within acceptable range
        """
        logger.info("Test: Measuring time to interactive")

        # Initialize performance checker
        perf = PerformanceChecker(loaded_home_page.page)

        # Measure TTI
        tti = perf.measure_time_to_interactive()

        # Assert TTI within 6 seconds
        assert tti > 0, "❌ Time to interactive not measured"
        assert tti <= 6, \
            f"❌ Time to interactive {tti:.2f}s exceeds 6s limit"

        logger.info(f"✓ Page interactive in {tti:.2f}s")

    def test_resource_optimization(self, loaded_home_page: HomePage):
        """
        Test page resources are optimized.

        Test Steps:
        1. Load home page
        2. Count loaded resources
        3. Verify reasonable resource counts
        """
        logger.info("Test: Checking resource optimization")

        # Initialize performance checker
        perf = PerformanceChecker(loaded_home_page.page)

        # Get resource counts
        resources = perf.get_resource_count()

        total = resources.get('total', 0)
        scripts = resources.get('scripts', 0)
        images = resources.get('images', 0)

        # Assert reasonable resource counts (not too bloated)
        assert total <= 200, \
            f"❌ Too many resources loaded: {total} (should be <= 200)"

        assert scripts <= 50, \
            f"❌ Too many scripts: {scripts} (should be <= 50)"

        logger.info(f"✓ Resource counts within acceptable limits")
        logger.info(f"  Total resources: {total}")
        logger.info(f"  Scripts: {scripts}")
        logger.info(f"  Images: {images}")