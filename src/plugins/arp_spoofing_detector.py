"""
ARP Spoofing Detector Plugin - Feature 2

Detects ARP spoofing attacks (Man-in-the-Middle) in real-time.
Educational tool to teach network security concepts.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict

try:
    from scapy.all import ARP, sniff, conf
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class ARPEntry:
    """Represents an ARP cache entry."""
    ip: str
    mac: str
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SpoofingAlert:
    """Represents a detected spoofing attack."""
    ip: str
    old_mac: str
    new_mac: str
    timestamp: float
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    educational_note: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ARPSpoofingDetector(Plugin):
    """
    ARP Spoofing Detector - Detects MITM attacks.
    
    Educational Features:
    - Real-time ARP monitoring
    - MAC address change detection
    - Alert severity levels
    - Educational explanations
    - Attack pattern recognition
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # ARP cache: {ip: ARPEntry}
        self.arp_cache: Dict[str, ARPEntry] = {}
        
        # Alert history
        self.alerts: List[SpoofingAlert] = []
        
        # MAC change tracking: {ip: [mac1, mac2, ...]}
        self.mac_history: Dict[str, List[str]] = defaultdict(list)
        
        # Known good MACs (trusted devices)
        self.trusted_devices: Set[str] = set()
        
        # Detection settings
        self.alert_threshold = 2  # Alerts if MAC changes this many times
        self.monitor_window = 300  # 5 minutes
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.stats = {
            'arp_packets': 0,
            'mac_changes': 0,
            'alerts_raised': 0,
            'critical_alerts': 0
        }
    
    def initialize(self) -> None:
        """Initialize plugin."""
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect detection data."""
        return self.get_data()
    
    def start(self):
        """Start ARP monitoring."""
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        logger.info("Starting ARP Spoofing Detector...")
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_arp, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop ARP monitoring."""
        logger.info("Stopping ARP Spoofing Detector...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def get_data(self) -> Dict[str, Any]:
        """Get current detection status."""
        return {
            'monitoring': not self._stop_event.is_set(),
            'arp_cache_size': len(self.arp_cache),
            'alert_count': len(self.alerts),
            'recent_alerts': [a.to_dict() for a in self.alerts[-10:]],
            'stats': self.stats.copy(),
            'trusted_devices': list(self.trusted_devices)
        }
    
    def requires_root(self) -> bool:
        """ARP sniffing requires root privileges."""
        return True
    
    def add_trusted_device(self, mac: str, ip: str = None):
        """Add a device to trusted list."""
        mac = mac.lower()
        self.trusted_devices.add(mac)
        logger.info(f"Added trusted device: {mac} ({ip or 'unknown IP'})")
    
    def _monitor_arp(self):
        """Monitor ARP traffic continuously."""
        while not self._stop_event.is_set():
            try:
                # Sniff ARP packets (1 second batches)
                sniff(
                    filter="arp",
                    prn=self._process_arp_packet,
                    store=0,
                    timeout=1
                )
            except Exception as e:
                logger.error(f"ARP monitoring error: {e}")
                time.sleep(1)
    
    def _process_arp_packet(self, packet):
        """Process individual ARP packet."""
        if not packet.haslayer(ARP):
            return
        
        self.stats['arp_packets'] += 1
        
        arp_layer = packet[ARP]
        
        # We care about ARP replies (responses)
        if arp_layer.op == 2:  # ARP Reply
            ip = arp_layer.psrc
            mac = arp_layer.hwsrc.lower()
            
            self._check_arp_entry(ip, mac)
    
    def _check_arp_entry(self, ip: str, mac: str):
        """Check if ARP entry is suspicious."""
        current_time = time.time()
        
        # New IP seen
        if ip not in self.arp_cache:
            self.arp_cache[ip] = ARPEntry(
                ip=ip,
                mac=mac,
                timestamp=current_time
            )
            self.mac_history[ip].append(mac)
            return
        
        # Existing IP - check if MAC changed
        old_entry = self.arp_cache[ip]
        
        if old_entry.mac != mac:
            self._handle_mac_change(ip, old_entry.mac, mac, current_time)
    
    def _handle_mac_change(self, ip: str, old_mac: str, new_mac: str, timestamp: float):
        """Handle detected MAC address change."""
        self.stats['mac_changes'] += 1
        
        # Update cache
        self.arp_cache[ip] = ARPEntry(
            ip=ip,
            mac=new_mac,
            timestamp=timestamp
        )
        
        # Track MAC history
        self.mac_history[ip].append(new_mac)
        
        # Check if this is suspicious
        severity = self._assess_threat_level(ip, old_mac, new_mac)
        
        if severity != "NONE":
            self._raise_alert(ip, old_mac, new_mac, timestamp, severity)
    
    def _assess_threat_level(self, ip: str, old_mac: str, new_mac: str) -> str:
        """Assess threat level of MAC change."""
        
        # Check if both MACs are trusted
        if old_mac in self.trusted_devices and new_mac in self.trusted_devices:
            return "NONE"
        
        # Check frequency of changes
        recent_changes = len([m for m in self.mac_history[ip] 
                             if m != self.mac_history[ip][0]])
        
        # Gateway IP change is CRITICAL
        if self._is_gateway_ip(ip):
            return "CRITICAL"
        
        # Multiple rapid changes = HIGH
        if recent_changes >= self.alert_threshold:
            return "HIGH"
        
        # Single change to untrusted device = MEDIUM
        if new_mac not in self.trusted_devices:
            return "MEDIUM"
        
        return "LOW"
    
    def _is_gateway_ip(self, ip: str) -> bool:
        """Check if IP is likely a gateway."""
        # Common gateway patterns
        return ip.endswith('.1') or ip.endswith('.254')
    
    def _raise_alert(self, ip: str, old_mac: str, new_mac: str, timestamp: float, severity: str):
        """Raise a spoofing alert."""
        self.stats['alerts_raised'] += 1
        
        if severity == "CRITICAL":
            self.stats['critical_alerts'] += 1
        
        # Generate educational note
        educational_note = self._generate_educational_note(severity, ip)
        
        alert = SpoofingAlert(
            ip=ip,
            old_mac=old_mac,
            new_mac=new_mac,
            timestamp=timestamp,
            severity=severity,
            description=f"MAC address changed for {ip}",
            educational_note=educational_note
        )
        
        self.alerts.append(alert)
        
        logger.warning(f"🚨 ARP SPOOFING ALERT [{severity}]: {ip} changed from {old_mac} to {new_mac}")
        
        # Keep only recent alerts (last 100)
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def _generate_educational_note(self, severity: str, ip: str) -> str:
        """Generate educational explanation for alert."""
        if severity == "CRITICAL":
            return (
                f"🚨 CRITICAL: Possível ataque ao gateway ({ip})!\n"
                "   Um atacante pode estar tentando interceptar TODO o tráfego da rede.\n"
                "   Isso é um ataque Man-in-the-Middle (MITM) - muito perigoso!\n"
                "   AÇÃO: Desconecte da rede imediatamente e investigue."
            )
        elif severity == "HIGH":
            return (
                f"⚠️ HIGH: Múltiplas mudanças de MAC para {ip}.\n"
                "   Isso pode indicar um ataque de ARP spoofing ativo.\n"
                "   Alguém pode estar tentando se passar por este dispositivo.\n"
                "   AÇÃO: Monitore de perto e verifique dispositivos conectados."
            )
        elif severity == "MEDIUM":
            return (
                f"⚠️ MEDIUM: Dispositivo desconhecido assumiu IP {ip}.\n"
                "   Pode ser legítimo (novo dispositivo) ou ataque.\n"
                "   AÇÃO: Verifique se você reconhece o novo dispositivo."
            )
        else:  # LOW
            return (
                f"ℹ️ LOW: Mudança de MAC detectada para {ip}.\n"
                "   Provavelmente normal (dispositivo reiniciado ou substituído).\n"
                "   AÇÃO: Apenas para informação."
            )


class MockARPSpoofingDetector(Plugin):
    """Mock version for testing without network access."""
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Generate mock data
        self.mock_alerts = [
            {
                'ip': '192.168.1.1',
                'old_mac': 'aa:bb:cc:dd:ee:ff',
                'new_mac': '11:22:33:44:55:66',
                'timestamp': time.time() - 300,
                'severity': 'CRITICAL',
                'description': 'Gateway MAC changed',
                'educational_note': '🚨 Ataque ao gateway detectado!'
            },
            {
                'ip': '192.168.1.50',
                'old_mac': '11:22:33:44:55:66',
                'new_mac': 'aa:bb:cc:dd:ee:ff',
                'timestamp': time.time() - 60,
                'severity': 'HIGH',
                'description': 'Multiple MAC changes',
                'educational_note': '⚠️ Possível ARP spoofing'
            }
        ]
        
        self.stats = {
            'arp_packets': 1523,
            'mac_changes': 3,
            'alerts_raised': 2,
            'critical_alerts': 1
        }
    
    def initialize(self) -> None:
        """Initialize mock plugin."""
        logger.info("Mock ARP Spoofing Detector initialized")
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect mock data."""
        return self.get_data()
    
    def get_data(self) -> Dict[str, Any]:
        """Get mock detection data."""
        return {
            'monitoring': True,
            'arp_cache_size': 12,
            'alert_count': len(self.mock_alerts),
            'recent_alerts': self.mock_alerts,
            'stats': self.stats,
            'trusted_devices': ['aa:bb:cc:dd:ee:ff', '11:22:33:44:55:66']
        }
    
    def requires_root(self) -> bool:
        """Mock doesn't need root."""
        return False
    
    def start(self):
        """Mock start."""
        logger.info("Mock ARP Detector started")
    
    def stop(self):
        """Mock stop."""
        logger.info("Mock ARP Detector stopped")
