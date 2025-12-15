"""
String Character Frequency Counter
Task 2: Count character occurrences and output in order of first appearance.
"""


def count_character_frequency(input_string: str) -> str:
    """
    Count character occurrences in a string and output in order of first appearance.

    Args:
        input_string: The string to analyze

    Returns:
        Formatted string like "h:1, e:1, l:3, o:2, ..."
    """
    if not input_string:
        return ""

    # Dictionary to store character counts
    char_count = {}
    # List to maintain order of first appearance
    order = []

    # Single pass through the string
    for char in input_string:
        if char not in char_count:
            char_count[char] = 1
            order.append(char)  # Track first appearance
        else:
            char_count[char] += 1

    # Build output string in order of first appearance
    result = ", ".join(f"{char}:{count}" for char, count in
                       ((c, char_count[c]) for c in order))

    return result


def count_character_frequency_ignore_whitespace(input_string: str) -> str:
    """
    Count character occurrences excluding whitespace.

    Args:
        input_string: The string to analyze

    Returns:
        Formatted string with character counts (whitespace excluded)
    """
    if not input_string:
        return ""

    char_count = {}
    order = []

    for char in input_string:
        # Skip whitespace characters
        if char.isspace():
            continue

        if char not in char_count:
            char_count[char] = 1
            order.append(char)
        else:
            char_count[char] += 1

    result = ", ".join(f"{char}:{count}" for char, count in
                       ((c, char_count[c]) for c in order))

    return result


def count_character_frequency_case_insensitive(input_string: str) -> str:
    """
    Count character occurrences treating uppercase and lowercase as same.

    Args:
        input_string: The string to analyze

    Returns:
        Formatted string with character counts (case-insensitive)
    """
    if not input_string:
        return ""

    char_count = {}
    order = []

    for char in input_string:
        # Convert to lowercase for comparison
        char_lower = char.lower()

        if char_lower not in char_count:
            char_count[char_lower] = 1
            order.append(char_lower)
        else:
            char_count[char_lower] += 1

    result = ", ".join(f"{char}:{count}" for char, count in
                       ((c, char_count[c]) for c in order))

    return result


# Main execution example
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "hello world",
        "aaa",
        "",
        "Hello World",
        "123 test!",
        "a"
    ]

    print("String Character Frequency Counter")
    print("=" * 50)

    for test in test_cases:
        result = count_character_frequency(test)
        print(f"\nInput: '{test}'")
        print(f"Output: {result}")

    print("\n" + "=" * 50)
    print("Alternative: Ignore Whitespace")
    print("=" * 50)

    result = count_character_frequency_ignore_whitespace("hello world")
    print(f"\nInput: 'hello world'")
    print(f"Output: {result}")

    print("\n" + "=" * 50)
    print("Alternative: Case Insensitive")
    print("=" * 50)

    result = count_character_frequency_case_insensitive("Hello World")
    print(f"\nInput: 'Hello World'")
    print(f"Output: {result}")