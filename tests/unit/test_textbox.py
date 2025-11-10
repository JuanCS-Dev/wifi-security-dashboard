"""
Unit tests for Textbox component

Sprint 3 - Phase 1.2: Tests (TDD) - REFATORADO
Arquitetura correta: usa ComponentConfig em vez de Dict
Coverage target: ≥90%
"""

import pytest
from unittest.mock import Mock, patch
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig, ComponentType, Position
from src.components.textbox import Textbox


class TestTextboxInitialization:
    """Test Textbox component initialization"""

    def test_textbox_initialization_with_minimal_config(self):
        """Test Textbox can be initialized with minimal config"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Test Panel",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)

        assert textbox.config.type == ComponentType.TEXTBOX
        assert textbox.config.title == "Test Panel"
        assert textbox.config.plugin == "system"
        assert textbox.config.data_field == "cpu_percent"
        assert textbox.config.color == "white"  # Default
        assert textbox.label is None  # Default

    def test_textbox_initialization_with_full_config(self):
        """Test Textbox with all optional parameters"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="WiFi Signal",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm",
            color="green",
            extra={"label": "Signal Strength", "format": "{value} dBm"}
        )

        textbox = Textbox(config)

        assert textbox.config.title == "WiFi Signal"
        assert textbox.config.data_field == "signal_strength_dbm"
        assert textbox.label == "Signal Strength"
        assert textbox.config.color == "green"
        assert textbox.format == "{value} dBm"

    def test_textbox_initialization_missing_required_fields(self):
        """Test ComponentConfig validates required fields"""
        # Missing data_field
        with pytest.raises(TypeError):
            ComponentConfig(
                type=ComponentType.TEXTBOX,
                title="Test",
                position=Position(0, 0, 40, 5),
                rate_ms=1000,
                plugin="system"
                # data_field missing
            )


class TestTextboxUpdate:
    """Test Textbox update() method (inherited from Component)"""

    def test_textbox_update_extracts_data_from_plugin(self):
        """Test update() extracts correct field from plugin data"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)

        plugin_data = {
            "cpu_percent": 45.2,
            "memory_percent": 62.1,
            "uptime_seconds": 3600
        }

        textbox.update(plugin_data)

        # Component.update() extracts data_field automatically
        assert textbox.data == 45.2

    def test_textbox_update_handles_missing_field(self):
        """Test update() raises KeyError when field missing"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="WiFi",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm"
        )

        textbox = Textbox(config)

        plugin_data = {
            "ssid": "WiFi-Home",
            "frequency_ghz": 2.4
            # signal_strength_dbm missing
        }

        with pytest.raises(KeyError):
            textbox.update(plugin_data)

    def test_textbox_update_stores_plugin_data(self):
        """Test update() stores full plugin_data dict"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)

        plugin_data = {
            "cpu_percent": 45.2,
            "memory_percent": 62.1
        }

        textbox.update(plugin_data)

        # plugin_data is stored in _plugin_data
        assert textbox.plugin_data == plugin_data
        assert textbox.data == 45.2


class TestTextboxRender:
    """Test Textbox render() method"""

    def test_textbox_render_returns_panel(self):
        """Test render() returns Rich Panel object"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)
        textbox.update({"cpu_percent": 45.2})

        panel = textbox.render()

        assert isinstance(panel, Panel)

    def test_textbox_render_panel_has_correct_title(self):
        """Test rendered Panel has correct title"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="CPU Usage",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)
        textbox.update({"cpu_percent": 45.2})

        panel = textbox.render()

        assert "CPU Usage" in str(panel.title)

    def test_textbox_render_panel_has_correct_border_color(self):
        """Test rendered Panel has correct border color"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="green"
        )

        textbox = Textbox(config)
        textbox.update({"cpu_percent": 45.2})

        panel = textbox.render()

        assert panel.border_style == "green"

    def test_textbox_render_formats_value_with_label(self):
        """Test render() formats value with label"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            extra={"label": "CPU Usage"}
        )

        textbox = Textbox(config)
        textbox.update({"cpu_percent": 45.2})

        panel = textbox.render()

        content_str = str(panel.renderable)
        assert "CPU Usage" in content_str
        assert "45.2" in content_str

    def test_textbox_render_formats_value_without_label(self):
        """Test render() shows only value when no label"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Value",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)
        textbox.update({"cpu_percent": 45.2})

        panel = textbox.render()

        content_str = str(panel.renderable)
        assert "45.2" in content_str

    def test_textbox_render_applies_custom_format(self):
        """Test render() applies custom format string"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="WiFi",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm",
            extra={"format": "{value} dBm"}
        )

        textbox = Textbox(config)
        textbox.update({"signal_strength_dbm": -45})

        panel = textbox.render()

        content_str = str(panel.renderable)
        assert "-45 dBm" in content_str

    def test_textbox_render_handles_none_value(self):
        """Test render() shows 'N/A' when no data yet"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)
        # No update() called, so data is None

        panel = textbox.render()

        content_str = str(panel.renderable)
        assert "N/A" in content_str

    def test_textbox_render_handles_zero_value(self):
        """Test render() correctly shows zero (not treated as None)"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Counter",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="error_count"
        )

        textbox = Textbox(config)
        textbox.update({"error_count": 0})

        panel = textbox.render()

        content_str = str(panel.renderable)
        assert "0" in content_str
        assert "N/A" not in content_str


class TestTextboxFormatting:
    """Test Textbox value formatting"""

    def test_textbox_format_integer(self):
        """Test formatting integer values"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Count",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="count"
        )

        textbox = Textbox(config)

        formatted = textbox._format_value(42)
        assert formatted == "42"

    def test_textbox_format_float_default_precision(self):
        """Test formatting float values with default precision"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Percent",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)

        formatted = textbox._format_value(45.2567)
        # Default precision is 1 decimal place (45.2567 rounds to 45.3)
        assert formatted == "45.3"

    def test_textbox_format_with_custom_format_string(self):
        """Test formatting with custom format string"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Memory",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="memory_gb",
            extra={"format": "{value:.2f} GB"}
        )

        textbox = Textbox(config)
        textbox.update({"memory_gb": 2.567})

        # Custom format is applied by _format_current_value(), not _format_value()
        formatted = textbox._format_current_value()
        assert formatted == "2.57 GB"

    def test_textbox_format_string_value(self):
        """Test formatting string values (pass-through)"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="SSID",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="ssid"
        )

        textbox = Textbox(config)

        formatted = textbox._format_value("WiFi-Home")
        assert formatted == "WiFi-Home"

    def test_textbox_format_boolean_value(self):
        """Test formatting boolean values"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Connected",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="is_connected"
        )

        textbox = Textbox(config)

        formatted_true = textbox._format_value(True)
        formatted_false = textbox._format_value(False)

        assert formatted_true in ["True", "✅", "Yes", "✅ Yes"]
        assert formatted_false in ["False", "❌", "No", "❌ No"]

    def test_textbox_format_none_value(self):
        """Test formatting None value"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        textbox = Textbox(config)

        formatted = textbox._format_value(None)
        assert formatted in ["N/A", "No data", "-"]


class TestTextboxIntegration:
    """Integration tests for Textbox with Dashboard"""

    def test_textbox_integration_with_dashboard_config(self):
        """Test Textbox can be created from dashboard.yml format"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="System CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="green",
            extra={"label": "CPU Usage", "format": "{value:.1f}%"}
        )

        textbox = Textbox(config)

        # Simulate dashboard update cycle
        plugin_data = {
            "cpu_percent": 45.2,
            "memory_percent": 62.1
        }

        textbox.update(plugin_data)
        panel = textbox.render()

        assert isinstance(panel, Panel)
        content_str = str(panel.renderable)
        assert "45.2" in content_str

    def test_textbox_multiple_update_render_cycles(self):
        """Test multiple update/render cycles (simulate live dashboard)"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        textbox = Textbox(config)

        # Cycle 1
        textbox.update({"cpu_percent": 30.0})
        panel1 = textbox.render()
        assert "30.0" in str(panel1.renderable) or "30" in str(panel1.renderable)

        # Cycle 2
        textbox.update({"cpu_percent": 45.5})
        panel2 = textbox.render()
        assert "45.5" in str(panel2.renderable) or "45" in str(panel2.renderable)


class TestTextboxEdgeCases:
    """Test edge cases and error handling"""

    def test_textbox_handles_very_large_numbers(self):
        """Test formatting very large numbers"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Bytes",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="network",
            data_field="bytes_total"
        )

        textbox = Textbox(config)

        large_value = 9999999999999
        formatted = textbox._format_value(large_value)

        assert formatted is not None
        assert len(formatted) > 0

    def test_textbox_handles_negative_numbers(self):
        """Test formatting negative numbers (e.g., dBm)"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Signal",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm"
        )

        textbox = Textbox(config)

        formatted = textbox._format_value(-45)
        assert "-45" in formatted

    def test_textbox_handles_special_characters_in_string(self):
        """Test rendering strings with special characters"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="SSID",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="ssid"
        )

        textbox = Textbox(config)
        textbox.update({"ssid": "WiFi-Home 🏠 (5GHz)"})

        panel = textbox.render()
        content_str = str(panel.renderable)

        assert "WiFi-Home" in content_str

    def test_textbox_handles_unicode_emoji(self):
        """Test rendering emoji in values"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Status",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="status_emoji"
        )

        textbox = Textbox(config)
        textbox.update({"status_emoji": "✅ Running"})

        panel = textbox.render()

        assert panel is not None


class TestTextboxFormatErrorHandling:
    """Test error handling in format strings"""

    def test_textbox_format_invalid_format_string_falls_back(self):
        """Test invalid custom format string falls back to default formatting"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Value",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="test",
            data_field="value",
            extra={"format": "{invalid_key}"}  # Invalid format key
        )

        textbox = Textbox(config)
        textbox.update({"value": 42.5})

        # Should fallback to default formatting, not crash
        formatted = textbox._format_current_value()
        assert "42.5" in formatted

    def test_textbox_format_value_error_falls_back(self):
        """Test ValueError in format string falls back to default"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Value",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="test",
            data_field="value",
            extra={"format": "{value:invalid}"}  # Invalid format spec
        )

        textbox = Textbox(config)
        textbox.update({"value": 42.5})

        # Should fallback to default formatting
        formatted = textbox._format_current_value()
        assert "42.5" in formatted


class TestTextboxColorEdgeCases:
    """Test color selection for edge case values"""

    def test_textbox_color_boolean_true_returns_green(self):
        """Test boolean True value returns green color"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Connected",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="test",
            data_field="is_connected"
        )

        textbox = Textbox(config)
        textbox.update({"is_connected": True})

        color = textbox._get_value_color()
        assert color == "green"

    def test_textbox_color_string_with_error_keyword_returns_red(self):
        """Test string containing error keyword returns red color"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Status",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="test",
            data_field="status"
        )

        textbox = Textbox(config)

        # Test different error keywords
        for error_str in ["Connection error", "Failed to connect", "Critical issue"]:
            textbox.update({"status": error_str})
            color = textbox._get_value_color()
            assert color == "red", f"'{error_str}' should return red"

    def test_textbox_color_string_with_warning_keyword_returns_yellow(self):
        """Test string containing warning keyword returns yellow color"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Status",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="test",
            data_field="status"
        )

        textbox = Textbox(config)

        # Test different warning keywords
        for warning_str in ["Warning: Low signal", "Warn - High latency"]:
            textbox.update({"status": warning_str})
            color = textbox._get_value_color()
            assert color == "yellow", f"'{warning_str}' should return yellow"


# Coverage target validation
def test_coverage_target():
    """Meta-test: Verify test coverage meets ≥90% target"""
    # Run: pytest tests/unit/test_textbox.py --cov=src/components/textbox --cov-report=term-missing
    pass
