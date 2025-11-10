# WiFi Security Education Dashboard - Architecture

Comprehensive architecture documentation for v2.0 with design patterns, data flow, and extensibility guidelines.

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Core Components](#core-components)
4. [Design Patterns](#design-patterns)
5. [Data Flow](#data-flow)
6. [Plugin System](#plugin-system)
7. [Event System](#event-system)
8. [UI Components](#ui-components)
9. [Configuration](#configuration)
10. [Testing Strategy](#testing-strategy)
11. [Performance Considerations](#performance-considerations)
12. [Future Extensibility](#future-extensibility)

---

## Overview

WiFi Security Education Dashboard v2.0 is built on a **plugin-based architecture** with **event-driven communication** and **factory-pattern UI components**. The system prioritizes:

- **Modularity**: Plugins are independent, can be enabled/disabled
- **Testability**: Mock mode for safe testing without root privileges
- **Extensibility**: New plugins can be added without modifying core
- **Performance**: <100ms refresh rate target (10 FPS)
- **Educational value**: Clear code structure for learning purposes

## High-Level Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    main_v2.py (Entry Point)                    │
│  - Parses CLI arguments (--real, --config)                     │
│  - Loads configuration from YAML                               │
│  - Initializes Dashboard with appropriate mode                 │
└────────────────────────┬──────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
┌─────────────────────┐       ┌─────────────────────┐
│   Dashboard (Core)  │◄──────┤  ConfigLoader       │
│  - Main event loop  │       │  - YAML parsing     │
│  - UI coordination  │       │  - Validation       │
│  - Lifecycle mgmt   │       │  - Defaults         │
└──────────┬──────────┘       └─────────────────────┘
           │
           ├──► PluginManager ───┬──► SystemPlugin (CPU, RAM, Disk)
           │    - Discovery      │
           │    - Registration   ├──► WiFiPlugin (SSID, Signal, Quality)
           │    - Scheduling     │
           │                     ├──► NetworkPlugin (Bandwidth, Connections)
           │                     │
           │                     └──► [Custom Plugins...]
           │
           ├──► EventBus ────────┬──► Event: system_update
           │    - Pub/Sub        ├──► Event: wifi_update
           │    - Decoupling     ├──► Event: network_update
           │                     └──► Event: error
           │
           └──► UIFactory ───────┬──► TextBox (static text)
                - Component      ├──► Sparkline (time-series graph)
                - creation       ├──► BarChart (horizontal bars)
                                 ├──► RunChart (line graph with legend)
                                 └──► [Custom Components...]
```

## Core Components

### 1. Dashboard (`src/core/dashboard.py`)

**Responsibility**: Main coordinator and event loop manager

**Key Methods**:
- `run()`: Main event loop (target: 10 FPS / 100ms)
- `_update_plugins()`: Schedules plugin data collection
- `_render_ui()`: Coordinates UI rendering via Rich Console
- `_handle_events()`: Processes EventBus messages

**State Management**:
- `_running`: Boolean flag for graceful shutdown
- `_plugins`: Dict[str, BasePlugin] - Registered plugins
- `_last_update`: Dict[str, float] - Plugin update timestamps
- `_layout`: Rich Layout object for UI structure

**Lifecycle**:
```python
Dashboard.run()
  ├─> _initialize_plugins()
  ├─> while _running:
  │     ├─> _update_plugins()  # Data collection
  │     ├─> _render_ui()       # UI update
  │     └─> sleep(100ms)       # Rate limiting
  └─> _cleanup()
```

### 2. PluginManager (`src/core/plugin_manager.py`)

**Responsibility**: Plugin lifecycle and scheduling

**Key Methods**:
- `register_plugin(plugin: BasePlugin)`: Adds plugin to system
- `unregister_plugin(name: str)`: Removes plugin
- `get_plugin(name: str) -> BasePlugin`: Retrieves plugin instance
- `collect_all_data() -> Dict[str, Any]`: Aggregates data from all plugins

**Plugin Discovery**:
- Auto-discovers plugins in `src/plugins/` directory
- Looks for classes inheriting from `BasePlugin`
- Validates plugin metadata (name, version, update_rate_ms)

**Scheduling Strategy**:
- Each plugin has independent `update_rate_ms` (e.g., CPU: 1000ms, WiFi: 5000ms)
- Uses timestamp-based scheduling to avoid unnecessary updates
- Implements **adaptive scheduling** if plugin takes too long

### 3. EventBus (`src/core/event_bus.py`)

**Responsibility**: Pub/Sub communication between components

**Key Methods**:
- `subscribe(event_type: str, callback: Callable)`: Register listener
- `publish(event_type: str, data: Any)`: Emit event to all subscribers
- `unsubscribe(event_type: str, callback: Callable)`: Remove listener

**Event Types**:
```python
# Data events
"system_update"   # CPU, RAM, Disk data
"wifi_update"     # SSID, Signal, Connected devices
"network_update"  # Bandwidth, Connections

# Control events
"error"           # Error messages for UI
"shutdown"        # Graceful shutdown signal
"plugin_loaded"   # Plugin initialization complete
```

**Decoupling Benefits**:
- Plugins don't need to know about UI
- UI doesn't need to know about data sources
- Easy to add logging, analytics, or alerts as subscribers

### 4. ConfigLoader (`src/config/config_loader.py`)

**Responsibility**: YAML configuration parsing and validation

**Key Methods**:
- `load_config(path: str) -> Dict[str, Any]`: Loads and validates YAML
- `get_default_config() -> Dict[str, Any]`: Returns sensible defaults
- `validate_config(config: Dict) -> bool`: Schema validation

**Configuration Schema**:
```yaml
dashboard:
  refresh_rate_ms: 100      # Main loop rate (10 FPS)
  mock_mode: true           # Safe mode without root

plugins:
  system:
    enabled: true
    rate_ms: 1000           # Update every 1 second
  wifi:
    enabled: true
    rate_ms: 5000           # Update every 5 seconds
  network:
    enabled: true
    rate_ms: 2000           # Update every 2 seconds

ui:
  theme: "default"
  show_legend: true
  sparkline_width: 50
```

## Design Patterns

### 1. Plugin Architecture (Strategy Pattern)

**Problem**: Different data sources need different collection strategies

**Solution**: `BasePlugin` abstract class with `collect_data()` template method

```python
class BasePlugin(ABC):
    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """Template method - must be implemented by subclasses"""
        pass
```

**Benefits**:
- New plugins don't require core changes
- Easy A/B testing of different implementations
- Plugins can be distributed as separate packages

### 2. Factory Pattern (UI Components)

**Problem**: Creating UI components with consistent styling

**Solution**: `UIFactory` class with factory methods

```python
class UIFactory:
    @staticmethod
    def create_sparkline(data: List[float], **kwargs) -> Sparkline:
        return Sparkline(data, colors=["green", "yellow", "red"], **kwargs)

    @staticmethod
    def create_bar_chart(data: Dict[str, float], **kwargs) -> BarChart:
        return BarChart(data, bar_color="blue", **kwargs)
```

**Benefits**:
- Consistent styling across dashboard
- Easy to swap UI library (Rich → Textual in v3.0)
- Simplifies component creation in plugins

### 3. Observer Pattern (Event Bus)

**Problem**: Components need to react to changes without tight coupling

**Solution**: EventBus with pub/sub mechanism

**Example**:
```python
# Publisher (Plugin)
event_bus.publish("wifi_update", {"ssid": "MyNetwork", "signal": -45})

# Subscriber (Dashboard)
def on_wifi_update(data):
    self._update_wifi_ui(data)
event_bus.subscribe("wifi_update", on_wifi_update)
```

### 4. Mock Object Pattern (Testing)

**Problem**: Real hardware/network access requires root and is non-deterministic

**Solution**: `MockDataGenerator` with realistic simulated data

```python
class MockDataGenerator:
    def get_cpu_percent(self) -> float:
        """Returns realistic CPU usage (30-80%) with brownian motion"""
        return self._brownian_walk(self._cpu_baseline, min=0, max=100)
```

**Benefits**:
- Students can run dashboard without root
- Deterministic testing
- Simulates family network scenario for education

### 5. Template Method Pattern (Base Plugin)

**Problem**: Plugins need common initialization but custom data collection

**Solution**: `BasePlugin` with template methods

```python
class BasePlugin(ABC):
    def __init__(self, name: str, update_rate_ms: int):
        self.name = name
        self.update_rate_ms = update_rate_ms
        self._last_update = 0
        self.initialize()  # Hook for subclasses

    def initialize(self):
        """Optional hook for plugin-specific setup"""
        pass

    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """Required implementation"""
        pass
```

## Data Flow

### Complete Data Flow (Mock Mode)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User runs: python3 main_v2.py                            │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. main_v2.py initializes Dashboard(mock_mode=True)         │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Dashboard creates PluginManager, EventBus, UIFactory     │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PluginManager registers: SystemPlugin, WiFiPlugin,       │
│    NetworkPlugin (all using MockDataGenerator)              │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Dashboard.run() starts main event loop (100ms interval)  │
└────────────────────────┬────────────────────────────────────┘
                         ▼
         ┌───────────────┴───────────────┐
         │  Every 100ms (10 FPS):        │
         │  ┌─────────────────────────┐  │
         │  │ 6. Check plugin timing  │  │
         │  └──────────┬──────────────┘  │
         │             ▼                  │
         │  ┌─────────────────────────┐  │
         │  │ 7. Plugin.collect_data()│  │
         │  │    (if rate_ms elapsed) │  │
         │  └──────────┬──────────────┘  │
         │             ▼                  │
         │  ┌─────────────────────────┐  │
         │  │ 8. EventBus.publish()   │  │
         │  │    "system_update", etc │  │
         │  └──────────┬──────────────┘  │
         │             ▼                  │
         │  ┌─────────────────────────┐  │
         │  │ 9. Dashboard receives   │  │
         │  │    event, updates UI    │  │
         │  └──────────┬──────────────┘  │
         │             ▼                  │
         │  ┌─────────────────────────┐  │
         │  │ 10. Rich Console.print()│  │
         │  │     renders UI          │  │
         │  └──────────┬──────────────┘  │
         │             │                  │
         └─────────────┴──────────────────┘
                       │
                       ▼ (loop continues)
```

### Real Mode Data Flow

In `--real` mode, plugins use actual system APIs:

```python
# SystemPlugin (real mode)
import psutil
cpu_percent = psutil.cpu_percent(interval=0.1)

# WiFiPlugin (real mode)
import subprocess
result = subprocess.run(['iw', 'dev', 'wlan0', 'scan'], capture_output=True)

# NetworkPlugin (real mode)
import scapy
packets = scapy.sniff(iface='wlan0', count=100, timeout=2)
```

## Plugin System

### Plugin Interface

All plugins must implement `BasePlugin`:

```python
from src.core.base_plugin import BasePlugin
from typing import Dict, Any

class MyCustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__(
            name="my_plugin",
            update_rate_ms=3000  # Update every 3 seconds
        )

    def collect_data(self) -> Dict[str, Any]:
        """
        Collect data and return as dictionary.

        Returns:
            Dict with plugin-specific data structure
        """
        return {
            "metric1": 42,
            "metric2": [1, 2, 3],
            "timestamp": time.time()
        }
```

### Plugin Registration

Plugins are auto-discovered and registered:

```python
# In PluginManager.__init__()
for file in os.listdir("src/plugins"):
    if file.endswith("_plugin.py"):
        module = importlib.import_module(f"src.plugins.{file[:-3]}")
        for item in dir(module):
            cls = getattr(module, item)
            if isinstance(cls, type) and issubclass(cls, BasePlugin):
                self.register_plugin(cls())
```

### Plugin Lifecycle

```
Plugin Created
     │
     ├─> __init__() called
     │       │
     │       └─> initialize() hook (optional)
     │
     ├─> PluginManager.register_plugin()
     │       │
     │       └─> EventBus.publish("plugin_loaded")
     │
     ├─> Every update_rate_ms:
     │       │
     │       └─> collect_data() called
     │               │
     │               └─> EventBus.publish(f"{name}_update", data)
     │
     └─> On shutdown:
             │
             └─> cleanup() hook (optional)
```

## Event System

### Event Bus Implementation

Simple, synchronous pub/sub:

```python
class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any):
        for callback in self._subscribers.get(event_type, []):
            callback(data)  # Synchronous call
```

### Event Best Practices

1. **Keep callbacks fast** (<10ms) - they block the event loop
2. **Use specific event types** - avoid generic "update" events
3. **Include timestamp** - helps with debugging and logging
4. **Handle errors** - wrap callbacks in try/except
5. **Document event schema** - what data structure is expected?

## UI Components

### Component Hierarchy

```
UIComponent (Abstract Base)
    │
    ├─> TextBox
    │     └─> Simple static or dynamic text
    │
    ├─> Sparkline
    │     └─> Time-series mini graph (CPU, RAM)
    │
    ├─> BarChart
    │     └─> Horizontal bars (Disk usage, WiFi signal)
    │
    └─> RunChart
          └─> Line graph with legend (Network bandwidth)
```

### Rich Layout Structure

```python
layout = Layout()
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3)
)

layout["body"].split_row(
    Layout(name="left"),
    Layout(name="right")
)

layout["left"].split_column(
    Layout(name="system", ratio=2),
    Layout(name="wifi", ratio=3)
)
```

## Configuration

### Configuration Hierarchy

1. **Defaults** (`src/config/defaults.py`) - Hardcoded sensible defaults
2. **System config** (`/etc/wifi_dashboard/config.yml`) - System-wide
3. **User config** (`~/.config/wifi_dashboard/config.yml`) - User-specific
4. **CLI flags** (`--real`, `--config path/to/config.yml`) - Highest priority

### Configuration Validation

Uses JSON Schema for validation:

```python
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "dashboard": {
            "type": "object",
            "properties": {
                "refresh_rate_ms": {"type": "integer", "minimum": 100, "maximum": 5000}
            }
        }
    },
    "required": ["dashboard"]
}
```

## Testing Strategy

### Test Pyramid

```
        ┌─────────────┐
        │   Manual    │  11 tests (MOCK-*, REAL-*)
        │  E2E Tests  │
        ├─────────────┤
        │ Integration │  50 tests
        │    Tests    │
        ├─────────────┤
        │    Unit     │  341 tests
        │   Tests     │
        └─────────────┘
```

### Test Coverage (98%)

- **Unit tests** (`tests/unit/`): Test individual functions/classes
- **Integration tests** (`tests/integration/`): Test plugin + EventBus
- **Manual tests** (`tests/manual/`): Test full dashboard in both modes

### Mocking Strategy

- **psutil** → `MockPsutil` class
- **subprocess** (iw, ip commands) → `MockSubprocess`
- **scapy** → `MockScapy` with packet fixtures
- **time.time()** → Controlled clock for deterministic tests

## Performance Considerations

### Target Performance

- **Frame rate**: 10 FPS (100ms per frame)
- **Plugin budget**: <50ms for all plugins combined
- **UI render budget**: <30ms for Rich Console.print()
- **Event bus overhead**: <5ms per frame

### Performance Monitoring

Use `scripts/benchmark.py` to measure:
- Per-plugin collection time
- Full frame time (all plugins + UI)
- FPS over 1000 iterations
- Memory usage

### Optimization Techniques

1. **Lazy updates**: Only update plugins when `update_rate_ms` elapsed
2. **Batch rendering**: Update all UI components in single Rich.print()
3. **Data caching**: Cache expensive computations (WiFi scan)
4. **Adaptive rates**: Slow down plugins that consistently take too long

## Future Extensibility

### v2.1 Planned Features

- **Plugin marketplace**: Download plugins from registry
- **Web UI**: Browser-based dashboard (FastAPI + WebSockets)
- **Alerts**: Configurable thresholds with notifications
- **Logging**: Structured logging to files/syslog

### v3.0 Migration (Textual TUI)

Replace Rich with Textual for:
- **Mouse support**: Click buttons, drag windows
- **Async architecture**: Non-blocking plugin execution
- **Multiple screens**: Navigate between different views
- **Themes**: User-selectable color schemes

### Plugin API Stability

**Guaranteed stable** (won't break in minor versions):
- `BasePlugin.collect_data()` signature
- `EventBus.publish()` / `subscribe()` signatures
- Configuration YAML schema

**May change** (with deprecation warnings):
- `UIFactory` methods (moving to Textual)
- Dashboard internal methods
- PluginManager discovery mechanism

---

## References

- **Design patterns**: Gang of Four (Observer, Factory, Strategy, Template Method)
- **Event-driven architecture**: Martin Fowler's "Enterprise Integration Patterns"
- **Plugin systems**: "Software Architecture Patterns" by Mark Richards
- **Rich library**: https://rich.readthedocs.io/

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for architecture change proposals and [PLUGIN_API.md](./PLUGIN_API.md) for plugin development guide.

---

**Framework**: Constituição Vértice v3.0 (P5 - Consciência Sistêmica)

**Soli Deo Gloria** ✝️
