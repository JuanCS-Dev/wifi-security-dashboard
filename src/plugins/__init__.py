"""
Plugin system for WiFi Security Education Dashboard.

This package contains all data collection plugins.

Author: Juan-Dev - Soli Deo Gloria 
Date: 2025-11-09
"""

from .base import Plugin, PluginConfig, PluginStatus
from .system_plugin import SystemPlugin
from .network_plugin import NetworkPlugin
from .wifi_plugin import WiFiPlugin

__all__ = [
    "Plugin",
    "PluginConfig",
    "PluginStatus",
    "SystemPlugin",
    "NetworkPlugin",
    "WiFiPlugin",
]
