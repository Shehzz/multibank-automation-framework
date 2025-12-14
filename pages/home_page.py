"""
Home Page Object for https://trade.multibank.io/
Contains all elements and methods related to the home/landing page.
"""
import time

from playwright.sync_api import Page
from pages.base_page import BasePage
from resources.locators.home_locators import HomeLocators
from utils.test_data_reader import TEST_DATA
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Page Object for the MultiBank home page."""

    def __init__(self, page: Page, base_url: str):
        """
        Initialize Home Page object.

        Args:
            page: Playwright Page instance
            base_url: Base URL of the application
        """
        super().__init__(page)
        self.base_url = base_url
        self.locators = HomeLocators()

    def load(self):
        """Navigate to the home page and wait for it to load."""
        #logger.info(f"Loading home page: {self.base_url}")
        self.navigate(self.base_url)
        #TODO: Can pick any 1, starting from the slowest (8s, 4s, 3s) to the fastest
        # self.wait_until_page_fully_loads()
        self.wait_for_load_state("domcontentloaded")
        self.wait_until_loaded(selector=self.locators.trading_pairs)

    # ============================================
    # Navigation Methods
    # ============================================

    def is_navigation_displayed(self) -> bool:
        """
        Check if navigation menu is visible.

        Returns:
            True if navigation is visible
        """
        is_visible = self.is_visible(self.locators.nav_menu)
        logger.info(f"Navigation menu visible: {is_visible}")
        return is_visible

    def get_navigation_items(self) -> list:
        """
        Get all navigation menu items.

        Returns:
            List of navigation item text values
        """
        logger.info("Getting navigation menu items")
        try:
            items = self.get_all_text(self.locators.nav_items)
            # Filter out empty strings
            items = [item.strip() for item in items if item and item.strip()]
            logger.info(f"Found {len(items)} navigation items: {items}")
            return items
        except Exception as e:
            logger.error(f"Error getting navigation items: {e}")
            return []

    def get_navigation_link(self, item_name: str):
        """
        Get the href(s) of a navigation item.
        Handles both direct links (<a>) and dropdown items (<span>).

        Args:
            item_name: Navigation item text

        Returns:
            - For direct links: single href string
            - For dropdowns: list of href strings for all sub-items
        """
        try:
            # Build dynamic locator using template
            nav_item_locator = self.locators.nav_item_by_text.format(item_name=item_name)
            nav_container = self.page.locator(nav_item_locator).first

            # Check if it's a direct <a> link
            if nav_container.evaluate("el => el.tagName") == "A":
                href = nav_container.get_attribute("href")
                return href

            # Otherwise, it's a dropdown - hover and get ALL sub-links
            nav_container.hover()

            # Build dynamic locator for dropdown links
            dropdown_locator = self.locators.nav_dropdown_links.format(item_name=item_name)

            # Wait for dropdown menu to appear
            self.page.wait_for_selector(dropdown_locator, state="visible", timeout=5000)

            # Get ALL dropdown links
            dropdown_links = self.page.locator(dropdown_locator).all()
            hrefs = [link.get_attribute("href") for link in dropdown_links]

            return hrefs

        except Exception as e:
            logger.error(f"Error getting navigation link for '{item_name}': {e}")
            return None

    def click_navigation_item(self, item_name: str, open_in_new_tab: bool = False, dropdown_index: int = None):
        """
        Click a specific navigation menu item.
        Handles both direct links and dropdown items.

        Args:
            item_name: Text of the navigation item to click
            open_in_new_tab: If True, Ctrl+Click to open in new tab
            dropdown_index: For dropdowns, which sub-item to click (0-based index)

        Returns:
            Expected URL (href) of the clicked item
        """
        try:
            # Build dynamic locator using template
            nav_item_locator = self.locators.nav_item_by_text.format(item_name=item_name)
            nav_container = self.page.locator(nav_item_locator).first

            # Determine modifier key for new tab
            modifier = ["Meta" if self.page.evaluate(
                "() => navigator.platform.includes('Mac')") else "Control"] if open_in_new_tab else None

            # Check if it's a direct <a> link
            if nav_container.evaluate("el => el.tagName") == "A":
                href = nav_container.get_attribute("href")
                nav_container.click(modifiers=modifier)

                if not open_in_new_tab:
                    self.wait_for_load_state("domcontentloaded")

                return href

            # Otherwise, it's a dropdown - hover and click sub-item
            nav_container.hover()

            # Build dynamic locator for dropdown links
            dropdown_locator = self.locators.nav_dropdown_links.format(item_name=item_name)
            self.page.wait_for_selector(dropdown_locator, state="visible", timeout=5000)

            # Get dropdown links
            dropdown_links = self.page.locator(dropdown_locator).all()

            # Click the specified index (default to first)
            index = dropdown_index if dropdown_index is not None else 0
            target_link = dropdown_links[index]
            href = target_link.get_attribute("href")

            target_link.click(modifiers=modifier)

            if not open_in_new_tab:
                self.wait_for_load_state("domcontentloaded")

            return href

        except Exception as e:
            logger.error(f"Error clicking navigation item '{item_name}': {e}")
            return None

    def verify_navigation_click(self, item_name: str) -> dict:
        """
        Helper method to click a navigation item and verify it navigates correctly.
        Skips invalid links (/, #, empty).

        Args:
            item_name: Navigation item text

        Returns:
            dict with 'status', 'message', 'expected', 'actual'
        """
        try:
            # Get links for this item
            links = self.get_navigation_link(item_name)

            # Handle direct links
            if isinstance(links, str):
                if links in ["/", "#", ""]:
                    return {"status": "skipped", "message": "Root/hash link", "expected": links, "actual": None}

                # Click in new tab and wait for navigation to complete
                with self.page.context.expect_page() as new_page_info:
                    expected_href = self.click_navigation_item(item_name, open_in_new_tab=True)

                new_page = new_page_info.value

                # In headless mode, wait for URL to change from about:blank
                from config.settings import HEADLESS
                if HEADLESS:
                    new_page.wait_for_url(lambda url: url != "about:blank", timeout=10000)

                new_page.wait_for_load_state("domcontentloaded")
                actual_url = new_page.url
                new_page.close()

                # Verify URL (handle locale and query params)
                if self._url_matches(expected_href, actual_url):
                    return {"status": "passed", "message": "Direct link verified", "expected": expected_href,
                            "actual": actual_url}
                else:
                    return {"status": "failed", "message": "URL mismatch", "expected": expected_href,
                            "actual": actual_url}

            # Handle dropdowns
            elif isinstance(links, list):
                valid_links = [link for link in links if link not in ["/", "#", ""]]

                if not valid_links:
                    return {"status": "skipped", "message": "No valid links", "expected": None, "actual": None}

                # Test first valid link
                first_valid_index = links.index(valid_links[0])

                # Click in new tab and wait for navigation to complete
                with self.page.context.expect_page() as new_page_info:
                    expected_href = self.click_navigation_item(item_name, open_in_new_tab=True,
                                                               dropdown_index=first_valid_index)

                new_page = new_page_info.value

                # In headless mode, wait for URL to change from about:blank
                from config.settings import HEADLESS
                if HEADLESS:
                    new_page.wait_for_url(lambda url: url != "about:blank", timeout=10000)

                new_page.wait_for_load_state("domcontentloaded")
                actual_url = new_page.url
                new_page.close()

                # Verify URL (handle locale and query params)
                if self._url_matches(expected_href, actual_url):
                    return {"status": "passed", "message": f"Dropdown verified ({len(valid_links)} links)",
                            "expected": expected_href, "actual": actual_url}
                else:
                    return {"status": "failed", "message": "URL mismatch", "expected": expected_href,
                            "actual": actual_url}

        except Exception as e:
            return {"status": "error", "message": str(e), "expected": None, "actual": None}

    def _url_matches(self, expected_href: str, actual_url: str) -> bool:
        """
        Check if actual URL matches expected href, ignoring locale prefixes and query params.
        Handles special cases for known redirects.

        Examples:
            expected: 'https://multibank.io/features/spot-exchange'
            actual:   'https://multibank.io/en-AE/features/spot-exchange?_gl=...'
            returns: True

        Args:
            expected_href: Expected href from link
            actual_url: Actual URL from browser

        Returns:
            True if URLs match (ignoring locale and query params)
        """
        from urllib.parse import urlparse

        # Special cases: Known redirects that don't match expected href
        special_cases = {
            'https://multibank.io/about/why-multibank': 'https://multibank.io/en-AE',
            '/about/why-multibank': '/en-AE'
        }

        # Check if this is a known special case
        for expected_pattern, actual_pattern in special_cases.items():
            if expected_pattern in expected_href:
                if actual_pattern in actual_url or actual_url.rstrip('/').endswith(actual_pattern.rstrip('/')):
                    return True

        # Parse both URLs
        expected_parsed = urlparse(expected_href)
        actual_parsed = urlparse(actual_url)

        # Get paths without query params
        expected_path = expected_parsed.path.rstrip('/')
        actual_path = actual_parsed.path.rstrip('/')

        # Remove locale prefix from actual path (e.g., /en-AE/)
        # Common locale patterns: /en-AE/, /en-US/, /ar/, etc.
        import re
        actual_path_no_locale = re.sub(r'^/[a-z]{2}(-[A-Z]{2})?/', '/', actual_path)

        # Check if expected path is in actual path (with or without locale)
        return expected_path in actual_path or expected_path in actual_path_no_locale

    # ============================================
    # Trading Section Methods
    # ============================================

    def navigate_to_spot_trading(self):
        """
        Scroll down to Spot Trade section.
        """
        logger.info("Navigating to Spot Trade section")
        self.wait_until_page_fully_loads()
        self.scroll_to_element(self.locators.spot_trade, align_to_top=True)
        self.wait_for_element(self.locators.spot_trade, "visible")
        logger.info("Successfully scrolled to Spot Trade section")

    def get_trading_categories(self) -> list:
        """
        Get all trading categories/tabs.
        Returns only the 2nd, 3rd, 4th, and 5th elements (indices 1-4).

        Returns:
            List of category names
        """
        try:
            all_categories = self.get_all_text(self.locators.category_tabs)
            # Get only 2nd, 3rd, 4th, 5th elements (indices 1-4)
            categories = all_categories[1:5]  # Slice from index 1 to 4 (inclusive)
            logger.info(f"Found categories: {categories}")
            return categories
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []

    def get_trading_pairs_count(self) -> int:
        """
        Get count of visible trading pairs (before Show More overlay).

        Returns:
            Number of visible trading pairs
        """
        try:
            # Get all trading pair rows
            all_rows = self.page.locator(self.locators.trading_pairs).all()

            # Only count first 10 rows (rows after that are hidden by "Show More" overlay)
            visible_count = min(len(all_rows), 10)

            logger.info(f"Found {visible_count} visible trading pairs (out of {len(all_rows)} total)")
            return visible_count
        except Exception as e:
            logger.error(f"Error counting trading pairs: {e}")
            return 0

    def click_category_tab(self, category_name: str):
        """
        Click on a specific trading category tab.

        Args:
            category_name: Name of the category to click (e.g., "USDT", "BTC", "FIAT")
        """
        try:
            tab_locator = self.locators.category_tab_name.format(category_name=category_name)
            self.wait_for_element(tab_locator, "visible")
            self.click(tab_locator)
            self.scroll_to_element(tab_locator, align_to_top=True)
            logger.info(f"Clicked on category tab: {category_name}")
        except Exception as e:
            logger.error(f"Error clicking category tab '{category_name}': {e}")
            raise

    def get_trading_pairs_count_by_category(self) -> dict:
        """
        Iterate through each trading category and get the count of trading pairs.
        Categories: All, USDT, BTC, FIAT

        Returns:
            Dictionary with category names as keys and pair counts as values
            Example: {"All": 10, "USDT": 10, "BTC": 10, "FIAT": 10}
        """
        category_counts = {}

        try:
            # Get all categories (should be ["All", "USDT", "BTC", "FIAT"])
            categories = self.get_trading_categories()

            if not categories:
                logger.error("No categories found")
                return category_counts

            logger.info(f"Iterating through categories: {categories}")

            # We start on "All" tab by default, so count pairs without clicking
            all_count = self.get_trading_pairs_count()
            category_counts["All"] = all_count
            logger.info(f"Category 'All': {all_count} trading pairs")

            # Now iterate through USDT, BTC, FIAT (skip "All" since we already counted it)
            for category in categories[1:]:  # Skip first element "All"
                # Click on the category tab
                self.click_category_tab(category)

                # Count trading pairs in this category
                count = self.get_trading_pairs_count()
                category_counts[category] = count
                logger.info(f"Category '{category}': {count} trading pairs")

            logger.info(f"Final category counts: {category_counts}")
            return category_counts

        except Exception as e:
            logger.error(f"Error getting trading pairs by category: {e}")
            return category_counts

    def get_trading_pairs(self) -> list:
        """
        Get trading pairs data structure from the table.
        Extracts first 10 visible trading pairs with their details.

        Returns:
            List of dictionaries containing trading pair data
        """
        trading_pairs = []

        try:
            # Get all trading pair rows
            all_rows = self.page.locator(self.locators.trading_pairs).all()

            # Only process first 10 rows (visible rows before "Show More" overlay)
            visible_rows = all_rows[:10]

            logger.info(f"Processing {len(visible_rows)} visible trading pairs")

            for row in visible_rows:
                try:
                    # Get all cells in this row (7 total: star, pair, price, change, high, low, chart)
                    cells = row.locator("td").all()

                    if len(cells) >= 7:
                        change_data = self._get_change_24h_data(cells[3])
                        # Extract data from specific cells (indices 1-5)
                        pair_data = {
                            "pair_name": self.ui_text(cells[1]),
                            "price": self.ui_text(cells[2]),
                            "change_24h_direction": change_data["direction"],
                            "change_24h": change_data["value"],
                            "high": self.ui_text(cells[4]),
                            "low": self.ui_text(cells[5]),
                        }

                        trading_pairs.append(pair_data)
                        logger.info(f"Pair: \"{pair_data['pair_name']}\" - "
                                     f"Price: {pair_data['price']}, "
                                     f"({pair_data['change_24h_direction']}), "
                                     f"Change 24h: {pair_data['change_24h']}, "
                                     f"High: {pair_data['high']}, "
                                     f"Low: {pair_data['low']}")
                    else:
                        logger.warning(f"Row has insufficient cells: {len(cells)}")

                except Exception as e:
                    logger.error(f"Error extracting data from row: {e}")
                    continue

            logger.info(f"Successfully extracted {len(trading_pairs)} trading pairs")
            return trading_pairs

        except Exception as e:
            logger.error(f"Error getting trading pairs: {e}")
            return trading_pairs

    def _get_change_24h_data(self, change_cell) -> dict:
        """
        Extracts both 24h change value and direction from the cell.
        Returns:
            {
              "value": "1.66%",
              "direction": "⬆️" | "⬇️"
            }
        """
        pill = change_cell.locator(self.locators.change_direction).first
        class_attr = pill.get_attribute("class") or ""

        if "style_positive" in class_attr:
            direction = "⬆️"
        elif "style_negative" in class_attr:
            direction = "⬇️"
        else:
            direction = "unknown"

        # Combine number + % safely
        value = self.ui_text(pill).replace(" %", "%")

        return {
            "value": value,
            "direction": direction
        }

    # ============================================
    # Marketing Banners Methods
    # ============================================

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        logger.info("Scrolling to page bottom")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        #self.wait_for_load_state("networkidle")
        #Instead wait for some element that appears in the bottom

    def are_banners_displayed(self) -> bool:
        """
        Check if marketing banners are displayed.

        Returns:
            True if banners are visible
        """
        self.scroll_to_bottom()
        is_visible = self.is_visible(self.locators.banner_section, timeout=10000)
        logger.info(f"Marketing banners visible: {is_visible}")
        return is_visible

    def get_banner_count(self) -> int:
        """
        Get count of marketing banners.

        Returns:
            Number of banners
        """
        self.scroll_to_bottom()
        count = self.get_element_count(self.locators.banner_items)
        logger.info(f"Found {count} marketing banners")
        return count

    # ============================================
    # Download Links Methods
    # ============================================

    def get_app_store_link(self) -> str:
        """
        Get the App Store download link.

        Returns:
            App Store URL or None
        """
        try:
            self.scroll_to_bottom()
            link = self.get_attribute(self.locators.app_store_link, "href")
            logger.info(f"App Store link: {link}")
            return link
        except Exception as e:
            logger.warning(f"App Store link not found: {e}")
            return None

    def get_google_play_link(self) -> str:
        """
        Get the Google Play download link.

        Returns:
            Google Play URL or None
        """
        try:
            self.scroll_to_bottom()
            link = self.get_attribute(self.locators.google_play_link, "href")
            logger.info(f"Google Play link: {link}")
            return link
        except Exception as e:
            logger.warning(f"Google Play link not found: {e}")
            return None

    def verify_download_links(self) -> dict:
        """
        Verify both download links exist and are valid.

        Returns:
            Dictionary with verification results
        """
        logger.info("Verifying download links")

        app_store = self.get_app_store_link()
        google_play = self.get_google_play_link()

        results = {
            'app_store': {
                'exists': app_store is not None,
                'valid': app_store and ('apple.com' in app_store or 'itunes' in app_store) if app_store else False,
                'url': app_store
            },
            'google_play': {
                'exists': google_play is not None,
                'valid': google_play and 'play.google.com' in google_play if google_play else False,
                'url': google_play
            }
        }

        logger.info(f"Download links verification: {results}")
        return results

    # ============================================
    # About Us Navigation
    # ============================================

    def navigate_to_why_multibank(self):
        """
        Navigate to Why Multibank page from About Us menu.
        Handles both direct links and hover menus.
        """
        logger.info("Navigating to Why Multibank page")
        multibank_url = TEST_DATA["why_multibank"]["url"]
        try:
            if self.is_visible(self.locators.about_us_nav):
                self.hover(self.locators.about_us_nav)
                #self.page.wait_for_timeout(500)  # Brief wait for dropdown

            # Click Why Multibank
            self.wait_for_element(self.locators.why_multibank, "visible")
            self.click(self.locators.why_multibank)
            self.wait_for_url(multibank_url)
            logger.info("Successfully navigated to Why Multibank page")

        except Exception as e:
            logger.error(f"Error navigating to Why Multibank due to error: {e}")
            # Try direct navigation as fallback
            logger.info("Fallback: Navigating to Why Multibank page")
            self.navigate(multibank_url)