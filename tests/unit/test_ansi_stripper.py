#!/usr/bin/env python3
"""
Unit tests for ANSI Escape Code Stripper.

Tests the regex-based ANSI code removal utility to ensure py_cui compatibility.

Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 8 (Critical Fix - ANSI Rendering)
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.ansi_stripper import (
    strip_ansi_codes,
    has_ansi_codes,
    get_ansi_code_positions,
    ANSI_ESCAPE_PATTERN
)


class TestStripAnsiCodes:
    """Test strip_ansi_codes() function"""

    def test_basic_color_codes(self):
        """Test basic ANSI color code removal"""
        text = "\x1b[31mRED\x1b[0m \x1b[32mGREEN\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "RED GREEN"

    def test_plotext_style_codes(self):
        """Test plotext-style 256-color codes (the bug we're fixing!)"""
        text = "\x1b[48;5;15m██\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "██"

    def test_complex_plotext_output(self):
        """Test real plotext output with multiple ANSI codes"""
        text = "\x1b[48;5;15m  \x1b[0m\x1b[48;5;15m  \x1b[0m\x1b[48;5;15m  \x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "      "  # 6 spaces (2+2+2)

    def test_no_ansi_codes(self):
        """Test that plain text is unchanged"""
        text = "Plain text without ANSI codes"
        result = strip_ansi_codes(text)
        assert result == text

    def test_empty_string(self):
        """Test empty string handling"""
        assert strip_ansi_codes("") == ""

    def test_none_value(self):
        """Test None value handling"""
        assert strip_ansi_codes(None) is None

    def test_unicode_preservation(self):
        """Test that Unicode characters are preserved"""
        text = "▁▂▃▄▅▆▇█ ✓ ⚠️  █"
        result = strip_ansi_codes(text)
        assert result == text

    def test_mixed_unicode_and_ansi(self):
        """Test Unicode with ANSI codes"""
        text = "\x1b[31m▁▂▃▄▅▆▇█\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "▁▂▃▄▅▆▇█"

    def test_cursor_movement_codes(self):
        """Test cursor movement ANSI codes"""
        text = "\x1b[2J\x1b[H"  # Clear screen + home cursor
        result = strip_ansi_codes(text)
        assert result == ""

    def test_bold_italic_codes(self):
        """Test text formatting codes"""
        text = "\x1b[1mBOLD\x1b[0m \x1b[3mITALIC\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "BOLD ITALIC"

    def test_8bit_c1_codes(self):
        """Test 8-bit C1 control codes (alternate CSI introducer)"""
        text = "\x9B31mRED\x9B0m"
        result = strip_ansi_codes(text)
        assert result == "RED"

    def test_multiline_text(self):
        """Test ANSI stripping across multiple lines"""
        text = "\x1b[31mLine 1\x1b[0m\n\x1b[32mLine 2\x1b[0m\n\x1b[33mLine 3\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "Line 1\nLine 2\nLine 3"


class TestHasAnsiCodes:
    """Test has_ansi_codes() detection function"""

    def test_detects_ansi_codes(self):
        """Test detection of ANSI codes"""
        assert has_ansi_codes("\x1b[31mRED\x1b[0m") is True

    def test_detects_plotext_codes(self):
        """Test detection of plotext-style codes"""
        assert has_ansi_codes("\x1b[48;5;15m██\x1b[0m") is True

    def test_plain_text_no_codes(self):
        """Test plain text returns False"""
        assert has_ansi_codes("Plain text") is False

    def test_empty_string(self):
        """Test empty string returns False"""
        assert has_ansi_codes("") is False

    def test_none_value(self):
        """Test None value returns False"""
        assert has_ansi_codes(None) is False

    def test_unicode_no_codes(self):
        """Test Unicode without ANSI returns False"""
        assert has_ansi_codes("▁▂▃▄▅▆▇█") is False


class TestGetAnsiCodePositions:
    """Test get_ansi_code_positions() debugging function"""

    def test_single_code(self):
        """Test finding single ANSI code"""
        text = "Hello \x1b[31mWorld\x1b[0m"
        positions = get_ansi_code_positions(text)
        assert len(positions) == 2
        # First code: \x1b[31m at position 6
        assert positions[0][0] == 6
        assert positions[0][2] == "\x1b[31m"
        # Second code: \x1b[0m at position 16 (after "World")
        assert positions[1][2] == "\x1b[0m"

    def test_plotext_codes(self):
        """Test finding plotext-style codes"""
        text = "\x1b[48;5;15m██\x1b[0m"
        positions = get_ansi_code_positions(text)
        assert len(positions) == 2
        assert positions[0][2] == "\x1b[48;5;15m"
        assert positions[1][2] == "\x1b[0m"

    def test_no_codes(self):
        """Test text without codes returns empty list"""
        positions = get_ansi_code_positions("Plain text")
        assert positions == []

    def test_empty_string(self):
        """Test empty string returns empty list"""
        positions = get_ansi_code_positions("")
        assert positions == []


class TestAnsiEscapePattern:
    """Test the ECMA-48 regex pattern directly"""

    def test_pattern_matches_csi_sequences(self):
        """Test pattern matches CSI sequences"""
        # Basic color code
        match = ANSI_ESCAPE_PATTERN.search("\x1b[31m")
        assert match is not None

        # 256-color code
        match = ANSI_ESCAPE_PATTERN.search("\x1b[48;5;15m")
        assert match is not None

        # Reset code
        match = ANSI_ESCAPE_PATTERN.search("\x1b[0m")
        assert match is not None

    def test_pattern_matches_8bit_c1(self):
        """Test pattern matches 8-bit C1 codes"""
        match = ANSI_ESCAPE_PATTERN.search("\x9B31m")
        assert match is not None

    def test_pattern_does_not_match_plain_text(self):
        """Test pattern does not match plain text"""
        match = ANSI_ESCAPE_PATTERN.search("Plain text")
        assert match is None

    def test_pattern_does_not_match_unicode(self):
        """Test pattern does not match Unicode characters"""
        match = ANSI_ESCAPE_PATTERN.search("▁▂▃▄▅▆▇█")
        assert match is None


class TestRealWorldScenarios:
    """Test real-world scenarios from the dashboard"""

    def test_plotext_chart_output(self):
        """Test realistic plotext chart output"""
        # Simulated plotext output with ANSI codes
        chart = (
            "\x1b[48;5;15m  \x1b[0m\x1b[48;5;15m  \x1b[0m\n"
            "\x1b[48;5;15m██\x1b[0m\x1b[48;5;15m██\x1b[0m\n"
            "CPU: 45.2%"
        )
        result = strip_ansi_codes(chart)
        assert "\x1b[" not in result
        assert "CPU: 45.2%" in result
        assert "██" in result

    def test_tabulate_grid_output(self):
        """Test that tabulate output (no ANSI) is unchanged"""
        table = (
            "+----------+--------+\n"
            "| Protocol | Count  |\n"
            "+----------+--------+\n"
            "| HTTPS    | 450    |\n"
            "+----------+--------+"
        )
        result = strip_ansi_codes(table)
        assert result == table

    def test_sparkline_unicode_output(self):
        """Test that sparkline Unicode is preserved"""
        sparkline = "CPU: ▁▂▃▄▅▆▇█ (45.2%)"
        result = strip_ansi_codes(sparkline)
        assert result == sparkline

    def test_mixed_content(self):
        """Test mixed content with ANSI, Unicode, and plain text"""
        content = (
            "\x1b[31mError:\x1b[0m Network issue ⚠️\n"
            "Status: ▁▂▃▄▅▆▇█\n"
            "\x1b[32m✓ Fixed\x1b[0m"
        )
        result = strip_ansi_codes(content)
        assert "\x1b[" not in result
        assert "Error:" in result
        assert "⚠️" in result
        assert "▁▂▃▄▅▆▇█" in result
        assert "✓ Fixed" in result


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_incomplete_escape_sequence(self):
        """Test handling of incomplete escape sequences"""
        # Note: \x1b[i is actually a VALID ANSI sequence (final byte 'i')
        # according to ECMA-48, so it will be stripped.
        # Truly incomplete sequence would be just \x1b or \x1b[
        text = "\x1bText"  # Just ESC without [
        result = strip_ansi_codes(text)
        # Should preserve truly incomplete sequence
        assert result == text

    def test_consecutive_codes(self):
        """Test consecutive ANSI codes without text between"""
        text = "\x1b[31m\x1b[1mText\x1b[0m\x1b[0m"
        result = strip_ansi_codes(text)
        assert result == "Text"

    def test_very_long_text(self):
        """Test performance with long text"""
        # Create long text with many ANSI codes
        text = "\x1b[31mRED\x1b[0m " * 1000
        result = strip_ansi_codes(text)
        assert "\x1b[" not in result
        assert result == "RED " * 1000


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
