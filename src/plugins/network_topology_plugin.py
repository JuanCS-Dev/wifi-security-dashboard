"""
Network Topology Mapper Plugin

Discovers all devices connected to the local network using:
- ARP scanning (scapy)
- MAC vendor lookup (OUI database)
- Hostname resolution

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import socket

try:
    from scapy.all import ARP, Ether, srp, conf
    conf.verb = 0  # Suppress scapy verbosity
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

import requests

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class NetworkDevice:
    """Represents a discovered network device."""
    ip: str
    mac: str
    hostname: str
    vendor: str
    last_seen: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NetworkTopologyPlugin(Plugin):
    """
    Network Topology Mapper - Discovers devices on local network.
    
    Features:
    - ARP scanning for device discovery
    - MAC vendor lookup via API
    - Hostname resolution
    - Real-time device tracking
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.devices: Dict[str, NetworkDevice] = {}
        self.gateway_ip: Optional[str] = None
        self.subnet: str = "192.168.1.0/24"
        self._stop_event = threading.Event()
        self._scan_thread: Optional[threading.Thread] = None
        
        # Cache for vendor lookups (avoid API spam)
        self._vendor_cache: Dict[str, str] = {}
        
    def start(self):
        """Start network scanning."""
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        logger.info("Starting Network Topology Mapper...")
        self._stop_event.clear()
        
        # Detect gateway and subnet
        self._detect_network()
        
        # Start scanning thread
        self._scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self._scan_thread.start()
        
    def stop(self):
        """Stop network scanning."""
        logger.info("Stopping Network Topology Mapper...")
        self._stop_event.set()
        if self._scan_thread:
            self._scan_thread.join(timeout=2.0)
    
    def get_data(self) -> Dict[str, Any]:
        """Get current topology data."""
        return {
            "gateway_ip": self.gateway_ip,
            "subnet": self.subnet,
            "device_count": len(self.devices),
            "devices": [device.to_dict() for device in self.devices.values()]
        }
    
    def requires_root(self) -> bool:
        """ARP scanning requires root privileges."""
        return True
    
    def _detect_network(self):
        """Detect gateway IP and subnet."""
        try:
            import netifaces
            
            # Get default gateway
            gws = netifaces.gateways()
            default_gw = gws.get('default', {}).get(netifaces.AF_INET)
            
            if default_gw:
                self.gateway_ip = default_gw[0]
                interface = default_gw[1]
                
                # Get subnet from interface
                addrs = netifaces.ifaddresses(interface)
                ipv4_info = addrs.get(netifaces.AF_INET, [{}])[0]
                ip = ipv4_info.get('addr')
                netmask = ipv4_info.get('netmask')
                
                if ip and netmask:
                    # Calculate subnet (simple /24 assumption)
                    parts = ip.split('.')
                    self.subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                    
                logger.info(f"Detected gateway: {self.gateway_ip}, subnet: {self.subnet}")
        except Exception as e:
            logger.warning(f"Failed to detect network: {e}. Using defaults.")
            self.gateway_ip = "192.168.1.1"
            self.subnet = "192.168.1.0/24"
    
    def _scan_loop(self):
        """Main scanning loop."""
        while not self._stop_event.is_set():
            try:
                self._scan_network()
            except Exception as e:
                logger.error(f"Scan error: {e}")
            
            # Wait before next scan (avoid network spam)
            self._stop_event.wait(timeout=30.0)
    
    def _scan_network(self):
        """Perform ARP scan of subnet."""
        if not SCAPY_AVAILABLE:
            return
        
        logger.debug(f"Scanning subnet: {self.subnet}")
        
        # Create ARP request packet
        arp = ARP(pdst=self.subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        
        # Send and capture responses
        result = srp(packet, timeout=2, verbose=0)[0]
        
        current_time = time.time()
        
        # Process responses
        for sent, received in result:
            ip = received.psrc
            mac = received.hwsrc
            
            # Skip if already discovered recently
            if ip in self.devices:
                self.devices[ip].last_seen = current_time
                continue
            
            # Resolve hostname
            hostname = self._resolve_hostname(ip)
            
            # Lookup vendor
            vendor = self._lookup_vendor(mac)
            
            # Add device
            device = NetworkDevice(
                ip=ip,
                mac=mac,
                hostname=hostname,
                vendor=vendor,
                last_seen=current_time
            )
            self.devices[ip] = device
            logger.info(f"Discovered device: {ip} ({mac}) - {vendor}")
        
        # Remove stale devices (not seen in 5 minutes)
        stale_threshold = current_time - 300
        stale_ips = [ip for ip, dev in self.devices.items() if dev.last_seen < stale_threshold]
        for ip in stale_ips:
            logger.info(f"Removing stale device: {ip}")
            del self.devices[ip]
    
    def _resolve_hostname(self, ip: str) -> str:
        """Resolve hostname from IP."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except Exception:
            return "Unknown"
    
    def _lookup_vendor(self, mac: str) -> str:
        """Lookup MAC vendor using macvendors.com API."""
        # Check cache first
        if mac in self._vendor_cache:
            return self._vendor_cache[mac]
        
        try:
            response = requests.get(f"https://api.macvendors.com/{mac}", timeout=2)
            if response.status_code == 200:
                vendor = response.text.strip()
                self._vendor_cache[mac] = vendor
                return vendor
        except Exception:
            pass
        
        # Fallback: extract OUI prefix
        oui = mac[:8].upper()
        self._vendor_cache[mac] = f"OUI:{oui}"
        return f"OUI:{oui}"


class MockNetworkTopologyPlugin(Plugin):
    """Mock version for testing without network access."""
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.gateway_ip = "192.168.1.1"
        self.subnet = "192.168.1.0/24"
        self.devices = [
            {
                "ip": "192.168.1.1",
                "mac": "AA:BB:CC:DD:EE:FF",
                "hostname": "router.local",
                "vendor": "TP-Link",
                "last_seen": time.time()
            },
            {
                "ip": "192.168.1.10",
                "mac": "11:22:33:44:55:66",
                "hostname": "arduino.local",
                "vendor": "Arduino",
                "last_seen": time.time()
            },
            {
                "ip": "192.168.1.15",
                "mac": "AA:BB:CC:11:22:33",
                "hostname": "iphone.local",
                "vendor": "Apple Inc.",
                "last_seen": time.time()
            },
            {
                "ip": "192.168.1.20",
                "mac": "DD:EE:FF:44:55:66",
                "hostname": "laptop.local",
                "vendor": "Dell Inc.",
                "last_seen": time.time()
            },
            {
                "ip": "192.168.1.25",
                "mac": "BB:CC:DD:77:88:99",
                "hostname": "raspberrypi.local",
                "vendor": "Raspberry Pi Foundation",
                "last_seen": time.time()
            }
        ]
    
    def initialize(self) -> None:
        """Initialize mock plugin."""
        logger.info("Mock Network Topology Mapper initialized")
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect mock topology data."""
        return self.get_data()
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        logger.info("Mock Network Topology Mapper cleaned up")
    
    def start(self):
        logger.info("Mock Network Topology Mapper started")
    
    def stop(self):
        logger.info("Mock Network Topology Mapper stopped")
    
    def get_data(self) -> Dict[str, Any]:
        return {
            "gateway_ip": self.gateway_ip,
            "subnet": self.subnet,
            "device_count": len(self.devices),
            "devices": self.devices
        }
    
    def requires_root(self) -> bool:
        return False
