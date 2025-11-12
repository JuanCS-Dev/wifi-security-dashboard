"""
Mock data generator for educational demonstrations.

Provides realistic, cohesive simulated data for the dashboard in mock mode.
Designed for teaching children about WiFi networks and internet usage.

The simulation represents a typical family of 4:
- 2 parents (smartphones + laptops)
- 2 children ages 7-8 (tablets)
- Shared devices (Smart TV, gaming console)

Data varies naturally but maintains consistency for educational clarity.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import time
import math
import random
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class MockDevice:
    """Represents a simulated device on the network"""
    mac: str
    ip: str
    hostname: str
    type: str  # smartphone, laptop, tablet, smart_tv, gaming, iot
    owner: str  # Family member
    is_active: bool = True

    # Traffic patterns (MB/s baseline)
    baseline_download: float = 0.0
    baseline_upload: float = 0.0

    # Current app usage
    current_app: str = "Idle"


class MockDataGenerator:
    """
    Generates cohesive, realistic mock data for educational purposes.

    This generator creates a stable, understandable scenario rather than
    random data. Perfect for teaching children about networks.

    Features:
    - Fixed devices (family of 4)
    - Realistic traffic patterns
    - Natural variations (not chaotic)
    - Time-based activity (morning/afternoon/evening patterns)
    - Cohesive events (Netflix = higher traffic)

    Usage:
        >>> generator = MockDataGenerator()
        >>> system_data = generator.get_system_metrics()
        >>> print(f"CPU: {system_data['cpu_percent']}%")
    """

    def __init__(self):
        """Initialize mock data generator with family scenario"""
        self._start_time = time.time()
        self._cycle_time = 0.0  # Smooth animation cycle

        # Educational family scenario
        self.devices = self._create_family_devices()
        self.wifi_info = self._create_wifi_info()

        # Activity state (changes slowly for consistency)
        self._current_scenario = "normal_browsing"
        self._scenario_start = time.time()

    def _create_family_devices(self) -> List[MockDevice]:
        """
        Create devices for a typical family of 4.

        Returns:
            List of mock devices with realistic configuration
        """
        return [
            # Parents
            MockDevice(
                mac="AA:BB:CC:DD:EE:01",
                ip="192.168.1.101",
                hostname="Dad-Phone",
                type="smartphone",
                owner="Pai",
                baseline_download=0.5,
                baseline_upload=0.1,
                current_app="WhatsApp"
            ),
            MockDevice(
                mac="AA:BB:CC:DD:EE:02",
                ip="192.168.1.102",
                hostname="Mom-Phone",
                type="smartphone",
                owner="Mãe",
                baseline_download=0.3,
                baseline_upload=0.05,
                current_app="Instagram"
            ),
            MockDevice(
                mac="AA:BB:CC:DD:EE:03",
                ip="192.168.1.103",
                hostname="Dad-Laptop",
                type="laptop",
                owner="Pai",
                baseline_download=1.2,
                baseline_upload=0.3,
                current_app="Gmail"
            ),

            # Children
            MockDevice(
                mac="AA:BB:CC:DD:EE:11",
                ip="192.168.1.111",
                hostname="Filho-Tablet",
                type="tablet",
                owner="Filho (8 anos)",
                baseline_download=0.8,
                baseline_upload=0.05,
                current_app="YouTube Kids"
            ),
            MockDevice(
                mac="AA:BB:CC:DD:EE:12",
                ip="192.168.1.112",
                hostname="Filha-Tablet",
                type="tablet",
                owner="Filha (7 anos)",
                baseline_download=0.7,
                baseline_upload=0.05,
                current_app="Netflix Kids"
            ),

            # Shared devices
            MockDevice(
                mac="AA:BB:CC:DD:EE:20",
                ip="192.168.1.120",
                hostname="Smart-TV-Sala",
                type="smart_tv",
                owner="Família",
                baseline_download=3.5,
                baseline_upload=0.1,
                current_app="Netflix"
            ),
        ]

    def _create_wifi_info(self) -> Dict[str, Any]:
        """Create realistic WiFi information"""
        return {
            "ssid": "Casa-Familia",
            "security": "WPA2",
            "frequency": 5.0,  # 5 GHz
            "channel": 36,
            "signal_strength": -45,  # Good signal
            "link_speed": 300,  # Mbps
        }

    def _update_cycle(self) -> None:
        """Update smooth animation cycle (0.0 to 1.0 every 30 seconds)"""
        elapsed = time.time() - self._start_time
        self._cycle_time = (elapsed % 30.0) / 30.0  # 30-second cycle

    def _natural_variation(self, base: float, amplitude: float = 0.1) -> float:
        """
        Add natural variation to a value.

        Uses smooth sine wave + small noise for realistic fluctuation.

        Args:
            base: Base value
            amplitude: How much variation (0.1 = ±10%)

        Returns:
            Value with natural variation
        """
        # Smooth sine wave
        smooth = base * (1.0 + amplitude * math.sin(self._cycle_time * 2 * math.pi))

        # Tiny random noise for realism (not chaos!)
        noise = base * random.uniform(-0.02, 0.02)

        # Return smooth + noise (allow negative values for signal strength, etc)
        return smooth + noise

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get simulated system metrics.

        Metrics are realistic and stable:
        - CPU: 25-35% (light load)
        - RAM: 55-65% (typical usage)
        - Disk: ~80% (home computer)
        - Temperature: 45-55°C (normal)

        Returns:
            Dictionary with system metrics (matches SystemPlugin real mode format)
        """
        self._update_cycle()

        # RAM values - mock uses GB, convert to MB to match real mode
        ram_total_gb = 16.0
        ram_used_gb = 9.6
        ram_percent = self._natural_variation(60.0, 0.08)

        return {
            "cpu_percent": self._natural_variation(30.0, 0.15),
            "cpu_count": 8,
            # Match real mode field names (memory_* not ram_*)
            "memory_percent": ram_percent,
            "memory_used_mb": ram_used_gb * 1024,  # GB to MB
            "memory_total_mb": ram_total_gb * 1024,  # GB to MB
            "disk_percent": 78.5,  # Stable
            "disk_used_gb": 402.0,
            "disk_total_gb": 512.0,
            "temperature_celsius": self._natural_variation(50.0, 0.1),
            "uptime_seconds": int(time.time() - self._start_time),
        }

    def get_wifi_info(self) -> Dict[str, Any]:
        """
        Get simulated WiFi information.

        Signal strength varies slightly (-45 to -48 dBm = excellent).
        Other values are stable for educational clarity.

        Returns:
            Dictionary with WiFi information
        """
        self._update_cycle()

        info = self.wifi_info.copy()

        # Signal varies slightly (natural wall/movement effects)
        info["signal_strength"] = int(self._natural_variation(-45.0, 0.06))

        return info

    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get simulated network statistics.

        Traffic patterns are cohesive:
        - Baseline: Light browsing (1-2 Mbps down, 0.2 Mbps up)
        - Peaks: Streaming video (8-10 Mbps down)
        - Natural variation, not random spikes

        Returns:
            Dictionary with network statistics
        """
        self._update_cycle()

        # Calculate total traffic from active devices
        total_download = sum(d.baseline_download for d in self.devices if d.is_active)
        total_upload = sum(d.baseline_upload for d in self.devices if d.is_active)

        # Add natural variation
        download_mbps = self._natural_variation(total_download, 0.15)
        upload_mbps = self._natural_variation(total_upload, 0.15)

        return {
            "bandwidth_rx_mbps": download_mbps,  # Mbps (match real mode field name)
            "bandwidth_tx_mbps": upload_mbps,  # Mbps (match real mode field name)
            "bytes_sent": int((total_upload * 1024 * 1024 / 8) * (time.time() - self._start_time)),
            "bytes_recv": int((total_download * 1024 * 1024 / 8) * (time.time() - self._start_time)),
            "packets_sent": int(total_upload * 1000 * (time.time() - self._start_time)),
            "packets_recv": int(total_download * 1500 * (time.time() - self._start_time)),
        }

    def get_devices(self) -> List[Dict[str, Any]]:
        """
        Get list of simulated devices.

        Devices are stable with occasional activity changes.

        Returns:
            List of device dictionaries
        """
        devices_data = []

        for device in self.devices:
            devices_data.append({
                "mac": device.mac,
                "ip": device.ip,
                "hostname": device.hostname,
                "type": device.type,
                "owner": device.owner,
                "is_active": device.is_active,
                "traffic_down_mbps": self._natural_variation(device.baseline_download, 0.2),
                "traffic_up_mbps": self._natural_variation(device.baseline_upload, 0.2),
                "current_app": device.current_app,
            })

        return devices_data

    def get_top_apps(self) -> Dict[str, float]:
        """
        Get top applications by bandwidth usage.

        Apps match the devices' current_app field for consistency.

        Returns:
            Dictionary of {app_name: traffic_mbps}
        """
        apps = {}

        for device in self.devices:
            if device.is_active and device.current_app != "Idle":
                current_traffic = self._natural_variation(device.baseline_download, 0.15)

                if device.current_app in apps:
                    apps[device.current_app] += current_traffic
                else:
                    apps[device.current_app] = current_traffic

        return apps

    def get_packet_analysis(self) -> Dict[str, Any]:
        """
        Get simulated packet analysis data (Wireshark-style).

        Returns realistic packet distribution coherent with family devices:
        - Protocols match device activities (HTTPS for browsing, H264 for streaming)
        - Source IPs match MockDevice IPs (192.168.1.100-112)
        - Destinations are real educational IPs (Google, Netflix, DNS)
        - Educational flags (safe/unsafe) for HTTP vs HTTPS

        Returns:
            Dictionary with packet analysis data including:
            - top_protocols: Protocol distribution (HTTPS, DNS, HTTP, etc)
            - top_sources: Source IP packet counts
            - top_destinations: Destination IP packet counts
            - packet_rate: Packets per second
            - total_packets: Total packet count
            - recent_packets: List of recent packets with educational flags
            - backend: 'mock'
        """
        self._update_cycle()

        # Protocol distribution (educational and realistic)
        # Based on device activities: HTTPS (secure browsing), H264 (video), DNS (lookups)
        base_https = 450  # Majority is encrypted
        base_dns = 89     # Name resolution queries
        base_http = 32    # Small amount of insecure (educational warning!)
        base_h264 = 156   # Video streaming (Smart TV + tablets)
        base_quic = 78    # Modern HTTP/3 (Google services)

        protocols = {
            'HTTPS': int(self._natural_variation(base_https, 0.1)),
            'DNS': int(self._natural_variation(base_dns, 0.15)),
            'HTTP': int(self._natural_variation(base_http, 0.2)),
            'H264': int(self._natural_variation(base_h264, 0.12)),
            'QUIC': int(self._natural_variation(base_quic, 0.15)),
            'MDNS': int(self._natural_variation(12, 0.3)),  # Local discovery
        }

        # Source IPs (match MockDevice IPs for consistency - P5)
        # Higher traffic devices (streaming) have more packets
        sources = {}
        for device in self.devices:
            if device.is_active:
                # Base packet count proportional to bandwidth
                base_pkts = int(device.baseline_download * 20)  # ~20 pkts per MB/s
                sources[device.ip] = int(self._natural_variation(base_pkts, 0.15))

        # Sort by packet count and get top 10
        sources = dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10])

        # Destination IPs (educational: real well-known IPs)
        destinations = {
            '142.250.185.46': int(self._natural_variation(234, 0.12)),  # Google (YouTube, Gmail)
            '54.192.147.14': int(self._natural_variation(156, 0.1)),    # Netflix CDN
            '8.8.8.8': int(self._natural_variation(89, 0.15)),          # Google DNS
            '1.1.1.1': int(self._natural_variation(34, 0.2)),           # Cloudflare DNS
            '185.60.218.35': int(self._natural_variation(45, 0.18)),    # Instagram
            '31.13.86.36': int(self._natural_variation(23, 0.25)),      # Facebook/WhatsApp
        }

        # Recent packets (educational: show HTTPS vs HTTP difference)
        recent_packets = [
            {
                'timestamp': '14:32:15.234',
                'src': '192.168.1.102',  # Dad Laptop
                'dst': '142.250.185.46',  # Google
                'protocol': 'HTTPS',
                'info': 'Gmail - Encrypted ✅',
                'safe': True
            },
            {
                'timestamp': '14:32:15.456',
                'src': '192.168.1.104',  # Kid Tablet
                'dst': '93.184.216.34',  # Example.com
                'protocol': 'HTTP',
                'info': '⚠️ Unencrypted website! Passwords visible!',
                'safe': False  # Educational warning!
            },
            {
                'timestamp': '14:32:15.678',
                'src': '192.168.1.105',  # Smart TV
                'dst': '54.192.147.14',  # Netflix
                'protocol': 'H264',
                'info': 'Netflix - Video streaming ✅',
                'safe': True
            },
            {
                'timestamp': '14:32:15.890',
                'src': '192.168.1.100',  # Dad Phone
                'dst': '31.13.86.36',  # WhatsApp
                'protocol': 'QUIC',
                'info': 'WhatsApp - Encrypted messaging ✅',
                'safe': True
            },
            {
                'timestamp': '14:32:16.012',
                'src': '192.168.1.112',  # Kid2 Tablet
                'dst': '142.250.185.46',  # YouTube
                'protocol': 'HTTPS',
                'info': 'YouTube Kids - Encrypted ✅',
                'safe': True
            },
        ]

        # Calculate total packets and rate
        total_packets = sum(protocols.values())
        packet_rate = self._natural_variation(85.0, 0.15)  # ~85 pkts/s average

        return {
            'top_protocols': protocols,
            'top_sources': sources,
            'top_destinations': destinations,
            'packet_rate': packet_rate,
            'total_packets': total_packets,
            'recent_packets': recent_packets,
            'backend': 'mock'
        }


# Singleton instance
_generator_instance = None


def get_mock_generator() -> MockDataGenerator:
    """
    Get the global mock data generator instance.

    Uses singleton pattern to maintain consistency across all plugins.

    Returns:
        MockDataGenerator instance
    """
    global _generator_instance

    if _generator_instance is None:
        _generator_instance = MockDataGenerator()

    return _generator_instance


def get_mock_packet_generator() -> MockDataGenerator:
    """
    Get the global mock packet generator instance.

    Alias for get_mock_generator() for explicit packet analysis use.
    Maintains singleton pattern for consistency across all plugins.

    Returns:
        MockDataGenerator instance
    """
    return get_mock_generator()
