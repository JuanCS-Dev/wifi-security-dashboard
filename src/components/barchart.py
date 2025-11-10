"""
Barchart Component - Display categorical comparisons with ASCII bar charts

Sprint 3 - Fase 3.3: Implementation
Baseado em spike_barchart.py e TDD tests.
"""

from typing import List, Tuple, Dict, Any, Optional
import plotext as plt
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig


class Barchart(Component):
    """
    Barchart component renders categorical data as ASCII bar charts.

    Uses plotext library to generate terminal-based bar charts for
    comparing values across categories (e.g., top apps, device counts).

    Example config (dashboard.yml):
        components:
          - type: barchart
            title: "Top Network Apps"
            position: {x: 60, y: 27, width: 60, height: 10}
            rate_ms: 3000
            plugin: "network"
            data_field: "top_apps"
            color: "blue"
            extra:
              orientation: "horizontal"
              max_bars: 5
              max_label_length: 20

    Renders as:
        ╭──────── Top Network Apps ────────╮
        │   Chrome ███████████████ 150 MB  │
        │     Zoom ██████████ 120 MB       │
        │  Spotify ██████ 80 MB            │
        ╰──────────────────────────────────╯
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize Barchart component.

        Args:
            config: ComponentConfig dataclass
                Required:
                - type: ComponentType.BARCHART
                - title: str - Panel title
                - plugin: str - Plugin name
                - data_field: str - Field with dict or list of (label, value) pairs

                Optional (via config.extra):
                - orientation: str - "horizontal" or "vertical" (default: "horizontal")
                - max_bars: int - Max number of bars to display (default: 10)
                - max_label_length: int - Truncate labels to N chars (default: 30)
        """
        super().__init__(config)

        # Extract Barchart-specific config
        orientation = config.extra.get("orientation", "horizontal")
        # Validate orientation
        if orientation not in ["horizontal", "vertical"]:
            orientation = "horizontal"

        self.orientation: str = orientation
        self.max_bars: int = config.extra.get("max_bars", 10)
        self.max_label_length: int = config.extra.get("max_label_length", 30)

    def render(self) -> Panel:
        """
        Render Barchart as Rich Panel.

        Returns:
            Rich Panel with ASCII bar chart
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
        if self.data is None:
            return Text("No data yet", style="dim italic")

        # Process data into labels and values
        labels, values = self._process_data(self.data)

        if not labels:
            return Text("No data available", style="dim italic")

        # Truncate labels
        labels = self._truncate_labels(labels)

        # Render chart
        chart_str = self._render_chart(labels, values)

        if chart_str is None:
            return Text("No chart data", style="dim italic")

        return Text(chart_str)

    def _process_data(self, data: Any) -> Tuple[List[str], List[float]]:
        """
        Process data into labels and values lists.

        Args:
            data: Dict {label: value} or List [(label, value), ...]

        Returns:
            Tuple of (labels, values) lists, sorted by value descending,
            limited to max_bars
        """
        if data is None:
            return [], []

        # Handle dict input
        if isinstance(data, dict):
            if not data:
                return [], []

            # Sort by value descending and limit to max_bars
            sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
            sorted_items = sorted_items[:self.max_bars]

            labels = [str(label) for label, _ in sorted_items]
            values = [float(value) for _, value in sorted_items]

            return labels, values

        # Handle list of tuples input
        if isinstance(data, list):
            if not data:
                return [], []

            # Sort by value descending and limit to max_bars
            sorted_items = sorted(data, key=lambda x: x[1], reverse=True)
            sorted_items = sorted_items[:self.max_bars]

            labels = [str(label) for label, _ in sorted_items]
            values = [float(value) for _, value in sorted_items]

            return labels, values

        # Unknown format
        return [], []

    def _truncate_labels(self, labels: List[str]) -> List[str]:
        """
        Truncate long labels to max_label_length.

        Args:
            labels: List of label strings

        Returns:
            List of truncated labels
        """
        truncated = []
        for label in labels:
            if len(label) > self.max_label_length:
                # Truncate and add ellipsis
                truncated_label = label[:self.max_label_length - 3] + "..."
                truncated.append(truncated_label)
            else:
                truncated.append(label)

        return truncated

    def _render_chart(self, labels: List[str], values: List[float]) -> Optional[str]:
        """
        Render bar chart using plotext.

        Args:
            labels: Category labels
            values: Numeric values

        Returns:
            ASCII chart string or None if empty
        """
        if not labels or not values:
            return None

        # Clear previous plot
        plt.clf()

        # Set plot size based on component position
        width = self.config.position.width - 4  # Account for panel borders
        height = self.config.position.height - 4

        plt.plotsize(width, height)

        # Create bar chart
        plt.bar(labels, values, orientation=self.orientation)

        # Optional: set title (will be in panel title anyway)
        # plt.title(self.config.title)

        # Build and return ASCII string
        chart_str = plt.build()

        return chart_str
