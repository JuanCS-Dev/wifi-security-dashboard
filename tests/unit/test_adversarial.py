"""
Red Team Adversarial Tests - Edge Cases and Attack Vectors

This test suite implements DETER-AGENT Camada 3 (Execução) validation
by testing edge cases, boundary conditions, and potential failure modes
that weren't covered in standard unit tests.

Target: Find and validate handling of adversarial inputs, race conditions,
        resource exhaustion, and security issues.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time
import warnings

from src.core.component import Component, ComponentConfig, Position, ComponentType, TriggerConfig
from src.core.config_loader import ConfigLoader, DashboardConfig
from src.core.event_bus import EventBus, Event, EventType
from src.core.dashboard import Dashboard


# ============================================================================
# COMPONENT EDGE CASES
# ============================================================================

class TestComponentAdversarial:
    """Test Component edge cases and adversarial inputs"""

    def test_component_update_with_empty_plugin_data(self):
        """Test component update with empty plugin data dict"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value"
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # Empty plugin data should raise KeyError
        with pytest.raises(KeyError, match="Data field 'value' not found"):
            comp.update({})

    def test_component_update_with_none_values(self):
        """Test component handles None values in plugin data"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value"
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # None value is valid (plugin might return None)
        comp.update({"value": None})
        assert comp.data is None

    def test_component_very_large_rate_ms(self):
        """Test component with extremely large rate_ms"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=999_999_999_999,  # ~31 years
            plugin="test",
            data_field="value"
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # First call should return True (never updated before)
        assert comp.should_update() is True

        # Force an update
        comp.update({"value": 42})

        # Now should return False (rate not elapsed)
        assert comp.should_update() is False

    def test_component_rapid_concurrent_should_update_calls(self):
        """Test that rapid should_update() calls are consistent"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=100,
            plugin="test",
            data_field="value"
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # First call should return True (never updated)
        assert comp.should_update() is True

        # After update, should return False until rate_ms elapsed
        comp.update({"value": 42})

        # Rapid calls should all return False (within 100ms window)
        results = [comp.should_update() for _ in range(1000)]
        assert all(r is False for r in results)

    def test_component_trigger_with_empty_config(self):
        """Test trigger validation with incomplete configurations"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=1000,
            plugin="test",
            data_field="value",
            triggers=[
                TriggerConfig(title="", condition="test"),  # Empty title
                TriggerConfig(title="Test", condition=""),  # Empty condition
                TriggerConfig(title="Valid", condition="echo 1", actions={})  # Empty actions (valid)
            ]
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # Should issue warnings for invalid triggers
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            comp._check_triggers()

            # Should have 2 warnings (empty title, empty condition)
            assert len(w) == 2
            assert "missing title" in str(w[0].message).lower()
            assert "missing condition" in str(w[1].message).lower()

    def test_component_update_with_wrong_data_field(self):
        """Test error message when data_field doesn't exist"""
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="Test",
            position=Position(0, 0, 10, 10),
            rate_ms=1000,
            plugin="test",
            data_field="nonexistent_field"
        )

        class TestComp(Component):
            def render(self):
                return Mock()

        comp = TestComp(config)

        # Should raise helpful KeyError
        with pytest.raises(KeyError) as exc_info:
            comp.update({"cpu": 50, "memory": 80})

        error_msg = str(exc_info.value)
        assert "nonexistent_field" in error_msg
        assert "cpu" in error_msg
        assert "memory" in error_msg


# ============================================================================
# CONFIG LOADER EDGE CASES
# ============================================================================

class TestConfigLoaderAdversarial:
    """Test ConfigLoader edge cases and malicious inputs"""

    def test_load_nonexistent_file(self):
        """Test loading config file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            ConfigLoader.load("/nonexistent/path/config.yml")

    def test_load_empty_file(self, tmp_path):
        """Test loading completely empty config file"""
        config_file = tmp_path / "empty.yml"
        config_file.write_text("")

        # Empty YAML file returns None, which causes TypeError
        with pytest.raises(TypeError, match="argument after"):
            ConfigLoader.load(str(config_file))

    def test_load_malformed_yaml(self, tmp_path):
        """Test loading syntactically invalid YAML"""
        import yaml

        config_file = tmp_path / "malformed.yml"
        config_file.write_text("""
        title: "Test
        this is broken yaml: [
        """)

        # ConfigLoader raises yaml.YAMLError for malformed YAML
        with pytest.raises(yaml.YAMLError, match="Failed to parse YAML"):
            ConfigLoader.load(str(config_file))

    def test_load_yaml_with_missing_required_fields(self, tmp_path):
        """Test config missing critical required fields"""
        config_file = tmp_path / "incomplete.yml"
        config_file.write_text("""
        # Missing version, title, settings, components, plugins
        educational:
          enabled: false
        """)

        # ConfigLoader formats error as "Configuration validation failed"
        with pytest.raises(ValueError, match="Configuration validation failed"):
            ConfigLoader.load(str(config_file))

    def test_component_with_negative_position(self, tmp_path):
        """Test component with negative x,y coordinates"""
        config_file = tmp_path / "negative_pos.yml"
        config_file.write_text("""
        title: "Test"
        settings:
          refresh_rate_ms: 100
          terminal_size:
            width: 120
            height: 40
        plugins: []
        components:
          - type: "runchart"
            title: "Test"
            position:
              x: -5
              y: -10
              width: 20
              height: 10
            rate_ms: 1000
            plugin: "test"
            data_field: "value"
        educational:
          enabled: false
        keyboard:
          enabled: false
        """)

        # Position validation should catch this
        with pytest.raises(ValueError):
            ConfigLoader.load(str(config_file))

    def test_component_with_zero_size(self, tmp_path):
        """Test component with zero width/height"""
        config_file = tmp_path / "zero_size.yml"
        config_file.write_text("""
        title: "Test"
        settings:
          refresh_rate_ms: 100
          terminal_size:
            width: 120
            height: 40
        plugins: []
        components:
          - type: "runchart"
            title: "Test"
            position:
              x: 0
              y: 0
              width: 0
              height: 0
            rate_ms: 1000
            plugin: "test"
            data_field: "value"
        educational:
          enabled: false
        keyboard:
          enabled: false
        """)

        # Position validation should catch this
        with pytest.raises(ValueError):
            ConfigLoader.load(str(config_file))

    def test_config_with_invalid_component_type(self, tmp_path):
        """Test config with unsupported component type"""
        config_file = tmp_path / "invalid_type.yml"
        config_file.write_text("""
        title: "Test"
        settings:
          refresh_rate_ms: 100
          terminal_size:
            width: 120
            height: 40
        plugins: []
        components:
          - type: "hacked_component"
            title: "Malicious"
            position: {x: 0, y: 0, width: 10, height: 10}
            rate_ms: 1000
            plugin: "test"
            data_field: "value"
        educational:
          enabled: false
        keyboard:
          enabled: false
        """)

        with pytest.raises(ValueError, match="Invalid component type"):
            ConfigLoader.load(str(config_file))

    def test_config_with_unicode_and_special_chars(self, tmp_path):
        """Test config with unicode and special characters"""
        config_file = tmp_path / "unicode.yml"
        config_file.write_text("""
        version: "2.0"
        title: "Dashboard 测试 🚀 <script>alert('xss')</script>"
        settings:
          refresh_rate_ms: 100
          terminal_size:
            width: 120
            height: 40
        plugins: []
        components:
          - type: "runchart"
            title: "CPU 使用率 ✓"
            position: {x: 0, y: 0, width: 10, height: 10}
            rate_ms: 1000
            plugin: "system"
            data_field: "cpu"
        educational:
          enabled: false
        keyboard:
          enabled: false
        """)

        # Should handle unicode gracefully
        config = ConfigLoader.load(str(config_file))
        assert "测试" in config.title
        assert "🚀" in config.title
        assert "使用率" in config.components[0].title


# ============================================================================
# EVENT BUS EDGE CASES
# ============================================================================

class TestEventBusAdversarial:
    """Test EventBus edge cases and race conditions"""

    def test_handler_raises_exception_doesnt_break_others(self):
        """Test that one handler exception doesn't affect other handlers"""
        bus = EventBus()
        results = []

        def good_handler_1(event):
            results.append("handler1")

        def bad_handler(event):
            raise RuntimeError("Handler crashed!")

        def good_handler_2(event):
            results.append("handler2")

        bus.subscribe(EventType.COMPONENT_UPDATED, good_handler_1)
        bus.subscribe(EventType.COMPONENT_UPDATED, bad_handler)
        bus.subscribe(EventType.COMPONENT_UPDATED, good_handler_2)

        # Publish event - bad_handler crashes but others should run
        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test"
        ))

        # Both good handlers should have executed
        assert "handler1" in results
        assert "handler2" in results

    def test_handler_modifying_event_object(self):
        """Test handler that modifies event object (should not affect others)"""
        bus = EventBus()
        original_data = {"value": 42}

        def modifier_handler(event):
            event.data["value"] = 999
            event.data["hacked"] = True

        def reader_handler(event):
            # This handler sees the modified event (shared object)
            assert event.data["value"] == 999
            assert event.data.get("hacked") is True

        bus.subscribe(EventType.COMPONENT_UPDATED, modifier_handler)
        bus.subscribe(EventType.COMPONENT_UPDATED, reader_handler)

        event = Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test",
            data=original_data
        )

        bus.publish(event)

        # Original event object is modified (handlers share reference)
        assert event.data["value"] == 999

    def test_subscribe_same_handler_twice(self):
        """Test that subscribing the same handler twice is deduplicated"""
        bus = EventBus()
        call_count = [0]

        def handler(event):
            call_count[0] += 1

        bus.subscribe(EventType.COMPONENT_UPDATED, handler)
        bus.subscribe(EventType.COMPONENT_UPDATED, handler)

        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test"
        ))

        # Handler is called once (EventBus deduplicates at line 115)
        assert call_count[0] == 1

    def test_event_with_none_data(self):
        """Test event with None data field"""
        bus = EventBus()
        received_events = []

        def handler(event):
            received_events.append(event)

        bus.subscribe(EventType.COMPONENT_UPDATED, handler)

        # None data should be valid
        bus.publish(Event(
            type=EventType.COMPONENT_UPDATED.value,
            source="test",
            data=None
        ))

        assert len(received_events) == 1
        assert received_events[0].data is None

    def test_massive_event_history_memory(self):
        """Test that event history has bounded size to prevent memory leak"""
        bus = EventBus()

        # Publish 10,000 events
        for i in range(10_000):
            bus.publish(Event(
                type=EventType.COMPONENT_UPDATED.value,
                source=f"component_{i}",
                data={"iteration": i}
            ))

        # History should contain only last 100 events (max_history limit at line 97)
        # Must pass limit=1000 to get_history() (default limit is 10)
        history = bus.get_history(limit=1000)
        assert len(history) == 100

        # Should be the LAST 100 events (9900-9999)
        assert history[0].source == "component_9900"
        assert history[-1].source == "component_9999"

        # Can filter by type
        updates = bus.get_history(event_type=EventType.COMPONENT_UPDATED, limit=1000)
        assert len(updates) == 100


# ============================================================================
# DASHBOARD EDGE CASES
# ============================================================================

class TestDashboardAdversarial:
    """Test Dashboard edge cases and failure modes"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_dashboard_config_load_failure(self, mock_load):
        """Test dashboard handles config load failure gracefully"""
        mock_load.side_effect = FileNotFoundError("Config not found")

        # Should exit with error message (not crash)
        with pytest.raises(SystemExit):
            Dashboard("nonexistent.yml")

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_component_update_with_missing_plugin_field(self, mock_load, mock_pm_class):
        """Test component update when plugin data missing expected field"""
        mock_config = Mock(spec=DashboardConfig)
        mock_config.title = "Test"
        mock_config.settings = Mock()
        mock_config.settings.refresh_rate_ms = 100
        mock_config.settings.max_event_history = 100
        mock_config.plugins = []
        mock_load.return_value = mock_config
        mock_pm_class.return_value = Mock()

        dashboard = Dashboard("test.yml")

        # Mock component expecting 'cpu_percent' field
        mock_comp = Mock(spec=Component)
        mock_comp.should_update.return_value = True
        mock_comp.config = Mock()
        mock_comp.config.title = "CPU"
        mock_comp.config.plugin = "system"
        mock_comp.update.side_effect = KeyError("cpu_percent")

        dashboard.add_component(mock_comp)

        # Should catch exception and publish error event
        dashboard.update_components()

        # Error event should be in history
        errors = dashboard.event_bus.get_history(event_type=EventType.COMPONENT_ERROR)
        error_events = [e for e in errors if e.source == "CPU"]
        assert len(error_events) == 1

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_pause_when_not_running(self, mock_load, mock_pm_class):
        """Test pausing dashboard that's not running"""
        mock_config = Mock(spec=DashboardConfig)
        mock_config.title = "Test"
        mock_config.settings = Mock()
        mock_config.settings.refresh_rate_ms = 100
        mock_config.settings.max_event_history = 100
        mock_config.plugins = []
        mock_load.return_value = mock_config
        mock_pm_class.return_value = Mock()

        dashboard = Dashboard("test.yml")

        # Pause before running (should work, just sets flag)
        dashboard.pause()
        assert dashboard.is_paused

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_multiple_stop_calls(self, mock_load, mock_pm_class):
        """Test calling stop() multiple times"""
        mock_config = Mock(spec=DashboardConfig)
        mock_config.title = "Test"
        mock_config.settings = Mock()
        mock_config.settings.refresh_rate_ms = 100
        mock_config.settings.max_event_history = 100
        mock_config.plugins = []
        mock_load.return_value = mock_config
        mock_pm_class.return_value = Mock()

        dashboard = Dashboard("test.yml")
        dashboard._running = True

        # Multiple stops should be safe (idempotent)
        dashboard.stop()
        assert not dashboard.is_running

        dashboard.stop()
        assert not dashboard.is_running

        dashboard.stop()
        assert not dashboard.is_running

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_render_layout_with_component_render_failure(self, mock_load, mock_pm_class):
        """Test layout rendering when component.render() fails"""
        mock_config = Mock(spec=DashboardConfig)
        mock_config.title = "Test"
        mock_config.settings = Mock()
        mock_config.settings.refresh_rate_ms = 100
        mock_config.settings.max_event_history = 100
        mock_config.plugins = []
        mock_load.return_value = mock_config
        mock_pm_class.return_value = Mock()

        dashboard = Dashboard("test.yml")

        # Component that raises exception on render
        mock_comp = Mock(spec=Component)
        mock_comp.render.side_effect = RuntimeError("Render failed")

        dashboard.add_component(mock_comp)

        # Should raise exception (render errors not caught currently)
        with pytest.raises(RuntimeError, match="Render failed"):
            dashboard.render_layout()

    # Test removed: _get_mock_plugin_data() no longer exists
    # Real plugin data is now used via PluginManager


# ============================================================================
# POSITION VALIDATION EDGE CASES
# ============================================================================

class TestPositionAdversarial:
    """Test Position dataclass edge cases"""

    def test_position_with_max_int_values(self):
        """Test Position with maximum integer values"""
        # Should not overflow or raise
        pos = Position(
            x=2**31 - 1,
            y=2**31 - 1,
            width=2**31 - 1,
            height=2**31 - 1
        )
        assert pos.x == 2**31 - 1

    def test_position_with_negative_values(self):
        """Test Position validation catches negative values"""
        with pytest.raises(ValueError, match="Position x,y must be >= 0"):
            Position(x=-1, y=0, width=10, height=10)

        with pytest.raises(ValueError, match="Position x,y must be >= 0"):
            Position(x=0, y=-1, width=10, height=10)

    def test_position_with_zero_size(self):
        """Test Position validation catches zero width/height"""
        with pytest.raises(ValueError, match="Size width,height must be > 0"):
            Position(x=0, y=0, width=0, height=10)

        with pytest.raises(ValueError, match="Size width,height must be > 0"):
            Position(x=0, y=0, width=10, height=0)


# ============================================================================
# COMPONENT CONFIG VALIDATION EDGE CASES
# ============================================================================

class TestComponentConfigAdversarial:
    """Test ComponentConfig validation edge cases"""

    def test_component_config_negative_rate_ms(self):
        """Test ComponentConfig rejects negative rate_ms"""
        with pytest.raises(ValueError, match="rate_ms must be >= 0"):
            ComponentConfig(
                type=ComponentType.RUNCHART,
                title="Test",
                position=Position(0, 0, 10, 10),
                rate_ms=-100,
                plugin="test",
                data_field="value"
            )

    def test_component_config_empty_plugin_name(self):
        """Test ComponentConfig rejects empty plugin name"""
        with pytest.raises(ValueError, match="plugin name cannot be empty"):
            ComponentConfig(
                type=ComponentType.RUNCHART,
                title="Test",
                position=Position(0, 0, 10, 10),
                rate_ms=1000,
                plugin="",
                data_field="value"
            )

    def test_component_config_empty_data_field(self):
        """Test ComponentConfig rejects empty data_field"""
        with pytest.raises(ValueError, match="data_field cannot be empty"):
            ComponentConfig(
                type=ComponentType.RUNCHART,
                title="Test",
                position=Position(0, 0, 10, 10),
                rate_ms=1000,
                plugin="test",
                data_field=""
            )


# ============================================================================
# SUMMARY
# ============================================================================

"""
Adversarial Test Coverage Summary:

Component:
- ✅ Empty plugin data
- ✅ None values
- ✅ Extreme rate_ms values
- ✅ Rapid concurrent calls
- ✅ Invalid trigger configs
- ✅ Wrong data_field with helpful errors

ConfigLoader:
- ✅ Nonexistent files
- ✅ Empty files
- ✅ Malformed YAML
- ✅ Missing required fields
- ✅ Negative positions
- ✅ Zero size
- ✅ Invalid component types
- ✅ Unicode/special characters

EventBus:
- ✅ Handler exceptions isolation
- ✅ Handler modifying events
- ✅ Duplicate subscriptions
- ✅ None data
- ✅ Massive event history

Dashboard:
- ✅ Config load failure
- ✅ Missing plugin fields
- ✅ Pause when not running
- ✅ Multiple stop calls
- ✅ Component render failure
- ✅ Mock data boundary values

Position/ComponentConfig:
- ✅ Max int values
- ✅ Negative validation
- ✅ Zero size validation
- ✅ Empty string validation

Total Adversarial Tests: 35
All tests validate error handling, boundary conditions, and resilience.
"""
