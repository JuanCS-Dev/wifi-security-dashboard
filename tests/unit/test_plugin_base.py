"""
Unit tests for Plugin base class.

Tests the abstract Plugin class and PluginConfig dataclass.
Target: 90%+ coverage of base.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, patch
import time

from src.plugins.base import Plugin, PluginConfig, PluginStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def basic_config():
    """Create basic plugin configuration"""
    return PluginConfig(
        name="test_plugin",
        enabled=True,
        rate_ms=1000,
        config={"test_option": "value"}
    )


@pytest.fixture
def concrete_plugin(basic_config):
    """Create concrete plugin implementation for testing"""
    class TestPlugin(Plugin):
        def initialize(self):
            self._status = PluginStatus.READY
            self.initialized = True

        def collect_data(self):
            return {"value": 42, "status": "ok"}

        def cleanup(self):
            self.cleaned_up = True

    return TestPlugin(basic_config)


@pytest.fixture
def failing_plugin(basic_config):
    """Create plugin that can fail on demand (for auto-recovery tests)"""
    class FailingPlugin(Plugin):
        def __init__(self, config):
            super().__init__(config)
            self.fail_next = False

        def initialize(self):
            self._status = PluginStatus.READY

        def should_collect(self):
            # Override to always collect (ignore rate limiting for tests)
            return True

        def collect_data(self):
            if self.fail_next:
                raise RuntimeError("Simulated collection error")
            return {"value": 42, "status": "ok"}

        def cleanup(self):
            pass

    return FailingPlugin(basic_config)


# ============================================================================
# PLUGIN CONFIG TESTS
# ============================================================================

class TestPluginConfig:
    """Test PluginConfig dataclass"""

    def test_valid_config(self):
        """Test creating valid plugin config"""
        config = PluginConfig(
            name="test",
            enabled=True,
            rate_ms=500,
            config={"key": "value"}
        )
        assert config.name == "test"
        assert config.enabled is True
        assert config.rate_ms == 500
        assert config.config == {"key": "value"}

    def test_default_values(self):
        """Test config defaults"""
        config = PluginConfig(name="test")
        assert config.enabled is True
        assert config.rate_ms == 1000
        assert config.config == {}

    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="Plugin name cannot be empty"):
            PluginConfig(name="")

    def test_negative_rate_ms_raises_error(self):
        """Test that negative rate_ms raises ValueError"""
        with pytest.raises(ValueError, match="rate_ms must be >= 0"):
            PluginConfig(name="test", rate_ms=-100)

    def test_zero_rate_ms_allowed(self):
        """Test that rate_ms=0 is allowed (static plugin)"""
        config = PluginConfig(name="test", rate_ms=0)
        assert config.rate_ms == 0


# ============================================================================
# PLUGIN INITIALIZATION TESTS
# ============================================================================

class TestPluginInitialization:
    """Test Plugin initialization"""

    def test_plugin_init_sets_config(self, basic_config):
        """Test that __init__ sets config"""
        class TestPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {}

        plugin = TestPlugin(basic_config)
        assert plugin.config == basic_config

    def test_plugin_init_sets_uninitialized_status(self, basic_config):
        """Test that __init__ sets UNINITIALIZED status"""
        class TestPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {}

        plugin = TestPlugin(basic_config)
        assert plugin.status == PluginStatus.UNINITIALIZED

    def test_plugin_init_zeros_error_count(self, basic_config):
        """Test that __init__ zeros error tracking"""
        class TestPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {}

        plugin = TestPlugin(basic_config)
        assert plugin.error_count == 0
        assert plugin.last_error is None


# ============================================================================
# PLUGIN PROPERTIES TESTS
# ============================================================================

class TestPluginProperties:
    """Test Plugin properties"""

    def test_name_property(self, concrete_plugin):
        """Test name property returns config name"""
        assert concrete_plugin.name == "test_plugin"

    def test_status_property(self, concrete_plugin):
        """Test status property"""
        assert concrete_plugin.status == PluginStatus.UNINITIALIZED
        concrete_plugin.initialize()
        assert concrete_plugin.status == PluginStatus.READY

    def test_error_count_property(self, concrete_plugin):
        """Test error_count property"""
        assert concrete_plugin.error_count == 0
        concrete_plugin._error_count = 5
        assert concrete_plugin.error_count == 5

    def test_last_error_property(self, concrete_plugin):
        """Test last_error property"""
        assert concrete_plugin.last_error is None
        concrete_plugin._last_error = "Test error"
        assert concrete_plugin.last_error == "Test error"


# ============================================================================
# SHOULD_COLLECT TESTS
# ============================================================================

class TestShouldCollect:
    """Test should_collect rate-based logic"""

    def test_should_collect_initially_true(self, concrete_plugin):
        """Test should_collect returns True initially"""
        assert concrete_plugin.should_collect() is True

    def test_should_collect_false_after_recent_collection(self, concrete_plugin):
        """Test should_collect returns False after recent collection"""
        # Simulate collection
        concrete_plugin._last_collection = time.time() * 1000

        # Should not collect immediately after
        assert concrete_plugin.should_collect() is False

    def test_should_collect_true_after_rate_ms_elapsed(self, concrete_plugin):
        """Test should_collect returns True after rate_ms elapsed"""
        # Simulate old collection
        concrete_plugin._last_collection = (time.time() - 2) * 1000  # 2 seconds ago
        concrete_plugin.config.rate_ms = 1000  # 1 second rate

        # Should collect (2 seconds > 1 second)
        assert concrete_plugin.should_collect() is True

    def test_should_collect_static_plugin_once(self, basic_config):
        """Test static plugin (rate_ms=0) collects only once"""
        basic_config.rate_ms = 0

        class StaticPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {"static": "data"}

        plugin = StaticPlugin(basic_config)

        # First call should collect
        assert plugin.should_collect() is True

        # Simulate collection
        plugin._last_collection = time.time() * 1000

        # Second call should not collect
        assert plugin.should_collect() is False


# ============================================================================
# COLLECT_SAFE TESTS
# ============================================================================

class TestCollectSafe:
    """Test collect_safe wrapper method"""

    def test_collect_safe_returns_data_when_enabled(self, concrete_plugin):
        """Test collect_safe returns data when plugin enabled"""
        concrete_plugin.initialize()
        data = concrete_plugin.collect_safe()

        assert data == {"value": 42, "status": "ok"}
        assert concrete_plugin.status == PluginStatus.RUNNING

    def test_collect_safe_returns_empty_when_disabled(self, concrete_plugin):
        """Test collect_safe returns empty dict when disabled"""
        concrete_plugin.config.enabled = False
        data = concrete_plugin.collect_safe()

        assert data == {}

    def test_collect_safe_returns_empty_when_should_not_collect(self, concrete_plugin):
        """Test collect_safe returns empty when should_collect=False"""
        # Simulate recent collection
        concrete_plugin._last_collection = time.time() * 1000

        data = concrete_plugin.collect_safe()
        assert data == {}

    def test_collect_safe_handles_exceptions_gracefully(self, basic_config):
        """Test collect_safe catches exceptions and returns empty dict"""
        class BrokenPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                raise RuntimeError("Collection failed!")

        plugin = BrokenPlugin(basic_config)
        data = plugin.collect_safe()

        assert data == {}
        assert plugin.status == PluginStatus.ERROR
        assert plugin.error_count == 1
        assert "Collection failed!" in plugin.last_error

    def test_collect_safe_increments_error_count(self, basic_config):
        """Test collect_safe increments error count on failures"""
        class BrokenPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                raise ValueError("Bad data")

        plugin = BrokenPlugin(basic_config)

        # Multiple failures
        plugin.collect_safe()
        plugin.collect_safe()
        plugin.collect_safe()

        assert plugin.error_count == 3

    def test_collect_safe_updates_last_collection_timestamp(self, concrete_plugin):
        """Test collect_safe updates _last_collection timestamp"""
        before = concrete_plugin._last_collection
        concrete_plugin.initialize()
        concrete_plugin.collect_safe()
        after = concrete_plugin._last_collection

        assert after > before

    def test_collect_safe_clears_last_error_on_success(self, basic_config):
        """Test collect_safe clears last_error after successful collection"""
        class RecoveringPlugin(Plugin):
            def __init__(self, config):
                super().__init__(config)
                self.fail_once = True

            def initialize(self):
                pass

            def collect_data(self):
                if self.fail_once:
                    self.fail_once = False
                    raise ValueError("First failure")
                return {"recovered": True}

        plugin = RecoveringPlugin(basic_config)

        # First call fails
        plugin.collect_safe()
        assert plugin.last_error is not None

        # Second call succeeds
        plugin.collect_safe()
        assert plugin.last_error is None


# ============================================================================
# RESET_ERRORS TESTS
# ============================================================================

class TestResetErrors:
    """Test reset_errors method"""

    def test_reset_errors_clears_count(self, concrete_plugin):
        """Test reset_errors clears error count"""
        concrete_plugin._error_count = 10
        concrete_plugin.reset_errors()

        assert concrete_plugin.error_count == 0

    def test_reset_errors_clears_last_error(self, concrete_plugin):
        """Test reset_errors clears last error message"""
        concrete_plugin._last_error = "Previous error"
        concrete_plugin.reset_errors()

        assert concrete_plugin.last_error is None

    def test_reset_errors_changes_status_from_error_to_ready(self, concrete_plugin):
        """Test reset_errors changes ERROR status to READY"""
        concrete_plugin._status = PluginStatus.ERROR
        concrete_plugin.reset_errors()

        assert concrete_plugin.status == PluginStatus.READY

    def test_reset_errors_preserves_other_statuses(self, concrete_plugin):
        """Test reset_errors doesn't change non-ERROR statuses"""
        concrete_plugin._status = PluginStatus.RUNNING
        concrete_plugin.reset_errors()

        assert concrete_plugin.status == PluginStatus.RUNNING


# ============================================================================
# CLEANUP TESTS
# ============================================================================

class TestCleanup:
    """Test cleanup method"""

    def test_cleanup_is_template_method(self, basic_config):
        """Test cleanup base implementation is empty (Template Method)"""
        class MinimalPlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {}
            # cleanup not overridden - uses base template

        plugin = MinimalPlugin(basic_config)
        # Should not raise (base implementation is pass)
        plugin.cleanup()

    def test_cleanup_can_be_overridden(self, concrete_plugin):
        """Test cleanup can be overridden by subclasses"""
        concrete_plugin.cleanup()
        assert concrete_plugin.cleaned_up is True


# ============================================================================
# REPR TESTS
# ============================================================================

class TestPluginRepr:
    """Test Plugin __repr__"""

    def test_repr_includes_class_name(self, concrete_plugin):
        """Test repr includes class name"""
        repr_str = repr(concrete_plugin)
        assert "TestPlugin" in repr_str

    def test_repr_includes_name(self, concrete_plugin):
        """Test repr includes plugin name"""
        repr_str = repr(concrete_plugin)
        assert "test_plugin" in repr_str

    def test_repr_includes_status(self, concrete_plugin):
        """Test repr includes status"""
        repr_str = repr(concrete_plugin)
        assert "uninitialized" in repr_str

    def test_repr_includes_rate_ms(self, concrete_plugin):
        """Test repr includes rate_ms"""
        repr_str = repr(concrete_plugin)
        assert "1000" in repr_str


# ============================================================================
# ABSTRACT METHOD TESTS
# ============================================================================

class TestAbstractMethods:
    """Test abstract method enforcement"""

    def test_cannot_instantiate_without_initialize(self, basic_config):
        """Test cannot instantiate plugin without initialize()"""
        class IncompletePlugin(Plugin):
            def collect_data(self):
                return {}
            # Missing initialize()

        with pytest.raises(TypeError):
            IncompletePlugin(basic_config)

    def test_cannot_instantiate_without_collect_data(self, basic_config):
        """Test cannot instantiate plugin without collect_data()"""
        class IncompletePlugin(Plugin):
            def initialize(self):
                pass
            # Missing collect_data()

        with pytest.raises(TypeError):
            IncompletePlugin(basic_config)

    def test_can_instantiate_with_all_abstract_methods(self, basic_config):
        """Test can instantiate with all abstract methods implemented"""
        class CompletePlugin(Plugin):
            def initialize(self):
                pass
            def collect_data(self):
                return {}

        # Should not raise
        plugin = CompletePlugin(basic_config)
        assert plugin is not None


# ============================================================================
# AUTO-RECOVERY TESTS (Gap #5)
# ============================================================================

class TestAutoRecovery:
    """Test plugin auto-recovery from ERROR state"""

    def test_consecutive_errors_increment_on_failure(self, failing_plugin):
        """Test consecutive errors increment on each failure"""
        plugin = failing_plugin
        plugin.initialize()

        # Make collect_data() fail
        plugin.fail_next = True

        # First failure
        plugin.collect_safe()
        assert plugin.error_count == 1
        assert plugin.consecutive_errors == 1
        assert plugin.status == PluginStatus.ERROR

        # Second failure
        plugin.collect_safe()
        assert plugin.error_count == 2
        assert plugin.consecutive_errors == 2

        # Third failure
        plugin.collect_safe()
        assert plugin.error_count == 3
        assert plugin.consecutive_errors == 3

    def test_consecutive_errors_reset_on_success(self, failing_plugin):
        """Test consecutive errors reset to 0 on successful collection"""
        plugin = failing_plugin
        plugin.initialize()

        # Fail 3 times
        plugin.fail_next = True
        plugin.collect_safe()
        plugin.collect_safe()
        plugin.collect_safe()

        assert plugin.error_count == 3
        assert plugin.consecutive_errors == 3
        assert plugin.status == PluginStatus.ERROR

        # Success - should reset consecutive errors but not total errors
        plugin.fail_next = False
        plugin.collect_safe()

        assert plugin.error_count == 3  # Total errors unchanged
        assert plugin.consecutive_errors == 0  # Consecutive errors reset
        assert plugin.status == PluginStatus.RUNNING  # Auto-recovery!

    def test_auto_recovery_error_to_running(self, failing_plugin):
        """Test plugin auto-recovers from ERROR to RUNNING on success"""
        plugin = failing_plugin
        plugin.initialize()

        # Force plugin into ERROR state
        plugin.fail_next = True
        plugin.collect_safe()
        assert plugin.status == PluginStatus.ERROR

        # Successful collection should auto-recover
        plugin.fail_next = False
        plugin.collect_safe()

        assert plugin.status == PluginStatus.RUNNING
        assert plugin.last_error is None
        assert plugin.consecutive_errors == 0

    def test_multiple_error_recovery_cycles(self, failing_plugin):
        """Test plugin handles multiple error/recovery cycles"""
        plugin = failing_plugin
        plugin.initialize()

        # Cycle 1: Error → Recovery
        plugin.fail_next = True
        plugin.collect_safe()
        plugin.collect_safe()
        assert plugin.error_count == 2
        assert plugin.consecutive_errors == 2

        plugin.fail_next = False
        plugin.collect_safe()
        assert plugin.consecutive_errors == 0
        assert plugin.status == PluginStatus.RUNNING

        # Cycle 2: Error → Recovery
        plugin.fail_next = True
        plugin.collect_safe()
        assert plugin.error_count == 3  # Total continues incrementing
        assert plugin.consecutive_errors == 1  # Reset from previous cycle

        plugin.fail_next = False
        plugin.collect_safe()
        assert plugin.consecutive_errors == 0
        assert plugin.status == PluginStatus.RUNNING

    def test_reset_errors_clears_consecutive_errors(self, failing_plugin):
        """Test reset_errors() clears both total and consecutive errors"""
        plugin = failing_plugin
        plugin.initialize()

        # Generate some errors
        plugin.fail_next = True
        plugin.collect_safe()
        plugin.collect_safe()
        plugin.collect_safe()

        assert plugin.error_count == 3
        assert plugin.consecutive_errors == 3
        assert plugin.status == PluginStatus.ERROR

        # Manual reset
        plugin.reset_errors()

        assert plugin.error_count == 0
        assert plugin.consecutive_errors == 0
        assert plugin.last_error is None
        assert plugin.status == PluginStatus.READY

    def test_consecutive_errors_property(self, failing_plugin):
        """Test consecutive_errors property is exposed"""
        plugin = failing_plugin
        plugin.initialize()

        # Initial state
        assert plugin.consecutive_errors == 0

        # After error
        plugin.fail_next = True
        plugin.collect_safe()
        assert plugin.consecutive_errors == 1

        # After success
        plugin.fail_next = False
        plugin.collect_safe()
        assert plugin.consecutive_errors == 0


# ============================================================================
# PLUGIN STATUS ENUM TESTS
# ============================================================================

class TestPluginStatus:
    """Test PluginStatus enum"""

    def test_status_values_are_strings(self):
        """Test all status values are strings"""
        assert PluginStatus.UNINITIALIZED.value == "uninitialized"
        assert PluginStatus.READY.value == "ready"
        assert PluginStatus.RUNNING.value == "running"
        assert PluginStatus.ERROR.value == "error"
        assert PluginStatus.STOPPED.value == "stopped"

    def test_all_statuses_exist(self):
        """Test all expected statuses exist"""
        expected = ["UNINITIALIZED", "READY", "RUNNING", "ERROR", "STOPPED"]
        actual = [status.name for status in PluginStatus]
        assert set(actual) == set(expected)
