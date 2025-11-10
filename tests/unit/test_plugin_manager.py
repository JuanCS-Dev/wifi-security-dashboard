"""
Unit tests for PluginManager.

Tests plugin lifecycle management, auto-discovery, and data collection.
Target: 90%+ coverage of plugin_manager.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.plugin_manager import PluginManager, register_plugin, BUILTIN_PLUGINS
from src.plugins.base import Plugin, PluginConfig, PluginStatus
from src.core.event_bus import EventBus, EventType


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def event_bus():
    """Create EventBus instance"""
    return EventBus()


@pytest.fixture
def mock_plugin_class():
    """Create mock plugin class"""
    class MockPlugin(Plugin):
        def __init__(self, config):
            super().__init__(config)
            self.init_called = False
            self.collect_called = False
            self.cleanup_called = False

        def initialize(self):
            self.init_called = True
            self._status = PluginStatus.READY

        def collect_data(self):
            self.collect_called = True
            return {"test": "data", "value": 123}

        def cleanup(self):
            self.cleanup_called = True
            self._status = PluginStatus.STOPPED

    return MockPlugin


@pytest.fixture
def plugin_configs():
    """Create list of plugin configurations"""
    return [
        PluginConfig(name="test1", enabled=True, rate_ms=1000),
        PluginConfig(name="test2", enabled=True, rate_ms=500),
    ]


# ============================================================================
# REGISTER_PLUGIN TESTS
# ============================================================================

class TestRegisterPlugin:
    """Test register_plugin function"""

    def test_register_plugin_adds_to_registry(self, mock_plugin_class):
        """Test register_plugin adds plugin to BUILTIN_PLUGINS"""
        # Clear registry first
        BUILTIN_PLUGINS.clear()

        register_plugin("custom", mock_plugin_class)

        assert "custom" in BUILTIN_PLUGINS
        assert BUILTIN_PLUGINS["custom"] == mock_plugin_class

    def test_register_plugin_duplicate_raises_error(self, mock_plugin_class):
        """Test registering duplicate plugin name raises error"""
        BUILTIN_PLUGINS.clear()

        register_plugin("duplicate", mock_plugin_class)

        with pytest.raises(ValueError, match="already registered"):
            register_plugin("duplicate", mock_plugin_class)

    def test_register_plugin_non_plugin_class_raises_error(self):
        """Test registering non-Plugin class raises error"""
        class NotAPlugin:
            pass

        with pytest.raises(ValueError, match="must inherit from Plugin"):
            register_plugin("invalid", NotAPlugin)


# ============================================================================
# PLUGIN MANAGER INITIALIZATION TESTS
# ============================================================================

class TestPluginManagerInitialization:
    """Test PluginManager initialization"""

    def test_init_stores_configs_and_event_bus(self, plugin_configs, event_bus):
        """Test __init__ stores plugin configs and event bus"""
        manager = PluginManager(plugin_configs, event_bus)

        assert manager.plugin_configs == plugin_configs
        assert manager.event_bus == event_bus

    def test_init_creates_empty_plugin_dict(self, plugin_configs, event_bus):
        """Test __init__ creates empty plugins dictionary"""
        manager = PluginManager(plugin_configs, event_bus)

        assert manager.plugins == {}

    def test_init_creates_empty_data_cache(self, plugin_configs, event_bus):
        """Test __init__ creates empty data cache"""
        manager = PluginManager(plugin_configs, event_bus)

        assert manager._data_cache == {}


# ============================================================================
# INITIALIZE_ALL TESTS
# ============================================================================

class TestInitializeAll:
    """Test initialize_all method"""

    def test_initialize_all_loads_enabled_plugins(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test initialize_all loads enabled plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)
        register_plugin("test2", mock_plugin_class)

        manager = PluginManager(plugin_configs, event_bus)
        manager.initialize_all()

        assert len(manager.plugins) == 2
        assert "test1" in manager.plugins
        assert "test2" in manager.plugins

    def test_initialize_all_calls_plugin_initialize(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test initialize_all calls initialize() on plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        plugin = manager.plugins["test1"]
        assert plugin.init_called is True

    def test_initialize_all_skips_disabled_plugins(self, event_bus, mock_plugin_class):
        """Test initialize_all skips disabled plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("disabled", mock_plugin_class)

        configs = [PluginConfig(name="disabled", enabled=False)]
        manager = PluginManager(configs, event_bus)
        manager.initialize_all()

        assert "disabled" not in manager.plugins

    def test_initialize_all_publishes_success_event(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test initialize_all publishes PLUGIN_LOADED event"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        events = event_bus.get_history(event_type=EventType.PLUGIN_LOADED, limit=100)
        assert len(events) >= 1
        plugin_events = [e for e in events if e.source == "test1"]
        assert len(plugin_events) == 1

    def test_initialize_all_handles_plugin_errors_gracefully(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test initialize_all continues on plugin initialization errors"""
        class BrokenPlugin(Plugin):
            def initialize(self):
                raise RuntimeError("Init failed!")
            def collect_data(self):
                return {}

        BUILTIN_PLUGINS.clear()
        register_plugin("broken", BrokenPlugin)
        register_plugin("good", mock_plugin_class)

        configs = [
            PluginConfig(name="broken"),
            PluginConfig(name="good"),
        ]

        manager = PluginManager(configs, event_bus)
        manager.initialize_all()

        # broken plugin should not be in plugins
        assert "broken" not in manager.plugins
        # good plugin should be loaded
        assert "good" in manager.plugins

    def test_initialize_all_publishes_error_event_on_failure(
        self, plugin_configs, event_bus
    ):
        """Test initialize_all publishes PLUGIN_ERROR on initialization failure"""
        class BrokenPlugin(Plugin):
            def initialize(self):
                raise ValueError("Bad config")
            def collect_data(self):
                return {}

        BUILTIN_PLUGINS.clear()
        register_plugin("broken", BrokenPlugin)

        manager = PluginManager([PluginConfig(name="broken")], event_bus)
        manager.initialize_all()

        errors = event_bus.get_history(event_type=EventType.PLUGIN_ERROR, limit=100)
        error_events = [e for e in errors if e.source == "broken"]
        assert len(error_events) >= 1
        assert "initialization" in error_events[0].data["stage"]


# ============================================================================
# GET_PLUGIN_DATA TESTS
# ============================================================================

class TestGetPluginData:
    """Test get_plugin_data method"""

    def test_get_plugin_data_returns_collected_data(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_plugin_data returns data from plugin"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        data = manager.get_plugin_data("test1")

        assert data == {"test": "data", "value": 123}

    def test_get_plugin_data_caches_result(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_plugin_data caches the result"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        manager.get_plugin_data("test1")

        assert "test1" in manager._data_cache
        assert manager._data_cache["test1"] == {"test": "data", "value": 123}

    def test_get_plugin_data_returns_cached_when_should_not_collect(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_plugin_data returns cached data when shouldn't collect"""
        import time

        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        # First call collects
        data1 = manager.get_plugin_data("test1")

        # Set last_collection to now (so shouldn't collect again)
        plugin = manager.plugins["test1"]
        plugin._last_collection = time.time() * 1000

        data2 = manager.get_plugin_data("test1")

        # Should return same cached data
        assert data2 == data1

    def test_get_plugin_data_returns_empty_for_unknown_plugin(
        self, plugin_configs, event_bus
    ):
        """Test get_plugin_data returns empty dict for unknown plugin"""
        manager = PluginManager([], event_bus)
        data = manager.get_plugin_data("nonexistent")

        assert data == {}

    def test_get_plugin_data_publishes_collection_event(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_plugin_data publishes PLUGIN_DATA_COLLECTED event"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        manager.get_plugin_data("test1")

        events = event_bus.get_history(
            event_type=EventType.PLUGIN_DATA_COLLECTED,
            limit=100
        )
        plugin_events = [e for e in events if e.source == "test1"]
        assert len(plugin_events) >= 1


# ============================================================================
# GET_ALL_PLUGIN_DATA TESTS
# ============================================================================

class TestGetAllPluginData:
    """Test get_all_plugin_data method"""

    def test_get_all_plugin_data_returns_all_plugins(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_all_plugin_data returns data from all plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)
        register_plugin("test2", mock_plugin_class)

        manager = PluginManager(plugin_configs, event_bus)
        manager.initialize_all()

        all_data = manager.get_all_plugin_data()

        assert "test1" in all_data
        assert "test2" in all_data
        assert all_data["test1"] == {"test": "data", "value": 123}
        assert all_data["test2"] == {"test": "data", "value": 123}

    def test_get_all_plugin_data_returns_empty_when_no_plugins(self, event_bus):
        """Test get_all_plugin_data returns empty dict when no plugins"""
        manager = PluginManager([], event_bus)
        all_data = manager.get_all_plugin_data()

        assert all_data == {}


# ============================================================================
# PLUGIN STATUS TESTS
# ============================================================================

class TestPluginStatus:
    """Test get_plugin_status methods"""

    def test_get_plugin_status_returns_status(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_plugin_status returns plugin status"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        status = manager.get_plugin_status("test1")

        assert status == PluginStatus.READY

    def test_get_plugin_status_returns_none_for_unknown(self, event_bus):
        """Test get_plugin_status returns None for unknown plugin"""
        manager = PluginManager([], event_bus)
        status = manager.get_plugin_status("nonexistent")

        assert status is None

    def test_get_all_plugin_statuses_returns_all(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test get_all_plugin_statuses returns all plugin statuses"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)
        register_plugin("test2", mock_plugin_class)

        manager = PluginManager(plugin_configs, event_bus)
        manager.initialize_all()

        statuses = manager.get_all_plugin_statuses()

        assert len(statuses) == 2
        assert statuses["test1"] == PluginStatus.READY
        assert statuses["test2"] == PluginStatus.READY


# ============================================================================
# RESET_PLUGIN_ERRORS TESTS
# ============================================================================

class TestResetPluginErrors:
    """Test reset_plugin_errors method"""

    def test_reset_plugin_errors_calls_reset_on_plugin(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test reset_plugin_errors calls reset_errors on plugin"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        plugin = manager.plugins["test1"]
        plugin._error_count = 5
        plugin._last_error = "Test error"

        manager.reset_plugin_errors("test1")

        assert plugin.error_count == 0
        assert plugin.last_error is None

    def test_reset_plugin_errors_handles_unknown_plugin(self, event_bus):
        """Test reset_plugin_errors handles unknown plugin gracefully"""
        manager = PluginManager([], event_bus)

        # Should not raise
        manager.reset_plugin_errors("nonexistent")


# ============================================================================
# CLEANUP_ALL TESTS
# ============================================================================

class TestCleanupAll:
    """Test cleanup_all method"""

    def test_cleanup_all_calls_cleanup_on_all_plugins(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test cleanup_all calls cleanup() on all plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)
        register_plugin("test2", mock_plugin_class)

        manager = PluginManager(plugin_configs, event_bus)
        manager.initialize_all()

        manager.cleanup_all()

        # Plugins should be removed from manager
        assert len(manager.plugins) == 0

    def test_cleanup_all_publishes_stopped_events(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test cleanup_all publishes PLUGIN_STOPPED events"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        manager.cleanup_all()

        events = event_bus.get_history(event_type=EventType.PLUGIN_STOPPED, limit=100)
        stopped_events = [e for e in events if e.source == "test1"]
        assert len(stopped_events) >= 1

    def test_cleanup_all_handles_cleanup_errors(
        self, plugin_configs, event_bus
    ):
        """Test cleanup_all handles cleanup errors gracefully"""
        class BrokenCleanupPlugin(Plugin):
            def initialize(self):
                self._status = PluginStatus.READY

            def collect_data(self):
                return {}

            def cleanup(self):
                raise RuntimeError("Cleanup failed!")

        BUILTIN_PLUGINS.clear()
        register_plugin("broken", BrokenCleanupPlugin)

        manager = PluginManager([PluginConfig(name="broken")], event_bus)
        manager.initialize_all()

        # Should not raise
        manager.cleanup_all()

        # Should publish error event
        errors = event_bus.get_history(event_type=EventType.PLUGIN_ERROR, limit=100)
        cleanup_errors = [
            e for e in errors
            if e.source == "broken" and e.data.get("stage") == "cleanup"
        ]
        assert len(cleanup_errors) >= 1

    def test_cleanup_all_clears_data_cache(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test cleanup_all clears data cache"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        manager.get_plugin_data("test1")  # Populate cache

        manager.cleanup_all()

        assert manager._data_cache == {}


# ============================================================================
# GET_PLUGIN_CLASS TESTS
# ============================================================================

class TestGetPluginClass:
    """Test _get_plugin_class method"""

    def test_get_plugin_class_returns_builtin(self, event_bus, mock_plugin_class):
        """Test _get_plugin_class returns builtin plugin"""
        BUILTIN_PLUGINS.clear()
        register_plugin("builtin", mock_plugin_class)

        manager = PluginManager([], event_bus)
        plugin_class = manager._get_plugin_class("builtin")

        assert plugin_class == mock_plugin_class

    def test_get_plugin_class_raises_for_unknown(self, event_bus):
        """Test _get_plugin_class raises ValueError for unknown plugin"""
        BUILTIN_PLUGINS.clear()

        manager = PluginManager([], event_bus)

        with pytest.raises(ValueError, match="not found"):
            manager._get_plugin_class("nonexistent")

    def test_get_plugin_class_dynamic_import_success(self, event_bus):
        """Test _get_plugin_class dynamically imports plugin when not builtin"""
        # Clear builtin registry to force dynamic import
        BUILTIN_PLUGINS.clear()

        manager = PluginManager([], event_bus)

        # Should dynamically import src.plugins.system_plugin.SystemPlugin
        plugin_class = manager._get_plugin_class("system")

        assert plugin_class.__name__ == "SystemPlugin"
        assert issubclass(plugin_class, Plugin)

    def test_get_plugin_class_validates_plugin_inheritance(self, event_bus):
        """Test _get_plugin_class validates plugin inherits from Plugin"""
        BUILTIN_PLUGINS.clear()

        manager = PluginManager([], event_bus)

        # Mock a module that has a class but doesn't inherit from Plugin
        with patch('importlib.import_module') as mock_import:
            # Create a fake class that doesn't inherit from Plugin
            class FakePlugin:
                pass

            fake_module = Mock()
            fake_module.FakePlugin = FakePlugin
            mock_import.return_value = fake_module

            with pytest.raises(ValueError, match="must inherit from Plugin"):
                manager._get_plugin_class("fake")


# ============================================================================
# REPR TESTS
# ============================================================================

class TestPluginManagerRepr:
    """Test PluginManager __repr__"""

    def test_repr_includes_plugin_count(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test repr includes number of plugins"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)
        register_plugin("test2", mock_plugin_class)

        manager = PluginManager(plugin_configs, event_bus)
        manager.initialize_all()

        repr_str = repr(manager)

        assert "plugins=2" in repr_str

    def test_repr_includes_plugin_names(
        self, plugin_configs, event_bus, mock_plugin_class
    ):
        """Test repr includes loaded plugin names"""
        BUILTIN_PLUGINS.clear()
        register_plugin("test1", mock_plugin_class)

        manager = PluginManager(plugin_configs[:1], event_bus)
        manager.initialize_all()

        repr_str = repr(manager)

        assert "test1" in repr_str
