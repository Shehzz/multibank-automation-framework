"""
Home Page Locators for Playwright
Loads locators from locators.json
"""
from utils.locator_reader import LOCATORS


class HomeLocators:
    """Locators for Home Page - Playwright compatible"""

    def __init__(self):
        locators = LOCATORS["Home Page"]

        # One-liner locator assignments (clean and maintainable)
        self.nav_menu = locators["nav_menu"]["locator"]
        self.nav_items = locators["nav_items"]["locator"]
        self.nav_item_by_text = locators["nav_item_by_text"]["locator"]
        self.nav_dropdown_links = locators["nav_dropdown_links"]["locator"]
        self.spot_trade = locators["spot_trade"]["locator"]
        self.category_tabs = locators["category_tabs"]["locator"]
        self.category_tab_name = locators["category_tab_name"]["locator"]
        self.trading_pairs = locators["trading_pairs"]["locator"]
        self.change_direction = locators["change_direction"]["locator"]
        self.banner_section = locators["banner_section"]["locator"]
        self.banner_items = locators["banner_items"]["locator"]
        self.app_store_link = locators["app_store_link"]["locator"]
        self.google_play_link = locators["google_play_link"]["locator"]
        self.about_us_nav = locators["about_us_nav"]["locator"]
        self.why_multibank = locators["why_multibank"]["locator"]