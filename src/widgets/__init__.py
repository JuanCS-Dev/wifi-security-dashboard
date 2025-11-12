"""Textual widgets for WiFi Security Dashboard v3.0 - Sampler Style"""

from .network_chart import NetworkChart
from .packet_table import PacketTable
from .tooltip_widget import Tooltip, EducationalTip, get_tip, SECURITY_TIPS
from .system_widgets import (
    CPUWidget,
    RAMWidget,
    DiskWidget,
    NetworkStatsWidget,
    WiFiWidget,
    PacketStatsWidget
)

__all__ = [
    'NetworkChart',
    'PacketTable',
    'Tooltip',
    'EducationalTip',
    'get_tip',
    'SECURITY_TIPS',
    'CPUWidget',
    'RAMWidget',
    'DiskWidget',
    'NetworkStatsWidget',
    'WiFiWidget',
    'PacketStatsWidget',
]
