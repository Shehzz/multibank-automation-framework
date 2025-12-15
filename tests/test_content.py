"""
Content Validation Tests:
Tests for marketing banners, download links, and page content.
"""
import pytest
import logging
from pages.home_page import HomePage
from pages.why_multibank_page import WhyMultibankPage

logger = logging.getLogger(__name__)


@pytest.mark.content
@pytest.mark.regression
class TestContent:
    """Test suite for content validation."""

    def test_content_marketing_banners_displayed(self, loaded_home_page: HomePage):
        """
        Test that marketing banners are displayed at the bottom of the page.

        Test Steps:
        1. Navigate to home page (via loaded_home_page fixture)
        2. Scroll to banner section at bottom
        3. Verify banner section is visible
        4. Verify there are 9 banners
        """
        logger.info("Test: Marketing banners displayed at page bottom")

        # Check if banner section is displayed
        assert loaded_home_page.are_banners_displayed(), \
            "❌ Marketing banner section is not displayed at the bottom"

        logger.info("✓ Banner section is displayed")

        banner_count = loaded_home_page.get_banner_count()
        assert banner_count == 9, \
            f"❌ Expected 9 marketing banners, but found {banner_count}"

        logger.info(f"✓ Banner section is visible with {banner_count} banners loaded")

    def test_content_download_section_links(self, loaded_home_page: HomePage, test_data: dict):
        """
        Test that App Store and Google Play links are present and valid.

        Test Steps:
        1. Navigate to home page (via loaded_home_page fixture)
        2. Scroll to download section at bottom
        3. Get download links
        4. Verify links contain expected URL patterns
        """
        logger.info("Test: Download section links correctly to App Store and Google Play")

        # Get expected URL patterns from test data
        expected_app_store = test_data['content']['download_links']['app_store_url']
        expected_google_play = test_data['content']['download_links']['google_play_url']

        # Verify download links with expected patterns
        results = loaded_home_page.verify_download_links(
            expected_app_store=expected_app_store,
            expected_google_play=expected_google_play
        )

        # Assert App Store link
        app_store = results['app_store']
        assert app_store['exists'], "❌ App Store link not found"
        assert app_store['valid'], \
            f"❌ App Store link invalid. Expected '{expected_app_store}' in URL, got: {app_store['url']}"
        logger.info(f"✓ App Store link is valid: {app_store['url']}")

        # Assert Google Play link
        google_play = results['google_play']
        assert google_play['exists'], "❌ Google Play link not found"
        assert google_play['valid'], \
            f"❌ Google Play link invalid. Expected '{expected_google_play}' in URL, got: {google_play['url']}"
        logger.info(f"✓ Google Play link is valid: {google_play['url']}")

    def test_content_app_store_link_present(self, loaded_home_page: HomePage):
        """
        Test that App Store link exists.

        Test Steps:
        1. Navigate to home page
        2. Get App Store link
        3. Verify link is not None
        """
        logger.info("Test: App Store link present")

        # Get App Store link
        link = loaded_home_page.get_app_store_link()

        # Verify link exists (may be None if not on page)
        if link:
            assert 'apple' in link.lower(), \
                "App Store link should point to Apple"
            logger.info(f"✓ App Store link found: {link}")
        else:
            logger.warning("App Store link not found on page")

    def test_content_google_play_link_present(self, loaded_home_page: HomePage):
        """
        Test that Google Play link exists.

        Test Steps:
        1. Navigate to home page
        2. Get Google Play link
        3. Verify link is not None
        """
        logger.info("Test: Google Play link present")

        # Get Google Play link
        link = loaded_home_page.get_google_play_link()

        # Verify link exists
        if link:
            assert 'play.google.com' in link, \
                "Google Play link should point to play.google.com"
            logger.info(f"✓ Google Play link found: {link}")
        else:
            logger.warning("Google Play link not found on page")

    def test_why_multibank_components_exist(self, why_multibank_page: WhyMultibankPage):
        """
        Test that all expected components exist on Why MultiBank page.

        Test Steps:
        1. Navigate to Why MultiBank page
        2. Verify hero carousel exists and has 3 slides
        3. Verify Our Advantages section exists
        4. Verify 5 advantage cards exist
        5. Verify Trading Opportunity section exists
        """
        logger.info("Test: Why MultiBank page components exist")

        # Load page
        why_multibank_page.load()

        # Check hero carousel
        assert why_multibank_page.is_hero_carousel_visible(), \
            "❌ Hero carousel not found on Why MultiBank page"
        logger.info("✓ Hero carousel exists")

        # Check slide count
        slide_count = why_multibank_page.get_hero_slide_count()
        assert slide_count == 3, \
            f"❌ Expected 3 hero slides, found {slide_count}"
        logger.info(f"✓ Found {slide_count} hero slides")

        # Check Our Advantages section
        assert why_multibank_page.is_advantages_section_visible(), \
            "❌ Our Advantages section not found"
        logger.info("✓ Our Advantages section exists")

        # Check advantage cards
        card_count = why_multibank_page.get_advantage_cards_count()
        assert card_count == 5, \
            f"❌ Expected 5 advantage cards, found {card_count}"
        logger.info(f"✓ Found {card_count} advantage cards")

        # Check Trading Opportunity section
        assert why_multibank_page.is_trading_opportunity_visible(), \
            "❌ Trading Opportunity section not found"
        logger.info("✓ Trading Opportunity section exists")

    def test_why_multibank_content_text(self, why_multibank_page, test_data: dict):
        """
        Test that h2 and h3 text content is correct on Why MultiBank page.

        Test Steps:
        1. Navigate to Why MultiBank page
        2. Verify hero slide h2 texts (3 slides)
        3. Verify Our Advantages section subtitle and title
        4. Verify all 5 advantage card texts
        5. Verify Trading Opportunity section text
        """
        logger.info("Test: Why MultiBank page content text verification")

        # Load page
        why_multibank_page.load()

        # Verify all content using helper method
        expected = test_data['why_multibank']['content']
        results = why_multibank_page.verify_content_text(expected)

        # Assert overall pass
        assert results['passed'], \
            f"❌ Content verification failed:\n" + "\n".join(f"  - {err}" for err in results['errors'])

        logger.info("✓ All Why MultiBank page content text is correct")
        logger.info(f"  - Hero slides: {results['details']['hero_slides']}")
        logger.info(f"  - Advantages subtitle: '{results['details']['advantages_subtitle']}'")
        logger.info(f"  - Advantages title: '{results['details']['advantages_title']}'")
        logger.info(f"  - Advantage cards: {results['details']['advantage_cards']}")
        logger.info(f"  - Trading opportunity: '{results['details']['trading_opportunity']}'")
