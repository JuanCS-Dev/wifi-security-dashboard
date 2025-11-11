"""
Textbox Component Adapter for py_cui.

Adapter that converts Textbox component to py_cui TextBlock widget.

Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 2 (Vitória Rápida)
"""

from typing import Any, Optional
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


class TextboxAdapter(ComponentAdapter):
    """
    Adapter for Textbox component → py_cui TextBlock.

    Textbox displays a single value (or key-value pair) in a simple text widget.
    Uses py_cui's TextBlock widget with dynamic text updates.

    Example:
        >>> from src.components.textbox import Textbox
        >>> component = Textbox(config)
        >>> adapter = TextboxAdapter(component)
        >>> widget = adapter.create_widget(pycui_root, row=0, col=0, row_span=5, col_span=40)
        >>> adapter.update_widget({'system': {'cpu_percent': 45.2}})
    """

    def __init__(self, component: Any):
        """
        Initialize adapter.

        Args:
            component: Textbox component instance
        """
        super().__init__(component)

        # Extract Textbox-specific config
        self.label: Optional[str] = component.config.extra.get('label', None)
        self.format: Optional[str] = component.config.extra.get('format', None)

    def create_widget(
        self,
        pycui_root: py_cui.PyCUI,
        row: int,
        col: int,
        row_span: int,
        col_span: int
    ) -> Any:
        """
        Create py_cui TextBlock for textbox display.

        Args:
            pycui_root: PyCUI root instance
            row: Starting grid row
            col: Starting grid column
            row_span: Number of rows to span
            col_span: Number of columns to span

        Returns:
            py_cui TextBlock widget
        """
        # Create TextBlock widget
        widget = pycui_root.add_text_block(
            title=self.component.config.title,
            row=row,
            column=col,
            row_span=row_span,
            column_span=col_span
        )

        # Set initial color if specified
        if self.component.config.color in COLOR_MAP:
            widget.set_color(COLOR_MAP[self.component.config.color])

        # Store widget reference
        self.widget = widget

        return widget

    def update_widget(self, plugin_data: dict) -> None:
        """
        Update widget with new plugin data.

        Extracts data from plugin_data and formats it for display.

        Args:
            plugin_data: Dictionary of plugin data
                {
                    'plugin_name': {'field': value, ...},
                    ...
                }
        """
        if not self.widget:
            return

        # Extract data from plugin
        plugin_name = self.component.config.plugin
        data_field = self.component.config.data_field

        if plugin_name not in plugin_data:
            self.widget.set_text("N/A - Plugin not available")
            return

        plugin_vals = plugin_data[plugin_name]

        if data_field not in plugin_vals:
            self.widget.set_text(f"N/A - Field '{data_field}' not found")
            return

        value = plugin_vals[data_field]

        # Build formatted text
        text = self._format_value(value)

        # Update widget
        self.widget.set_text(text)

    def _format_value(self, value: Any) -> str:
        """
        Format value for display.

        Applies label and format string if configured.

        Args:
            value: Value to format

        Returns:
            Formatted string
        """
        # Apply format string if configured
        if self.format:
            try:
                formatted = self.format.format(value=value)
            except (KeyError, ValueError, TypeError):
                # Fallback if format fails
                formatted = str(value)
        else:
            formatted = str(value)

        # Add label if configured
        if self.label:
            text = f"{self.label}: {formatted}"
        else:
            text = formatted

        return text

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"TextboxAdapter("
            f"component={self.component.config.title}, "
            f"label={self.label}, "
            f"format={self.format})"
        )
