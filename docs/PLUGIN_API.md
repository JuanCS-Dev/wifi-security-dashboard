# Plugin API Guide

Comprehensive guide for developing custom plugins for WiFi Security Education Dashboard v2.0.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Plugin Basics](#plugin-basics)
3. [BasePlugin API Reference](#baseplugin-api-reference)
4. [Data Collection](#data-collection)
5. [Mock Mode Support](#mock-mode-support)
6. [Event Bus Integration](#event-bus-integration)
7. [UI Integration](#ui-integration)
8. [Configuration](#configuration)
9. [Testing Your Plugin](#testing-your-plugin)
10. [Best Practices](#best-practices)
11. [Example Plugins](#example-plugins)
12. [Troubleshooting](#troubleshooting)

---

## Quick Start

Create a plugin in 5 minutes:

```python
# src/plugins/temperature_plugin.py
from src.core.base_plugin import BasePlugin
from typing import Dict, Any
import random

class TemperaturePlugin(BasePlugin):
    """Monitors system temperature (mock mode supported)."""

    def __init__(self, mock_mode: bool = True):
        super().__init__(
            name="temperature",
            update_rate_ms=2000  # Update every 2 seconds
        )
        self.mock_mode = mock_mode

    def collect_data(self) -> Dict[str, Any]:
        """Collect temperature data."""
        if self.mock_mode:
            # Mock: Random temperature between 40-70°C
            temp = random.uniform(40, 70)
        else:
            # Real: Read from /sys/class/thermal/thermal_zone0/temp
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                temp = int(f.read().strip()) / 1000.0

        return {
            "temperature_celsius": round(temp, 1),
            "status": "normal" if temp < 60 else "hot"
        }
```

That's it! The plugin will be auto-discovered and registered on dashboard start.

## Plugin Basics

### Plugin Lifecycle

```
1. Discovery
   └─> PluginManager scans src/plugins/*.py

2. Instantiation
   └─> YourPlugin(mock_mode=True/False)

3. Registration
   └─> PluginManager.register_plugin(plugin)

4. Initialization
   └─> plugin.initialize() [optional hook]

5. Data Collection (every update_rate_ms)
   └─> plugin.collect_data()
        └─> EventBus.publish(f"{name}_update", data)

6. Cleanup (on shutdown)
   └─> plugin.cleanup() [optional hook]
```

### Directory Structure

```
src/plugins/
├── __init__.py
├── system_plugin.py      # CPU, RAM, Disk
├── wifi_plugin.py        # SSID, Signal, Quality
├── network_plugin.py     # Bandwidth, Connections
└── your_plugin.py        # Your custom plugin
```

### Naming Conventions

- **File**: `{name}_plugin.py` (e.g., `temperature_plugin.py`)
- **Class**: `{Name}Plugin` (e.g., `TemperaturePlugin`)
- **Plugin name**: Lowercase, no underscores (e.g., `"temperature"`)

## BasePlugin API Reference

### Abstract Base Class

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    """Base class for all dashboard plugins."""

    def __init__(self, name: str, update_rate_ms: int):
        """
        Initialize plugin.

        Args:
            name: Unique plugin identifier (lowercase, no spaces)
            update_rate_ms: How often to collect data (milliseconds)
        """
        self.name = name
        self.update_rate_ms = update_rate_ms
        self.enabled = True
        self._last_update = 0
        self.initialize()

    def initialize(self):
        """
        Optional hook for plugin-specific setup.

        Called after __init__, before first collect_data().
        Use for:
        - Opening files/sockets
        - Initializing caches
        - Validating dependencies
        """
        pass

    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """
        Collect plugin data (MUST be implemented).

        Returns:
            Dictionary with plugin data. Structure is plugin-defined.

        Raises:
            Any exception will be caught and logged by PluginManager.
        """
        pass

    def cleanup(self):
        """
        Optional hook for cleanup on shutdown.

        Use for:
        - Closing files/sockets
        - Flushing buffers
        - Releasing resources
        """
        pass

    def should_update(self, current_time: float) -> bool:
        """
        Check if plugin needs update (internal use).

        Args:
            current_time: Current timestamp in seconds

        Returns:
            True if update_rate_ms has elapsed since last update
        """
        return (current_time - self._last_update) * 1000 >= self.update_rate_ms
```

### Required Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique plugin identifier |
| `update_rate_ms` | `int` | Update interval (100-60000ms) |
| `enabled` | `bool` | Whether plugin is active |

### Optional Hooks

| Method | When Called | Use Case |
|--------|-------------|----------|
| `initialize()` | After `__init__` | Setup resources |
| `cleanup()` | Before shutdown | Release resources |

### Required Method

| Method | Return Type | Description |
|--------|-------------|-------------|
| `collect_data()` | `Dict[str, Any]` | Collect and return data |

## Data Collection

### Return Value Structure

Your `collect_data()` must return a dictionary. Structure is flexible:

```python
# Simple scalar values
return {
    "cpu_percent": 45.2,
    "status": "ok"
}

# Lists for time-series
return {
    "history": [10, 20, 30, 40, 50],
    "current": 50
}

# Nested structures
return {
    "devices": [
        {"name": "Phone", "ip": "192.168.1.100"},
        {"name": "Laptop", "ip": "192.168.1.101"}
    ],
    "total": 2
}
```

### Performance Guidelines

**Target**: `collect_data()` should complete in <50ms

**Tips**:
- Cache expensive operations
- Use shorter timeouts for network calls
- Consider increasing `update_rate_ms` if data is slow to collect
- Lazy-load dependencies

**Example**:
```python
class SlowPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="slow", update_rate_ms=10000)  # 10 seconds
        self._cache = None
        self._cache_time = 0

    def collect_data(self) -> Dict[str, Any]:
        # Cache for 30 seconds
        if time.time() - self._cache_time > 30:
            self._cache = self._expensive_operation()
            self._cache_time = time.time()
        return self._cache
```

### Error Handling

The PluginManager catches exceptions, but you should handle expected errors:

```python
def collect_data(self) -> Dict[str, Any]:
    try:
        data = self._read_sensor()
        return {"value": data, "status": "ok"}
    except FileNotFoundError:
        # Sensor not available
        return {"value": None, "status": "unavailable"}
    except PermissionError:
        # Need root access
        return {"value": None, "status": "no_permission"}
    # Let unexpected errors propagate to PluginManager
```

## Mock Mode Support

### Why Mock Mode?

- **Educational**: Students can run dashboard without root
- **Testing**: Deterministic data for unit tests
- **Demos**: Realistic family network scenario

### Implementing Mock Mode

**Pattern 1: Constructor flag**
```python
class MyPlugin(BasePlugin):
    def __init__(self, mock_mode: bool = True):
        super().__init__(name="my_plugin", update_rate_ms=1000)
        self.mock_mode = mock_mode

    def collect_data(self) -> Dict[str, Any]:
        if self.mock_mode:
            return self._mock_data()
        else:
            return self._real_data()
```

**Pattern 2: Dependency injection**
```python
class MyPlugin(BasePlugin):
    def __init__(self, data_source=None):
        super().__init__(name="my_plugin", update_rate_ms=1000)
        self.data_source = data_source or MockDataSource()

    def collect_data(self) -> Dict[str, Any]:
        return self.data_source.get_data()
```

### Mock Data Best Practices

1. **Make it realistic**: Use Brownian motion, not random()
2. **Simulate patterns**: Daily cycles, weekly trends
3. **Include edge cases**: 100% disk, 0% signal
4. **Correlate data**: High CPU → high temperature

**Example**:
```python
class MockDataGenerator:
    def __init__(self):
        self._baseline = 50.0
        self._trend = 0.0

    def brownian_walk(self, current: float, volatility: float = 5.0) -> float:
        """Realistic random walk (not pure random)."""
        delta = random.normalvariate(0, volatility)
        new_value = current + delta
        return max(0, min(100, new_value))  # Clamp to [0, 100]

    def get_cpu_percent(self) -> float:
        self._baseline = self.brownian_walk(self._baseline)
        return round(self._baseline, 1)
```

## Event Bus Integration

### Publishing Events

Your plugin automatically publishes events via PluginManager:

```python
# When you return data from collect_data():
def collect_data(self) -> Dict[str, Any]:
    return {"cpu": 45.2}

# PluginManager automatically does:
event_bus.publish("my_plugin_update", {"cpu": 45.2})
```

### Subscribing to Events

If your plugin needs data from other plugins:

```python
class DependentPlugin(BasePlugin):
    def initialize(self):
        # Subscribe to another plugin's events
        from src.core.event_bus import event_bus
        event_bus.subscribe("cpu_update", self._on_cpu_update)
        self.cpu_data = None

    def _on_cpu_update(self, data: Dict[str, Any]):
        self.cpu_data = data

    def collect_data(self) -> Dict[str, Any]:
        # Use data from other plugin
        if self.cpu_data and self.cpu_data["cpu_percent"] > 80:
            return {"alert": "High CPU detected"}
        return {"alert": None}
```

### Event Types

Standard event types (you can create custom ones):

- `{plugin_name}_update` - Data update from plugin
- `error` - Error messages
- `shutdown` - Graceful shutdown signal
- `plugin_loaded` - Plugin initialization complete

## UI Integration

### Displaying Your Data

The Dashboard will automatically display your data if you provide it in expected format.

**For TextBox display**:
```python
return {
    "display_text": "Temperature: 45.2°C [OK]"
}
```

**For Sparkline (time-series graph)**:
```python
return {
    "history": [40, 42, 45, 47, 45],  # Last N values
    "current": 45
}
```

**For BarChart**:
```python
return {
    "bars": {
        "CPU": 45.2,
        "GPU": 60.1,
        "Disk": 75.0
    }
}
```

### Custom UI Components

To add custom UI rendering:

```python
class MyPlugin(BasePlugin):
    def get_ui_component(self):
        """Optional method for custom UI."""
        from src.ui.components import CustomWidget
        return CustomWidget(self.collect_data())
```

## Configuration

### Plugin Configuration

Enable configuration via YAML:

```yaml
# config/dashboard-example.yml
plugins:
  temperature:
    enabled: true
    rate_ms: 2000
    threshold_celsius: 60
    alert_enabled: true
```

**Access in plugin**:
```python
class TemperaturePlugin(BasePlugin):
    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        super().__init__(
            name="temperature",
            update_rate_ms=config.get("rate_ms", 2000)
        )
        self.threshold = config.get("threshold_celsius", 60)
        self.alert_enabled = config.get("alert_enabled", True)
```

### Configuration Validation

Validate your config in `initialize()`:

```python
def initialize(self):
    if self.update_rate_ms < 1000:
        raise ValueError("update_rate_ms must be >= 1000")
    if not 0 < self.threshold < 100:
        raise ValueError("threshold must be between 0 and 100")
```

## Testing Your Plugin

### Unit Test Template

```python
# tests/unit/test_temperature_plugin.py
import pytest
from src.plugins.temperature_plugin import TemperaturePlugin

def test_plugin_initialization():
    plugin = TemperaturePlugin(mock_mode=True)
    assert plugin.name == "temperature"
    assert plugin.update_rate_ms == 2000

def test_mock_data_collection():
    plugin = TemperaturePlugin(mock_mode=True)
    data = plugin.collect_data()

    assert "temperature_celsius" in data
    assert 40 <= data["temperature_celsius"] <= 70
    assert data["status"] in ["normal", "hot"]

def test_real_data_collection(monkeypatch):
    # Mock file system for testing
    def mock_open(path, *args, **kwargs):
        class FakeFile:
            def read(self):
                return "50000\n"  # 50°C in millidegrees
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return FakeFile()

    monkeypatch.setattr("builtins.open", mock_open)

    plugin = TemperaturePlugin(mock_mode=False)
    data = plugin.collect_data()

    assert data["temperature_celsius"] == 50.0
    assert data["status"] == "normal"

def test_error_handling():
    plugin = TemperaturePlugin(mock_mode=False)
    # Test with non-existent file should not crash
    data = plugin.collect_data()
    assert data is not None  # Should return fallback data
```

### Integration Test

```python
# tests/integration/test_temperature_integration.py
from src.core.plugin_manager import PluginManager
from src.core.event_bus import EventBus
from src.plugins.temperature_plugin import TemperaturePlugin

def test_plugin_registration():
    manager = PluginManager()
    plugin = TemperaturePlugin(mock_mode=True)

    manager.register_plugin(plugin)
    assert manager.get_plugin("temperature") is not None

def test_event_publication():
    event_bus = EventBus()
    received_data = []

    def on_update(data):
        received_data.append(data)

    event_bus.subscribe("temperature_update", on_update)

    plugin = TemperaturePlugin(mock_mode=True)
    data = plugin.collect_data()
    event_bus.publish("temperature_update", data)

    assert len(received_data) == 1
    assert "temperature_celsius" in received_data[0]
```

### Manual Testing

```bash
# Run dashboard with your plugin
python3 main_v2.py

# Run tests
pytest tests/unit/test_temperature_plugin.py -v

# Check coverage
pytest tests/unit/test_temperature_plugin.py --cov=src.plugins.temperature_plugin
```

## Best Practices

### 1. Graceful Degradation

```python
def collect_data(self) -> Dict[str, Any]:
    try:
        # Try primary data source
        return self._get_primary_data()
    except Exception:
        try:
            # Fallback to secondary source
            return self._get_fallback_data()
        except Exception:
            # Return safe default
            return {"status": "unavailable"}
```

### 2. Dependency Validation (P2: Validação Preventiva)

```python
def initialize(self):
    # Check dependencies before use
    try:
        import psutil
        self.has_psutil = True
    except ImportError:
        self.has_psutil = False
        print("Warning: psutil not available, using mock data")

def collect_data(self) -> Dict[str, Any]:
    if self.has_psutil:
        import psutil
        return {"cpu": psutil.cpu_percent()}
    else:
        return {"cpu": 50.0}  # Mock fallback
```

### 3. Resource Cleanup

```python
class FilePlugin(BasePlugin):
    def initialize(self):
        self.log_file = open("/var/log/myapp.log", "r")

    def collect_data(self) -> Dict[str, Any]:
        lines = self.log_file.readlines()
        return {"lines": len(lines)}

    def cleanup(self):
        if hasattr(self, 'log_file'):
            self.log_file.close()
```

### 4. Type Hints

```python
from typing import Dict, Any, List, Optional

def collect_data(self) -> Dict[str, Any]:
    devices: List[str] = self._scan_network()
    count: int = len(devices)
    return {"devices": devices, "count": count}
```

### 5. Docstrings

```python
class MyPlugin(BasePlugin):
    """
    Monitor system XYZ.

    Collects data from /path/to/source every N seconds.
    Supports both mock and real modes.

    Attributes:
        threshold: Alert threshold value
        alert_enabled: Whether to emit alerts

    Example:
        >>> plugin = MyPlugin(mock_mode=True)
        >>> data = plugin.collect_data()
        >>> print(data["value"])
        42
    """
```

## Example Plugins

### Example 1: Simple Metric

```python
# Battery percentage plugin
from src.core.base_plugin import BasePlugin
import psutil

class BatteryPlugin(BasePlugin):
    def __init__(self, mock_mode: bool = True):
        super().__init__(name="battery", update_rate_ms=5000)
        self.mock_mode = mock_mode

    def collect_data(self) -> Dict[str, Any]:
        if self.mock_mode:
            return {"percent": 85, "plugged": True}

        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged
            }
        return {"percent": None, "plugged": None}
```

### Example 2: Time Series

```python
# Network traffic history plugin
from src.core.base_plugin import BasePlugin
import psutil
from collections import deque

class TrafficPlugin(BasePlugin):
    def __init__(self, mock_mode: bool = True, history_size: int = 50):
        super().__init__(name="traffic", update_rate_ms=1000)
        self.mock_mode = mock_mode
        self.history = deque(maxlen=history_size)
        self.last_bytes = None

    def collect_data(self) -> Dict[str, Any]:
        if self.mock_mode:
            import random
            bytes_per_sec = random.randint(1000, 10000)
        else:
            net = psutil.net_io_counters()
            total_bytes = net.bytes_sent + net.bytes_recv
            if self.last_bytes:
                bytes_per_sec = total_bytes - self.last_bytes
            else:
                bytes_per_sec = 0
            self.last_bytes = total_bytes

        self.history.append(bytes_per_sec)
        return {
            "current_bps": bytes_per_sec,
            "history": list(self.history)
        }
```

### Example 3: Multi-Device Monitoring

```python
# Connected devices plugin
from src.core.base_plugin import BasePlugin
import subprocess

class DevicesPlugin(BasePlugin):
    def __init__(self, mock_mode: bool = True):
        super().__init__(name="devices", update_rate_ms=10000)
        self.mock_mode = mock_mode

    def collect_data(self) -> Dict[str, Any]:
        if self.mock_mode:
            return {
                "devices": [
                    {"name": "Phone", "ip": "192.168.1.100", "mac": "AA:BB:CC:DD:EE:01"},
                    {"name": "Laptop", "ip": "192.168.1.101", "mac": "AA:BB:CC:DD:EE:02"}
                ],
                "count": 2
            }

        # Real: Parse 'arp -a' output
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        devices = self._parse_arp(result.stdout)
        return {"devices": devices, "count": len(devices)}

    def _parse_arp(self, output: str) -> List[Dict[str, str]]:
        # Parse logic here...
        pass
```

## Troubleshooting

### Plugin Not Loaded

**Symptom**: Plugin doesn't appear in dashboard

**Checklist**:
- [ ] File named `*_plugin.py` in `src/plugins/`?
- [ ] Class inherits from `BasePlugin`?
- [ ] `collect_data()` method implemented?
- [ ] No syntax errors? Run `python3 -m py_compile src/plugins/your_plugin.py`

### Plugin Crashes

**Symptom**: Dashboard exits or plugin data missing

**Debug**:
```python
# Add logging to your plugin
import logging
logger = logging.getLogger(__name__)

def collect_data(self) -> Dict[str, Any]:
    logger.debug("Starting data collection")
    try:
        data = self._get_data()
        logger.debug(f"Collected: {data}")
        return data
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
```

### Slow Performance

**Symptom**: Dashboard FPS drops below 10

**Profile**:
```bash
python3 scripts/benchmark.py
```

**Fix**:
- Increase `update_rate_ms` (e.g., 1000 → 5000)
- Cache expensive operations
- Use async I/O (v3.0 feature)
- Move to separate process (advanced)

### Mock Mode Not Working

**Symptom**: Plugin requires root even in mock mode

**Fix**:
```python
# Ensure mock_mode flag is respected
def collect_data(self) -> Dict[str, Any]:
    if self.mock_mode:
        return self._mock_data()  # ALWAYS return mock if flag set
    else:
        return self._real_data()
```

---

## API Stability Guarantee

**Will NOT change** (safe to use):
- `BasePlugin.__init__(name, update_rate_ms)`
- `BasePlugin.collect_data()` → `Dict[str, Any]`
- `BasePlugin.initialize()` hook
- `BasePlugin.cleanup()` hook

**May change** (with deprecation warning):
- `BasePlugin.should_update()` (internal method)
- Plugin auto-discovery mechanism
- Configuration format

## Further Reading

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [tests/unit/test_*_plugin.py](../tests/unit/) - Plugin test examples
- [src/plugins/](../src/plugins/) - Existing plugin implementations

---

**Framework**: Constituição Vértice v3.0 (P4 - Rastreabilidade Total)

**Soli Deo Gloria** ✝️
