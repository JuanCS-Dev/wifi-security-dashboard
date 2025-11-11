"""
Visual Components for Dashboard v2.0

Sprint 3: Component Architecture
- Textbox (Rich Panel)
- Sparkline (Unicode chars)
- Barchart (plotext)
- Runchart (plotext)

Note: Base Component class is in src.core.component
"""

from src.components.textbox import Textbox
from src.components.sparkline import Sparkline
from src.components.barchart import Barchart
from src.components.runchart import Runchart
from src.components.packet_table import PacketTable

__all__ = [
    "Textbox",
    "Sparkline",
    "Barchart",
    "Runchart",
    "PacketTable",
]
