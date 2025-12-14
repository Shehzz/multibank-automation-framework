"""
Base Page class containing common methods for all page objects.
Implements POM pattern with Playwright.
"""
from playwright.sync_api import Page, expect
from pathlib import Path
import logging
from config.settings import DEFAULT_TIMEOUT, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects.
    Contains common methods used across all pages.
    """

    def __init__(self, page: Page):
        """
        Initialize the base page with a Playwright page object.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.timeout = DEFAULT_TIMEOUT
        logger.info(f"Initialized {self.__class__.__name__}")

    def navigate(self, url: str):
        """
        Navigate to a specific URL.

        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)

    def click(self, locator: str):
        """
        Click on an element with automatic waiting.

        Args:
            locator: CSS selector or other locator string
        """
        logger.info(f"Clicking element: {locator}")
        self.page.locator(locator).click(timeout=self.timeout)

    def fill(self, locator: str, text: str):
        """
        Fill an input field with text.

        Args:
            locator: CSS selector or other locator string
            text: Text to enter
        """
        logger.info(f"Filling '{locator}' with text")
        self.page.locator(locator).fill(text, timeout=self.timeout)

    def get_text(self, locator: str) -> str:
        """
        Get text content of an element.

        Args:
            locator: CSS selector or other locator string

        Returns:
            Text content of the element
        """
        element = self.page.locator(locator).first
        return element.text_content(timeout=self.timeout)

    def get_all_text(self, locator: str) -> list:
        """
        Get text content from all matching elements.

        Args:
            locator: CSS selector or other locator string

        Returns:
            List of text contents
        """
        elements = self.page.locator(locator).all()
        return [elem.text_content() for elem in elements if elem.text_content()]

    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible on the page.

        Args:
            locator: CSS selector or other locator string
            timeout: Maximum time to wait (default 5 seconds)

        Returns:
            True if visible, False otherwise
        """
        try:
            return self.page.locator(locator).first.is_visible(timeout=timeout)
        except Exception:
            return False

    def wait_for_element(self, locator: str, state: str = "visible"):
        """
        Wait for element to reach a specific state.

        Args:
            locator: CSS selector or other locator string
            state: Element state (visible, hidden, attached, detached)
        """
        logger.info(f"Waiting for element '{locator}' to be {state}")
        self.page.locator(locator).first.wait_for(state=state, timeout=self.timeout)

    def scroll_to_element(self, locator: str):
        """
        Scroll element into view.

        Args:
            locator: CSS selector or other locator string
        """
        logger.info(f"Scrolling to element: {locator}")
        self.page.locator(locator).first.scroll_into_view_if_needed(timeout=self.timeout)

    def get_attribute(self, locator: str, attribute: str) -> str:
        """
        Get attribute value of an element.

        Args:
            locator: CSS selector or other locator string
            attribute: Attribute name

        Returns:
            Attribute value
        """
        return self.page.locator(locator).first.get_attribute(attribute, timeout=self.timeout)

    def take_screenshot(self, name: str = None) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            name: Screenshot filename (without extension)

        Returns:
            Path to the screenshot file
        """
        if name is None:
            from datetime import datetime
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        screenshot_path = SCREENSHOTS_DIR / f"{name}.png"
        logger.info(f"Taking screenshot: {screenshot_path}")
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        return screenshot_path

    def wait_for_load_state(self, state: str = "load"):
        """
        Wait for page to reach a specific load state.

        Args:
            state: Load state (load, domcontentloaded, networkidle)
        """
        logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state, timeout=self.timeout)

    def wait_until_loaded(self, selector: str = None, timeout: int = None):
        """
        Wait until page is fully loaded by combining multiple strategies.

        Args:
            selector: Optional specific element to wait for (e.g., main navigation)
            timeout: Optional timeout in milliseconds
        """
        if timeout is None:
            timeout = self.timeout

        logger.info("Waiting for page to be fully loaded")

        # Strategy 1: Wait for DOM
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

        # Strategy 2: If selector provided, wait for it
        if selector:
            logger.info(f"Waiting for element: {selector}")
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)

        logger.info("Page loaded successfully")

    def wait_until_page_fully_loads(self, key_elements: list = None, timeout: int = None):
        """
        Comprehensive page load wait using multiple strategies.
        More reliable than networkidle for sites with constant network activity.

        Args:
            key_elements: List of critical element selectors that indicate page is ready
                         (e.g., ['//nav', '//footer', '//main'])
            timeout: Optional timeout in milliseconds

        Strategy:
        1. Wait for DOM to be ready
        2. Wait for document.readyState === 'complete'
        3. Wait for all key elements to be visible

        Example:
            page.wait_until_page_fully_loads(key_elements=['//nav', '//main'])
        """
        if timeout is None:
            timeout = self.timeout

        logger.info("Starting comprehensive page load wait")

        try:
            # Strategy 1: Wait for DOM content to load
            logger.info("Step 1/3: Waiting for DOM content")
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

            # Strategy 2: Wait for document.readyState to be 'complete'
            logger.info("Step 2/3: Waiting for document.readyState === 'complete'")
            self.page.wait_for_function(
                "document.readyState === 'complete'",
                timeout=timeout
            )

            # Strategy 3: Wait for key elements if provided
            if key_elements:
                logger.info(f"Step 3/3: Waiting for {len(key_elements)} key elements")
                for idx, element in enumerate(key_elements, 1):
                    logger.info(f"  [{idx}/{len(key_elements)}] Waiting for: {element}")
                    self.page.wait_for_selector(
                        element,
                        state="visible",
                        timeout=timeout
                    )
            else:
                logger.info("Step 3/3: No key elements specified, skipping")


            logger.info("✓ Page fully loaded successfully")

        except Exception as e:
            logger.error(f"Page load wait failed: {e}")
            raise

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def hover(self, locator: str):
        """
        Hover over an element.

        Args:
            locator: CSS selector or other locator string
        """
        logger.info(f"Hovering over: {locator}")
        self.page.locator(locator).first.hover(timeout=self.timeout)

    def get_element_count(self, locator: str) -> int:
        """
        Get count of elements matching the locator.

        Args:
            locator: CSS selector or other locator string

        Returns:
            Number of matching elements
        """
        return self.page.locator(locator).count()

    def wait_for_url(self, url_pattern: str):
        """
        Wait for URL to match a pattern.

        Args:
            url_pattern: URL pattern to match
        """
        logger.info(f"Waiting for URL: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=self.timeout)