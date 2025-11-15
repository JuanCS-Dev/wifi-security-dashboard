"""
Global game state management.
Stores current network data, character states, quest progress, etc.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class NetworkState:
    """Current network data from plugins."""

    # WiFi
    ssid: str = "Unknown"
    signal_dbm: int = -100
    signal_percent: int = 0
    encryption: str = "None"
    channel: int = 0
    bssid: str = "00:00:00:00:00:00"

    # System
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    disk_percent: float = 0.0

    # Network traffic
    bandwidth_kbps: float = 0.0
    packets_total: int = 0
    packets_https: int = 0
    packets_http: int = 0

    # Threats
    rogue_aps_detected: List[str] = field(default_factory=list)
    arp_spoofing_active: bool = False
    weak_encryption: bool = False

    # Mode
    mock_mode: bool = False  # Educational mock mode flag

    # Timestamp
    last_updated: float = field(default_factory=lambda: datetime.now().timestamp())

    @property
    def signal_strength_category(self) -> str:
        """Categorize signal strength."""
        if self.signal_dbm >= -50:
            return "excellent"
        elif self.signal_dbm >= -60:
            return "good"
        elif self.signal_dbm >= -70:
            return "fair"
        else:
            return "weak"


@dataclass
class CharacterState:
    """State of a game character."""

    character_id: str
    health: float = 100.0
    mood: str = "idle"  # idle, alert, happy, worried
    position: tuple = (0, 0)
    current_action: Optional[str] = None


@dataclass
class GameState:
    """Complete game state."""

    # Network data
    network: NetworkState = field(default_factory=NetworkState)

    # Characters
    characters: Dict[str, CharacterState] = field(default_factory=dict)

    # Game progression
    current_scenario: Optional[str] = None
    scenarios_completed: List[str] = field(default_factory=list)
    total_xp: int = 0
    badges_earned: List[str] = field(default_factory=list)

    # Settings
    paused: bool = False
    mock_mode: bool = True

    def update_from_plugins(self, plugin_data: Dict[str, Any]) -> None:
        """
        Update network state from plugin data.

        Args:
            plugin_data: Dict with keys 'wifi', 'system', 'network', 'packets', 'threats'
        """
        # WiFi data
        if "wifi" in plugin_data:
            wifi = plugin_data["wifi"]
            self.network.ssid = wifi.get("ssid", "Unknown")
            self.network.signal_dbm = wifi.get("signal_strength_dbm", -100)
            self.network.signal_percent = wifi.get("signal_strength_percent", 0)
            self.network.encryption = wifi.get("security", "None")
            self.network.channel = wifi.get("channel", 0)
            self.network.bssid = wifi.get("bssid", "00:00:00:00:00:00")

        # System data
        if "system" in plugin_data:
            system = plugin_data["system"]
            self.network.cpu_percent = system.get("cpu_percent", 0.0)
            self.network.ram_percent = system.get("ram_percent", 0.0)
            self.network.disk_percent = system.get("disk_percent", 0.0)

        # Propagate mock mode flag
        self.network.mock_mode = self.mock_mode

        # Network traffic
        if "network" in plugin_data:
            network = plugin_data["network"]
            self.network.bandwidth_kbps = network.get("bandwidth_kbps", 0.0)

        # Packets
        if "packets" in plugin_data:
            packets = plugin_data["packets"]
            self.network.packets_total = packets.get("total", 0)

            protocols = packets.get("protocols", {})
            self.network.packets_https = protocols.get("HTTPS", 0)
            self.network.packets_http = protocols.get("HTTP", 0)

        # Threats
        if "threats" in plugin_data:
            threats = plugin_data["threats"]
            self.network.rogue_aps_detected = threats.get("rogue_aps", [])
            self.network.arp_spoofing_active = threats.get("arp_spoofing", False)
            self.network.weak_encryption = self.network.encryption in ["None", "WEP"]

        self.network.last_updated = datetime.now().timestamp()
