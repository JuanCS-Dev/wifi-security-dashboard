"""
Unit tests for Dashboard orchestrator.

These tests mock Rich Live and components to test Dashboard logic
without actually rendering to terminal.

Target: 80%+ coverage of dashboard.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import time

from src.core.dashboard import Dashboard
from src.core.component import Component, ComponentConfig, Position, ComponentType
from src.core.event_bus import Event, EventType
from src.core.config_loader import DashboardConfig


# ============================================================================
# FIXTURES AND HELPERS
# ============================================================================

@pytest.fixture
def mock_config():
    """Create mock DashboardConfig"""
    config = Mock(spec=DashboardConfig)
    config.title = "Test Dashboard"
    config.settings = Mock()
    config.settings.refresh_rate_ms = 100
    config.settings.max_event_history = 100
    config.settings.terminal_size = Mock()
    config.settings.terminal_size.width = 120
    config.settings.terminal_size.height = 46
    config.plugins = []
    config.components = []
    config.educational = Mock()
    config.keyboard = Mock()
    return config


@pytest.fixture
def mock_component():
    """Create mock Component"""
    comp = Mock(spec=Component)
    comp.should_update.return_value = False
    comp.config = Mock()
    comp.config.title = "Mock Component"
    comp.config.plugin = "mock_plugin"
    comp.config.data_field = "value"
    comp.render.return_value = Mock()  # Mock Panel
    return comp


# ============================================================================
# DASHBOARD INITIALIZATION TESTS
# ============================================================================

class TestDashboardInitialization:
    """Test Dashboard initialization and setup"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_dashboard_loads_config(self, mock_load, mock_config):
        """Test that dashboard loads configuration on init"""
        mock_load.return_value = mock_config

        dashboard = Dashboard("test.yml")

        mock_load.assert_called_once_with("test.yml")
        assert dashboard.config == mock_config

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_dashboard_initializes_empty_state(self, mock_load, mock_pm_class, mock_config):
        """Test dashboard starts with empty state"""
        mock_load.return_value = mock_config
        mock_pm_class.return_value = Mock()

        dashboard = Dashboard("test.yml")

        assert dashboard._running is False
        assert dashboard._paused is False
        assert len(dashboard.components) == 0
        assert dashboard.plugin_manager is not None

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_dashboard_publishes_startup_event(self, mock_load, mock_config):
        """Test that dashboard publishes DASHBOARD_STARTED event"""
        mock_load.return_value = mock_config

        dashboard = Dashboard("test.yml")

        # Check event was published
        events = dashboard.event_bus.get_history(
            event_type=EventType.DASHBOARD_STARTED
        )
        assert len(events) == 1
        assert events[0].source == "dashboard"

    @patch('src.core.dashboard.PluginManager')
    @patch('src.core.dashboard.ConfigLoader.load')
    def test_dashboard_handles_plugin_init_error(self, mock_load, mock_pm_class, mock_config):
        """Test dashboard handles plugin initialization errors gracefully"""
        mock_load.return_value = mock_config

        # Mock plugin manager that raises error on initialize_all
        mock_pm = Mock()
        mock_pm.initialize_all.side_effect = RuntimeError("Plugin failed to load")
        mock_pm_class.return_value = mock_pm

        # Dashboard should still initialize (warning shown, not crash)
        dashboard = Dashboard("test.yml")

        # Dashboard should be created despite plugin error
        assert dashboard is not None
        assert dashboard.plugin_manager is not None


# ============================================================================
# COMPONENT MANAGEMENT TESTS
# ============================================================================

class TestComponentManagement:
    """Test adding and managing components"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_add_component(self, mock_load, mock_config, mock_component):
        """Test adding a component to dashboard"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard.add_component(mock_component)

        assert len(dashboard.components) == 1
        assert dashboard.components[0] == mock_component

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_add_multiple_components(self, mock_load, mock_config):
        """Test adding multiple components"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        comp1 = Mock(spec=Component)
        comp2 = Mock(spec=Component)
        comp3 = Mock(spec=Component)

        dashboard.add_component(comp1)
        dashboard.add_component(comp2)
        dashboard.add_component(comp3)

        assert len(dashboard.components) == 3


# ============================================================================
# UPDATE CYCLE TESTS
# ============================================================================

class TestUpdateCycle:
    """Test component update cycle"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_update_components_skips_when_not_ready(
        self, mock_load, mock_config, mock_component
    ):
        """Test that components not ready to update are skipped"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        mock_component.should_update.return_value = False
        dashboard.add_component(mock_component)

        dashboard.update_components()

        # should_update called but update not called
        mock_component.should_update.assert_called_once()
        mock_component.update.assert_not_called()

    @patch('src.core.dashboard.ConfigLoader.load')
    @patch('src.core.dashboard.PluginManager')
    def test_update_components_updates_when_ready(
        self, mock_pm_class, mock_load, mock_config, mock_component
    ):
        """Test that components ready to update are updated"""
        mock_load.return_value = mock_config

        # Mock PluginManager instance
        mock_pm = Mock()
        mock_pm.get_plugin_data.return_value = {"value": 42}
        mock_pm_class.return_value = mock_pm

        dashboard = Dashboard("test.yml")

        mock_component.should_update.return_value = True
        mock_component.config.plugin = "test"
        dashboard.add_component(mock_component)

        dashboard.update_components()

        mock_component.should_update.assert_called_once()
        mock_component.update.assert_called_once()

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_update_components_publishes_event(
        self, mock_load, mock_config, mock_component
    ):
        """Test that component updates publish events"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        mock_component.should_update.return_value = True
        mock_component.config.title = "Test Component"
        mock_component.data = 42.5
        dashboard.add_component(mock_component)

        dashboard.update_components()

        # Check event was published
        events = dashboard.event_bus.get_history(
            event_type=EventType.COMPONENT_UPDATED
        )
        assert len(events) >= 1  # At least 1 (may have startup events)
        # Find our component's event
        comp_events = [e for e in events if e.source == "Test Component"]
        assert len(comp_events) == 1
        assert comp_events[0].data["value"] == 42.5

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_update_components_handles_exceptions(
        self, mock_load, mock_config, mock_component
    ):
        """Test that exceptions in component update don't crash dashboard"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        # Component that raises error
        mock_component.should_update.return_value = True
        mock_component.update.side_effect = RuntimeError("Test error")
        mock_component.config.title = "Broken Component"
        dashboard.add_component(mock_component)

        # Should not raise exception
        dashboard.update_components()

        # Error event should be published
        errors = dashboard.event_bus.get_history(
            event_type=EventType.COMPONENT_ERROR
        )
        error_events = [e for e in errors if e.source == "Broken Component"]
        assert len(error_events) == 1
        assert "Test error" in str(error_events[0].data.get('error'))


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling functionality"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_on_component_error_logs_to_console(
        self, mock_load, mock_config
    ):
        """Test that component errors are logged to console"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        # Create error event
        error_event = Event(
            type=EventType.COMPONENT_ERROR.value,
            source="Test Component",
            data={"error": "Something went wrong"}
        )

        # Mock console
        with patch.object(dashboard.console, 'print') as mock_print:
            dashboard._on_component_error(error_event)

            # Should have called print twice (error title + message)
            assert mock_print.call_count == 2
            # Check that component name and error message appeared
            calls_str = str(mock_print.call_args_list)
            assert "Test Component" in calls_str
            assert "Something went wrong" in calls_str


# ============================================================================
# STATE CONTROL TESTS
# ============================================================================

class TestStateControl:
    """Test pause/resume/stop functionality"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_pause(self, mock_load, mock_config):
        """Test pausing dashboard"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        assert not dashboard.is_paused

        dashboard.pause()

        assert dashboard.is_paused
        assert dashboard._paused is True

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_resume(self, mock_load, mock_config):
        """Test resuming dashboard"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard.pause()
        assert dashboard.is_paused

        dashboard.resume()

        assert not dashboard.is_paused
        assert dashboard._paused is False

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_stop(self, mock_load, mock_config):
        """Test stopping dashboard"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard._running = True
        assert dashboard.is_running

        dashboard.stop()

        assert not dashboard.is_running
        assert dashboard._running is False

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_pause_publishes_event(self, mock_load, mock_config):
        """Test that pause publishes event"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard.pause()

        events = dashboard.event_bus.get_history(
            event_type=EventType.DASHBOARD_PAUSED
        )
        assert len(events) == 1

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_resume_publishes_event(self, mock_load, mock_config):
        """Test that resume publishes event"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard.pause()
        dashboard.resume()

        events = dashboard.event_bus.get_history(
            event_type=EventType.DASHBOARD_RESUMED
        )
        assert len(events) == 1


# ============================================================================
# MOCK DATA TESTS - REMOVED
# ============================================================================
# _get_mock_plugin_data() was removed when real PluginManager was integrated
# These tests are now obsolete


# ============================================================================
# LAYOUT RENDERING TESTS
# ============================================================================

class TestLayoutRendering:
    """Test layout rendering"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_render_layout_with_no_components(self, mock_load, mock_config):
        """Test rendering layout with no components"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        layout = dashboard.render_layout()

        assert layout is not None
        # Should have header and welcome message

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_render_layout_with_components(
        self, mock_load, mock_config, mock_component
    ):
        """Test rendering layout with components"""
        mock_load.return_value = mock_config
        dashboard = Dashboard("test.yml")

        dashboard.add_component(mock_component)
        layout = dashboard.render_layout()

        assert layout is not None
        # Component render() should be called
        mock_component.render.assert_called()


# ============================================================================
# REPR TESTS
# ============================================================================

class TestDashboardRepr:
    """Test Dashboard string representation"""

    @patch('src.core.dashboard.ConfigLoader.load')
    def test_repr(self, mock_load, mock_config):
        """Test Dashboard repr"""
        mock_load.return_value = mock_config
        mock_config.title = "My Dashboard"
        dashboard = Dashboard("test.yml")

        dashboard.add_component(Mock())
        dashboard.add_component(Mock())

        repr_str = repr(dashboard)

        assert "Dashboard" in repr_str
        assert "My Dashboard" in repr_str
        assert "components=2" in repr_str
        assert "running=False" in repr_str
