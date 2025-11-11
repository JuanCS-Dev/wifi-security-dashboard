"""
ANSI Escape Code Stripper Utility

This module provides utilities to remove ANSI escape sequences from text.
Essential for py_cui compatibility, as curses does not interpret ANSI codes.

Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 8 (Critical Fix - ANSI Rendering)

References:
    - ECMA-48 Standard (Control Functions for Coded Character Sets)
    - py_cui Issue #79: https://github.com/jwlodek/py_cui/issues/79
    - StackOverflow: https://stackoverflow.com/questions/14693701
"""

import re
from typing import Pattern


# ECMA-48 compliant ANSI escape sequence pattern
# Matches:
# - CSI sequences: \x1B[...  (e.g., \x1B[31m for red color)
# - 8-bit C1 codes: \x9B...
ANSI_ESCAPE_PATTERN: Pattern = re.compile(
    r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]'
)


def strip_ansi_codes(text: str) -> str:
    """
    Remove all ANSI escape sequences from text.

    This function strips ANSI color codes, cursor movement codes, and other
    control sequences that curses cannot interpret. Essential for py_cui
    compatibility.

    Args:
        text: String potentially containing ANSI escape sequences

    Returns:
        Clean text with all ANSI sequences removed

    Example:
        >>> text = "\\x1b[31mRED\\x1b[0m \\x1b[32mGREEN\\x1b[0m"
        >>> strip_ansi_codes(text)
        'RED GREEN'

    Notes:
        - Uses ECMA-48 compliant regex pattern
        - Handles both 7-bit (\\x1B[) and 8-bit (\\x9B) sequences
        - Safe to call on text without ANSI codes (returns unchanged)

    Technical Details:
        Pattern breakdown:
        - (\\x9B|\\x1B\\[): Match CSI introducer (ESC[ or 8-bit C1)
        - [0-?]*: Parameter bytes (digits, semicolons, etc)
        - [ -/]*: Intermediate bytes
        - [@-~]: Final byte (determines command type)

    References:
        - ECMA-48: Control Functions for Coded Character Sets
        - ISO/IEC 6429: Similar standard
        - https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    if not text:
        return text

    return ANSI_ESCAPE_PATTERN.sub('', text)


def has_ansi_codes(text: str) -> bool:
    """
    Check if text contains ANSI escape sequences.

    Useful for validation and debugging.

    Args:
        text: String to check

    Returns:
        True if ANSI codes found, False otherwise

    Example:
        >>> has_ansi_codes("\\x1b[31mRED\\x1b[0m")
        True
        >>> has_ansi_codes("Plain text")
        False
    """
    if not text:
        return False

    return ANSI_ESCAPE_PATTERN.search(text) is not None


def get_ansi_code_positions(text: str) -> list[tuple[int, int, str]]:
    """
    Find all ANSI code positions in text.

    Useful for debugging visualization issues.

    Args:
        text: String to analyze

    Returns:
        List of tuples (start_pos, end_pos, code_text)

    Example:
        >>> text = "Hello \\x1b[31mRED\\x1b[0m World"
        >>> positions = get_ansi_code_positions(text)
        >>> print(positions)
        [(6, 11, '\\x1b[31m'), (14, 18, '\\x1b[0m')]
    """
    if not text:
        return []

    positions = []
    for match in ANSI_ESCAPE_PATTERN.finditer(text):
        positions.append((
            match.start(),
            match.end(),
            match.group()
        ))

    return positions


# Alias for backwards compatibility
strip_ansi = strip_ansi_codes


if __name__ == "__main__":
    # Self-test
    print("=" * 70)
    print("ANSI Stripper Self-Test")
    print("=" * 70)

    # Test 1: Basic color codes
    test1 = "\x1b[31mRED\x1b[0m \x1b[32mGREEN\x1b[0m"
    clean1 = strip_ansi_codes(test1)
    print(f"\nTest 1 (colors):")
    print(f"  Input:  {repr(test1)}")
    print(f"  Output: {repr(clean1)}")
    print(f"  Expected: 'RED GREEN'")
    print(f"  ✅ PASS" if clean1 == "RED GREEN" else f"  ❌ FAIL")

    # Test 2: plotext-style codes
    test2 = "\x1b[48;5;15m██\x1b[0m"
    clean2 = strip_ansi_codes(test2)
    print(f"\nTest 2 (plotext):")
    print(f"  Input:  {repr(test2)}")
    print(f"  Output: {repr(clean2)}")
    print(f"  Expected: '██'")
    print(f"  ✅ PASS" if clean2 == "██" else f"  ❌ FAIL")

    # Test 3: No ANSI codes
    test3 = "Plain text"
    clean3 = strip_ansi_codes(test3)
    print(f"\nTest 3 (no codes):")
    print(f"  Input:  {repr(test3)}")
    print(f"  Output: {repr(clean3)}")
    print(f"  Expected: 'Plain text'")
    print(f"  ✅ PASS" if clean3 == "Plain text" else f"  ❌ FAIL")

    # Test 4: Detection
    test4_has = has_ansi_codes("\x1b[31mRED\x1b[0m")
    test4_no = has_ansi_codes("Plain")
    print(f"\nTest 4 (detection):")
    print(f"  has_ansi_codes('\\x1b[31mRED\\x1b[0m'): {test4_has}")
    print(f"  has_ansi_codes('Plain'): {test4_no}")
    print(f"  ✅ PASS" if (test4_has and not test4_no) else f"  ❌ FAIL")

    # Test 5: Position finding
    test5 = "Hello \x1b[31mRED\x1b[0m World"
    positions = get_ansi_code_positions(test5)
    print(f"\nTest 5 (positions):")
    print(f"  Input: {repr(test5)}")
    print(f"  Positions: {positions}")
    print(f"  ✅ PASS" if len(positions) == 2 else f"  ❌ FAIL")

    print("\n" + "=" * 70)
    print("Self-test complete. Run with pytest for comprehensive testing.")
    print("=" * 70)
