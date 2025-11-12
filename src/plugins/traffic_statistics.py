"""
Traffic Statistics Plugin - Feature 7

Monitors network traffic per device with detailed statistics.
Educational tool to visualize bandwidth usage and protocol distribution.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

try:
    from scapy.all import sniff, IP, TCP, UDP, conf
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class DeviceStats:
    """Statistics for a single device."""
    mac: str
    ip: str
    hostname: str
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    protocols: Dict[str, int]  # {protocol: packet_count}
    first_seen: float
    last_seen: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @property
    def total_bytes(self) -> int:
        """Total bytes (sent + received)."""
        return self.bytes_sent + self.bytes_received
    
    @property
    def total_packets(self) -> int:
        """Total packets (sent + received)."""
        return self.packets_sent + self.packets_received


@dataclass
class TrafficAlert:
    """Alert for unusual traffic patterns."""
    device_ip: str
    alert_type: str  # BANDWIDTH_SPIKE, NEW_PROTOCOL, EXCESSIVE_TRAFFIC
    description: str
    value: Any
    threshold: Any
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TrafficStatistics(Plugin):
    """
    Traffic Statistics - Monitor network bandwidth and protocols.
    
    Educational Features:
    - Per-device bandwidth tracking
    - Protocol distribution analysis
    - Traffic pattern detection
    - Bandwidth usage alerts
    - Historical data tracking
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Device statistics: {ip: DeviceStats}
        self.devices: Dict[str, DeviceStats] = {}
        
        # Device IP to MAC mapping
        self.ip_to_mac: Dict[str, str] = {}
        
        # Alerts
        self.alerts: List[TrafficAlert] = []
        
        # Configuration
        self.bandwidth_alert_threshold = 10 * 1024 * 1024  # 10 MB/s
        self.update_interval = 5  # seconds
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Global statistics
        self.global_stats = {
            'total_bytes': 0,
            'total_packets': 0,
            'start_time': time.time(),
            'protocols': defaultdict(int)
        }
    
    def initialize(self) -> None:
        """Initialize plugin."""
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect statistics data."""
        return self.get_data()
    
    def start(self):
        """Start traffic monitoring."""
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        logger.info("Starting Traffic Statistics Monitor...")
        self._stop_event.clear()
        self.global_stats['start_time'] = time.time()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_traffic, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop traffic monitoring."""
        logger.info("Stopping Traffic Statistics Monitor...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def get_data(self) -> Dict[str, Any]:
        """Get current statistics."""
        uptime = time.time() - self.global_stats['start_time']
        
        return {
            'monitoring': not self._stop_event.is_set(),
            'uptime': uptime,
            'device_count': len(self.devices),
            'devices': [dev.to_dict() for dev in self.devices.values()],
            'global_stats': {
                'total_bytes': self.global_stats['total_bytes'],
                'total_packets': self.global_stats['total_packets'],
                'protocols': dict(self.global_stats['protocols']),
                'bandwidth_mbps': self._calculate_bandwidth(uptime)
            },
            'alerts': [a.to_dict() for a in self.alerts[-10:]],
            'top_talkers': self._get_top_talkers(5)
        }
    
    def requires_root(self) -> bool:
        """Packet sniffing requires root privileges."""
        return True
    
    def register_device(self, ip: str, mac: str, hostname: str = "Unknown"):
        """Register a device for tracking."""
        if ip not in self.devices:
            self.devices[ip] = DeviceStats(
                mac=mac,
                ip=ip,
                hostname=hostname,
                bytes_sent=0,
                bytes_received=0,
                packets_sent=0,
                packets_received=0,
                protocols={},
                first_seen=time.time(),
                last_seen=time.time()
            )
            self.ip_to_mac[ip] = mac
            logger.info(f"Registered device for tracking: {ip} ({mac})")
    
    def _monitor_traffic(self):
        """Monitor network traffic continuously."""
        while not self._stop_event.is_set():
            try:
                # Sniff packets in batches
                sniff(
                    prn=self._process_packet,
                    store=0,
                    timeout=1,
                    filter="ip"  # Only IP packets
                )
            except Exception as e:
                logger.error(f"Traffic monitoring error: {e}")
                time.sleep(1)
    
    def _process_packet(self, packet):
        """Process individual packet."""
        if not packet.haslayer(IP):
            return
        
        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        packet_size = len(packet)
        
        # Determine protocol
        protocol = self._get_protocol(packet)
        
        # Update global stats
        self.global_stats['total_packets'] += 1
        self.global_stats['total_bytes'] += packet_size
        self.global_stats['protocols'][protocol] += 1
        
        # Update source device
        if src_ip in self.devices:
            self._update_device_stats(src_ip, packet_size, protocol, is_sent=True)
        
        # Update destination device
        if dst_ip in self.devices:
            self._update_device_stats(dst_ip, packet_size, protocol, is_sent=False)
    
    def _update_device_stats(self, ip: str, size: int, protocol: str, is_sent: bool):
        """Update statistics for a device."""
        device = self.devices[ip]
        
        if is_sent:
            device.bytes_sent += size
            device.packets_sent += 1
        else:
            device.bytes_received += size
            device.packets_received += 1
        
        # Update protocol count
        if protocol not in device.protocols:
            device.protocols[protocol] = 0
        device.protocols[protocol] += 1
        
        device.last_seen = time.time()
        
        # Check for alerts
        self._check_traffic_alerts(device)
    
    def _get_protocol(self, packet) -> str:
        """Determine packet protocol."""
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            # Identify common protocols by port
            if tcp_layer.dport == 80 or tcp_layer.sport == 80:
                return "HTTP"
            elif tcp_layer.dport == 443 or tcp_layer.sport == 443:
                return "HTTPS"
            elif tcp_layer.dport == 22 or tcp_layer.sport == 22:
                return "SSH"
            else:
                return "TCP"
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            if udp_layer.dport == 53 or udp_layer.sport == 53:
                return "DNS"
            elif udp_layer.dport == 67 or udp_layer.sport == 67:
                return "DHCP"
            else:
                return "UDP"
        else:
            return "OTHER"
    
    def _check_traffic_alerts(self, device: DeviceStats):
        """Check for unusual traffic patterns."""
        # Calculate current bandwidth
        time_window = 10  # seconds
        recent_bytes = device.bytes_sent + device.bytes_received
        bandwidth = recent_bytes / time_window
        
        # Alert on bandwidth spike
        if bandwidth > self.bandwidth_alert_threshold:
            self._raise_alert(
                device.ip,
                "BANDWIDTH_SPIKE",
                f"Device {device.ip} using {bandwidth / (1024*1024):.2f} MB/s",
                bandwidth,
                self.bandwidth_alert_threshold
            )
    
    def _raise_alert(self, device_ip: str, alert_type: str, description: str, 
                     value: Any, threshold: Any):
        """Raise a traffic alert."""
        alert = TrafficAlert(
            device_ip=device_ip,
            alert_type=alert_type,
            description=description,
            value=value,
            threshold=threshold,
            timestamp=time.time()
        )
        
        self.alerts.append(alert)
        logger.warning(f"🚨 TRAFFIC ALERT [{alert_type}]: {description}")
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def _calculate_bandwidth(self, uptime: float) -> float:
        """Calculate average bandwidth in Mbps."""
        if uptime == 0:
            return 0.0
        
        bytes_per_second = self.global_stats['total_bytes'] / uptime
        mbps = (bytes_per_second * 8) / (1024 * 1024)
        return round(mbps, 2)
    
    def _get_top_talkers(self, limit: int) -> List[Dict[str, Any]]:
        """Get devices with most traffic."""
        sorted_devices = sorted(
            self.devices.values(),
            key=lambda d: d.total_bytes,
            reverse=True
        )
        
        return [
            {
                'ip': dev.ip,
                'hostname': dev.hostname,
                'total_bytes': dev.total_bytes,
                'total_packets': dev.total_packets
            }
            for dev in sorted_devices[:limit]
        ]


class MockTrafficStatistics(Plugin):
    """Mock version for testing without network access."""
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Generate mock data
        self.mock_devices = [
            {
                'mac': 'aa:bb:cc:dd:ee:ff',
                'ip': '192.168.1.100',
                'hostname': 'laptop.local',
                'bytes_sent': 1024 * 1024 * 50,  # 50 MB
                'bytes_received': 1024 * 1024 * 200,  # 200 MB
                'packets_sent': 5000,
                'packets_received': 20000,
                'protocols': {'HTTPS': 15000, 'DNS': 500, 'HTTP': 100},
                'first_seen': time.time() - 3600,
                'last_seen': time.time()
            },
            {
                'mac': '11:22:33:44:55:66',
                'ip': '192.168.1.101',
                'hostname': 'phone.local',
                'bytes_sent': 1024 * 1024 * 20,  # 20 MB
                'bytes_received': 1024 * 1024 * 80,  # 80 MB
                'packets_sent': 2000,
                'packets_received': 8000,
                'protocols': {'HTTPS': 7000, 'DNS': 200, 'UDP': 800},
                'first_seen': time.time() - 1800,
                'last_seen': time.time()
            }
        ]
        
        self.mock_stats = {
            'total_bytes': 1024 * 1024 * 350,  # 350 MB
            'total_packets': 35000,
            'protocols': {'HTTPS': 22000, 'DNS': 700, 'HTTP': 100, 'UDP': 800, 'TCP': 11400},
            'bandwidth_mbps': 5.2
        }
    
    def initialize(self) -> None:
        """Initialize mock plugin."""
        logger.info("Mock Traffic Statistics initialized")
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect mock data."""
        return self.get_data()
    
    def get_data(self) -> Dict[str, Any]:
        """Get mock statistics."""
        return {
            'monitoring': True,
            'uptime': 3600,
            'device_count': len(self.mock_devices),
            'devices': self.mock_devices,
            'global_stats': self.mock_stats,
            'alerts': [],
            'top_talkers': self.mock_devices[:2]
        }
    
    def requires_root(self) -> bool:
        """Mock doesn't need root."""
        return False
    
    def start(self):
        """Mock start."""
        logger.info("Mock Traffic Statistics started")
    
    def stop(self):
        """Mock stop."""
        logger.info("Mock Traffic Statistics stopped")
