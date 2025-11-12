"""
Packet analyzer plugin for educational network monitoring.

Collects and analyzes network packets using Scapy (primary), PyShark (fallback),
or MockDataGenerator (educational mode). Provides Wireshark-style packet inspection
for teaching network security concepts.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import Dict, Any, List, Optional
import time

from .base import Plugin, PluginConfig, PluginStatus


class PacketAnalyzerPlugin(Plugin):
    """
    Packet analysis plugin for educational network monitoring.

    Provides real-time packet inspection and protocol analysis similar to Wireshark,
    with three operational modes:

    1. **Real Mode (Scapy)**: Live packet capture using Scapy (requires root)
       - High performance native Python parsing
       - 90% protocol coverage
       - Recommended for production

    2. **Real Mode (PyShark)**: Fallback to PyShark if Scapy unavailable
       - Uses Wireshark's tshark dissectors
       - 100% protocol coverage
       - Requires tshark installed

    3. **Mock Mode**: Educational simulation (safe, no root required)
       - Coherent family network scenario
       - Educational HTTP vs HTTPS examples
       - Perfect for learning and demonstrations

    Data Fields:
        top_protocols: Dict[str, int] - Protocol distribution (HTTPS: 450, DNS: 89, ...)
        top_sources: Dict[str, int] - Top source IP addresses with packet counts
        top_destinations: Dict[str, int] - Top destination IP addresses
        packet_rate: float - Packets per second
        total_packets: int - Total packets captured in this collection
        recent_packets: List[Dict] - Last N packets with educational flags (safe/unsafe)
        backend: str - Backend used ('scapy', 'pyshark', or 'mock')

    Example:
        >>> config = PluginConfig(name="packet_analyzer", rate_ms=1000)
        >>> plugin = PacketAnalyzerPlugin(config)
        >>> plugin.initialize()
        >>> data = plugin.collect_data()
        >>> print(f"Top protocol: {list(data['top_protocols'].keys())[0]}")
        Top protocol: HTTPS
    """

    def initialize(self) -> None:
        """
        Initialize packet analyzer plugin.

        Detects operational mode and selects appropriate backend:
        1. Mock mode (mock_mode=True): Uses MockDataGenerator
        2. Real mode: Tries Scapy first, falls back to PyShark
        3. Fails gracefully if no backend available

        Raises:
            RuntimeError: If no backend available in real mode

        Note:
            In mock mode, skips all dependency checks and uses educational
            simulation data. This is safe for children and requires no privileges.
        """
        # Check if running in mock mode
        self._mock_mode = self.config.config.get('mock_mode', False)

        if self._mock_mode:
            # Mock mode: use MockDataGenerator (educational, no deps)
            from src.utils.mock_data_generator import get_mock_packet_generator
            self._generator = get_mock_packet_generator()
            self._backend = 'mock'
            self._status = PluginStatus.READY
            return

        # Real mode: Try Scapy first (preferred)
        try:
            if self._try_initialize_scapy():
                return
        except Exception as e:
            print(f"Warning: Scapy initialization failed: {e}")

        # Fallback to PyShark
        try:
            if self._try_initialize_pyshark():
                return
        except Exception as e:
            print(f"Warning: PyShark initialization failed: {e}")

        # No backend available - graceful degradation
        print("Warning: No packet capture backend available. Showing unavailable status.")
        self._backend = 'unavailable'
        self._status = PluginStatus.READY
        self._unavailable_reason = 'no_backend'
        from src.utils.mock_data_generator import get_mock_packet_generator
        self._generator = get_mock_packet_generator()
        self._backend = 'mock'
        self._mock_mode = True
        self._status = PluginStatus.READY

    def _try_initialize_scapy(self) -> bool:
        """
        Try to initialize Scapy backend.

        Returns:
            True if Scapy initialized successfully, False otherwise

        Note:
            Validates interface exists before proceeding.
        """
        try:
            # Lazy import (P2: Validation preventive)
            from scapy.all import sniff, conf
            self.sniff = sniff
            self.conf = conf

            self._backend = 'scapy'

            # Get interface to monitor
            self._interface = self.config.config.get('interface', 'wlan0')

            # Validate interface exists (P2: Validation preventive)
            if not hasattr(self.conf, 'ifaces'):
                return False

            if self._interface not in self.conf.ifaces:
                raise RuntimeError(
                    f"Interface '{self._interface}' not found.\n"
                    f"Available interfaces: {list(self.conf.ifaces.keys())}"
                )

            self._status = PluginStatus.READY
            return True

        except (ImportError, Exception) as e:
            # Scapy not available or failed, will try PyShark
            return False

    def _try_initialize_pyshark(self) -> bool:
        """
        Try to initialize PyShark backend (fallback).

        Returns:
            True if PyShark initialized successfully, False otherwise

        Note:
            Validates tshark is installed before proceeding.
        """
        try:
            # Lazy import (P2: Validation preventive)
            import pyshark
            import subprocess

            self.pyshark = pyshark

            # Validate tshark is installed (P2: Validation preventive)
            subprocess.run(
                ['tshark', '--version'],
                capture_output=True,
                check=True,
                timeout=2
            )

            self._backend = 'pyshark'
            self._interface = self.config.config.get('interface', 'wlan0')

            self._status = PluginStatus.READY
            return True

        except (ImportError, subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # PyShark or tshark not available
            return False

    def collect_data(self) -> Dict[str, Any]:
        """
        Collect packet analysis data with graceful degradation.

        Returns:
            Dictionary with packet statistics or unavailable status
        """
        # Check if unavailable
        if hasattr(self, '_unavailable_reason'):
            return self._get_unavailable_status()
        
        # Collect based on backend
        try:
            if self._backend == 'mock':
                return self._collect_mock()
            elif self._backend == 'scapy':
                return self._collect_scapy()
            else:  # pyshark
                return self._collect_pyshark()
        except Exception as e:
            # Handle capture errors gracefully
            return self._get_error_status(str(e))
    
    def _get_unavailable_status(self) -> Dict[str, Any]:
        """Return status when packet capture unavailable"""
        return {
            'available': False,
            'status': 'unavailable',
            'message': 'Packet capture not available',
            'educational_tip': 'Install Scapy: pip install scapy\nOr run with --mock for educational mode',
            'backend': 'unavailable',
            'total_packets': 0,
            'packet_rate': 0.0,
            'top_protocols': {},
            'top_sources': {},
            'top_destinations': {},
            'recent_packets': []
        }
    
    def _get_error_status(self, error: str) -> Dict[str, Any]:
        """Return status when capture error occurs"""
        # Check if permission error
        if 'permission' in error.lower() or 'operation not permitted' in error.lower():
            message = 'Packet capture requires root privileges'
            tip = 'Run with sudo, or use --mock for educational mode'
        else:
            message = f'Capture error: {error[:50]}'
            tip = 'Check permissions and network interface'
        
        return {
            'available': False,
            'status': 'error',
            'message': message,
            'educational_tip': tip,
            'backend': self._backend,
            'total_packets': 0,
            'packet_rate': 0.0,
            'top_protocols': {},
            'top_sources': {},
            'top_destinations': {},
            'recent_packets': []
        }

    def _collect_mock(self) -> Dict[str, Any]:
        """
        Collect mock packet data (educational mode).

        Returns:
            Dictionary with simulated packet analysis data

        Note:
            Data is coherent with MockDataGenerator family devices.
            Includes educational HTTP vs HTTPS examples.
        """
        return self._generator.get_packet_analysis()

    def _collect_scapy(self) -> Dict[str, Any]:
        """
        Collect packets using Scapy backend (high performance).

        Captures N packets with timeout, analyzes protocols and IP addresses.

        Returns:
            Dictionary with packet analysis data including:
            - top_protocols: Protocol distribution
            - top_sources: Source IP packet counts
            - top_destinations: Destination IP packet counts
            - packet_rate: Packets per second
            - total_packets: Total packets in this capture
            - backend: 'scapy'

        Note:
            Sniff parameters (count, timeout) are configurable via plugin config.
        """
        # Get capture parameters from config
        count = self.config.config.get('capture_count', 100)
        timeout = self.config.config.get('capture_timeout', 1)

        # Capture packets
        start_time = time.time()
        packets = self.sniff(
            iface=self._interface,
            count=count,
            timeout=timeout,
            store=True
        )
        elapsed = time.time() - start_time

        # Analyze packets
        protocols = {}
        sources = {}
        destinations = {}

        for pkt in packets:
            # Protocol (last layer name)
            proto = pkt.lastlayer().name
            protocols[proto] = protocols.get(proto, 0) + 1

            # IP addresses (if present)
            if pkt.haslayer('IP'):
                src = pkt['IP'].src
                dst = pkt['IP'].dst
                sources[src] = sources.get(src, 0) + 1
                destinations[dst] = destinations.get(dst, 0) + 1

        # Sort and limit to top 10
        top_protocols = dict(
            sorted(protocols.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        top_sources = dict(
            sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        top_destinations = dict(
            sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:10]
        )

        # Calculate packet rate
        packet_rate = len(packets) / elapsed if elapsed > 0 else 0.0

        return {
            'top_protocols': top_protocols,
            'top_sources': top_sources,
            'top_destinations': top_destinations,
            'packet_rate': packet_rate,
            'total_packets': len(packets),
            'recent_packets': [],  # Real mode: no recent packets list (privacy)
            'backend': 'scapy'
        }

    def _collect_pyshark(self) -> Dict[str, Any]:
        """
        Collect packets using PyShark backend (fallback).

        Uses tshark dissectors for comprehensive protocol support.

        Returns:
            Dictionary with packet analysis data

        Note:
            Implementation similar to Scapy but using PyShark API.
            Slower than Scapy but supports all Wireshark protocols.
        """
        # Get capture parameters
        count = self.config.config.get('capture_count', 100)
        timeout = self.config.config.get('capture_timeout', 1)

        # Create capture object
        capture = self.pyshark.LiveCapture(interface=self._interface)

        # Capture packets
        start_time = time.time()
        packets = []
        try:
            capture.sniff(packet_count=count, timeout=timeout)
            packets = list(capture)
        except Exception:
            # Capture may timeout, return what we have
            packets = list(capture)
        elapsed = time.time() - start_time

        # Analyze packets
        protocols = {}
        sources = {}
        destinations = {}

        for pkt in packets:
            # Protocol (highest layer)
            proto = pkt.highest_layer
            protocols[proto] = protocols.get(proto, 0) + 1

            # IP addresses (if present)
            if hasattr(pkt, 'ip'):
                src = pkt.ip.src
                dst = pkt.ip.dst
                sources[src] = sources.get(src, 0) + 1
                destinations[dst] = destinations.get(dst, 0) + 1

        # Sort and limit to top 10
        top_protocols = dict(
            sorted(protocols.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        top_sources = dict(
            sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        top_destinations = dict(
            sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:10]
        )

        # Calculate packet rate
        packet_rate = len(packets) / elapsed if elapsed > 0 else 0.0

        return {
            'top_protocols': top_protocols,
            'top_sources': top_sources,
            'top_destinations': top_destinations,
            'packet_rate': packet_rate,
            'total_packets': len(packets),
            'recent_packets': [],  # Real mode: no recent packets list (privacy)
            'backend': 'pyshark'
        }

    def cleanup(self) -> None:
        """
        Cleanup packet analyzer plugin.

        Scapy and PyShark don't require explicit cleanup, but we set status.
        """
        self._status = PluginStatus.STOPPED
