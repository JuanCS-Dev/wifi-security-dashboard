"""
Core component abstraction for dashboard visualization.

This module provides the base Component class that all visual components
(Runchart, Sparkline, Barchart, etc.) must inherit from.

Inspired by Sampler's component architecture with rate-based updates.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from enum import Enum
import time

from rich.panel import Panel
from rich.console import RenderableType


class ComponentType(Enum):
    """Supported component types"""
    RUNCHART = "runchart"
    SPARKLINE = "sparkline"
    BARCHART = "barchart"
    GAUGE = "gauge"
    TEXTBOX = "textbox"
    TABLE = "table"
    ASCIIBOX = "asciibox"
    PACKETTABLE = "packettable"


@dataclass
class Position:
    """
    Component position in terminal grid.

    Attributes:
        x: Column position (0-based)
        y: Row position (0-based)
        width: Width in characters
        height: Height in lines
    """
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        """Validate position values"""
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Position x,y must be >= 0, got ({self.x}, {self.y})")
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"Size width,height must be > 0, got ({self.width}, {self.height})")


@dataclass
class TriggerConfig:
    """
    Configuration for component triggers/alerts.

    Attributes:
        title: Trigger description
        condition: Shell command that returns 0 (true) or 1 (false)
        actions: Dictionary of actions (visual, sound, terminal_bell, command)
    """
    title: str
    condition: str
    actions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentConfig:
    """
    Configuration for a dashboard component.

    Attributes:
        type: Component type (runchart, sparkline, etc.)
        title: Display title
        position: Grid position and size
        rate_ms: Update interval in milliseconds
        plugin: Plugin name to fetch data from
        data_field: Field name in plugin data
        color: Border/accent color (Rich color name or hex)
        triggers: List of trigger configurations
        extra: Additional component-specific configuration
    """
    type: ComponentType
    title: str
    position: Position
    rate_ms: int
    plugin: str
    data_field: str
    color: str = "white"
    triggers: List[TriggerConfig] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration"""
        if self.rate_ms < 0:
            raise ValueError(f"rate_ms must be >= 0, got {self.rate_ms}")
        if not self.plugin:
            raise ValueError("plugin name cannot be empty")
        if not self.data_field:
            raise ValueError("data_field cannot be empty")


class Component(ABC):
    """
    Abstract base class for all dashboard visual components.

    This class implements the core update logic with rate-based updates,
    similar to Sampler's architecture. Subclasses must implement the
    render() method to provide visual output.

    Example:
        >>> class MyChart(Component):
        ...     def render(self) -> Panel:
        ...         return Panel(f"Value: {self.data}")
        ...
        >>> config = ComponentConfig(...)
        >>> chart = MyChart(config)
        >>> if chart.should_update():
        ...     chart.update(plugin_data)
        >>> panel = chart.render()
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize component.

        Args:
            config: Component configuration

        Raises:
            ValueError: If config is invalid
        """
        self.config = config
        self._last_update: float = 0
        self._data: Any = None
        self._plugin_data: Dict[str, Any] = {}
        self._triggered: bool = False

    @property
    def data(self) -> Any:
        """Get current component data"""
        return self._data

    @property
    def plugin_data(self) -> Dict[str, Any]:
        """Get full plugin data dictionary"""
        return self._plugin_data

    @property
    def triggered(self) -> bool:
        """Check if any trigger is currently active"""
        return self._triggered

    def should_update(self) -> bool:
        """
        Determine if component should update based on rate_ms.

        Returns:
            True if elapsed time >= rate_ms, False otherwise

        Note:
            Components with rate_ms=0 only update once (static content)
        """
        # Static components (rate_ms=0) only update if never updated
        if self.config.rate_ms == 0:
            return self._last_update == 0

        now = time.time() * 1000  # Convert to milliseconds
        elapsed = now - self._last_update

        return elapsed >= self.config.rate_ms

    def update(self, plugin_data: Dict[str, Any]) -> None:
        """
        Update component with new data from plugin.

        Args:
            plugin_data: Data dictionary from plugin's collect_data()

        Raises:
            KeyError: If data_field not found in plugin_data

        Note:
            This method calls the on_update() hook for subclass-specific processing.

            Special case: If data_field is "all", entire plugin_data is used.
        """
        self._plugin_data = plugin_data

        # Special case: "all" means use entire plugin data
        if self.config.data_field == "all":
            self._data = plugin_data
            self._last_update = time.time() * 1000
        # Extract relevant data field
        elif self.config.data_field not in plugin_data:
            raise KeyError(
                f"Data field '{self.config.data_field}' not found in plugin data. "
                f"Available fields: {list(plugin_data.keys())}"
            )
        else:
            self._data = plugin_data[self.config.data_field]
            self._last_update = time.time() * 1000

        # Call subclass hook
        self.on_update()

        # Check triggers
        self._check_triggers()

    def on_update(self) -> None:
        """
        Hook called after data update.

        Template Method pattern - base implementation is intentionally empty.
        Subclasses override this to perform component-specific processing
        when new data arrives (e.g., adding to circular buffer, aggregation).

        This is a legitimate use of pass as a hook method (not a placeholder).

        Example:
            >>> class MyChart(Component):
            ...     def on_update(self):
            ...         self.buffer.append(self.data)
        """
        # Intentionally empty - Template Method pattern
        # Subclasses override as needed
        pass

    def _check_triggers(self) -> None:
        """
        Check all triggers and execute actions if conditions met.

        Basic implementation validates trigger configurations.
        Shell command execution and action dispatch are deferred to Sprint 5
        for security and architectural reasons (requires subprocess sandboxing).

        Note:
            This is a simplified but functional implementation that:
            1. Validates trigger configs are well-formed
            2. Logs warnings for incomplete configs
            3. Sets triggered flag appropriately
        """
        self._triggered = False

        if not self.config.triggers:
            return

        # Validate each trigger configuration
        for idx, trigger in enumerate(self.config.triggers):
            # Check required fields
            if not trigger.title:
                import warnings
                warnings.warn(
                    f"Trigger {idx} in component '{self.config.title}' "
                    f"missing title - will be ignored"
                )
                continue

            if not trigger.condition:
                import warnings
                warnings.warn(
                    f"Trigger '{trigger.title}' in component '{self.config.title}' "
                    f"missing condition - will be ignored"
                )
                continue

            # Trigger config is valid
            # Actual condition evaluation requires shell execution (Sprint 5)
            # Current implementation validates structure only

    @abstractmethod
    def render(self) -> RenderableType:
        """
        Render component as Rich renderable object.

        Returns:
            Rich Panel or other renderable object

        Note:
            Subclasses MUST implement this method.
        """
        pass

    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"{self.__class__.__name__}("
            f"title='{self.config.title}', "
            f"plugin='{self.config.plugin}', "
            f"rate_ms={self.config.rate_ms})"
        )
