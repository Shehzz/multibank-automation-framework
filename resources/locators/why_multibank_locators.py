"""
Why Multibank Page Locators for Playwright
Loads locators from locators.json
"""
from utils.locator_reader import LOCATORS


class WhyMultibankLocators:
    """Locators for Home Page - Playwright compatible"""

    def __init__(self):
        locators = LOCATORS["Why Multibank Page"]

        # Hero Banner Carousel
        self.hero_carousel = locators["hero_carousel"]["locator"]
        self.hero_slides = locators["hero_slides"]["locator"]

        # Our Advantages Section
        self.advantages_section = locators["advantages_section"]["locator"]
        self.advantages_subtitle_h5 = locators["advantages_subtitle_h5"]["locator"]
        self.advantages_title_h2 = locators["advantages_title_h2"]["locator"]

        # Advantage Cards
        self.advantage_cards = locators["advantage_cards"]["locator"]
        self.card_fiat = locators["card_fiat"]["locator"]
        self.card_regulated = locators["card_regulated"]["locator"]
        self.card_security = locators["card_security"]["locator"]
        self.card_crypto = locators["card_crypto"]["locator"]
        self.card_service = locators["card_service"]["locator"]

        # Trading Opportunity Section
        self.trading_opportunity_h3 = locators["trading_opportunity_h3"]["locator"]

