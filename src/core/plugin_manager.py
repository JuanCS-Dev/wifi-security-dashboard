"""
Plugin manager for dynamic plugin loading and lifecycle management.

This module provides the PluginManager class that:
- Auto-discovers available plugins
- Instantiates plugins from configuration
- Manages plugin lifecycle (initialize, collect, cleanup)
- Provides plugin data to components

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import Dict, Any, List, Type, Optional
import importlib
import sys
from pathlib import Path

from src.plugins.base import Plugin, PluginConfig, PluginStatus
from .event_bus import EventBus, Event, EventType


# Plugin registry (name -> class)
BUILTIN_PLUGINS: Dict[str, Type[Plugin]] = {}


def register_plugin(name: str, plugin_class: Type[Plugin]) -> None:
    """
    Register a plugin class.

    Args:
        name: Plugin identifier
        plugin_class: Plugin class (must inherit from Plugin)

    Raises:
        ValueError: If plugin already registered or invalid class
    """
    if name in BUILTIN_PLUGINS:
        raise ValueError(f"Plugin '{name}' already registered")

    if not issubclass(plugin_class, Plugin):
        raise ValueError(f"Plugin class must inherit from Plugin")

    BUILTIN_PLUGINS[name] = plugin_class


class PluginManager:
    """
    Manages plugin lifecycle and data collection.

    The PluginManager is responsible for:
    1. Loading plugin classes (builtin or custom)
    2. Instantiating plugins from configuration
    3. Initializing plugins
    4. Collecting data from plugins
    5. Handling plugin errors gracefully
    6. Cleanup on shutdown

    Example:
        >>> configs = [
        ...     PluginConfig(name="system", rate_ms=1000),
        ...     PluginConfig(name="network", rate_ms=1000),
        ... ]
        >>> manager = PluginManager(configs, event_bus)
        >>> manager.initialize_all()
        >>> data = manager.get_plugin_data("system")
        >>> print(data["cpu_percent"])
    """

    def __init__(self, plugin_configs: List[PluginConfig], event_bus: EventBus, mock_mode: bool = False):
        """
        Initialize plugin manager.

        Args:
            plugin_configs: List of plugin configurations
            event_bus: Event bus for publishing plugin events
            mock_mode: Run plugins in mock mode with simulated data

        Raises:
            ValueError: If configuration is invalid
        """
        self.mock_mode = mock_mode
        self.plugin_configs = plugin_configs
        self.event_bus = event_bus

        # Active plugin instances (name -> Plugin)
        self.plugins: Dict[str, Plugin] = {}

        # Plugin data cache (name -> data)
        self._data_cache: Dict[str, Dict[str, Any]] = {}

    def initialize_all(self) -> None:
        """
        Initialize all configured plugins.

        Loads plugin classes, instantiates them, and calls initialize().
        Publishes events for successful/failed initialization.

        Note:
            Plugins that fail to initialize are skipped with error logged.
        """
        for config in self.plugin_configs:
            if not config.enabled:
                continue

            try:
                # Get plugin class
                plugin_class = self._get_plugin_class(config.name)

                # Add mock_mode to config
                config.config['mock_mode'] = self.mock_mode

                # Instantiate plugin
                plugin = plugin_class(config)

                # Initialize plugin
                plugin.initialize()

                # Store plugin
                self.plugins[config.name] = plugin

                # Publish success event
                self.event_bus.publish(Event(
                    type=EventType.PLUGIN_LOADED.value,
                    source=config.name,
                    data={
                        "status": "initialized",
                        "plugin_class": plugin_class.__name__
                    }
                ))

            except Exception as e:
                # Log error but continue with other plugins
                self.event_bus.publish(Event(
                    type=EventType.PLUGIN_ERROR.value,
                    source=config.name,
                    data={
                        "error": str(e),
                        "stage": "initialization"
                    }
                ))

    def get_plugin_data(self, plugin_name: str) -> Dict[str, Any]:
        """
        Get data from a specific plugin.

        Calls plugin.collect_safe() and caches the result.
        Returns cached data if plugin shouldn't collect yet.

        Args:
            plugin_name: Name of plugin to collect from

        Returns:
            Dictionary with plugin data, or empty dict if plugin unavailable

        Note:
            Uses collect_safe() which handles errors gracefully.
        """
        plugin = self.plugins.get(plugin_name)

        if not plugin:
            # Plugin not loaded
            return self._data_cache.get(plugin_name, {})

        # Collect data (respects rate_ms)
        data = plugin.collect_safe()

        # Update cache if data was collected
        if data:
            self._data_cache[plugin_name] = data

            # Publish data collection event
            self.event_bus.publish(Event(
                type=EventType.PLUGIN_DATA_COLLECTED.value,
                source=plugin_name,
                data={"fields": list(data.keys())}
            ))

        # Return cached data (fresh or previous)
        return self._data_cache.get(plugin_name, {})

    def get_all_plugin_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Get data from all plugins.

        Returns:
            Dictionary mapping plugin names to their data

        Example:
            >>> data = manager.get_all_plugin_data()
            >>> print(data["system"]["cpu_percent"])
            >>> print(data["network"]["bandwidth_tx_mbps"])
        """
        all_data = {}
        for plugin_name in self.plugins.keys():
            all_data[plugin_name] = self.get_plugin_data(plugin_name)
        return all_data

    def get_plugin_status(self, plugin_name: str) -> Optional[PluginStatus]:
        """
        Get status of a plugin.

        Args:
            plugin_name: Name of plugin

        Returns:
            PluginStatus or None if plugin not loaded
        """
        plugin = self.plugins.get(plugin_name)
        return plugin.status if plugin else None

    def get_all_plugin_statuses(self) -> Dict[str, PluginStatus]:
        """
        Get statuses of all plugins.

        Returns:
            Dictionary mapping plugin names to statuses
        """
        return {
            name: plugin.status
            for name, plugin in self.plugins.items()
        }

    def reset_plugin_errors(self, plugin_name: str) -> None:
        """
        Reset error tracking for a plugin.

        Args:
            plugin_name: Name of plugin to reset
        """
        plugin = self.plugins.get(plugin_name)
        if plugin:
            plugin.reset_errors()

    def cleanup_all(self) -> None:
        """
        Cleanup all plugins.

        Calls cleanup() on all plugins in reverse order of initialization.
        """
        for plugin_name in reversed(list(self.plugins.keys())):
            plugin = self.plugins[plugin_name]
            try:
                plugin.cleanup()

                self.event_bus.publish(Event(
                    type=EventType.PLUGIN_STOPPED.value,
                    source=plugin_name,
                    data={"status": "cleaned_up"}
                ))

            except Exception as e:
                self.event_bus.publish(Event(
                    type=EventType.PLUGIN_ERROR.value,
                    source=plugin_name,
                    data={
                        "error": str(e),
                        "stage": "cleanup"
                    }
                ))

        self.plugins.clear()
        self._data_cache.clear()

    def _get_plugin_class(self, plugin_name: str) -> Type[Plugin]:
        """
        Get plugin class by name.

        First checks builtin plugins, then attempts dynamic import
        from src.plugins module.

        Args:
            plugin_name: Plugin identifier

        Returns:
            Plugin class

        Raises:
            ValueError: If plugin not found or invalid
        """
        # Check builtin registry
        if plugin_name in BUILTIN_PLUGINS:
            return BUILTIN_PLUGINS[plugin_name]

        # Try dynamic import
        try:
            module_name = f"src.plugins.{plugin_name}_plugin"
            class_name = f"{plugin_name.capitalize()}Plugin"

            module = importlib.import_module(module_name)
            plugin_class = getattr(module, class_name)

            if not issubclass(plugin_class, Plugin):
                raise ValueError(f"{class_name} must inherit from Plugin")

            return plugin_class

        except (ImportError, AttributeError) as e:
            raise ValueError(
                f"Plugin '{plugin_name}' not found. "
                f"Expected module: {module_name}, class: {class_name}. "
                f"Error: {e}"
            )

    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"PluginManager("
            f"plugins={len(self.plugins)}, "
            f"loaded={list(self.plugins.keys())})"
        )


# Register builtin plugins
# This allows PluginManager to find them automatically
try:
    from src.plugins.system_plugin import SystemPlugin
    from src.plugins.network_plugin import NetworkPlugin
    from src.plugins.wifi_plugin import WiFiPlugin
    from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin

    register_plugin("system", SystemPlugin)
    register_plugin("network", NetworkPlugin)
    register_plugin("wifi", WiFiPlugin)
    register_plugin("packet_analyzer", PacketAnalyzerPlugin)

except ImportError as e:
    # Plugins will be loaded dynamically if not registered
    pass
