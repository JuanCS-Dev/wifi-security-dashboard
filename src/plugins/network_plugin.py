"""
Network metrics plugin using psutil.

Collects network interface statistics, bandwidth usage, and connection information.
Uses psutil library for cross-platform network monitoring.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import Dict, Any, Optional
import time

from .base import Plugin, PluginConfig, PluginStatus


class NetworkPlugin(Plugin):
    """
    Network metrics collection plugin.

    Provides real-time network metrics including:
    - Bandwidth (bytes sent/received)
    - Packet counts
    - Active connections
    - Per-interface statistics

    Data Fields:
        bandwidth_tx_mbps: Transmit bandwidth in Mbps (calculated)
        bandwidth_rx_mbps: Receive bandwidth in Mbps (calculated)
        bytes_sent: Total bytes sent since boot
        bytes_recv: Total bytes received since boot
        packets_sent: Total packets sent
        packets_recv: Total packets received
        connections_established: Number of ESTABLISHED TCP connections
        connections_total: Total number of connections (all states)
        errors_in: Total receive errors
        errors_out: Total transmit errors
        drops_in: Total receive drops
        drops_out: Total transmit drops

    Example:
        >>> config = PluginConfig(name="network", rate_ms=1000)
        >>> plugin = NetworkPlugin(config)
        >>> plugin.initialize()
        >>> data = plugin.collect_data()
        >>> print(f"TX: {data['bandwidth_tx_mbps']:.2f} Mbps")
        TX: 2.45 Mbps
    """

    def initialize(self) -> None:
        """
        Initialize network plugin.

        Sets up baseline network counters for bandwidth calculation.

        In mock mode, skips psutil initialization and uses MockDataGenerator.
        """
        # Check if running in mock mode
        self._mock_mode = self.config.config.get('mock_mode', False)

        if self._mock_mode:
            # Mock mode: use MockDataGenerator
            from src.utils.mock_data_generator import get_mock_generator
            self._mock_generator = get_mock_generator()
            self._status = PluginStatus.READY
            return

        # Real mode: Import psutil (lazy loading)
        try:
            import psutil
            self.psutil = psutil
        except ImportError:
            raise RuntimeError("psutil library not installed. Install with: pip install psutil")

        # Verify psutil is available
        if not hasattr(self.psutil, 'net_io_counters'):
            raise RuntimeError("psutil.net_io_counters not available")

        # Get interface to monitor (None = all interfaces)
        self._interface = self.config.config.get('interface', None)

        # Initialize baseline counters for bandwidth calculation
        try:
            counters = self.psutil.net_io_counters(pernic=False)
            self._last_bytes_sent = counters.bytes_sent
            self._last_bytes_recv = counters.bytes_recv
            self._last_time = time.time()
        except Exception as e:
            raise RuntimeError(f"Failed to get network counters: {e}")

        self._status = PluginStatus.READY

    def collect_data(self) -> Dict[str, Any]:
        """
        Collect network metrics.

        Returns:
            Dictionary with network metrics

        Note:
            Bandwidth is calculated by comparing current counters with
            previous counters. First collection may show 0 Mbps.

            In mock mode, returns simulated data from MockDataGenerator.
        """
        # Mock mode: return simulated data
        if self._mock_mode:
            return self._mock_generator.get_network_stats()

        # Real mode: Get network I/O counters (all interfaces combined)
        counters = self.psutil.net_io_counters(pernic=False)

        # Calculate bandwidth (bytes per second -> Mbps)
        current_time = time.time()
        time_delta = current_time - self._last_time

        if time_delta > 0:
            # bytes/second -> bits/second -> megabits/second
            bytes_sent_delta = counters.bytes_sent - self._last_bytes_sent
            bytes_recv_delta = counters.bytes_recv - self._last_bytes_recv

            bandwidth_tx_mbps = (bytes_sent_delta * 8) / (time_delta * 1_000_000)
            bandwidth_rx_mbps = (bytes_recv_delta * 8) / (time_delta * 1_000_000)
        else:
            # No time elapsed (first call or very rapid calls)
            bandwidth_tx_mbps = 0.0
            bandwidth_rx_mbps = 0.0

        # Update baseline for next calculation
        self._last_bytes_sent = counters.bytes_sent
        self._last_bytes_recv = counters.bytes_recv
        self._last_time = current_time

        # Get connection count
        connections = self.psutil.net_connections(kind='inet')
        connections_established = sum(
            1 for conn in connections if conn.status == 'ESTABLISHED'
        )
        connections_total = len(connections)

        data = {
            "bandwidth_tx_mbps": bandwidth_tx_mbps,
            "bandwidth_rx_mbps": bandwidth_rx_mbps,
            "bytes_sent": counters.bytes_sent,
            "bytes_recv": counters.bytes_recv,
            "packets_sent": counters.packets_sent,
            "packets_recv": counters.packets_recv,
            "connections_established": connections_established,
            "connections_total": connections_total,
            "errors_in": counters.errin,
            "errors_out": counters.errout,
            "drops_in": counters.dropin,
            "drops_out": counters.dropout,
        }

        return data

    def cleanup(self) -> None:
        """
        Cleanup network plugin.

        psutil doesn't require explicit cleanup.
        """
        self._status = PluginStatus.STOPPED
