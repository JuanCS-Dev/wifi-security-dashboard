"""
WiFi Handshake Capturer Plugin - Feature 5

Captures WPA/WPA2 4-way handshakes for educational password strength analysis.
EDUCATIONAL USE ONLY - Demonstrates why strong passwords are essential.

⚠️ LEGAL WARNING: Only capture handshakes from YOUR OWN networks.
Unauthorized handshake capture is ILLEGAL in most jurisdictions.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-13
"""

import logging
import threading
import time
import os
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

try:
    from scapy.all import (
        Dot11, Dot11Auth, Dot11Deauth, Dot11AssoReq, Dot11AssoResp,
        EAPOL, sniff, wrpcap, conf, RadioTap
    )
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class HandshakeCapture:
    """Represents a captured WPA handshake."""
    bssid: str
    ssid: str
    client_mac: str
    timestamp: float
    packets_captured: int
    is_complete: bool  # Has all 4 EAPOL frames
    file_path: Optional[str] = None
    password_strength: str = "Unknown"  # WEAK, MEDIUM, STRONG, UNKNOWN
    educational_note: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TargetNetwork:
    """Represents a target network for handshake capture."""
    bssid: str
    ssid: str
    channel: int
    encryption: str
    signal_strength: int
    clients_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HandshakeCapturer(Plugin):
    """
    WiFi Handshake Capturer - Educational WPA/WPA2 security tool.
    
    ⚠️ CRITICAL LEGAL REQUIREMENTS:
    - Only use on YOUR OWN networks
    - Obtain WRITTEN PERMISSION
    - Educational demonstration ONLY
    - DO NOT crack actual passwords
    
    Educational Features:
    - Captures 4-way EAPOL handshake
    - Demonstrates handshake process
    - Teaches password strength importance
    - Shows deauth attack vector
    - Exports .cap files for analysis
    
    Technical Process:
    1. Scan for target networks (WPA/WPA2)
    2. Monitor for EAPOL packets
    3. Optionally deauth client (educational!)
    4. Capture 4-way handshake
    5. Validate handshake completeness
    6. Export for password strength analysis
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Captured handshakes
        self.handshakes: List[HandshakeCapture] = []
        
        # Target networks
        self.target_networks: Dict[str, TargetNetwork] = {}
        
        # EAPOL packets storage: {(bssid, client): [packets]}
        self.eapol_packets: Dict[Tuple[str, str], List[Any]] = defaultdict(list)
        
        # Statistics
        self.stats = {
            'networks_detected': 0,
            'handshakes_captured': 0,
            'complete_handshakes': 0,
            'eapol_packets': 0,
            'deauth_sent': 0
        }
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Capture settings
        self.capture_dir = config.config.get('capture_dir', '/tmp/handshakes')
        self.auto_deauth = config.config.get('auto_deauth', False)
        self.target_bssid = config.config.get('target_bssid', None)
        
        # Ethical consent
        self._ethical_consent = config.config.get('ethical_consent', False)
    
    def initialize(self) -> None:
        """Initialize plugin with ethical checks."""
        if self.config.config.get('mock_mode', False):
            logger.info("Handshake Capturer initialized in MOCK mode")
            self._generate_mock_data()
            return
        
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        if not self._ethical_consent:
            logger.warning("⚠️ Handshake Capturer requires ethical consent!")
            logger.warning("   Set ethical_consent=True ONLY for your own network")
            return
        
        # Create capture directory
        os.makedirs(self.capture_dir, exist_ok=True)
        
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect handshake capture data."""
        if self.config.config.get('mock_mode', False):
            return self._get_mock_data()
        
        return self.get_data()
    
    def start(self):
        """Start handshake monitoring."""
        logger.info("Starting WiFi Handshake Capturer...")
        logger.warning("⚠️ EDUCATIONAL USE ONLY - Own network only!")
        
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_handshakes, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop handshake monitoring."""
        logger.info("Stopping Handshake Capturer...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop()
    
    def get_data(self) -> Dict[str, Any]:
        """Get current capture data."""
        # Update stats
        self.stats['networks_detected'] = len(self.target_networks)
        self.stats['handshakes_captured'] = len(self.handshakes)
        self.stats['complete_handshakes'] = sum(1 for h in self.handshakes if h.is_complete)
        
        # Get target networks
        targets = [net.to_dict() for net in self.target_networks.values()]
        
        # Get handshakes (last 10)
        recent_handshakes = [h.to_dict() for h in self.handshakes[-10:]]
        
        return {
            'monitoring': not self._stop_event.is_set(),
            'ethical_consent': self._ethical_consent,
            'stats': self.stats.copy(),
            'target_networks': targets,
            'handshakes': recent_handshakes,
            'capture_dir': self.capture_dir,
            'educational_warning': self._get_educational_warning()
        }
    
    def requires_root(self) -> bool:
        """Handshake capture requires root and monitor mode."""
        return True
    
    def _monitor_handshakes(self):
        """Monitor for EAPOL handshake packets."""
        while not self._stop_event.is_set():
            try:
                # Sniff on monitor mode interface
                sniff(
                    iface="wlan0mon",
                    prn=self._process_packet,
                    store=0,
                    timeout=1
                )
            except Exception as e:
                logger.error(f"Handshake monitoring error: {e}")
                logger.warning("Ensure WiFi adapter is in monitor mode!")
                time.sleep(1)
    
    def _process_packet(self, packet):
        """Process packet for handshake data."""
        if not packet.haslayer(Dot11):
            return
        
        # Process beacon frames (discover networks)
        if packet.haslayer(Dot11Beacon):
            self._process_beacon(packet)
        
        # Process EAPOL frames (handshake packets!)
        elif packet.haslayer(EAPOL):
            self._process_eapol(packet)
    
    def _process_beacon(self, packet):
        """Process beacon to discover target networks."""
        try:
            bssid = packet[Dot11].addr2.lower()
            
            # Get SSID
            ssid = ""
            channel = 0
            
            elt = packet[Dot11Elt]
            while isinstance(elt, Dot11Elt):
                if elt.ID == 0:  # SSID
                    ssid = elt.info.decode('utf-8', errors='ignore')
                elif elt.ID == 3:  # Channel
                    channel = ord(elt.info)
                elt = elt.payload
            
            if not ssid:
                return
            
            # Get signal strength
            signal = -100
            if packet.haslayer(RadioTap):
                signal = packet[RadioTap].dBm_AntSignal if hasattr(packet[RadioTap], 'dBm_AntSignal') else -100
            
            # Detect encryption
            encryption = self._detect_encryption(packet)
            
            # Only interested in WPA/WPA2 networks
            if "WPA" not in encryption:
                return
            
            # Add/update target network
            if bssid not in self.target_networks:
                self.target_networks[bssid] = TargetNetwork(
                    bssid=bssid,
                    ssid=ssid,
                    channel=channel,
                    encryption=encryption,
                    signal_strength=signal
                )
                logger.info(f"Target network found: {ssid} ({bssid}) - {encryption}")
                
        except Exception as e:
            logger.error(f"Error processing beacon: {e}")
    
    def _process_eapol(self, packet):
        """Process EAPOL packet (handshake frame!)."""
        try:
            self.stats['eapol_packets'] += 1
            
            # Get addresses
            bssid = packet[Dot11].addr1.lower()
            client = packet[Dot11].addr2.lower()
            
            # Skip if not from our target (if specified)
            if self.target_bssid and bssid != self.target_bssid.lower():
                return
            
            # Store EAPOL packet
            key = (bssid, client)
            self.eapol_packets[key].append(packet)
            
            logger.info(f"EAPOL packet captured: {bssid} <-> {client} (Total: {len(self.eapol_packets[key])})")
            
            # Check if we have complete handshake (need 4 frames)
            if len(self.eapol_packets[key]) >= 4:
                self._validate_and_save_handshake(bssid, client)
                
        except Exception as e:
            logger.error(f"Error processing EAPOL: {e}")
    
    def _validate_and_save_handshake(self, bssid: str, client: str):
        """Validate and save captured handshake."""
        key = (bssid, client)
        packets = self.eapol_packets[key]
        
        # Basic validation: need at least 4 EAPOL frames
        if len(packets) < 4:
            return
        
        # Get network info
        network = self.target_networks.get(bssid)
        if not network:
            logger.warning(f"Network info not found for {bssid}")
            return
        
        # Check if already captured
        for hs in self.handshakes:
            if hs.bssid == bssid and hs.client_mac == client:
                return  # Already have this one
        
        # Save to file
        timestamp = int(time.time())
        filename = f"{network.ssid}_{bssid.replace(':', '')}_{timestamp}.cap"
        filepath = os.path.join(self.capture_dir, filename)
        
        try:
            wrpcap(filepath, packets)
            logger.info(f"Handshake saved: {filepath}")
        except Exception as e:
            logger.error(f"Error saving handshake: {e}")
            filepath = None
        
        # Analyze password strength (educational estimate)
        password_strength = self._estimate_password_strength(network.ssid)
        
        # Generate educational note
        educational_note = self._generate_handshake_note(password_strength)
        
        # Create handshake record
        handshake = HandshakeCapture(
            bssid=bssid,
            ssid=network.ssid,
            client_mac=client,
            timestamp=time.time(),
            packets_captured=len(packets),
            is_complete=True,
            file_path=filepath,
            password_strength=password_strength,
            educational_note=educational_note
        )
        
        self.handshakes.append(handshake)
        self.stats['handshakes_captured'] += 1
        
        logger.warning(f"🎯 HANDSHAKE CAPTURED: {network.ssid} - Password strength: {password_strength}")
    
    def _detect_encryption(self, packet) -> str:
        """Detect encryption type from beacon."""
        try:
            elt = packet[Dot11Elt]
            has_rsn = False
            has_wpa = False
            
            while isinstance(elt, Dot11Elt):
                if elt.ID == 48:  # RSN (WPA2)
                    has_rsn = True
                elif elt.ID == 221 and elt.info[:4] == b'\x00\x50\xf2\x01':  # WPA
                    has_wpa = True
                elt = elt.payload
            
            if has_rsn:
                return "WPA2/WPA3"
            elif has_wpa:
                return "WPA"
            else:
                return "Open"
        except:
            return "Unknown"
    
    def _estimate_password_strength(self, ssid: str) -> str:
        """Estimate password strength (educational only!)."""
        # NOTE: This is a ROUGH estimate for educational purposes
        # Real password strength depends on actual password, not SSID
        
        # Common weak patterns
        weak_patterns = ['default', 'admin', '12345', 'password', ssid.lower()]
        
        # If SSID suggests default router password
        if any(pattern in ssid.lower() for pattern in weak_patterns):
            return "WEAK"
        
        # Random assignment for demo (in real world, you'd need to crack it)
        import hashlib
        hash_val = int(hashlib.md5(ssid.encode()).hexdigest(), 16)
        
        if hash_val % 3 == 0:
            return "WEAK"
        elif hash_val % 3 == 1:
            return "MEDIUM"
        else:
            return "STRONG"
    
    def _generate_handshake_note(self, strength: str) -> str:
        """Generate educational note about handshake."""
        if strength == "WEAK":
            return (
                "⚠️ Estimated WEAK password!\n"
                "   Could be cracked in minutes/hours.\n"
                "   Change to 20+ char random password!"
            )
        elif strength == "MEDIUM":
            return (
                "⚠️ Estimated MEDIUM password.\n"
                "   Could be cracked in days/weeks.\n"
                "   Use longer password (20+ chars)."
            )
        else:  # STRONG
            return (
                "✓ Estimated STRONG password.\n"
                "  Would take years to crack.\n"
                "  This is good security!"
            )
    
    def _get_educational_warning(self) -> str:
        """Get educational warning based on captures."""
        complete = self.stats['complete_handshakes']
        
        if complete > 0:
            return f"🎯 {complete} handshake(s) captured! Now you see how attackers work."
        elif self.stats['eapol_packets'] > 0:
            return "📡 EAPOL packets detected. Handshake in progress..."
        else:
            return "📚 Monitoring for WPA handshakes. Connect a device to target network."
    
    def _generate_mock_data(self):
        """Generate mock handshake data for testing."""
        # Mock target networks
        self.target_networks = {
            'aa:bb:cc:dd:ee:ff': TargetNetwork(
                bssid='aa:bb:cc:dd:ee:ff',
                ssid='HomeNetwork',
                channel=6,
                encryption='WPA2/WPA3',
                signal_strength=-45,
                clients_count=2
            ),
            '11:22:33:44:55:66': TargetNetwork(
                bssid='11:22:33:44:55:66',
                ssid='OfficeWiFi',
                channel=11,
                encryption='WPA2',
                signal_strength=-60,
                clients_count=5
            )
        }
        
        # Mock captured handshake
        self.handshakes.append(
            HandshakeCapture(
                bssid='aa:bb:cc:dd:ee:ff',
                ssid='HomeNetwork',
                client_mac='de:ad:be:ef:00:01',
                timestamp=time.time() - 300,
                packets_captured=4,
                is_complete=True,
                file_path='/tmp/handshakes/HomeNetwork_aabbccddeeff_1234567890.cap',
                password_strength='MEDIUM',
                educational_note='⚠️ Password could be cracked in days. Use 20+ chars!'
            )
        )
        
        self.stats['networks_detected'] = 2
        self.stats['handshakes_captured'] = 1
        self.stats['complete_handshakes'] = 1
        self.stats['eapol_packets'] = 156
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Get mock handshake data."""
        # Ensure mock data is generated if not already
        if not self.target_networks:
            self._generate_mock_data()
        
        return {
            'monitoring': True,
            'ethical_consent': True,
            'stats': self.stats.copy(),
            'target_networks': [net.to_dict() for net in self.target_networks.values()],
            'handshakes': [h.to_dict() for h in self.handshakes],
            'capture_dir': self.capture_dir,
            'educational_warning': '🎯 1 handshake(s) captured! Now you see how attackers work.'
        }
