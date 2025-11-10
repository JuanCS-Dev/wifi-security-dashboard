"""
Unit tests for NetworkPlugin.

Tests network metrics collection with mocked psutil.
Target: 90%+ coverage of network_plugin.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import time

from src.plugins.network_plugin import NetworkPlugin
from src.plugins.base import PluginConfig, PluginStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_psutil():
    """Create comprehensive psutil mock for network"""
    psutil = MagicMock()

    # Network I/O counters
    counters = MagicMock()
    counters.bytes_sent = 1000000  # 1 MB
    counters.bytes_recv = 2000000  # 2 MB
    counters.packets_sent = 5000
    counters.packets_recv = 6000
    counters.errin = 10
    counters.errout = 5
    counters.dropin = 2
    counters.dropout = 1

    psutil.net_io_counters = Mock(return_value=counters)

    # Network connections
    conn1 = MagicMock()
    conn1.status = 'ESTABLISHED'

    conn2 = MagicMock()
    conn2.status = 'TIME_WAIT'

    conn3 = MagicMock()
    conn3.status = 'ESTABLISHED'

    psutil.net_connections = Mock(return_value=[conn1, conn2, conn3])

    return psutil


@pytest.fixture
def plugin_config():
    """Create plugin configuration"""
    return PluginConfig(
        name="network",
        enabled=True,
        rate_ms=1000,
        config={}
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestNetworkPluginInitialization:
    """Test NetworkPlugin initialization"""

    @patch('time.time')
    def test_initialize_imports_psutil(self, mock_time_func, plugin_config, mock_psutil):
        """Test initialize imports psutil successfully"""
        mock_time_func.return_value = 1000.0

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin.psutil is not None
            assert plugin.status == PluginStatus.READY

    def test_initialize_raises_if_psutil_not_available(self, plugin_config):
        """Test initialize raises RuntimeError if psutil unavailable"""
        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', side_effect=ImportError("No psutil")):
            with pytest.raises(RuntimeError, match="psutil library not installed"):
                plugin.initialize()

    def test_initialize_validates_psutil_api(self, plugin_config):
        """Test initialize validates psutil has net_io_counters"""
        mock_psutil_broken = MagicMock()
        del mock_psutil_broken.net_io_counters

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil_broken):
            with pytest.raises(RuntimeError, match="net_io_counters not available"):
                plugin.initialize()

    @patch('time.time')
    def test_initialize_sets_baseline_counters(self, mock_time_func, plugin_config, mock_psutil):
        """Test initialize sets baseline counters for bandwidth calc"""
        mock_time_func.return_value = 1000.0

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin._last_bytes_sent == 1000000
            assert plugin._last_bytes_recv == 2000000
            assert plugin._last_time == 1000.0

    @patch('time.time')
    def test_initialize_handles_interface_config(self, mock_time_func, mock_psutil):
        """Test initialize handles interface configuration"""
        mock_time_func.return_value = 1000.0

        config = PluginConfig(
            name="network",
            config={"interface": "eth0"}
        )

        plugin = NetworkPlugin(config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            assert plugin._interface == "eth0"

    @patch('time.time')
    def test_initialize_handles_counter_error(self, mock_time_func, plugin_config):
        """Test initialize raises on counter collection error"""
        mock_time_func.return_value = 1000.0
        mock_psutil_broken = MagicMock()
        mock_psutil_broken.net_io_counters = Mock(side_effect=RuntimeError("No network"))

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil_broken):
            with pytest.raises(RuntimeError, match="Failed to get network counters"):
                plugin.initialize()


# ============================================================================
# DATA COLLECTION TESTS
# ============================================================================

class TestNetworkPluginDataCollection:
    """Test NetworkPlugin collect_data method"""

    @patch('time.time')
    def test_collect_data_returns_all_metrics(self, mock_time_func, plugin_config, mock_psutil):
        """Test collect_data returns all network metrics"""
        mock_time_func.side_effect = [1000.0, 1001.0]  # 1 second elapsed

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        # Check all expected fields
        assert "bandwidth_tx_mbps" in data
        assert "bandwidth_rx_mbps" in data
        assert "bytes_sent" in data
        assert "bytes_recv" in data
        assert "packets_sent" in data
        assert "packets_recv" in data
        assert "connections_established" in data
        assert "connections_total" in data
        assert "errors_in" in data
        assert "errors_out" in data
        assert "drops_in" in data
        assert "drops_out" in data

    @patch('time.time')
    def test_collect_data_calculates_bandwidth(self, mock_time_func, plugin_config):
        """Test collect_data calculates bandwidth correctly"""
        # Time: 1000.0 -> 1001.0 (1 second elapsed)
        mock_time_func.side_effect = [1000.0, 1001.0]

        # Initial counters: 1MB sent, 2MB recv
        initial_counters = MagicMock()
        initial_counters.bytes_sent = 1_000_000
        initial_counters.bytes_recv = 2_000_000
        initial_counters.packets_sent = 5000
        initial_counters.packets_recv = 6000
        initial_counters.errin = 10
        initial_counters.errout = 5
        initial_counters.dropin = 2
        initial_counters.dropout = 1

        # After 1 second: +125KB sent, +250KB recv
        new_counters = MagicMock()
        new_counters.bytes_sent = 1_125_000  # +125,000 bytes
        new_counters.bytes_recv = 2_250_000  # +250,000 bytes
        new_counters.packets_sent = 5100
        new_counters.packets_recv = 6200
        new_counters.errin = 10
        new_counters.errout = 5
        new_counters.dropin = 2
        new_counters.dropout = 1

        mock_psutil = MagicMock()
        mock_psutil.net_io_counters = Mock(side_effect=[initial_counters, new_counters])
        mock_psutil.net_connections = Mock(return_value=[])

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        # Bandwidth calculation:
        # bytes_delta * 8 / (time_delta * 1_000_000) = Mbps
        # TX: 125,000 * 8 / (1 * 1_000_000) = 1.0 Mbps
        # RX: 250,000 * 8 / (1 * 1_000_000) = 2.0 Mbps
        assert data["bandwidth_tx_mbps"] == pytest.approx(1.0, rel=0.01)
        assert data["bandwidth_rx_mbps"] == pytest.approx(2.0, rel=0.01)

    @patch('time.time')
    def test_collect_data_handles_zero_time_delta(self, mock_time_func, plugin_config, mock_psutil):
        """Test collect_data handles rapid calls (zero time delta)"""
        # Same time = zero delta
        mock_time_func.side_effect = [1000.0, 1000.0]

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        # Zero time delta = 0 Mbps
        assert data["bandwidth_tx_mbps"] == 0.0
        assert data["bandwidth_rx_mbps"] == 0.0

    @patch('time.time')
    def test_collect_data_counts_connections(self, mock_time_func, plugin_config):
        """Test collect_data counts ESTABLISHED vs total connections"""
        mock_time_func.side_effect = [1000.0, 1001.0]

        # Create connections with different statuses
        conns = [
            MagicMock(status='ESTABLISHED'),
            MagicMock(status='ESTABLISHED'),
            MagicMock(status='TIME_WAIT'),
            MagicMock(status='CLOSE_WAIT'),
            MagicMock(status='ESTABLISHED'),
        ]

        mock_psutil = MagicMock()
        mock_psutil.net_io_counters = Mock(return_value=MagicMock(
            bytes_sent=1000000,
            bytes_recv=2000000,
            packets_sent=5000,
            packets_recv=6000,
            errin=10,
            errout=5,
            dropin=2,
            dropout=1
        ))
        mock_psutil.net_connections = Mock(return_value=conns)

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert data["connections_established"] == 3
        assert data["connections_total"] == 5

    @patch('time.time')
    def test_collect_data_includes_errors_and_drops(self, mock_time_func, plugin_config, mock_psutil):
        """Test collect_data includes error and drop counters"""
        mock_time_func.side_effect = [1000.0, 1001.0]

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            data = plugin.collect_data()

        assert data["errors_in"] == 10
        assert data["errors_out"] == 5
        assert data["drops_in"] == 2
        assert data["drops_out"] == 1

    @patch('time.time')
    def test_collect_data_updates_baseline(self, mock_time_func, plugin_config):
        """Test collect_data updates baseline counters"""
        mock_time_func.side_effect = [1000.0, 1001.0, 1002.0]

        counter1 = MagicMock(bytes_sent=1000000, bytes_recv=2000000,
                            packets_sent=5000, packets_recv=6000,
                            errin=10, errout=5, dropin=2, dropout=1)
        counter2 = MagicMock(bytes_sent=1100000, bytes_recv=2100000,
                            packets_sent=5100, packets_recv=6100,
                            errin=10, errout=5, dropin=2, dropout=1)

        mock_psutil = MagicMock()
        mock_psutil.net_io_counters = Mock(side_effect=[counter1, counter2, counter2])
        mock_psutil.net_connections = Mock(return_value=[])

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()

            # First collection
            plugin.collect_data()

            # Check baseline updated
            assert plugin._last_bytes_sent == 1100000
            assert plugin._last_bytes_recv == 2100000


# ============================================================================
# CLEANUP TESTS
# ============================================================================

class TestNetworkPluginCleanup:
    """Test NetworkPlugin cleanup"""

    @patch('time.time')
    def test_cleanup_sets_stopped_status(self, mock_time_func, plugin_config, mock_psutil):
        """Test cleanup sets status to STOPPED"""
        mock_time_func.return_value = 1000.0

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            plugin.initialize()
            plugin.cleanup()

        assert plugin.status == PluginStatus.STOPPED


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestNetworkPluginIntegration:
    """Test NetworkPlugin full lifecycle"""

    @patch('time.time')
    def test_full_lifecycle(self, mock_time_func, plugin_config, mock_psutil):
        """Test complete plugin lifecycle"""
        mock_time_func.side_effect = [1000.0, 1001.0]

        plugin = NetworkPlugin(plugin_config)

        with patch('builtins.__import__', return_value=mock_psutil):
            # Initialize
            assert plugin.status == PluginStatus.UNINITIALIZED
            plugin.initialize()
            assert plugin.status == PluginStatus.READY

            # Collect data
            data = plugin.collect_data()
            assert len(data) == 12  # 12 metrics

            # Cleanup
            plugin.cleanup()
            assert plugin.status == PluginStatus.STOPPED


# ============================================================================
# MOCK MODE TESTS
# ============================================================================

class TestNetworkPluginMockMode:
    """Test NetworkPlugin in mock mode (educational simulation)"""

    def test_mock_mode_initialization(self):
        """Test plugin initializes in mock mode without psutil"""
        config = PluginConfig(name="network", rate_ms=500)
        config.config['mock_mode'] = True

        plugin = NetworkPlugin(config)
        plugin.initialize()

        assert plugin.status == PluginStatus.READY
        assert plugin._mock_mode is True
        assert hasattr(plugin, '_mock_generator')

    def test_mock_mode_collect_data(self):
        """Test plugin collects simulated network data in mock mode"""
        config = PluginConfig(name="network", rate_ms=500)
        config.config['mock_mode'] = True

        plugin = NetworkPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()

        # Validate structure
        assert "bandwidth_rx_mbps" in data
        assert "bandwidth_tx_mbps" in data
        assert "bytes_sent" in data
        assert "bytes_recv" in data
        assert "packets_sent" in data
        assert "packets_recv" in data

        # Validate realistic ranges (home network)
        assert 0 <= data["bandwidth_rx_mbps"] <= 20  # Max ~20 Mbps down
        assert 0 <= data["bandwidth_tx_mbps"] <= 5   # Upload lower
        assert data["bandwidth_rx_mbps"] >= data["bandwidth_tx_mbps"]  # Download > Upload

        # Validate non-negative counters
        assert data["bytes_sent"] >= 0
        assert data["bytes_recv"] >= 0
        assert data["packets_sent"] >= 0
        assert data["packets_recv"] >= 0

    def test_mock_mode_data_is_cohesive(self):
        """Test mock mode network data varies naturally, not randomly"""
        config = PluginConfig(name="network", rate_ms=500)
        config.config['mock_mode'] = True

        plugin = NetworkPlugin(config)
        plugin.initialize()

        # Collect multiple samples
        samples_rx = []
        samples_tx = []
        for _ in range(5):
            data = plugin.collect_data()
            samples_rx.append(data["bandwidth_rx_mbps"])
            samples_tx.append(data["bandwidth_tx_mbps"])
            time.sleep(0.1)

        # Should vary but stay in reasonable range (cohesive, not chaotic)
        avg_rx = sum(samples_rx) / len(samples_rx)
        for sample in samples_rx:
            deviation = abs(sample - avg_rx) / avg_rx if avg_rx > 0 else 0
            assert deviation < 0.3, f"RX bandwidth should be stable (±30%), got {deviation:.2%}"

        # Download should consistently exceed upload
        for rx, tx in zip(samples_rx, samples_tx):
            assert rx >= tx, "Download should be >= upload"
