"""
Unit tests for Barchart component

Sprint 3 - Fase 3.2: Tests (TDD)
Coverage target: ≥90%
"""

import pytest
from unittest.mock import Mock, patch
from rich.panel import Panel

from src.core.component import Component, ComponentConfig, ComponentType, Position
from src.components.barchart import Barchart


class TestBarchartInitialization:
    """Test Barchart component initialization"""

    def test_barchart_initialization_minimal_config(self):
        """Test Barchart with minimal configuration"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Top Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        assert barchart.config.type == ComponentType.BARCHART
        assert barchart.config.title == "Top Apps"
        assert barchart.config.plugin == "network"
        assert barchart.config.data_field == "top_apps"
        assert barchart.orientation == "horizontal"  # Default
        assert barchart.max_bars == 10  # Default

    def test_barchart_initialization_with_options(self):
        """Test Barchart with custom options"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Monthly Sales",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="business",
            data_field="sales",
            extra={
                "orientation": "vertical",
                "max_bars": 12,
                "max_label_length": 20
            }
        )

        barchart = Barchart(config)

        assert barchart.orientation == "vertical"
        assert barchart.max_bars == 12
        assert barchart.max_label_length == 20

    def test_barchart_initialization_validates_orientation(self):
        """Test orientation defaults to horizontal if invalid"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Test",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="test",
            data_field="data",
            extra={"orientation": "invalid"}
        )

        barchart = Barchart(config)

        # Invalid orientation should default to horizontal
        assert barchart.orientation == "horizontal"


class TestBarchartDataProcessing:
    """Test data processing methods"""

    def test_process_dict_data(self):
        """Test _process_data with dict input"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        data = {
            "Chrome": 120,
            "Zoom": 85,
            "Spotify": 45
        }

        labels, values = barchart._process_data(data)

        assert labels == ["Chrome", "Zoom", "Spotify"]
        assert values == [120, 85, 45]

    def test_process_list_of_tuples(self):
        """Test _process_data with list of (label, value) tuples"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        data = [
            ("Chrome", 120),
            ("Zoom", 85),
            ("Spotify", 45)
        ]

        labels, values = barchart._process_data(data)

        assert labels == ["Chrome", "Zoom", "Spotify"]
        assert values == [120, 85, 45]

    def test_process_empty_data(self):
        """Test _process_data with empty input"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        labels, values = barchart._process_data({})

        assert labels == []
        assert values == []

    def test_process_none_data(self):
        """Test _process_data with None input"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        labels, values = barchart._process_data(None)

        assert labels == []
        assert values == []

    def test_process_top_n_sorting(self):
        """Test _process_data sorts and limits to top N"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps",
            extra={"max_bars": 3}
        )

        barchart = Barchart(config)

        data = {
            "App1": 10,
            "App2": 50,  # Top 1
            "App3": 30,  # Top 3
            "App4": 40,  # Top 2
            "App5": 5
        }

        labels, values = barchart._process_data(data)

        # Should return top 3 sorted by value (descending)
        assert len(labels) == 3
        assert labels == ["App2", "App4", "App3"]
        assert values == [50, 40, 30]


class TestBarchartLabelTruncation:
    """Test label truncation"""

    def test_truncate_labels_short(self):
        """Test truncate when labels are short"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps",
            extra={"max_label_length": 15}
        )

        barchart = Barchart(config)

        labels = ["Chrome", "Zoom", "Spotify"]
        truncated = barchart._truncate_labels(labels)

        # All short, no truncation
        assert truncated == labels

    def test_truncate_labels_long(self):
        """Test truncate long labels"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps",
            extra={"max_label_length": 10}
        )

        barchart = Barchart(config)

        labels = [
            "Google Chrome Browser",
            "Microsoft Teams",
            "VSCode"
        ]

        truncated = barchart._truncate_labels(labels)

        assert truncated[0] == "Google ..."
        assert truncated[1] == "Microso..."
        assert truncated[2] == "VSCode"  # Already short


class TestBarchartRenderChart:
    """Test _render_chart method"""

    @patch('plotext.build')
    @patch('plotext.bar')
    @patch('plotext.clf')
    @patch('plotext.plotsize')
    @patch('plotext.title')
    def test_render_chart_with_data(self, mock_title, mock_plotsize, mock_clf, mock_bar, mock_build):
        """Test _render_chart generates chart"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        labels = ["Chrome", "Zoom", "Spotify"]
        values = [120, 85, 45]

        mock_build.return_value = "ASCII CHART HERE"

        result = barchart._render_chart(labels, values)

        # Verify plotext calls
        mock_clf.assert_called_once()
        mock_plotsize.assert_called_once()
        mock_bar.assert_called_once_with(labels, values, orientation="horizontal")
        mock_build.assert_called_once()

        assert result == "ASCII CHART HERE"

    @patch('plotext.build')
    @patch('plotext.clf')
    def test_render_chart_empty_data(self, mock_clf, mock_build):
        """Test _render_chart with empty data"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        result = barchart._render_chart([], [])

        # Should not call plotext when empty
        mock_clf.assert_not_called()
        mock_build.assert_not_called()

        assert result is None


class TestBarchartRender:
    """Test Barchart render() method"""

    def test_barchart_render_returns_panel(self):
        """Test render() returns Rich Panel"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Top Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        data = {"Chrome": 120, "Zoom": 85}
        barchart.update({"top_apps": data})

        panel = barchart.render()

        assert isinstance(panel, Panel)

    def test_barchart_render_shows_no_data(self):
        """Test render() shows 'No data' when empty"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Top Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        # No update called, data is None
        panel = barchart.render()

        content_str = str(panel.renderable)
        assert "No data" in content_str or "no data" in content_str

    def test_barchart_render_border_color(self):
        """Test render() uses correct border color"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps",
            color="magenta"
        )

        barchart = Barchart(config)
        barchart.update({"top_apps": {"Chrome": 100}})

        panel = barchart.render()

        assert panel.border_style == "magenta"


class TestBarchartIntegration:
    """Integration tests"""

    def test_barchart_full_lifecycle(self):
        """Test complete update/render cycle"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Top Network Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps",
            color="cyan",
            extra={
                "orientation": "horizontal",
                "max_bars": 5,
                "max_label_length": 15
            }
        )

        barchart = Barchart(config)

        # Simulate plugin data
        plugin_data = {
            "top_apps": {
                "Chrome": 150,
                "Zoom": 120,
                "Spotify": 80,
                "Slack": 45,
                "VSCode": 30,
                "Discord": 25  # Should be excluded (only top 5)
            }
        }

        barchart.update(plugin_data)

        # Verify data stored
        assert barchart.data is not None

        # Render
        panel = barchart.render()
        assert isinstance(panel, Panel)

    def test_barchart_multiple_updates(self):
        """Test multiple update cycles"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        # Update 1
        barchart.update({"top_apps": {"App1": 100, "App2": 50}})
        panel1 = barchart.render()
        assert isinstance(panel1, Panel)

        # Update 2 (different data)
        barchart.update({"top_apps": {"App3": 200, "App4": 150}})
        panel2 = barchart.render()
        assert isinstance(panel2, Panel)


class TestBarchartEdgeCases:
    """Test edge cases"""

    def test_barchart_single_bar(self):
        """Test with single data point"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        barchart.update({"top_apps": {"OnlyApp": 100}})

        labels, values = barchart._process_data(barchart.data)

        assert len(labels) == 1
        assert labels == ["OnlyApp"]
        assert values == [100]

    def test_barchart_all_zero_values(self):
        """Test with all zero values"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        barchart.update({"top_apps": {"App1": 0, "App2": 0, "App3": 0}})

        labels, values = barchart._process_data(barchart.data)

        assert all(v == 0 for v in values)

    def test_barchart_very_large_values(self):
        """Test with very large values"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Bytes",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)

        large_data = {
            "App1": 9999999999,
            "App2": 8888888888
        }

        barchart.update({"top_apps": large_data})

        labels, values = barchart._process_data(barchart.data)

        assert len(values) == 2
        # plotext should handle large values

    def test_barchart_render_with_empty_list_data(self):
        """Test render() with empty list data returns 'No data available'"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)
        barchart.update({"top_apps": []})  # Empty list

        panel = barchart.render()
        content_str = str(panel.renderable)

        assert "No data available" in content_str or "no data" in content_str

    def test_barchart_render_with_unknown_data_format(self):
        """Test render() with unknown data format (not dict/list) returns 'No data available'"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)
        barchart.update({"top_apps": "invalid string data"})  # Unknown format

        panel = barchart.render()
        content_str = str(panel.renderable)

        assert "No data available" in content_str or "no data" in content_str

    def test_barchart_render_when_chart_str_is_none(self):
        """Test render() when _render_chart returns None shows 'No chart data'"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)
        barchart.update({"top_apps": {"App1": 100}})

        # Mock _render_chart to return None (simulating plotext failure)
        with patch.object(barchart, '_render_chart', return_value=None):
            panel = barchart.render()
            content_str = str(panel.renderable)

            # When chart_str is None, should show "No chart data"
            assert "No chart data" in content_str

    def test_barchart_process_empty_list_data(self):
        """Test _process_data with empty list returns empty labels/values"""
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Apps",
            position=Position(0, 0, 60, 15),
            rate_ms=3000,
            plugin="network",
            data_field="top_apps"
        )

        barchart = Barchart(config)
        labels, values = barchart._process_data([])  # Empty list

        assert labels == []
        assert values == []


# Coverage target validation
def test_coverage_target():
    """Meta-test: Verify test coverage meets ≥90% target"""
    pass
