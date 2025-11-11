"""
Sparkline Component Adapter for py_cui.

Adapter that converts Sparkline component to SparklineWidget.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import Any
from collections import deque
import py_cui

from src.adapters.component_adapter import ComponentAdapter


# Color mapping: component color name → py_cui color code
COLOR_MAP = {
    'green': py_cui.GREEN_ON_BLACK,
    'yellow': py_cui.YELLOW_ON_BLACK,
    'red': py_cui.RED_ON_BLACK,
    'cyan': py_cui.CYAN_ON_BLACK,
    'blue': py_cui.BLUE_ON_BLACK,
    'magenta': py_cui.MAGENTA_ON_BLACK,
    'white': py_cui.WHITE_ON_BLACK,
}


class SparklineAdapter(ComponentAdapter):
    """
    Adapter for Sparkline component → py_cui TextBlock.

    Uses py_cui's built-in TextBlock widget which supports dynamic text updates.

    Example:
        >>> from src.components.sparkline import Sparkline
        >>> component = Sparkline(config, plugin_manager)
        >>> adapter = SparklineAdapter(component)
        >>> widget = adapter.create_widget(pycui_root, row=0, col=0, row_span=10, col_span=40)
        >>> adapter.update_widget({'system': {'cpu_percent': 45.2}})
    """

    # Unicode sparkline chars
    SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"

    def __init__(self, component: Any):
        """
        Initialize adapter.

        Args:
            component: Sparkline component instance
        """
        super().__init__(component)

        # History buffer (maintained by adapter)
        max_samples = self.component.config.extra.get('max_samples', 40)
        self.history = deque(maxlen=max_samples)
        self.label = self.component.config.extra.get('label', None)

    def create_widget(
        self,
        pycui_root: py_cui.PyCUI,
        row: int,
        col: int,
        row_span: int,
        col_span: int
    ) -> Any:
        """
        Create py_cui TextBlock for sparkline display.

        Args:
            pycui_root: PyCUI root instance
            row: Starting grid row
            col: Starting grid column
            row_span: Number of rows to span
            col_span: Number of columns to span

        Returns:
            py_cui TextBlock widget
        """
        # Extract config
        title = self.component.config.title
        color_name = self.component.config.color

        # Use TextBlock (built-in py_cui widget with set_text() method)
        widget = pycui_root.add_text_block(
            title,
            row,
            col,
            row_span=row_span,
            column_span=col_span,
            padx=1,
            pady=0
        )

        # Set color
        pycui_color = COLOR_MAP.get(color_name, py_cui.GREEN_ON_BLACK)
        widget.set_color(pycui_color)

        # Set initial text
        widget.set_text("No data yet")

        # Store widget reference
        self.widget = widget

        return widget

    def update_widget(self, plugin_data: dict) -> None:
        """
        Update widget with new plugin data.

        Args:
            plugin_data: Dictionary of plugin data
                {
                    'plugin_name': {'field': value, ...},
                    ...
                }
        """
        if not self.widget:
            return

        # Get plugin name and field from component config
        plugin_name = self.component.config.plugin
        data_field = self.component.config.data_field

        # Extract value from plugin data
        if plugin_name not in plugin_data:
            return

        plugin_values = plugin_data[plugin_name]
        if data_field not in plugin_values:
            return

        value = plugin_values[data_field]

        # Add value to history
        try:
            val = float(value)
            self.history.append(val)
        except (ValueError, TypeError):
            return

        # Build sparkline text
        sparkline_text = self._build_sparkline_text(value)

        # Update widget text
        self.widget.set_text(sparkline_text)

    def _build_sparkline_text(self, current_value) -> str:
        """Build sparkline text with label and value."""
        parts = []

        # Add label
        if self.label:
            parts.append(f"{self.label}: ")

        # Add sparkline
        if self.history:
            sparkline = self._render_sparkline()
            parts.append(sparkline)

            # Add current value
            parts.append(f" ({current_value})")
        else:
            parts.append("No data yet")

        return "".join(parts)

    def _render_sparkline(self) -> str:
        """Render history as Unicode sparkline."""
        if not self.history:
            return ""

        min_val = min(self.history)
        max_val = max(self.history)

        return "".join(
            self._value_to_char(v, min_val, max_val)
            for v in self.history
        )

    def _value_to_char(self, value: float, min_val: float, max_val: float) -> str:
        """Convert value to Unicode sparkline char."""
        # Normalize to 0-1
        if max_val == min_val:
            normalized = 0.5
        else:
            normalized = (value - min_val) / (max_val - min_val)

        # Map to index 0-7
        index = int(normalized * 7)
        index = max(0, min(7, index))

        return self.SPARKLINE_CHARS[index]
