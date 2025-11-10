"""
Unit tests for Component base class.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
import time
from rich.panel import Panel

from src.core.component import (
    Component, ComponentConfig, Position, TriggerConfig, ComponentType
)


# Test Component implementation
class MockComponent(Component):
    """Concrete component for testing"""

    def render(self) -> Panel:
        return Panel(f"Test: {self.data}")


class TestPosition:
    """Test Position dataclass"""

    def test_valid_position(self):
        """Test creating valid position"""
        pos = Position(x=10, y=5, width=40, height=10)
        assert pos.x == 10
        assert pos.y == 5
        assert pos.width == 40
        assert pos.height == 10

    def test_negative_coordinates_raises_error(self):
        """Test that negative x,y raises ValueError"""
        with pytest.raises(ValueError, match="must be >= 0"):
            Position(x=-1, y=5, width=40, height=10)

        with pytest.raises(ValueError, match="must be >= 0"):
            Position(x=10, y=-5, width=40, height=10)

    def test_zero_size_raises_error(self):
        """Test that zero/negative width/height raises ValueError"""
        with pytest.raises(ValueError, match="must be > 0"):
            Position(x=0, y=0, width=0, height=10)

        with pytest.raises(ValueError, match="must be > 0"):
            Position(x=0, y=0, width=40, height=-5)


class TestComponentConfig:
    """Test ComponentConfig dataclass"""

    def test_valid_config(self):
        """Test creating valid config"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test Chart",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test_plugin",
            data_field="value"
        )
        assert config.type == ComponentType.RUNCHART
        assert config.title == "Test Chart"
        assert config.rate_ms == 1000
        assert config.color == "white"  # default

    def test_negative_rate_ms_raises_error(self):
        """Test that negative rate_ms raises ValueError"""
        with pytest.raises(ValueError, match="rate_ms must be >= 0"):
            ComponentConfig(
                type=ComponentType.RUNCHART,
                title="Test",
                position=Position(0, 0, 40, 10),
                rate_ms=-100,
                plugin="test",
                data_field="value"
            )

    def test_empty_plugin_raises_error(self):
        """Test that empty plugin name raises ValueError"""
        with pytest.raises(ValueError, match="plugin name cannot be empty"):
            ComponentConfig(
                type=ComponentType.RUNCHART,
                title="Test",
                position=Position(0, 0, 40, 10),
                rate_ms=1000,
                plugin="",
                data_field="value"
            )


class TestComponent:
    """Test Component base class"""

    def test_component_initialization(self):
        """Test component initializes correctly"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value"
        )
        comp = MockComponent(config)

        assert comp.config == config
        assert comp.data is None
        assert comp.plugin_data == {}
        assert comp.triggered is False

    def test_should_update_initially_true(self):
        """Test that component should update on first call"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value"
        )
        comp = MockComponent(config)

        assert comp.should_update() is True

    def test_should_update_rate_based(self):
        """Test rate-based update logic"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=100,  # 100ms
            plugin="test",
            data_field="value"
        )
        comp = MockComponent(config)

        # Update once
        comp.update({"value": 42})

        # Should NOT update immediately after
        assert comp.should_update() is False

        # Wait for rate_ms
        time.sleep(0.15)  # 150ms > 100ms

        # Should update now
        assert comp.should_update() is True

    def test_static_component_updates_once(self):
        """Test that static components (rate_ms=0) only update once"""
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="Static",
            position=Position(0, 0, 40, 10),
            rate_ms=0,  # Static
            plugin="test",
            data_field="text"
        )
        comp = MockComponent(config)

        # Should update first time
        assert comp.should_update() is True

        # Update
        comp.update({"text": "Hello"})

        # Should NOT update again
        assert comp.should_update() is False

    def test_update_extracts_data_field(self):
        """Test that update() extracts correct data field"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test",
            data_field="cpu_percent"
        )
        comp = MockComponent(config)

        plugin_data = {
            "cpu_percent": 45.2,
            "memory_percent": 78.5,
            "other_field": "ignored"
        }

        comp.update(plugin_data)

        assert comp.data == 45.2
        assert comp.plugin_data == plugin_data

    def test_update_missing_field_raises_error(self):
        """Test that update() raises KeyError if field missing"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test",
            data_field="missing_field"
        )
        comp = MockComponent(config)

        with pytest.raises(KeyError, match="not found in plugin data"):
            comp.update({"other_field": 123})

    def test_render_abstract_method(self):
        """Test that Component.render() is abstract"""
        # Can't instantiate Component directly
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value"
        )

        with pytest.raises(TypeError):
            comp = Component(config)

    def test_component_repr(self):
        """Test component string representation"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="CPU Chart",
            position=Position(0, 0, 40, 10),
            rate_ms=1000,
            plugin="system",
            data_field="cpu"
        )
        comp = MockComponent(config)

        repr_str = repr(comp)
        assert "MockComponent" in repr_str
        assert "CPU Chart" in repr_str
        assert "system" in repr_str
        assert "1000" in repr_str
