"""
Runchart Component - Display time series trends with ASCII line charts

Sprint 3 - Fase 4.3: Implementation
Baseado em spike_runchart.py e TDD tests.
"""

from typing import Optional
from collections import deque
import plotext as plt
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig


class Runchart(Component):
    """
    Runchart component renders time series data as ASCII line charts.

    Uses plotext library to generate terminal-based line charts showing
    value trends over time (e.g., CPU usage, WiFi signal, network throughput).

    Example config (dashboard.yml):
        components:
          - type: runchart
            title: "WiFi Signal Strength (dBm)"
            position: {x: 0, y: 0, width: 60, height: 12}
            rate_ms: 1000
            plugin: "wifi"
            data_field: "signal_strength_dbm"
            color: "green"
            extra:
              max_samples: 60
              marker: "dot"

    Renders as:
        ╭────── WiFi Signal Strength (dBm) ───────╮
        │     -30 ┤        ╭─╮                    │
        │         │       ╭╯ ╰╮                   │
        │     -50 ┤   ╭──╯    ╰─╮                 │
        │         │  ╭╯         ╰╮                │
        │     -70 ┤──╯            ╰───            │
        ╰─────────────────────────────────────────╯
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize Runchart component.

        Args:
            config: ComponentConfig dataclass
                Required:
                - type: ComponentType.RUNCHART
                - title: str - Panel title
                - plugin: str - Plugin name
                - data_field: str - Numeric field to track over time

                Optional (via config.extra):
                - max_samples: int - Maximum history size (default: 60)
                - marker: str - Plot marker style (default: "braille")
        """
        super().__init__(config)

        # Extract Runchart-specific config
        self.max_samples: int = config.extra.get("max_samples", 60)
        self.marker: str = config.extra.get("marker", "braille")

        # Circular buffer for value history
        self.history: deque = deque(maxlen=self.max_samples)

    def on_update(self) -> None:
        """
        Hook called after data update.

        Adds numeric values to history buffer. Non-numeric values ignored.
        """
        if self.data is None:
            return

        # Convert to float and add to history
        try:
            value = float(self.data)
            self.history.append(value)
        except (ValueError, TypeError):
            # Ignore non-numeric values
            pass

    def render(self) -> Panel:
        """
        Render Runchart as Rich Panel.

        Returns:
            Rich Panel with ASCII line chart
        """
        content = self._build_content()

        panel = Panel(
            content,
            title=f"[bold]{self.config.title}[/bold]",
            border_style=self.config.color
        )

        return panel

    def _build_content(self) -> Text:
        """
        Build content Text or string with chart.

        Returns:
            Rich Text object or chart string
        """
        if not self.history:
            return Text("No data yet", style="dim italic")

        # Render chart
        chart_str = self._render_chart()

        if chart_str is None:
            return Text("No chart data", style="dim italic")

        return Text(chart_str)

    def _render_chart(self) -> Optional[str]:
        """
        Render line chart using plotext.

        Returns:
            ASCII chart string or None if empty
        """
        if not self.history:
            return None

        # Clear previous plot
        plt.clf()

        # Set plot size based on component position
        width = self.config.position.width - 4  # Account for panel borders
        height = self.config.position.height - 4

        plt.plotsize(width, height)

        # Create time series (x-axis = indices)
        timestamps = list(range(len(self.history)))
        values = list(self.history)

        # Create line chart
        plt.plot(timestamps, values, marker=self.marker)

        # Optional: set labels
        # plt.xlabel("Time")
        # plt.ylabel("Value")

        # Build and return ASCII string
        chart_str = plt.build()

        return chart_str
