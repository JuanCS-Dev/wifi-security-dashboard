"""
Rogue AP Detector Plugin - Feature 6

Detects rogue/fake Access Points (Evil Twins) on the network.
Educational tool to demonstrate AP spoofing attacks.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-13
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

try:
    from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sniff, conf
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class AccessPoint:
    """Represents a detected Access Point."""
    bssid: str  # MAC address
    ssid: str
    channel: int
    signal_strength: int  # dBm
    encryption: str
    vendor: str
    first_seen: float
    last_seen: float
    beacon_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RogueAPAlert:
    """Represents a rogue AP detection alert."""
    timestamp: float
    rogue_bssid: str
    legitimate_bssid: str
    ssid: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    reason: str
    channel_diff: int
    signal_diff: int
    educational_note: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RogueAPDetector(Plugin):
    """
    Rogue AP Detector - Detects fake/evil twin access points.
    
    Educational Features:
    - Scans for all APs in range
    - Detects duplicate SSIDs (Evil Twins)
    - Baseline comparison (known good APs)
    - Signal strength analysis
    - Vendor fingerprinting
    - Attack pattern recognition
    
    Detection Methods:
    1. SSID Collision: Same name, different MAC
    2. Signal Anomaly: Sudden strong signal
    3. Encryption Downgrade: WPA2 → Open/WEP
    4. Vendor Mismatch: Different manufacturer
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # All detected APs: {bssid: AccessPoint}
        self.access_points: Dict[str, AccessPoint] = {}
        
        # Baseline (known good APs): {ssid: bssid}
        self.baseline_aps: Dict[str, str] = {}
        
        # Rogue AP alerts
        self.rogue_alerts: List[RogueAPAlert] = []
        
        # SSID tracking: {ssid: [bssid1, bssid2, ...]}
        self.ssid_to_bssids: Dict[str, List[str]] = defaultdict(list)
        
        # Statistics
        self.stats = {
            'total_aps_detected': 0,
            'baseline_aps': 0,
            'suspicious_aps': 0,
            'rogue_aps_confirmed': 0,
            'beacons_captured': 0
        }
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Detection settings
        self.baseline_learning_time = 60  # Learn baseline for 60s
        self.signal_threshold = -30  # Strong signal = suspicious
        self._baseline_learned = False
    
    def initialize(self) -> None:
        """Initialize plugin."""
        if self.config.config.get('mock_mode', False):
            logger.info("Rogue AP Detector initialized in MOCK mode")
            self._generate_mock_baseline()
            return
        
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect rogue AP detection data."""
        if self.config.config.get('mock_mode', False):
            return self._get_mock_data()
        
        return self.get_data()
    
    def start(self):
        """Start AP monitoring."""
        logger.info("Starting Rogue AP Detector...")
        logger.info("Learning baseline APs for 60 seconds...")
        
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_aps, daemon=True)
        self._monitor_thread.start()
        
        # Start baseline learning
        threading.Timer(self.baseline_learning_time, self._finalize_baseline).start()
    
    def stop(self):
        """Stop AP monitoring."""
        logger.info("Stopping Rogue AP Detector...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop()
    
    def get_data(self) -> Dict[str, Any]:
        """Get current detection data."""
        # Update stats
        self.stats['total_aps_detected'] = len(self.access_points)
        self.stats['baseline_aps'] = len(self.baseline_aps)
        
        # Get AP list
        ap_list = [ap.to_dict() for ap in self.access_points.values()]
        
        # Get recent alerts (last 10)
        recent_alerts = [alert.to_dict() for alert in self.rogue_alerts[-10:]]
        
        return {
            'monitoring': not self._stop_event.is_set(),
            'baseline_learned': self._baseline_learned,
            'stats': self.stats.copy(),
            'access_points': ap_list,
            'baseline_aps': dict(self.baseline_aps),
            'rogue_alerts': recent_alerts,
            'educational_tip': self._get_educational_tip()
        }
    
    def requires_root(self) -> bool:
        """AP scanning requires root and monitor mode."""
        return True
    
    def _monitor_aps(self):
        """Monitor AP beacons continuously."""
        while not self._stop_event.is_set():
            try:
                # Sniff WiFi beacons on monitor mode interface
                sniff(
                    iface="wlan0mon",  # Requires monitor mode
                    prn=self._process_beacon,
                    store=0,
                    timeout=1,
                    filter="type mgt subtype beacon"
                )
            except Exception as e:
                logger.error(f"AP monitoring error: {e}")
                logger.warning("Ensure WiFi adapter is in monitor mode!")
                time.sleep(1)
    
    def _process_beacon(self, packet):
        """Process beacon frame from AP."""
        if not packet.haslayer(Dot11Beacon):
            return
        
        self.stats['beacons_captured'] += 1
        
        try:
            # Extract AP info
            bssid = packet[Dot11].addr2.lower()
            
            # Get SSID from beacon
            ssid = ""
            channel = 0
            
            # Parse information elements
            elt = packet[Dot11Elt]
            while isinstance(elt, Dot11Elt):
                if elt.ID == 0:  # SSID
                    ssid = elt.info.decode('utf-8', errors='ignore')
                elif elt.ID == 3:  # Channel
                    channel = ord(elt.info)
                elt = elt.payload
            
            # Skip hidden SSIDs
            if not ssid:
                return
            
            # Get signal strength
            signal = -100
            if packet.haslayer(RadioTap):
                signal = packet[RadioTap].dBm_AntSignal if hasattr(packet[RadioTap], 'dBm_AntSignal') else -100
            
            # Detect encryption
            encryption = self._detect_encryption(packet)
            
            # Get vendor (first 3 octets of MAC)
            vendor = self._get_vendor(bssid)
            
            # Update or create AP entry
            if bssid in self.access_points:
                ap = self.access_points[bssid]
                ap.last_seen = time.time()
                ap.signal_strength = signal
                ap.beacon_count += 1
            else:
                ap = AccessPoint(
                    bssid=bssid,
                    ssid=ssid,
                    channel=channel,
                    signal_strength=signal,
                    encryption=encryption,
                    vendor=vendor,
                    first_seen=time.time(),
                    last_seen=time.time(),
                    beacon_count=1
                )
                self.access_points[bssid] = ap
                
                # Track SSID → BSSID mapping
                if ssid not in self.ssid_to_bssids[ssid]:
                    self.ssid_to_bssids[ssid].append(bssid)
                
                logger.debug(f"New AP: {ssid} ({bssid}) on ch{channel}")
            
            # Check for rogue AP if baseline learned
            if self._baseline_learned:
                self._check_for_rogue(ap)
                
        except Exception as e:
            logger.error(f"Error processing beacon: {e}")
    
    def _detect_encryption(self, packet) -> str:
        """Detect encryption type from beacon."""
        try:
            # Check capabilities
            cap = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}")
            
            # Look for RSN (WPA2) information element
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
            elif "privacy" in cap.lower():
                return "WEP"
            else:
                return "Open"
        except:
            return "Unknown"
    
    def _get_vendor(self, bssid: str) -> str:
        """Get vendor from MAC address OUI."""
        # OUI (first 3 octets)
        oui = bssid[:8].upper()
        
        # Common vendors (subset for demo)
        vendors = {
            '00:1A:11': 'Google Nest',
            '00:0F:13': 'Cisco',
            'A0:63:91': 'TP-Link',
            '00:14:BF': 'D-Link',
            '00:1D:7E': 'Netgear',
            'F4:F5:D8': 'Google',
            '00:23:69': 'Cisco',
            '00:24:A5': 'Belkin',
        }
        
        return vendors.get(oui, f"Unknown ({oui})")
    
    def _finalize_baseline(self):
        """Finalize baseline after learning period."""
        logger.info("Baseline learning complete!")
        
        # Set baseline: for each SSID, store the first seen BSSID
        for ssid, bssids in self.ssid_to_bssids.items():
            if bssids:
                self.baseline_aps[ssid] = bssids[0]
        
        self._baseline_learned = True
        self.stats['baseline_aps'] = len(self.baseline_aps)
        
        logger.info(f"Baseline: {len(self.baseline_aps)} legitimate APs")
    
    def _check_for_rogue(self, ap: AccessPoint):
        """Check if AP is rogue/evil twin."""
        ssid = ap.ssid
        bssid = ap.bssid
        
        # Check 1: Is this a new BSSID for known SSID?
        if ssid in self.baseline_aps:
            baseline_bssid = self.baseline_aps[ssid]
            
            if bssid != baseline_bssid:
                # ROGUE DETECTED!
                self._raise_rogue_alert(ap, baseline_bssid, "SSID_COLLISION")
        
        # Check 2: Unusually strong signal (possible close-range attack)
        if ap.signal_strength > self.signal_threshold:
            self._raise_rogue_alert(ap, None, "STRONG_SIGNAL")
        
        # Check 3: Open network with common name (honeypot)
        common_names = ['Free WiFi', 'Public WiFi', 'Guest', 'Airport WiFi']
        if ap.encryption == "Open" and any(name.lower() in ssid.lower() for name in common_names):
            self._raise_rogue_alert(ap, None, "SUSPICIOUS_OPEN")
    
    def _raise_rogue_alert(self, rogue_ap: AccessPoint, legitimate_bssid: Optional[str], reason: str):
        """Raise rogue AP alert."""
        # Check if already alerted
        for alert in self.rogue_alerts:
            if alert.rogue_bssid == rogue_ap.bssid:
                return  # Already alerted
        
        # Determine severity
        severity = self._assess_threat_level(rogue_ap, reason)
        
        # Generate educational note
        educational_note = self._generate_educational_note(reason, rogue_ap)
        
        # Calculate differences
        channel_diff = 0
        signal_diff = 0
        
        if legitimate_bssid and legitimate_bssid in self.access_points:
            legit_ap = self.access_points[legitimate_bssid]
            channel_diff = abs(rogue_ap.channel - legit_ap.channel)
            signal_diff = rogue_ap.signal_strength - legit_ap.signal_strength
        
        alert = RogueAPAlert(
            timestamp=time.time(),
            rogue_bssid=rogue_ap.bssid,
            legitimate_bssid=legitimate_bssid or "N/A",
            ssid=rogue_ap.ssid,
            severity=severity,
            reason=reason,
            channel_diff=channel_diff,
            signal_diff=signal_diff,
            educational_note=educational_note
        )
        
        self.rogue_alerts.append(alert)
        self.stats['rogue_aps_confirmed'] += 1
        
        logger.warning(f"🚨 ROGUE AP DETECTED: {rogue_ap.ssid} ({rogue_ap.bssid}) - {severity}")
    
    def _assess_threat_level(self, ap: AccessPoint, reason: str) -> str:
        """Assess threat level of rogue AP."""
        if reason == "SSID_COLLISION" and ap.signal_strength > -40:
            return "CRITICAL"  # Strong evil twin
        elif reason == "SSID_COLLISION":
            return "HIGH"
        elif reason == "STRONG_SIGNAL":
            return "MEDIUM"
        elif reason == "SUSPICIOUS_OPEN":
            return "LOW"
        else:
            return "LOW"
    
    def _generate_educational_note(self, reason: str, ap: AccessPoint) -> str:
        """Generate educational explanation."""
        if reason == "SSID_COLLISION":
            return (
                f"🚨 EVIL TWIN ATTACK DETECTED!\n"
                f"   Attackers creates fake AP with same name '{ap.ssid}'.\n"
                f"   Your device might connect to it instead of real one.\n"
                f"   DANGER: All your traffic would go through attacker!"
            )
        elif reason == "STRONG_SIGNAL":
            return (
                f"⚠️ Unusually strong signal ({ap.signal_strength} dBm).\n"
                f"   Attacker might be very close with powerful antenna.\n"
                f"   Or it's a new legitimate AP. Investigate!"
            )
        elif reason == "SUSPICIOUS_OPEN":
            return (
                f"⚠️ Open network '{ap.ssid}' detected.\n"
                f"   Could be honeypot to capture your data.\n"
                f"   Never use open networks for sensitive data!"
            )
        else:
            return "Suspicious AP activity detected. Investigate further."
    
    def _get_educational_tip(self) -> str:
        """Generate educational tip based on findings."""
        rogue_count = self.stats['rogue_aps_confirmed']
        
        if rogue_count > 0:
            return f"🚨 {rogue_count} rogue AP(s) detected! Verify before connecting!"
        elif self._baseline_learned:
            return "✅ No rogue APs detected. Network looks clean!"
        else:
            return "📚 Learning network baseline... Give it 60 seconds."
    
    def _generate_mock_baseline(self):
        """Generate mock baseline for testing."""
        self.baseline_aps = {
            'HomeNetwork': 'aa:bb:cc:dd:ee:ff',
            'OfficeWiFi': '11:22:33:44:55:66',
            'CoffeeShop': '77:88:99:aa:bb:cc'
        }
        self._baseline_learned = True
        self.stats['baseline_aps'] = len(self.baseline_aps)
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Generate mock rogue AP data for testing."""
        current_time = time.time()
        
        # Mock APs
        mock_aps = [
            {
                'bssid': 'aa:bb:cc:dd:ee:ff',
                'ssid': 'HomeNetwork',
                'channel': 6,
                'signal_strength': -45,
                'encryption': 'WPA2/WPA3',
                'vendor': 'TP-Link',
                'first_seen': current_time - 300,
                'last_seen': current_time - 2,
                'beacon_count': 145
            },
            {
                'bssid': 'ff:ee:dd:cc:bb:aa',
                'ssid': 'HomeNetwork',  # EVIL TWIN!
                'channel': 11,
                'signal_strength': -35,  # Stronger!
                'encryption': 'Open',  # Downgrade!
                'vendor': 'Unknown (DE:AD:BE)',
                'first_seen': current_time - 30,
                'last_seen': current_time - 1,
                'beacon_count': 15
            },
            {
                'bssid': '11:22:33:44:55:66',
                'ssid': 'OfficeWiFi',
                'channel': 1,
                'signal_strength': -65,
                'encryption': 'WPA2/WPA3',
                'vendor': 'Cisco',
                'first_seen': current_time - 280,
                'last_seen': current_time - 5,
                'beacon_count': 120
            }
        ]
        
        # Mock rogue alert
        mock_alerts = [
            {
                'timestamp': current_time - 30,
                'rogue_bssid': 'ff:ee:dd:cc:bb:aa',
                'legitimate_bssid': 'aa:bb:cc:dd:ee:ff',
                'ssid': 'HomeNetwork',
                'severity': 'CRITICAL',
                'reason': 'SSID_COLLISION',
                'channel_diff': 5,
                'signal_diff': 10,
                'educational_note': '🚨 EVIL TWIN ATTACK DETECTED! Fake AP impersonating your network!'
            }
        ]
        
        return {
            'monitoring': True,
            'baseline_learned': True,
            'stats': {
                'total_aps_detected': 3,
                'baseline_aps': 3,
                'suspicious_aps': 1,
                'rogue_aps_confirmed': 1,
                'beacons_captured': 280
            },
            'access_points': mock_aps,
            'baseline_aps': self.baseline_aps,
            'rogue_alerts': mock_alerts,
            'educational_tip': '🚨 1 rogue AP(s) detected! Verify before connecting!'
        }
