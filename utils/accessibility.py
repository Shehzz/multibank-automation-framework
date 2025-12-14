"""
Accessibility Testing Utilities
Uses axe-core for WCAG compliance checks
"""
import logging

logger = logging.getLogger(__name__)


class AccessibilityChecker:
    """Accessibility testing using axe-core."""

    def __init__(self, page):
        """Initialize with Playwright page."""
        self.page = page
        self._inject_axe()

    def _inject_axe(self):
        """Inject axe-core library into the page."""
        try:
            # Inject axe-core from CDN
            self.page.add_script_tag(
                url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.2/axe.min.js"
            )
            logger.info("✓ axe-core library injected")
        except Exception as e:
            logger.warning(f"Failed to inject axe-core: {e}")

    def check_page(self, url: str = None) -> dict:
        """
        Run accessibility checks on current page.

        Args:
            url: Optional URL description for logging

        Returns:
            Dictionary with violations, passes, and incomplete checks
        """
        if url:
            logger.info(f"Running accessibility checks on: {url}")

        try:
            # Run axe accessibility checks
            results = self.page.evaluate("""
                () => {
                    return new Promise((resolve) => {
                        axe.run().then(results => {
                            resolve({
                                violations: results.violations,
                                passes: results.passes.length,
                                incomplete: results.incomplete.length
                            });
                        });
                    });
                }
            """)

            violations_count = len(results.get('violations', []))
            passes_count = results.get('passes', 0)

            if violations_count > 0:
                logger.warning(f"⚠️ Found {violations_count} accessibility violations")
                self._log_violations(results['violations'])
            else:
                logger.info(f"✓ No accessibility violations found ({passes_count} checks passed)")

            return results

        except Exception as e:
            logger.error(f"Accessibility check failed: {e}")
            return {"violations": [], "passes": 0, "incomplete": 0, "error": str(e)}

    def _log_violations(self, violations: list):
        """Log details of accessibility violations."""
        for violation in violations[:5]:  # Log first 5 violations
            impact = violation.get('impact', 'unknown')
            description = violation.get('description', 'No description')
            help_url = violation.get('helpUrl', '')

            logger.warning(f"  [{impact.upper()}] {description}")
            if help_url:
                logger.warning(f"    More info: {help_url}")

    def assert_no_critical_violations(self):
        """Assert that page has no critical accessibility violations."""
        results = self.check_page()
        violations = results.get('violations', [])

        critical_violations = [
            v for v in violations
            if v.get('impact') in ['critical', 'serious']
        ]

        if critical_violations:
            error_msg = f"Found {len(critical_violations)} critical/serious accessibility violations:\n"
            for v in critical_violations[:3]:
                error_msg += f"  - {v.get('description')}\n"
            raise AssertionError(error_msg)

        logger.info("✓ No critical accessibility violations")