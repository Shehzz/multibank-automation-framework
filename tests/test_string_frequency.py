"""
Unit tests for String Character Frequency Counter (Task 2).
"""
import pytest
from utils.string_frequency import (
    count_character_frequency,
    count_character_frequency_ignore_whitespace,
    count_character_frequency_case_insensitive
)


class TestStringFrequency:
    """Test suite for string character frequency counter."""

    def test_example_hello_world(self):
        """Test with the provided example: 'hello world'"""
        result = count_character_frequency("hello world")

        # Expected output (with space counted)
        assert "h:1" in result
        assert "e:1" in result
        assert "l:3" in result
        assert "o:2" in result
        assert "w:1" in result
        assert "r:1" in result
        assert "d:1" in result

        # Verify order of first appearance (h appears before e, etc.)
        assert result.index("h:1") < result.index("e:1")
        assert result.index("e:1") < result.index("l:3")

    def test_empty_string(self):
        """Test with empty string"""
        result = count_character_frequency("")
        assert result == "", "Empty string should return empty result"

    def test_single_character(self):
        """Test with single character"""
        result = count_character_frequency("a")
        assert result == "a:1"

    def test_all_same_characters(self):
        """Test with all same characters"""
        result = count_character_frequency("aaa")
        assert result == "a:3"

    def test_repeated_characters(self):
        """Test with repeated characters"""
        result = count_character_frequency("aabbcc")
        assert result == "a:2, b:2, c:2"

    def test_special_characters(self):
        """Test with special characters"""
        result = count_character_frequency("a!b@c#")
        assert "a:1" in result
        assert "!:1" in result
        assert "@:1" in result
        assert "#:1" in result

    def test_numbers(self):
        """Test with numbers"""
        result = count_character_frequency("123321")
        assert "1:2" in result
        assert "2:2" in result
        assert "3:2" in result

    def test_mixed_content(self):
        """Test with mixed content (letters, numbers, special chars)"""
        result = count_character_frequency("a1!a2!")
        assert "a:2" in result
        assert "1:1" in result
        assert "!:2" in result
        assert "2:1" in result

    def test_whitespace_counted(self):
        """Test that whitespace is counted by default"""
        result = count_character_frequency("a b c")
        assert " :2" in result  # Two spaces

    def test_order_preservation(self):
        """Test that order of first appearance is preserved"""
        result = count_character_frequency("dcba")
        # d appears first, then c, then b, then a
        assert result == "d:1, c:1, b:1, a:1"

    def test_case_sensitivity(self):
        """Test that uppercase and lowercase are treated differently"""
        result = count_character_frequency("AaBbCc")
        assert "A:1" in result
        assert "a:1" in result
        assert "B:1" in result
        assert "b:1" in result


class TestStringFrequencyIgnoreWhitespace:
    """Test suite for whitespace-ignoring variant."""

    def test_hello_world_no_spaces(self):
        """Test 'hello world' without counting spaces"""
        result = count_character_frequency_ignore_whitespace("hello world")
        assert " :" not in result  # Space should not be counted
        assert "h:1" in result
        assert "l:3" in result

    def test_only_spaces(self):
        """Test string with only spaces"""
        result = count_character_frequency_ignore_whitespace("   ")
        assert result == ""


class TestStringFrequencyCaseInsensitive:
    """Test suite for case-insensitive variant."""

    def test_hello_world_case_insensitive(self):
        """Test 'Hello World' treating H and h as same"""
        result = count_character_frequency_case_insensitive("Hello World")
        assert "h:1" in result  # H and h combined
        assert "l:3" in result  # l and L combined
        assert "H:1" not in result  # Uppercase H should not be separate

    def test_mixed_case(self):
        """Test mixed case characters"""
        result = count_character_frequency_case_insensitive("AaAa")
        assert "a:4" in result


# Parametrized tests for edge cases
@pytest.mark.parametrize("input_str,expected_contains", [
    ("a", "a:1"),
    ("aa", "a:2"),
    ("abc", "a:1, b:1, c:1"),
    ("aabbcc", "a:2, b:2, c:2"),
])
def test_parametrized_inputs(input_str, expected_contains):
    """Parametrized test for various inputs"""
    result = count_character_frequency(input_str)
    assert result == expected_contains


def test_performance_large_string():
    """Test performance with a large string"""
    # Create a large string
    large_string = "a" * 1000 + "b" * 1000 + "c" * 1000

    result = count_character_frequency(large_string)

    assert "a:1000" in result
    assert "b:1000" in result
    assert "c:1000" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])