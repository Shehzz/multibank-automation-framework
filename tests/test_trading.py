"""
Trading Tests:
Tests for Spot trading section and trading pair data structure.
"""
import pytest
import logging
from pages.home_page import HomePage

logger = logging.getLogger(__name__)


@pytest.mark.content
@pytest.mark.regression
class TestTrading:
    """Test suite for the trading functionality."""

    #TODO: Add TCs for the Trading functionality:
    # 1. Spot trading section displays trading pairs across different categories
    # 2. Trading pair data structure and presentation is correct

    def test_trade_spot_trading_categories_display(self, loaded_home_page: HomePage, test_data: dict):
        """
        Verify trading categories are matching

        Test Steps:
        1. Navigate to home page
        2. Go to Spot Trade section
        3. Verify if trading category matches
        """
        # Navigate to spot trading
        logger.info("Test: Verifying trading category names")
        loaded_home_page.navigate_to_spot_trading()

        # Get visible categories
        categories = loaded_home_page.get_trading_categories()
        expected_categories = test_data["trade"]["pair-categories"]

        assert categories == expected_categories, \
            f"Categories mismatch: expected {expected_categories}, got {categories}"
        logger.info("✓ Trading category names matching")

    def test_trade_spot_trading_all_categories_count(self, loaded_home_page: HomePage, test_data: dict):
        """
        Verify all the trading categories are displayed and functional

        Test Steps:
        1. Navigate to home page
        2. Go to Spot Trade section
        3. Iterate through each category: All, USDT, BTC, FIAT
        4. Verify each category displays exactly 10 trading pairs
        """
        logger.info("Test: Verifying trading pairs across all categories")
        loaded_home_page.navigate_to_spot_trading()

        category_counts = loaded_home_page.get_trading_pairs_count_by_category()
        expected_categories = test_data["trade"]["pair-categories"]

        # Verify each category has exactly 10 trading pairs
        for category in expected_categories:
            assert category in category_counts, \
                f"❌ Category '{category}' not found in results"

            count = category_counts[category]
            assert count == 10, \
                f"❌ Category '{category}' should have 10 trading pairs, got {count}"

            logger.info(f"✓ Category '{category}': {count} trading pairs")

        logger.info(f"✓ All categories verified: {category_counts}")

    def test_trade_trading_pair_structure(self, loaded_home_page: HomePage, test_data: dict):
        """
        Verify trading pair data structure

        Test Steps:
        1. Navigate to home page
        2. Go to Spot Trade section
        3. Get the trading pair data
        4. Verify the trading pair data structure
        """
        loaded_home_page.navigate_to_spot_trading()
        # Get trading pairs
        pairs = loaded_home_page.get_trading_pairs()

        # Verify we got some pairs
        assert len(pairs) > 0, "❌ No trading pairs found"
        logger.info(f"Found {len(pairs)} trading pairs")

        # Verify each pair has required fields (test first 5 for speed)
        required_fields = test_data["trade"]["pair_data_structure"]

        for pair in pairs:
            for field in required_fields:
                assert field in pair, f"❌ Field '{field}' missing in pair data structure"

            # Presentation checks
            assert pair["change_24h"].endswith("%")
            assert pair["change_24h_direction"] in ["⬆️", "⬇️"]

        logger.info("✓ All trading pair structures and presentation verified successfully")
