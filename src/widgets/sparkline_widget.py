"""
Sparkline Widget for py_cui.

Custom widget that displays value trends using Unicode block characters.
Integrates existing Sparkline component logic with py_cui rendering.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import Optional
from collections import deque
import py_cui


# Unicode block characters (8 levels: low → high)
SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"


class SparklineWidget(py_cui.widgets.Widget):
    """
    py_cui widget for sparkline visualization.

    Displays historical values as compact sparkline using Unicode chars ▁▂▃▄▅▆▇█.

    Example:
        CPU: ▂▄▃▆█▇▄▃▃▂▁▁▁▄▅▅▄▃ (48%)
    """

    def __init__(
        self,
        id,
        title,
        grid,
        row,
        column,
        row_span,
        column_span,
        padx,
        pady,
        max_samples=40,
        label=None,
        **kwargs  # Accept any extra kwargs from py_cui
    ):
        """
        Initialize sparkline widget.

        Args:
            id: Widget ID
            title: Widget title (displayed in border)
            grid: Parent grid
            row: Starting row
            column: Starting column
            row_span: Number of rows to span
            column_span: Number of columns to span
            padx: Horizontal padding
            pady: Vertical padding
            max_samples: Maximum history size
            label: Label before sparkline (e.g., "CPU")
            **kwargs: Extra arguments from py_cui (ignored)
        """
        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady)

        # Sparkline config
        self.max_samples = max_samples
        self.label = label

        # Value history
        self.history = deque(maxlen=max_samples)

        # Current value (for display)
        self.current_value = None

        # Color (py_cui color code)
        self._color = py_cui.GREEN_ON_BLACK

    def set_color(self, color_code):
        """
        Set sparkline color.

        Args:
            color_code: py_cui color code (e.g., py_cui.GREEN_ON_BLACK)
        """
        self._color = color_code

    def add_value(self, value):
        """
        Add value to history.

        Args:
            value: Numeric value to add
        """
        try:
            val = float(value)
            self.history.append(val)
            self.current_value = value
        except (ValueError, TypeError):
            # Ignore non-numeric
            pass

    def clear_history(self):
        """Clear value history."""
        self.history.clear()
        self.current_value = None

    def _draw(self):
        """
        Draw sparkline widget.

        Called by py_cui rendering loop.
        """
        # Clear widget area
        super()._draw()

        # Get drawable area (inside borders)
        start_y = self.start_y + self.pady + 1  # +1 for top border
        start_x = self.start_x + self.padx + 1  # +1 for left border
        height = self.height - 2  # Account for borders
        width = self.width - 2

        # Draw sparkline content
        if not self.history:
            # No data yet
            text = "No data yet"
            self._renderer.draw_text(
                self,
                text,
                start_y,
                start_x,
                selected=self._selected
            )
        else:
            # Build sparkline text
            sparkline_text = self._build_sparkline_text()

            # Draw on first content line
            self._renderer.draw_text(
                self,
                sparkline_text,
                start_y,
                start_x,
                color=self._color,
                selected=self._selected
            )

    def _build_sparkline_text(self) -> str:
        """
        Build sparkline text with label and current value.

        Returns:
            Formatted string like "CPU: ▁▂▃▄▅▆▇█ (48%)"
        """
        parts = []

        # Add label
        if self.label:
            parts.append(f"{self.label}: ")

        # Add sparkline
        sparkline = self._render_sparkline()
        parts.append(sparkline)

        # Add current value
        if self.current_value is not None:
            parts.append(f" ({self.current_value})")

        return "".join(parts)

    def _render_sparkline(self) -> str:
        """
        Render history values as Unicode sparkline.

        Returns:
            String with Unicode block characters ▁▂▃▄▅▆▇█
        """
        if not self.history:
            return ""

        min_val = min(self.history)
        max_val = max(self.history)

        return "".join(
            self._value_to_char(v, min_val, max_val)
            for v in self.history
        )

    def _value_to_char(self, value: float, min_val: float, max_val: float) -> str:
        """
        Convert numeric value to Unicode sparkline character.

        Args:
            value: Value to convert
            min_val: Minimum value in range
            max_val: Maximum value in range

        Returns:
            Unicode character from ▁▂▃▄▅▆▇█
        """
        # Normalize to 0-1
        if max_val == min_val:
            normalized = 0.5  # All equal = middle
        else:
            normalized = (value - min_val) / (max_val - min_val)

        # Map to index 0-7 (8 levels)
        index = int(normalized * 7)
        index = max(0, min(7, index))  # Clamp

        return SPARKLINE_CHARS[index]

    def _handle_key_press(self, key_pressed):
        """
        Handle key press events.

        Args:
            key_pressed: Key code

        Note:
            Sparkline is read-only, no special key handling needed.
        """
        # No special key handling for sparkline (read-only)
        return
