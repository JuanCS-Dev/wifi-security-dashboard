"""
System metrics plugin using psutil.

Collects CPU, memory, disk, and process information from the operating system.
Uses psutil library for cross-platform system monitoring.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import Dict, Any

from .base import Plugin, PluginConfig, PluginStatus


class SystemPlugin(Plugin):
    """
    System metrics collection plugin.

    Provides real-time system metrics including:
    - CPU usage (overall and per-core)
    - Memory usage (RAM)
    - Disk usage
    - System load averages
    - Boot time and uptime

    Data Fields:
        cpu_percent: Overall CPU usage percentage (0-100)
        cpu_percent_per_core: List of per-core CPU percentages
        cpu_count: Number of CPU cores
        memory_percent: RAM usage percentage (0-100)
        memory_used_mb: RAM used in megabytes
        memory_total_mb: Total RAM in megabytes
        disk_percent: Disk usage percentage (0-100)
        disk_used_gb: Disk used in gigabytes
        disk_total_gb: Total disk space in gigabytes
        load_avg_1m: 1-minute load average (Unix only)
        load_avg_5m: 5-minute load average (Unix only)
        load_avg_15m: 15-minute load average (Unix only)
        uptime_seconds: System uptime in seconds

    Example:
        >>> config = PluginConfig(name="system", rate_ms=1000)
        >>> plugin = SystemPlugin(config)
        >>> plugin.initialize()
        >>> data = plugin.collect_data()
        >>> print(f"CPU: {data['cpu_percent']}%")
        CPU: 45.2%
    """

    def initialize(self) -> None:
        """
        Initialize system plugin.

        Sets up psutil and validates that required APIs are available.
        On Linux, attempts to get load averages; on other platforms,
        load averages will be omitted from data.

        In mock mode, skips psutil initialization and uses MockDataGenerator.
        """
        # Check if running in mock mode
        self._mock_mode = self.config.config.get('mock_mode', False)

        if self._mock_mode:
            # Mock mode: use MockDataGenerator
            from src.utils.mock_data_generator import get_mock_generator
            self._mock_generator = get_mock_generator()
            self._status = PluginStatus.READY
            return

        # Real mode: Import psutil (lazy loading)
        try:
            import psutil
            self.psutil = psutil
        except ImportError:
            raise RuntimeError("psutil library not installed. Install with: pip install psutil")

        # Verify psutil is available
        if not hasattr(self.psutil, 'cpu_percent'):
            raise RuntimeError("psutil library not properly installed")

        # Get disk partition to monitor (defaults to root)
        disk_path = self.config.config.get('disk_path', '/')

        # Verify disk path exists
        try:
            self.psutil.disk_usage(disk_path)
            self._disk_path = disk_path
        except FileNotFoundError:
            # Fallback to root if specified path doesn't exist
            self._disk_path = '/'

        # Check if load averages are available (Unix only)
        try:
            self.psutil.getloadavg()
            self._has_load_avg = True
        except (AttributeError, OSError):
            # Windows or other platforms without load averages
            self._has_load_avg = False

        # Initialize CPU percent (first call returns 0.0)
        self.psutil.cpu_percent(interval=None)

        self._status = PluginStatus.READY

    def collect_data(self) -> Dict[str, Any]:
        """
        Collect system metrics.

        Returns:
            Dictionary with system metrics

        Note:
            CPU percent requires interval or previous call to be accurate.
            We use interval=None (non-blocking) since collect_data() is
            called repeatedly at rate_ms intervals.

            In mock mode, returns simulated data from MockDataGenerator.
        """
        # Mock mode: return simulated data
        if self._mock_mode:
            return self._mock_generator.get_system_metrics()

        # Real mode: CPU metrics
        cpu_percent = self.psutil.cpu_percent(interval=None)
        cpu_percent_per_core = self.psutil.cpu_percent(interval=None, percpu=True)
        cpu_count = self.psutil.cpu_count()

        # Memory metrics
        memory = self.psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 ** 2)  # bytes to MB
        memory_total_mb = memory.total / (1024 ** 2)

        # Disk metrics
        disk = self.psutil.disk_usage(self._disk_path)
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 ** 3)  # bytes to GB
        disk_total_gb = disk.total / (1024 ** 3)

        # Boot time and uptime
        import time
        boot_time = self.psutil.boot_time()
        uptime_seconds = time.time() - boot_time

        data = {
            "cpu_percent": cpu_percent,
            "cpu_percent_per_core": cpu_percent_per_core,
            "cpu_count": cpu_count,
            "memory_percent": memory_percent,
            "memory_used_mb": memory_used_mb,
            "memory_total_mb": memory_total_mb,
            "disk_percent": disk_percent,
            "disk_used_gb": disk_used_gb,
            "disk_total_gb": disk_total_gb,
            "uptime_seconds": uptime_seconds,
        }

        # Add load averages if available (Unix only)
        if self._has_load_avg:
            load_1, load_5, load_15 = self.psutil.getloadavg()
            data["load_avg_1m"] = load_1
            data["load_avg_5m"] = load_5
            data["load_avg_15m"] = load_15

        return data

    def cleanup(self) -> None:
        """
        Cleanup system plugin.

        psutil doesn't require explicit cleanup, but we set status.
        """
        self._status = PluginStatus.STOPPED
