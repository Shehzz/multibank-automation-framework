"""
Page Object for Why Multibank page (About Us → Why MultiBank)
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from resources.locators.why_multibank_locators import WhyMultibankLocators
import logging

from utils.test_data_reader import TEST_DATA

logger = logging.getLogger(__name__)


class WhyMultibankPage(BasePage):
    """Page Object Model for Why MultiBank page"""

    def __init__(self, page: Page):
        """
        Initialize Why MultiBank page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = TEST_DATA["why_multibank"]["url"]
        self.locators = WhyMultibankLocators()

    def load(self):
        """Navigate to Why MultiBank page and wait for it to load"""
        logger.info(f"Navigating to Why MultiBank page: {self.url}")
        self.navigate(self.url)
        self.wait_until_page_fully_loads(
            key_elements=[self.locators.hero_carousel]
        )
        logger.info("Why MultiBank page loaded successfully")

    # ============================================================================
    # Component Visibility Checks
    # ============================================================================

    def is_hero_carousel_visible(self) -> bool:
        """
        Check if hero carousel is visible.

        Returns:
            bool: True if carousel is visible
        """
        return self.is_visible(self.locators.hero_carousel)

    def get_hero_slide_count(self) -> int:
        """
        Get number of hero banner slides.

        Returns:
            int: Number of slides in carousel
        """
        return self.get_element_count(self.locators.hero_slides)

    def is_advantages_section_visible(self) -> bool:
        """
        Check if 'Our Advantages' section is visible.

        Returns:
            bool: True if section is visible
        """
        return self.is_visible(self.locators.advantages_section)

    def get_advantage_cards_count(self) -> int:
        """
        Get number of advantage cards.

        Returns:
            int: Number of advantage cards (expected: 5)
        """
        return self.get_element_count(self.locators.advantage_cards)

    def is_trading_opportunity_visible(self) -> bool:
        """
        Check if 'Trading Opportunity' section is visible.

        Returns:
            bool: True if section is visible
        """
        return self.is_visible(self.locators.trading_opportunity_h3)

    # ============================================================================
    # Text Content Getters
    # ============================================================================

    def get_hero_slide_texts(self) -> list[str]:
        """
        Get all hero slide h2 texts.

        Returns:
            list[str]: List of h2 texts from all slides
        """
        slides = self.page.locator(self.locators.hero_slides).all()
        texts = []

        for slide in slides:
            h2 = slide.locator("xpath=.//h2")
            if h2.count() > 0:
                text = h2.first.text_content()
                if text:
                    texts.append(text.strip())

        logger.debug(f"Found {len(texts)} hero slide texts: {texts}")
        return texts

    def get_advantages_subtitle(self) -> str:
        """
        Get advantages section subtitle (h5 tag).

        Returns:
            str: Subtitle text (e.g., "CRYPTO TRADING")
        """
        return self.get_text(self.locators.advantages_subtitle_h5)

    def get_advantages_title(self) -> str:
        """
        Get advantages section main title (h2 tag).

        Returns:
            str: Title text (e.g., "Our Advantages")
        """
        return self.get_text(self.locators.advantages_title_h2)

    def get_advantage_card_texts(self) -> list[str]:
        """
        Get all advantage card titles.

        Returns:
            list[str]: List of advantage card titles (expected: 5 items)
        """
        cards = self.page.locator(self.locators.advantage_cards).all()
        texts = [card.text_content().strip() for card in cards if card.text_content()]

        logger.debug(f"Found {len(texts)} advantage cards: {texts}")
        return texts

    def get_trading_opportunity_text(self) -> str:
        """
        Get trading opportunity section heading text.

        Returns:
            str: Heading text (e.g., "Catch Your Next Trading Opportunity")
        """
        return self.get_text(self.locators.trading_opportunity_h3)

    # ============================================================================
    # Verification Methods
    # ============================================================================

    def verify_all_components_exist(self) -> dict:
        """
        Verify all expected page components exist.

        Returns:
            dict: Results with 'passed' (bool) and 'details' (dict)
        """
        hero_carousel_exists = self.is_hero_carousel_visible()
        slide_count = self.get_hero_slide_count()
        advantages_exists = self.is_advantages_section_visible()
        cards_count = self.get_advantage_cards_count()
        trading_exists = self.is_trading_opportunity_visible()

        # Check if all components pass
        all_passed = (
                hero_carousel_exists and
                slide_count == 3 and
                advantages_exists and
                cards_count == 5 and
                trading_exists
        )

        return {
            'passed': all_passed,
            'details': {
                'hero_carousel': {'exists': hero_carousel_exists},
                'hero_slides': {'count': slide_count, 'expected': 3},
                'advantages_section': {'exists': advantages_exists},
                'advantage_cards': {'count': cards_count, 'expected': 5},
                'trading_opportunity': {'exists': trading_exists}
            }
        }

    def verify_content_text(self, expected_data: dict) -> dict:
        """
        Verify all text content matches expected values.

        Args:
            expected_data: Dictionary with expected text values from test_data.json

        Returns:
            dict: Results with 'passed' (bool), 'details' (dict), and 'errors' (list)
        """
        errors = []

        # Get all texts
        slide_texts = self.get_hero_slide_texts()
        subtitle = self.get_advantages_subtitle()
        title = self.get_advantages_title()
        card_texts = self.get_advantage_card_texts()
        trading_text = self.get_trading_opportunity_text()

        # Validate hero slides
        expected_slide_1 = expected_data['hero_slides']['slide_1']
        if expected_slide_1 not in slide_texts:
            errors.append(f"Slide 1 text not found. Expected: '{expected_slide_1}', Got: {slide_texts}")

        slide_2_keywords = expected_data['hero_slides']['slide_2_keywords']
        slide_2_found = any(all(kw in text for kw in slide_2_keywords) for text in slide_texts)
        if not slide_2_found:
            errors.append(f"Slide 2 keywords {slide_2_keywords} not found. Got: {slide_texts}")

        slide_3_keywords = expected_data['hero_slides']['slide_3_keywords']
        slide_3_found = any(all(kw in text for kw in slide_3_keywords) for text in slide_texts)
        if not slide_3_found:
            errors.append(f"Slide 3 keywords {slide_3_keywords} not found. Got: {slide_texts}")

        # Validate advantages section
        expected_subtitle = expected_data['advantages']['subtitle']
        if subtitle != expected_subtitle:
            errors.append(f"Advantages subtitle mismatch. Expected: '{expected_subtitle}', Got: '{subtitle}'")

        expected_title = expected_data['advantages']['title']
        if title != expected_title:
            errors.append(f"Advantages title mismatch. Expected: '{expected_title}', Got: '{title}'")

        # Validate advantage cards
        expected_cards = expected_data['advantage_cards']
        for expected_card in expected_cards:
            if expected_card not in card_texts:
                errors.append(f"Advantage card '{expected_card}' not found. Got: {card_texts}")

        # Validate trading opportunity
        expected_trading = expected_data['trading_opportunity']
        if expected_trading not in trading_text:
            errors.append(f"Trading Opportunity text mismatch. Expected: '{expected_trading}', Got: '{trading_text}'")

        return {
            'passed': len(errors) == 0,
            'errors': errors,
            'details': {
                'hero_slides': slide_texts,
                'advantages_subtitle': subtitle,
                'advantages_title': title,
                'advantage_cards': card_texts,
                'trading_opportunity': trading_text
            }
        }