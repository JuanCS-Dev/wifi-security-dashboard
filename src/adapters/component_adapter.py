"""
Base Component Adapter for py_cui Widgets.

Provides abstract interface for converting Component instances
to py_cui widgets while maintaining plugin architecture.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import py_cui


class ComponentAdapter(ABC):
    """
    Abstract base class for component adapters.

    Adapters translate between two architectures:

    OLD (Rich-based):
        Plugin → Component → render() → Panel (RenderableType)

    NEW (py_cui-based):
        Plugin → Adapter → py_cui Widget → _draw() → curses

    Each Component type (Sparkline, Runchart, etc.) will have
    a corresponding Adapter that creates and manages the appropriate
    py_cui widget.

    Example:
        >>> from src.components.sparkline import Sparkline
        >>> from src.adapters.sparkline_adapter import SparklineAdapter
        >>>
        >>> component = Sparkline(config, plugin_manager)
        >>> adapter = SparklineAdapter(component)
        >>> widget = adapter.create_widget(pycui_root, grid_position)
        >>> adapter.update_widget(plugin_data)
    """

    def __init__(self, component: Any):
        """
        Initialize adapter with component instance.

        Args:
            component: Component instance (Sparkline, Runchart, etc.)
        """
        self.component = component
        self.widget: Optional[Any] = None  # py_cui Widget instance

    @abstractmethod
    def create_widget(
        self,
        pycui_root: py_cui.PyCUI,
        row: int,
        col: int,
        row_span: int,
        col_span: int
    ) -> Any:
        """
        Create py_cui widget for this component.

        Args:
            pycui_root: PyCUI root instance
            row: Starting grid row
            col: Starting grid column
            row_span: Number of rows to span
            col_span: Number of columns to span

        Returns:
            py_cui Widget instance

        Note:
            Must store widget in self.widget for later updates.
        """
        pass

    @abstractmethod
    def update_widget(self, plugin_data: dict) -> None:
        """
        Update widget with new plugin data.

        Called by PyCUIRenderer during draw cycle to refresh widget
        with latest data from plugins.

        Args:
            plugin_data: Dictionary of plugin data
                {
                    'plugin_name': {'field': value, ...},
                    ...
                }

        Note:
            Should extract relevant data and call widget's update method.
        """
        pass

    def get_widget(self) -> Optional[Any]:
        """
        Get the py_cui widget instance.

        Returns:
            Widget instance or None if not created yet
        """
        return self.widget

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"component={self.component.__class__.__name__}, "
            f"widget={self.widget.__class__.__name__ if self.widget else None})"
        )
