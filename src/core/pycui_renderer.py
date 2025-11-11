"""
PyCUI-based Dashboard Renderer.

Provides pixel-perfect grid positioning using py_cui (curses-based TUI library).
Replaces GridRenderer (ANSI-based) with proper cell-based rendering.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import List, Dict, Optional, Any
import py_cui

from src.utils.coordinate_converter import CoordinateConverter, Position, GridPosition
from src.adapters.component_adapter import ComponentAdapter


class PyCUIRenderer:
    """
    Renders dashboard components using py_cui grid system.

    Provides Sampler-style pixel-perfect rendering by:
    1. Creating py_cui root with fine grid (1 cell = 1 character)
    2. Converting component positions to grid coordinates
    3. Creating widgets via adapters
    4. Updating widgets with plugin data

    Example:
        >>> renderer = PyCUIRenderer(width=160, height=60)
        >>> renderer.add_component(component, adapter)
        >>> renderer.start()  # Blocks until quit
    """

    def __init__(self, width: int = 160, height: int = 60):
        """
        Initialize py_cui renderer.

        Args:
            width: Terminal width in characters
            height: Terminal height in lines

        Note:
            Uses fine grid (rows=height, cols=width) for pixel-perfect
            positioning where 1 grid cell = 1 terminal character.
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Terminal dimensions must be > 0, got ({width}x{height})")

        self.width = width
        self.height = height

        # Create fine grid (1 cell = 1 char) for maximum precision
        self.grid_rows = height
        self.grid_cols = width

        # Create PyCUI root with fine grid
        self.root = py_cui.PyCUI(self.grid_rows, self.grid_cols)

        # Set terminal to exact size
        self.root.toggle_unicode_borders()  # Enable Unicode box-drawing chars

        # Initialize coordinate converter
        self.converter = CoordinateConverter(
            terminal_width=width,
            terminal_height=height,
            grid_rows=self.grid_rows,
            grid_cols=self.grid_cols
        )

        # Store adapters for updates
        self.adapters: List[ComponentAdapter] = []

        # Plugin manager reference (set externally)
        self.plugin_manager: Optional[Any] = None

        # Update callback
        self._update_callback = None

    def set_plugin_manager(self, plugin_manager: Any) -> None:
        """
        Set plugin manager for data updates.

        Args:
            plugin_manager: PluginManager instance
        """
        self.plugin_manager = plugin_manager

    def set_update_callback(self, callback) -> None:
        """
        Set callback function to update components.

        Args:
            callback: Function to call before each draw (e.g., dashboard.update_components)
        """
        self._update_callback = callback

    def add_component(self, component: Any, adapter: ComponentAdapter) -> None:
        """
        Add component with its adapter to renderer.

        Args:
            component: Component instance
            adapter: ComponentAdapter instance for this component

        Note:
            Component must have config.position with (x, y, width, height).
            Adapter will create corresponding py_cui widget.
        """
        # Get component position
        pos = Position(
            x=component.config.position.x,
            y=component.config.position.y,
            width=component.config.position.width,
            height=component.config.position.height
        )

        # Convert to grid coordinates
        grid_pos = self.converter.to_grid(pos)

        # Create widget via adapter
        widget = adapter.create_widget(
            self.root,
            row=grid_pos.row,
            col=grid_pos.col,
            row_span=grid_pos.row_span,
            col_span=grid_pos.col_span
        )

        # Store adapter for updates
        self.adapters.append(adapter)

    def _on_draw(self) -> None:
        """
        Callback called before each frame draw.

        Updates all widgets with latest plugin data.
        """
        # Call external update callback if set (e.g., dashboard.update_components)
        if self._update_callback:
            self._update_callback()

        # Get all plugin data
        if not self.plugin_manager:
            return

        plugin_data = self.plugin_manager.get_all_plugin_data()

        # Update all adapters/widgets
        for adapter in self.adapters:
            try:
                adapter.update_widget(plugin_data)
            except Exception as e:
                # Silently skip errors (logged elsewhere)
                pass

    def set_refresh_rate(self, rate_ms: int) -> None:
        """
        Set refresh rate for updates.

        Args:
            rate_ms: Refresh interval in milliseconds
        """
        # Convert ms to seconds for py_cui
        rate_seconds = rate_ms / 1000.0
        self.root.set_refresh_timeout(rate_seconds)

    def start(self) -> None:
        """
        Start py_cui event loop (blocking).

        This will take over terminal and run until user quits (q key).
        Sets up draw callback and refresh rate.
        """
        # Set draw callback
        self.root.set_on_draw_update_func(self._on_draw)

        # Set title bar
        self.root.set_title("WiFi Security Education Dashboard")

        # Set status bar
        self.root.set_status_bar_text("Press 'q' to quit | Soli Deo Gloria ✝️")

        # Start event loop (blocks until quit)
        self.root.start()

    def clear(self) -> None:
        """
        Clear all widgets from renderer.

        Note:
            py_cui doesn't have explicit clear like GridRenderer.
            Widgets persist until manually removed.
        """
        # py_cui widgets persist - no need to clear each frame
        pass

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"PyCUIRenderer("
            f"size={self.width}x{self.height}, "
            f"grid={self.grid_cols}x{self.grid_rows}, "
            f"adapters={len(self.adapters)})"
        )


class PyCUIDashboardRenderer:
    """
    High-level wrapper for PyCUIRenderer.

    Provides interface similar to GridDashboardRenderer for easy migration.

    Example:
        >>> renderer = PyCUIDashboardRenderer(width=160, height=60)
        >>> for component in dashboard.components:
        ...     adapter = create_adapter(component)  # Factory method
        ...     renderer.add_from_component(component, adapter)
        >>> renderer.set_plugin_manager(dashboard.plugin_manager)
        >>> renderer.start()
    """

    def __init__(self, width: Optional[int] = None, height: Optional[int] = None):
        """
        Initialize dashboard renderer.

        Args:
            width: Terminal width (None = auto-detect, not supported yet)
            height: Terminal height (None = auto-detect, not supported yet)

        Note:
            Auto-detection not supported in py_cui - must provide explicit size.
        """
        if width is None or height is None:
            # Default to standard dashboard size
            width = width or 160
            height = height or 60

        self.renderer = PyCUIRenderer(width, height)

    def add_from_component(self, component: Any, adapter: ComponentAdapter) -> None:
        """
        Add component using its Position config and adapter.

        Args:
            component: Component instance with config.position
            adapter: ComponentAdapter for this component type
        """
        self.renderer.add_component(component, adapter)

    def set_plugin_manager(self, plugin_manager: Any) -> None:
        """Set plugin manager for data updates."""
        self.renderer.set_plugin_manager(plugin_manager)

    def set_update_callback(self, callback) -> None:
        """Set callback to update components before each draw."""
        self.renderer.set_update_callback(callback)

    def set_refresh_rate(self, rate_ms: int) -> None:
        """Set refresh rate in milliseconds."""
        self.renderer.set_refresh_rate(rate_ms)

    def start(self) -> None:
        """Start py_cui event loop (blocking)."""
        self.renderer.start()

    def clear(self) -> None:
        """Clear widgets (no-op for py_cui)."""
        self.renderer.clear()
