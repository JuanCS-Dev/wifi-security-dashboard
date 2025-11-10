"""
Sparkline Component - Display value trends with Unicode block characters

Sprint 3 - Phase 2.3: Implementation
Baseado em spike_sparkline.py validation e TDD tests.
"""

from typing import Optional
from collections import deque
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig


# Unicode block characters (8 níveis: baixo → alto)
SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"


class Sparkline(Component):
    """
    Sparkline component renders value trends using Unicode block chars.

    Displays historical values as a compact sparkline visualization
    using characters ▁▂▃▄▅▆▇█.

    Example config (dashboard.yml):
        components:
          - type: sparkline
            title: "CPU Trend"
            position: {x: 0, y: 0, width: 60, height: 5}
            rate_ms: 1000
            plugin: "system"
            data_field: "cpu_percent"
            extra:
              max_samples: 60
              label: "CPU"

    Renders as:
        ╭───────────────── CPU Trend ─────────────────╮
        │ CPU: ▂▄▃▆█▇▄▃▃▂▁▁▁▄▅▅▄▃ (48%)               │
        ╰─────────────────────────────────────────────╯
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize Sparkline component.

        Args:
            config: ComponentConfig dataclass
                Required:
                - type: ComponentType.SPARKLINE
                - title: str - Panel title
                - plugin: str - Plugin name
                - data_field: str - Numeric field to track

                Optional (via config.extra):
                - max_samples: int - Maximum history size (default: 40)
                - label: str - Label before sparkline (default: None)
        """
        super().__init__(config)

        # Extract Sparkline-specific config
        self.max_samples: int = config.extra.get("max_samples", 40)
        self.label: Optional[str] = config.extra.get("label", None)

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
        Render Sparkline as Rich Panel.

        Returns:
            Rich Panel with sparkline visualization
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
        Build content Text object with sparkline.

        Returns:
            Rich Text object with formatted sparkline
        """
        text = Text()

        # Add label if configured
        if self.label:
            text.append(f"{self.label}: ", style="bold white")

        # Render sparkline or "No data"
        if not self.history:
            text.append("No data yet", style="dim italic")
        else:
            sparkline = self._render_sparkline()
            text.append(sparkline, style=self.config.color)

            # Add current value
            if self.data is not None:
                text.append(f" ({self.data})", style="white")

        return text

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

    def _normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """
        Normalize value to 0-1 range.

        Args:
            value: Current value
            min_val: Minimum value in dataset
            max_val: Maximum value in dataset

        Returns:
            Float between 0.0 and 1.0
        """
        if max_val == min_val:
            return 0.5  # All values equal = middle

        return (value - min_val) / (max_val - min_val)

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
        normalized = self._normalize_value(value, min_val, max_val)

        # Map to index 0-7 (8 levels)
        index = int(normalized * 7)
        index = max(0, min(7, index))  # Clamp to 0-7

        return SPARKLINE_CHARS[index]
