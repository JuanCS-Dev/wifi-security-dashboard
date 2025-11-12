"""Textual screens for WiFi Security Dashboard v3.0"""

from .landing_screen import LandingScreen
from .help_screen import HelpScreen
from .consolidated_dashboard import ConsolidatedDashboard
from .system_dashboard import SystemDashboard
from .network_dashboard import NetworkDashboard
from .wifi_dashboard import WiFiDashboard
from .packets_dashboard import PacketsDashboard

__all__ = [
    "LandingScreen",
    "HelpScreen",
    "ConsolidatedDashboard",
    "SystemDashboard",
    "NetworkDashboard",
    "WiFiDashboard",
    "PacketsDashboard",
]
