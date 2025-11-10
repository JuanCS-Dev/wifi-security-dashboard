# Architecture Summary

Quick overview of WiFi Security Dashboard v2.0 architecture.

## High-Level Architecture

```
┌──────────────────────────────────────────────┐
│         main_v2.py (Entry Point)             │
└────────────────┬─────────────────────────────┘
                 │
      ┌──────────┴─────────┐
      ▼                    ▼
┌─────────────┐    ┌─────────────┐
│  Dashboard  │    │   Config    │
│   (Core)    │◄───┤   Loader    │
└──────┬──────┘    └─────────────┘
       │
       ├──► PluginManager ──┬──► SystemPlugin (CPU, RAM)
       │                    ├──► WiFiPlugin (SSID, Signal)
       │                    └──► NetworkPlugin (Bandwidth)
       │
       ├──► EventBus (Pub/Sub)
       │
       └──► UIComponents ──┬──► TextBox
                           ├──► Sparkline
                           ├──► BarChart
                           └──► RunChart
```

## Key Design Patterns

1. **Plugin Architecture**: Modular data collection
2. **Event Bus**: Pub/Sub for decoupling  
3. **Factory Pattern**: Component creation
4. **Strategy Pattern**: Mock vs Real modes
5. **Template Method**: Base Plugin class

## Data Flow

```
Plugin.collect_data() → EventBus.publish() → Dashboard.update() → UI.render()
```

Full details: See ARCHITECTURE.md (planned for v2.1)
