"""
Base plugin abstraction for data collection.

This module provides the Plugin base class that all data collection plugins
must inherit from. Plugins are responsible for collecting real-time data
from various sources (system metrics, network, WiFi, etc.).

Inspired by Sampler's plugin architecture with autonomous data collection.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
import time


class PluginStatus(Enum):
    """Plugin operational status"""
    UNINITIALIZED = "uninitialized"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class PluginConfig:
    """
    Configuration for a plugin instance.

    Attributes:
        name: Unique plugin identifier
        enabled: Whether plugin is enabled
        rate_ms: Data collection interval in milliseconds
        config: Plugin-specific configuration options
    """
    name: str
    enabled: bool = True
    rate_ms: int = 1000
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate plugin configuration"""
        if not self.name:
            raise ValueError("Plugin name cannot be empty")
        if self.rate_ms < 0:
            raise ValueError(f"rate_ms must be >= 0, got {self.rate_ms}")


class Plugin(ABC):
    """
    Abstract base class for all data collection plugins.

    Plugins implement autonomous data collection from various sources.
    Each plugin runs independently and provides data to components via
    the Dashboard's plugin manager.

    Lifecycle:
        1. __init__(config) - Plugin created
        2. initialize() - Setup resources (files, connections, etc.)
        3. collect_data() - Called at rate_ms interval
        4. cleanup() - Release resources when plugin stops

    Example:
        >>> class CPUPlugin(Plugin):
        ...     def initialize(self) -> None:
        ...         import psutil
        ...         self.psutil = psutil
        ...
        ...     def collect_data(self) -> Dict[str, Any]:
        ...         return {
        ...             "cpu_percent": self.psutil.cpu_percent(),
        ...             "cpu_count": self.psutil.cpu_count()
        ...         }
        ...
        ...     def cleanup(self) -> None:
        ...         pass  # No cleanup needed
        ...
        >>> config = PluginConfig(name="cpu", rate_ms=1000)
        >>> plugin = CPUPlugin(config)
        >>> plugin.initialize()
        >>> data = plugin.collect_data()
        >>> print(data["cpu_percent"])
    """

    def __init__(self, config: PluginConfig):
        """
        Initialize plugin with configuration.

        Args:
            config: Plugin configuration

        Raises:
            ValueError: If config is invalid
        """
        self.config = config
        self._status = PluginStatus.UNINITIALIZED
        self._last_collection: float = 0
        self._error_count: int = 0
        self._consecutive_errors: int = 0
        self._last_error: Optional[str] = None

    @property
    def name(self) -> str:
        """Get plugin name"""
        return self.config.name

    @property
    def status(self) -> PluginStatus:
        """Get current plugin status"""
        return self._status

    @property
    def error_count(self) -> int:
        """Get total number of errors encountered (lifetime)"""
        return self._error_count

    @property
    def consecutive_errors(self) -> int:
        """
        Get number of consecutive errors since last success.

        Resets to 0 on successful collection (auto-recovery indicator).
        """
        return self._consecutive_errors

    @property
    def last_error(self) -> Optional[str]:
        """Get last error message (if any)"""
        return self._last_error

    def should_collect(self) -> bool:
        """
        Determine if plugin should collect data based on rate_ms.

        Returns:
            True if elapsed time >= rate_ms, False otherwise

        Note:
            Plugins with rate_ms=0 collect only once (static data).
        """
        # Static plugins (rate_ms=0) only collect if never collected
        if self.config.rate_ms == 0:
            return self._last_collection == 0

        now = time.time() * 1000  # Convert to milliseconds
        elapsed = now - self._last_collection

        return elapsed >= self.config.rate_ms

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize plugin resources.

        Called once when plugin is loaded. Use this to:
        - Import required libraries
        - Open file handles
        - Establish connections
        - Setup internal state

        Raises:
            Exception: If initialization fails

        Note:
            Subclasses MUST implement this method.
            Set self._status = PluginStatus.READY when done.
        """
        pass

    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """
        Collect data from plugin source.

        Returns:
            Dictionary with collected data. Keys should be descriptive
            and match component data_field configurations.

        Raises:
            Exception: If data collection fails

        Note:
            Subclasses MUST implement this method.
            This method is called at intervals defined by rate_ms.

        Example:
            >>> def collect_data(self) -> Dict[str, Any]:
            ...     return {
            ...         "cpu_percent": 45.2,
            ...         "memory_percent": 68.5,
            ...         "disk_percent": 42.1
            ...     }
        """
        pass

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        Called when plugin is stopped or dashboard exits. Use this to:
        - Close file handles
        - Terminate connections
        - Release system resources

        Template Method pattern - base implementation is intentionally empty.
        Subclasses override this if they need cleanup (e.g., file handles,
        network connections).

        This is a legitimate use of pass as a hook method (not a placeholder).

        Example:
            >>> def cleanup(self) -> None:
            ...     if hasattr(self, 'connection'):
            ...         self.connection.close()
        """
        # Intentionally empty - Template Method pattern
        # Subclasses override as needed
        pass

    def collect_safe(self) -> Dict[str, Any]:
        """
        Safely collect data with error handling and auto-recovery.

        Wraps collect_data() with error handling to prevent crashes.
        Updates internal error tracking and timestamps.

        Auto-Recovery Behavior:
            - On success: Resets consecutive error count and transitions from
              ERROR → RUNNING automatically (resilient to transient failures)
            - On failure: Increments both total and consecutive error counters

        Returns:
            Dictionary with collected data, or empty dict on error

        Note:
            This method is called by PluginManager, not directly.
            It ensures one plugin failure doesn't crash the dashboard.

        Example:
            >>> # Plugin fails 3 times, then succeeds - auto-recovers
            >>> plugin.collect_safe()  # Error 1: status → ERROR
            >>> plugin.collect_safe()  # Error 2: status = ERROR
            >>> plugin.collect_safe()  # Error 3: status = ERROR
            >>> plugin.collect_safe()  # Success: status → RUNNING (auto-recovery!)
        """
        if not self.config.enabled:
            return {}

        if not self.should_collect():
            return {}

        try:
            data = self.collect_data()
            self._last_collection = time.time() * 1000

            # Auto-recovery: Reset consecutive errors on success
            self._consecutive_errors = 0
            self._last_error = None

            # Transition ERROR → RUNNING (auto-recovery)
            if self._status == PluginStatus.ERROR or self._status == PluginStatus.READY:
                self._status = PluginStatus.RUNNING

            return data

        except Exception as e:
            self._error_count += 1
            self._consecutive_errors += 1
            self._last_error = str(e)
            self._status = PluginStatus.ERROR

            # Return empty dict to prevent component crashes
            return {}

    def reset_errors(self) -> None:
        """
        Reset error tracking (manual recovery).

        Clears all error counters and transitions ERROR → READY.
        Note: Auto-recovery happens automatically in collect_safe(),
        so this method is mainly for manual intervention.
        """
        self._error_count = 0
        self._consecutive_errors = 0
        self._last_error = None
        if self._status == PluginStatus.ERROR:
            self._status = PluginStatus.READY

    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"status={self.status.value}, "
            f"rate_ms={self.config.rate_ms})"
        )
