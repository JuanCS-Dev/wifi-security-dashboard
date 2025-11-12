"""
NetworkChart Widget - Real-time bandwidth monitoring

Displays RX/TX bandwidth in real-time using plotext charts.
Inspired by btop++ network graphs.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from collections import deque
from typing import Dict, Any

from textual.reactive import reactive
from textual_plotext import PlotextPlot


class NetworkChart(PlotextPlot):
    """
    Real-time network bandwidth chart widget.

    Displays two lines:
    - RX (Download) in cyan
    - TX (Upload) in yellow

    Features:
    - Circular buffer (60 points = 1 minute at 1Hz)
    - Auto-scaling Y-axis
    - Color-coded lines
    - Legend with current values
    """

    # Reactive attributes
    bandwidth_rx = reactive(0.0)
    bandwidth_tx = reactive(0.0)

    def __init__(self, **kwargs):
        """Initialize NetworkChart widget."""
        super().__init__(**kwargs)

        # Circular buffers for historical data (60 seconds at 1Hz)
        self.rx_history = deque([0.0] * 60, maxlen=60)
        self.tx_history = deque([0.0] * 60, maxlen=60)

        # X-axis (time in seconds, -60 to 0)
        self.time_axis = list(range(-60, 0))

    def on_mount(self) -> None:
        """Configure plot when widget is mounted."""
        # Configure theme (dark background)
        self.plt.theme("dark")

        # Note: Don't call refresh() here to avoid triggering watchers before mount complete

    def watch_bandwidth_rx(self, new_value: float) -> None:
        """React to bandwidth_rx changes."""
        self.rx_history.append(new_value)
        # refresh() called separately to avoid recursive loop

    def watch_bandwidth_tx(self, new_value: float) -> None:
        """React to bandwidth_tx changes."""
        self.tx_history.append(new_value)
        # refresh() called separately to avoid recursive loop

    def update_data(self, plugin_data: Dict[str, Any]) -> None:
        """
        Update chart with network plugin data.

        Args:
            plugin_data: Dict from NetworkPlugin with keys:
                - bandwidth_rx_mbps: float
                - bandwidth_tx_mbps: float
        """
        if 'network' in plugin_data:
            network_data = plugin_data['network']
            self.bandwidth_rx = network_data.get('bandwidth_rx_mbps', 0.0)
            self.bandwidth_tx = network_data.get('bandwidth_tx_mbps', 0.0)
            # Manually trigger plot refresh after both values updated
            self._refresh_plot()

    def on_resize(self) -> None:
        """Handle terminal resize."""
        self._refresh_plot()

    def _refresh_plot(self) -> None:
        """Refresh the plot with current data (internal method)."""
        # Clear previous plot
        self.plt.clear_figure()

        # Plot RX line (cyan)
        self.plt.plot(
            self.time_axis,
            list(self.rx_history),
            label=f"RX: {self.bandwidth_rx:.2f} Mbps",
            color="cyan",
            marker="braille"
        )

        # Plot TX line (yellow)
        self.plt.plot(
            self.time_axis,
            list(self.tx_history),
            label=f"TX: {self.bandwidth_tx:.2f} Mbps",
            color="yellow",
            marker="braille"
        )

        # Configure plot aesthetics
        self.plt.title("Network Bandwidth (Mbps)")
        self.plt.xlabel("Time (seconds)")
        self.plt.ylabel("Bandwidth (Mbps)")

        # Auto-scale Y-axis with minimum range
        max_value = max(max(self.rx_history), max(self.tx_history), 1.0)
        self.plt.ylim(0, max_value * 1.1)  # Add 10% headroom

        # Note: plotext doesn't have show_legend(), legend is shown automatically with labels

        # Trigger Textual refresh
        super().refresh()
