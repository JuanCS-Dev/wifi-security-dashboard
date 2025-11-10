"""
Textbox Component - Display single key-value pairs in Rich Panel

Sprint 3 - Phase 1.3: Implementation (REFATORADO)
Arquitetura correta: usa src.core.component.Component e ComponentConfig
"""

from typing import Any, Optional
from rich.panel import Panel
from rich.text import Text

from src.core.component import Component, ComponentConfig


class Textbox(Component):
    """
    Textbox component renders a single value in a Rich Panel.

    Displays key-value pairs with optional label and custom formatting.

    Example config (dashboard.yml):
        components:
          - type: textbox
            title: "CPU Usage"
            position: {x: 0, y: 0, width: 40, height: 5}
            rate_ms: 1000
            plugin: "system"
            data_field: "cpu_percent"
            extra:
              label: "CPU"
              format: "{value:.1f}%"

    Renders as:
        ╭──────────────── CPU Usage ────────────────╮
        │ CPU: 45.2%                                │
        ╰───────────────────────────────────────────╯
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize Textbox component.

        Args:
            config: ComponentConfig dataclass with configuration
                Required (via ComponentConfig):
                - type: "textbox"
                - title: str - Panel title
                - plugin: str - Plugin name
                - data_field: str - Field name in plugin data

                Optional (via config.extra):
                - label: str - Label to show before value (default: None)
                - format: str - Format string with {value} placeholder (default: None)
        """
        super().__init__(config)

        # Extract Textbox-specific config from extra
        self.label: Optional[str] = config.extra.get("label", None)
        self.format: Optional[str] = config.extra.get("format", None)

    def render(self) -> Panel:
        """
        Render Textbox as Rich Panel.

        Returns:
            Rich Panel with formatted value
        """
        # Build content
        content = self._build_content()

        # Create Panel
        panel = Panel(
            content,
            title=f"[bold]{self.config.title}[/bold]",
            border_style=self.config.color
        )

        return panel

    def _build_content(self) -> Text:
        """
        Build content Text object for Panel.

        Returns:
            Rich Text object with formatted value
        """
        content = Text()

        # Add label if configured
        if self.label:
            content.append(f"{self.label}: ", style="bold white")

        # Format and add value
        formatted_value = self._format_current_value()

        # Determine color based on value type
        value_color = self._get_value_color()
        content.append(formatted_value, style=value_color)

        return content

    def _format_current_value(self) -> str:
        """
        Format current value using format string or default formatting.

        Returns:
            Formatted string
        """
        if self.data is None:
            return "N/A"

        # Apply custom format string if provided
        if self.format:
            try:
                return self.format.format(value=self.data)
            except (ValueError, KeyError):
                # Fallback to default formatting on format error
                return self._format_value(self.data)

        # Use default formatting
        return self._format_value(self.data)

    def _get_value_color(self) -> str:
        """
        Determine color for value based on type and state.

        Returns:
            Color name for Rich styling
        """
        # N/A or missing data
        if self.data is None:
            return "dim italic"

        # Boolean values
        if isinstance(self.data, bool):
            return "green" if self.data else "red"

        # String values
        if isinstance(self.data, str):
            # Special keywords get colors
            lower_value = self.data.lower()
            if any(word in lower_value for word in ["error", "fail", "critical"]):
                return "red"
            if any(word in lower_value for word in ["warning", "warn"]):
                return "yellow"
            if any(word in lower_value for word in ["ok", "success", "running"]):
                return "green"
            return "cyan"

        # Numeric values - default white
        return "white"

    def _format_value(self, value: Any) -> str:
        """
        Format value with default logic.

        Args:
            value: Raw value from plugin data

        Returns:
            Formatted string for display
        """
        if value is None:
            return "N/A"

        # Boolean formatting with emoji
        if isinstance(value, bool):
            return "✅ Yes" if value else "❌ No"

        # String pass-through
        if isinstance(value, str):
            return value

        # Float formatting (1 decimal place)
        if isinstance(value, float):
            return f"{value:.1f}"

        # Integer and others
        return str(value)
