"""
Performance Testing Utilities
Measures page load times, network metrics, and performance scores
"""
import logging
import time

logger = logging.getLogger(__name__)


class PerformanceChecker:
    """Performance testing using Playwright metrics."""

    def __init__(self, page):
        """Initialize with Playwright page."""
        self.page = page

    def measure_page_load(self) -> dict:
        """
        Measure page load performance metrics.

        Returns:
            Dictionary with timing metrics
        """
        try:
            # Get performance timing from browser
            metrics = self.page.evaluate("""
                () => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    
                    // Helper to safely calculate duration
                    const safeDuration = (end, start) => {
                        if (!end || !start || end === 0 || start === 0) return 0;
                        return Math.round(end - start);
                    };
                    
                    return {
                        dns_lookup: safeDuration(perfData.domainLookupEnd, perfData.domainLookupStart),
                        tcp_connect: safeDuration(perfData.connectEnd, perfData.connectStart),
                        request_time: safeDuration(perfData.responseStart, perfData.requestStart),
                        response_time: safeDuration(perfData.responseEnd, perfData.responseStart),
                        dom_load: safeDuration(perfData.domContentLoadedEventEnd, perfData.domContentLoadedEventStart),
                        dom_interactive: safeDuration(perfData.domInteractive, perfData.fetchStart),
                        first_paint: Math.round(performance.getEntriesByType('paint')[0]?.startTime || 0),
                        // For client-side rendered apps, use domContentLoaded as fallback
                        page_load: perfData.loadEventEnd && perfData.loadEventEnd > 0 
                            ? Math.round(perfData.loadEventEnd - perfData.fetchStart)
                            : Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart)
                    };
                }
            """)

            logger.info("Performance Metrics:")
            logger.info(f"  DNS Lookup: {metrics['dns_lookup']}ms")
            logger.info(f"  TCP Connect: {metrics['tcp_connect']}ms")
            logger.info(f"  Request Time: {metrics['request_time']}ms")
            logger.info(f"  Response Time: {metrics['response_time']}ms")
            logger.info(f"  DOM Load: {metrics['dom_load']}ms")
            logger.info(f"  Page Load: {metrics['page_load']}ms")
            logger.info(f"  DOM Interactive: {metrics['dom_interactive']}ms")
            logger.info(f"  First Paint: {metrics['first_paint']}ms")

            return metrics

        except Exception as e:
            logger.error(f"Failed to measure performance: {e}")
            return {}

    def assert_page_loads_within(self, max_seconds: int = 5):
        """
        Assert that page loads within specified time.

        Args:
            max_seconds: Maximum allowed page load time
        """
        metrics = self.measure_page_load()
        page_load_ms = metrics.get('page_load', 0)
        page_load_seconds = page_load_ms / 1000

        assert page_load_seconds <= max_seconds, \
            f"❌ Page load time {page_load_seconds:.2f}s exceeds {max_seconds}s limit"

        logger.info(f"✓ Page loaded in {page_load_seconds:.2f}s (within {max_seconds}s limit)")

    def get_resource_count(self) -> dict:
        """
        Get count of resources loaded on page.

        Returns:
            Dictionary with resource counts by type
        """
        try:
            resources = self.page.evaluate("""
                () => {
                    const resources = performance.getEntriesByType('resource');
                    const counts = {
                        total: resources.length,
                        scripts: 0,
                        stylesheets: 0,
                        images: 0,
                        fonts: 0,
                        xhr: 0,
                        other: 0
                    };
                    
                    resources.forEach(r => {
                        if (r.initiatorType === 'script') counts.scripts++;
                        else if (r.initiatorType === 'link' || r.initiatorType === 'css') counts.stylesheets++;
                        else if (r.initiatorType === 'img') counts.images++;
                        else if (r.initiatorType === 'font') counts.fonts++;
                        else if (r.initiatorType === 'xmlhttprequest' || r.initiatorType === 'fetch') counts.xhr++;
                        else counts.other++;
                    });
                    
                    return counts;
                }
            """)

            logger.info("Resource Counts:")
            logger.info(f"  Total: {resources['total']}")
            logger.info(f"  Scripts: {resources['scripts']}")
            logger.info(f"  Stylesheets: {resources['stylesheets']}")
            logger.info(f"  Images: {resources['images']}")
            logger.info(f"  Fonts: {resources['fonts']}")
            logger.info(f"  XHR/Fetch: {resources['xhr']}")
            logger.info(f"  Other: {resources['other']}")

            return resources

        except Exception as e:
            logger.error(f"Failed to get resource count: {e}")
            return {}

    def measure_time_to_interactive(self) -> float:
        """
        Measure time until page becomes interactive.

        Returns:
            Time to interactive in seconds
        """
        try:
            tti_ms = self.page.evaluate("""
                () => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    if (!perfData.domInteractive || perfData.domInteractive === 0) {
                        // Fallback for client-side rendered apps
                        return Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart);
                    }
                    return Math.round(perfData.domInteractive - perfData.fetchStart);
                }
            """)

            tti_seconds = tti_ms / 1000
            logger.info(f"Time to Interactive: {tti_seconds:.2f}s")

            return tti_seconds

        except Exception as e:
            logger.error(f"Failed to measure TTI: {e}")
            return 0.0