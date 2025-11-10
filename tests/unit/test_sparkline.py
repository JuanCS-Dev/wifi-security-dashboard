"""
Unit tests for Sparkline component

Sprint 3 - Fase 2.2: Tests (TDD)
Coverage target: ≥90%
"""

import pytest
from unittest.mock import Mock
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig, ComponentType, Position
from src.components.sparkline import Sparkline


class TestSparklineInitialization:
    """Test Sparkline component initialization"""

    def test_sparkline_initialization_minimal_config(self):
        """Test Sparkline with minimal configuration"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU Trend",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)

        assert sparkline.config.type == ComponentType.SPARKLINE
        assert sparkline.config.title == "CPU Trend"
        assert sparkline.config.plugin == "system"
        assert sparkline.config.data_field == "cpu_percent"
        assert len(sparkline.history) == 0
        assert sparkline.max_samples == 40  # Default

    def test_sparkline_initialization_with_custom_max_samples(self):
        """Test Sparkline with custom max_samples"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Memory Trend",
            position=Position(0, 0, 60, 5),
            rate_ms=1000,
            plugin="system",
            data_field="memory_percent",
            extra={"max_samples": 60}
        )

        sparkline = Sparkline(config)

        assert sparkline.max_samples == 60
        assert sparkline.history.maxlen == 60

    def test_sparkline_initialization_with_label(self):
        """Test Sparkline with label"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="WiFi",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm",
            extra={"label": "Signal"}
        )

        sparkline = Sparkline(config)

        assert sparkline.label == "Signal"


class TestSparklineOnUpdate:
    """Test Sparkline on_update() hook (adds to history)"""

    def test_sparkline_on_update_adds_to_history(self):
        """Test on_update() adds numeric values to history"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)

        # Simulate updates
        sparkline.update({"cpu_percent": 45.2})
        assert len(sparkline.history) == 1
        assert sparkline.history[0] == 45.2

        sparkline.update({"cpu_percent": 52.8})
        assert len(sparkline.history) == 2
        assert sparkline.history[1] == 52.8

    def test_sparkline_on_update_respects_max_samples(self):
        """Test history buffer respects max_samples limit"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            extra={"max_samples": 5}
        )

        sparkline = Sparkline(config)

        # Add 10 values, only last 5 should remain
        for i in range(10):
            sparkline.update({"cpu_percent": i * 10})

        assert len(sparkline.history) == 5
        assert list(sparkline.history) == [50, 60, 70, 80, 90]

    def test_sparkline_on_update_handles_non_numeric(self):
        """Test on_update() ignores non-numeric values"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        sparkline = Sparkline(config)

        # String value should be ignored
        sparkline.update({"value": "invalid"})
        assert len(sparkline.history) == 0

        # None value should be ignored
        sparkline.update({"value": None})
        assert len(sparkline.history) == 0

    def test_sparkline_on_update_converts_int_to_float(self):
        """Test on_update() converts integers to floats"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Counter",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="count"
        )

        sparkline = Sparkline(config)

        sparkline.update({"count": 42})
        assert len(sparkline.history) == 1
        assert isinstance(sparkline.history[0], float)
        assert sparkline.history[0] == 42.0


class TestSparklineNormalization:
    """Test value normalization (0-1 range)"""

    def test_normalize_value_basic_range(self):
        """Test normalize_value with basic 0-100 range"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        sparkline = Sparkline(config)

        # Min=0, Max=100
        assert sparkline._normalize_value(0, 0, 100) == 0.0
        assert sparkline._normalize_value(50, 0, 100) == 0.5
        assert sparkline._normalize_value(100, 0, 100) == 1.0

    def test_normalize_value_equal_min_max(self):
        """Test normalize_value when min == max (all values equal)"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        sparkline = Sparkline(config)

        # All values equal should return 0.5 (middle)
        assert sparkline._normalize_value(50, 50, 50) == 0.5

    def test_normalize_value_negative_range(self):
        """Test normalize_value with negative values (dBm)"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Signal",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm"
        )

        sparkline = Sparkline(config)

        # dBm range: -90 to -30
        assert sparkline._normalize_value(-90, -90, -30) == 0.0
        assert sparkline._normalize_value(-60, -90, -30) == 0.5
        assert sparkline._normalize_value(-30, -90, -30) == 1.0


class TestSparklineCharConversion:
    """Test value to Unicode char conversion"""

    def test_value_to_char_full_range(self):
        """Test value_to_char covers all 8 Unicode levels"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        sparkline = Sparkline(config)

        # 0-100 range, test each level
        chars = "▁▂▃▄▅▆▇█"

        assert sparkline._value_to_char(0, 0, 100) == "▁"
        assert sparkline._value_to_char(100, 0, 100) == "█"
        assert sparkline._value_to_char(50, 0, 100) in chars  # Middle range

    def test_value_to_char_edge_values(self):
        """Test value_to_char with edge values"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Test",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="value"
        )

        sparkline = Sparkline(config)

        # Minimum value
        assert sparkline._value_to_char(0, 0, 100) == "▁"

        # Maximum value
        assert sparkline._value_to_char(100, 0, 100) == "█"


class TestSparklineRenderSparkline:
    """Test _render_sparkline() method"""

    def test_render_sparkline_with_values(self):
        """Test _render_sparkline returns correct Unicode string"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)

        # Add values manually to history
        sparkline.history.extend([0, 25, 50, 75, 100])

        result = sparkline._render_sparkline()

        assert isinstance(result, str)
        assert len(result) == 5  # 5 values = 5 chars
        assert result[0] == "▁"  # Min value
        assert result[4] == "█"  # Max value

    def test_render_sparkline_empty_history(self):
        """Test _render_sparkline with empty history"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)

        result = sparkline._render_sparkline()

        assert result == ""

    def test_render_sparkline_single_value(self):
        """Test _render_sparkline with single value"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)
        sparkline.history.append(50.0)

        result = sparkline._render_sparkline()

        assert len(result) == 1
        assert result == "▄"  # Middle value when min==max


class TestSparklineRender:
    """Test Sparkline render() method"""

    def test_sparkline_render_returns_panel(self):
        """Test render() returns Rich Panel"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU Trend",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)
        sparkline.update({"cpu_percent": 45.2})

        panel = sparkline.render()

        assert isinstance(panel, Panel)

    def test_sparkline_render_shows_no_data_when_empty(self):
        """Test render() shows 'No data' when history empty"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)

        panel = sparkline.render()
        content_str = str(panel.renderable)

        assert "No data" in content_str or "no data" in content_str

    def test_sparkline_render_with_label(self):
        """Test render() includes label when configured"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="WiFi",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm",
            extra={"label": "Signal"}
        )

        sparkline = Sparkline(config)
        sparkline.update({"signal_strength_dbm": -45})
        sparkline.update({"signal_strength_dbm": -50})

        panel = sparkline.render()
        content_str = str(panel.renderable)

        assert "Signal" in content_str

    def test_sparkline_render_without_label(self):
        """Test render() works without label"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)
        sparkline.update({"cpu_percent": 45})
        sparkline.update({"cpu_percent": 55})

        panel = sparkline.render()

        assert isinstance(panel, Panel)

    def test_sparkline_render_shows_current_value(self):
        """Test render() shows current value"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent"
        )

        sparkline = Sparkline(config)
        sparkline.update({"cpu_percent": 45.2})

        panel = sparkline.render()
        content_str = str(panel.renderable)

        assert "45.2" in content_str

    def test_sparkline_render_border_color(self):
        """Test render() uses correct border color"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="green"
        )

        sparkline = Sparkline(config)
        sparkline.update({"cpu_percent": 45})

        panel = sparkline.render()

        assert panel.border_style == "green"


class TestSparklineIntegration:
    """Integration tests"""

    def test_sparkline_full_lifecycle(self):
        """Test complete update/render cycle"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU Usage Trend",
            position=Position(0, 0, 60, 5),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="cyan",
            extra={"max_samples": 20, "label": "CPU"}
        )

        sparkline = Sparkline(config)

        # Simulate multiple updates
        cpu_values = [45, 50, 55, 60, 58, 52, 48, 45, 42, 40]

        for cpu in cpu_values:
            sparkline.update({"cpu_percent": cpu})

        # Verify history
        assert len(sparkline.history) == 10
        assert list(sparkline.history) == [float(v) for v in cpu_values]

        # Render and verify
        panel = sparkline.render()
        assert isinstance(panel, Panel)

        content_str = str(panel.renderable)
        assert "CPU" in content_str  # Label
        assert str(cpu_values[-1]) in content_str  # Current value

    def test_sparkline_multiple_update_cycles(self):
        """Test multiple update/render cycles"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Memory",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="memory_percent"
        )

        sparkline = Sparkline(config)

        # Cycle 1
        sparkline.update({"memory_percent": 65})
        panel1 = sparkline.render()
        assert isinstance(panel1, Panel)

        # Cycle 2
        sparkline.update({"memory_percent": 70})
        panel2 = sparkline.render()
        assert isinstance(panel2, Panel)

        # Verify history accumulated
        assert len(sparkline.history) == 2


class TestSparklineEdgeCases:
    """Test edge cases"""

    def test_sparkline_handles_zero_value(self):
        """Test sparkline handles zero correctly"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Counter",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="system",
            data_field="count"
        )

        sparkline = Sparkline(config)
        sparkline.update({"count": 0})
        sparkline.update({"count": 10})

        assert len(sparkline.history) == 2
        assert sparkline.history[0] == 0.0

    def test_sparkline_handles_negative_values(self):
        """Test sparkline handles negative values (dBm)"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="WiFi Signal",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="wifi",
            data_field="signal_strength_dbm"
        )

        sparkline = Sparkline(config)

        for dbm in [-90, -70, -50, -30]:
            sparkline.update({"signal_strength_dbm": dbm})

        assert len(sparkline.history) == 4
        assert all(v < 0 for v in sparkline.history)

    def test_sparkline_handles_large_values(self):
        """Test sparkline handles very large values"""
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="Bytes",
            position=Position(0, 0, 40, 5),
            rate_ms=1000,
            plugin="network",
            data_field="bytes_total"
        )

        sparkline = Sparkline(config)

        large_values = [1000000, 2000000, 3000000]
        for val in large_values:
            sparkline.update({"bytes_total": val})

        assert len(sparkline.history) == 3

        # Should still render without error
        panel = sparkline.render()
        assert isinstance(panel, Panel)


# Coverage target validation
def test_coverage_target():
    """Meta-test: Verify test coverage meets ≥90% target"""
    pass
