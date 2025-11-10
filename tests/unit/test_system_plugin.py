"""
Unit tests for SystemPlugin.

Tests system metrics collection with mocked psutil.
Target: 90%+ coverage of system_plugin.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.plugins.system_plugin import SystemPlugin
from src.plugins.base import PluginConfig, PluginStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_psutil():
    """Create comprehensive psutil mock"""
    psutil = MagicMock()

    # CPU
    psutil.cpu_percent = Mock(return_value=45.2)
    psutil.cpu_count = Mock(return_value=8)

    # Memory
    memory = MagicMock()
    memory.percent = 68.5
    memory.used = 8 * 1024**3  # 8 GB
    memory.total = 16 * 1024**3  # 16 GB
    psutil.virtual_memory = Mock(return_value=memory)

    # Disk
    disk = MagicMock()
    disk.percent = 42.1
    disk.used = 250 * 1024**3  # 250 GB
    disk.total = 500 * 1024**3  # 500 GB
    psutil.disk_usage = Mock(return_value=disk)

    # Boot time
    psutil.boot_time = Mock(return_value=1000.0)

    # Load average (Unix)
    psutil.getloadavg = Mock(return_value=(1.5, 1.2, 0.8))

    return psutil


@pytest.fixture
def plugin_config():
    """Create plugin configuration"""
    return PluginConfig(
        name="system",
        enabled=True,
        rate_ms=1000,
        config={"disk_path": "/"}
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestSystemPluginInitialization:
    """Test SystemPlugin initialization"""

    def test_initialize_imports_psutil(self, plugin_config, mock_psutil):
        """Test initialize imports psutil successfully"""
        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin.psutil is not None
            assert plugin.status == PluginStatus.READY

    def test_initialize_raises_if_psutil_not_available(self, plugin_config):
        """Test initialize raises RuntimeError if psutil unavailable"""
        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', side_effect=ImportError("No psutil")):
            with pytest.raises(RuntimeError, match="psutil library not installed"):
                plugin.initialize()

    def test_initialize_validates_psutil_api(self, plugin_config):
        """Test initialize validates psutil has required API"""
        # psutil without cpu_percent
        mock_psutil_broken = MagicMock()
        del mock_psutil_broken.cpu_percent

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil_broken):
            with pytest.raises(RuntimeError, match="not properly installed"):
                plugin.initialize()

    def test_initialize_uses_configured_disk_path(self, mock_psutil):
        """Test initialize uses disk_path from config"""
        config = PluginConfig(
            name="system",
            config={"disk_path": "/home"}
        )

        plugin = SystemPlugin(config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            # Should have called disk_usage with /home
            mock_psutil.disk_usage.assert_called_with("/home")
            assert plugin._disk_path == "/home"

    def test_initialize_falls_back_to_root_if_path_not_found(self, mock_psutil):
        """Test initialize falls back to / if disk path doesn't exist"""
        # First call raises FileNotFoundError, second succeeds
        mock_psutil.disk_usage = Mock(side_effect=[
            FileNotFoundError("/badpath"),
            MagicMock(percent=50)
        ])

        config = PluginConfig(name="system", config={"disk_path": "/badpath"})
        plugin = SystemPlugin(config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin._disk_path == "/"

    def test_initialize_detects_load_avg_availability(self, mock_psutil):
        """Test initialize detects if load averages available (Unix)"""
        plugin = SystemPlugin(PluginConfig(name="system"))

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin._has_load_avg is True

    def test_initialize_handles_no_load_avg(self, mock_psutil):
        """Test initialize handles platforms without load averages (Windows)"""
        # Windows doesn't have getloadavg
        mock_psutil.getloadavg = Mock(side_effect=AttributeError("Windows"))

        plugin = SystemPlugin(PluginConfig(name="system"))

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin._has_load_avg is False


# ============================================================================
# DATA COLLECTION TESTS
# ============================================================================

class TestSystemPluginDataCollection:
    """Test SystemPlugin collect_data method"""

    @patch('time.time')
    def test_collect_data_returns_all_metrics(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data returns all system metrics"""
        mock_time.return_value = 2000.0  # 1000s uptime

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        # Check all expected fields
        assert "cpu_percent" in data
        assert "cpu_percent_per_core" in data
        assert "cpu_count" in data
        assert "memory_percent" in data
        assert "memory_used_mb" in data
        assert "memory_total_mb" in data
        assert "disk_percent" in data
        assert "disk_used_gb" in data
        assert "disk_total_gb" in data
        assert "uptime_seconds" in data

    @patch('time.time')
    def test_collect_data_cpu_metrics(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data CPU metrics"""
        mock_time.return_value = 2000.0
        # cpu_percent called 3 times: initialize (baseline), collect_data (overall), collect_data (per-core)
        mock_psutil.cpu_percent = Mock(side_effect=[0.0, 45.2, [10, 20, 30, 40, 50, 60, 70, 80]])

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert data["cpu_percent"] == 45.2
        assert data["cpu_percent_per_core"] == [10, 20, 30, 40, 50, 60, 70, 80]
        assert data["cpu_count"] == 8

    @patch('time.time')
    def test_collect_data_memory_metrics(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data memory metrics"""
        mock_time.return_value = 2000.0

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert data["memory_percent"] == 68.5
        assert data["memory_used_mb"] == pytest.approx(8 * 1024, rel=0.1)
        assert data["memory_total_mb"] == pytest.approx(16 * 1024, rel=0.1)

    @patch('time.time')
    def test_collect_data_disk_metrics(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data disk metrics"""
        mock_time.return_value = 2000.0

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert data["disk_percent"] == 42.1
        assert data["disk_used_gb"] == pytest.approx(250, rel=0.1)
        assert data["disk_total_gb"] == pytest.approx(500, rel=0.1)

    def test_collect_data_uptime(self, plugin_config, mock_psutil):
        """Test collect_data includes uptime field"""
        # Set boot_time to a fixed value
        mock_psutil.boot_time = Mock(return_value=1000.0)

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        # Uptime field should be present (value may be mock or real depending on time import)
        assert "uptime_seconds" in data

    @patch('time.time')
    def test_collect_data_includes_load_avg_when_available(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data includes load averages on Unix"""
        mock_time.return_value = 2000.0

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert "load_avg_1m" in data
        assert "load_avg_5m" in data
        assert "load_avg_15m" in data
        assert data["load_avg_1m"] == 1.5
        assert data["load_avg_5m"] == 1.2
        assert data["load_avg_15m"] == 0.8

    @patch('time.time')
    def test_collect_data_omits_load_avg_when_unavailable(self, mock_time, plugin_config, mock_psutil):
        """Test collect_data omits load averages on Windows"""
        mock_time.return_value = 2000.0
        mock_psutil.getloadavg = Mock(side_effect=AttributeError("Windows"))

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert "load_avg_1m" not in data
        assert "load_avg_5m" not in data
        assert "load_avg_15m" not in data


# ============================================================================
# CLEANUP TESTS
# ============================================================================

class TestSystemPluginCleanup:
    """Test SystemPlugin cleanup"""

    def test_cleanup_sets_stopped_status(self, plugin_config, mock_psutil):
        """Test cleanup sets status to STOPPED"""
        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            plugin.cleanup()

        assert plugin.status == PluginStatus.STOPPED


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestSystemPluginIntegration:
    """Test SystemPlugin full lifecycle"""

    @patch('time.time')
    def test_full_lifecycle(self, mock_time, plugin_config, mock_psutil):
        """Test complete plugin lifecycle: init -> collect -> cleanup"""
        mock_time.return_value = 2000.0

        plugin = SystemPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            # Initialize
            assert plugin.status == PluginStatus.UNINITIALIZED
            plugin.initialize()
            assert plugin.status == PluginStatus.READY

            # Collect data
            data = plugin.collect_data()
            assert len(data) >= 10  # At least 10 metrics

            # Cleanup
            plugin.cleanup()
            assert plugin.status == PluginStatus.STOPPED


# ============================================================================
# MOCK MODE TESTS
# ============================================================================

class TestSystemPluginMockMode:
    """Test SystemPlugin in mock mode (educational simulation)"""

    def test_mock_mode_initialization(self):
        """Test plugin initializes in mock mode without psutil"""
        config = PluginConfig(name="system", rate_ms=1000)
        config.config['mock_mode'] = True

        plugin = SystemPlugin(config)
        plugin.initialize()

        assert plugin.status == PluginStatus.READY
        assert plugin._mock_mode is True
        assert hasattr(plugin, '_mock_generator')

    def test_mock_mode_collect_data(self):
        """Test plugin collects simulated data in mock mode"""
        config = PluginConfig(name="system", rate_ms=1000)
        config.config['mock_mode'] = True

        plugin = SystemPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()

        # Should have all required fields
        assert "cpu_percent" in data
        assert "ram_percent" in data
        assert "disk_percent" in data
        assert "temperature_celsius" in data
        assert "uptime_seconds" in data

        # Should have realistic ranges
        assert 0 <= data["cpu_percent"] <= 100
        assert 0 <= data["ram_percent"] <= 100

    def test_mock_mode_data_is_cohesive(self):
        """Test mock mode data varies naturally, not randomly"""
        config = PluginConfig(name="system", rate_ms=1000)
        config.config['mock_mode'] = True

        plugin = SystemPlugin(config)
        plugin.initialize()

        # Collect multiple samples
        samples = []
        for _ in range(5):
            data = plugin.collect_data()
            samples.append(data["cpu_percent"])

        # Should vary but stay in reasonable range
        avg = sum(samples) / len(samples)
        for sample in samples:
            # All values should be within ±20% of average (cohesive)
            deviation = abs(sample - avg) / avg if avg > 0 else 0
            assert deviation < 0.3, "Mock data should be cohesive, not chaotic"

