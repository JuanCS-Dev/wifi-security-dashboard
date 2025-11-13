"""Textual screens for WiFi Security Dashboard v3.0 - Sampler Style"""

from .landing_screen import LandingScreen
from .help_screen import HelpScreen
from .tutorial_screen import TutorialScreen
from .consolidated_dashboard import ConsolidatedDashboardV2 as ConsolidatedDashboard
from .system_dashboard import SystemDashboard
from .network_dashboard import NetworkDashboard
from .wifi_dashboard import WiFiDashboard
from .packets_dashboard import PacketsDashboard
from .topology_dashboard import TopologyDashboard
from .arp_detector_dashboard import ARPDetectorDashboard
from .traffic_dashboard import TrafficDashboard
from .dns_dashboard import DNSDashboard
from .http_sniffer_dashboard import HTTPSnifferDashboard
from .rogue_ap_dashboard import RogueAPDashboard
from .handshake_dashboard import HandshakeDashboard

__all__ = [
    "LandingScreen",
    "HelpScreen",
    "TutorialScreen",
    "ConsolidatedDashboard",
    "SystemDashboard",
    "NetworkDashboard",
    "WiFiDashboard",
    "PacketsDashboard",
    "TopologyDashboard",
    "ARPDetectorDashboard",
    "TrafficDashboard",
    "DNSDashboard",
    "HTTPSnifferDashboard",
    "RogueAPDashboard",
    "HandshakeDashboard",
]
