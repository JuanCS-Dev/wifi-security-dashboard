# 📊 DEEP RESEARCH - PARTE 3: ARQUITETURA & IMPLEMENTAÇÃO

**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Projeto:** WiFi Security Education Dashboard - Aula 2
**Objetivo:** Padrões arquiteturais e roadmap de implementação

---

## 🎯 ÍNDICE - PARTE 3

1. [ARQUITETURAS MODULARES](#arquiteturas)
   - 1.1 [Plugin Architecture](#plugin-arch)
   - 1.2 [Composite Pattern](#composite)
   - 1.3 [Observer Pattern](#observer)
   - 1.4 [MVC for TUI](#mvc-tui)
   - 1.5 [Event-Driven Architecture](#event-driven)

2. [PYTHON LIBRARIES PARA TUI](#python-libs)
   - 2.1 [Rich - Terminal Rendering](#rich)
   - 2.2 [Textual - TUI Framework](#textual)
   - 2.3 [urwid - Event Loop TUI](#urwid)
   - 2.4 [Comparativo Técnico](#lib-comparison)

3. [FEATURES PRIORIZADAS](#features)
   - 3.1 [P0 - Críticas (MVP)](#p0-features)
   - 3.2 [P1 - Importantes](#p1-features)
   - 3.3 [P2 - Nice-to-have](#p2-features)
   - 3.4 [Roadmap de Implementação](#roadmap)

4. [PADRÕES DE DESIGN PARA DASHBOARDS](#design-patterns)
   - 4.1 [Sistema de Configuração YAML](#yaml-config)
   - 4.2 [Hot-Reload de Componentes](#hot-reload)
   - 4.3 [Dependency Injection](#dependency-injection)
   - 4.4 [State Management](#state-management)

5. [IMPLEMENTAÇÃO PRÁTICA](#implementacao-pratica)
   - 5.1 [Estrutura de Projeto](#project-structure)
   - 5.2 [Exemplo Completo](#exemplo-completo)

---

<a name="arquiteturas"></a>
## 1. ARQUITETURAS MODULARES

<a name="plugin-arch"></a>
### 1.1 PLUGIN ARCHITECTURE

#### Conceito

Sistema onde **componentes** (dashboards) são **plugins** que podem ser carregados dinamicamente.

**Vantagens:**
- Extensibilidade sem modificar código-base
- Dashboards individuais isolados
- Hot-reload de plugins
- Fácil manutenção

---

#### Implementação Base

```python
# core/plugin_system.py

from abc import ABC, abstractmethod
from typing import Dict, List, Type
import importlib
import inspect

class DashboardPlugin(ABC):
    """Interface base para plugins de dashboard"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome único do dashboard"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição do dashboard"""
        pass

    @abstractmethod
    def collect_data(self):
        """Coleta dados do dashboard"""
        pass

    @abstractmethod
    def render(self) -> Panel:
        """Renderiza dashboard para Rich Panel"""
        pass

    @abstractmethod
    def get_config_schema(self) -> Dict:
        """Retorna schema de configuração"""
        pass


class PluginManager:
    """Gerencia descoberta e carregamento de plugins"""

    def __init__(self, plugin_dir: str = 'plugins'):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, DashboardPlugin] = {}

    def discover_plugins(self):
        """
        Descobre plugins automaticamente

        Busca em:
        - plugins/ directory
        - Classes que herdam de DashboardPlugin
        """
        import os
        import sys

        # Adiciona plugin_dir ao path
        if self.plugin_dir not in sys.path:
            sys.path.insert(0, self.plugin_dir)

        # Lista arquivos .py em plugin_dir
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]

                try:
                    # Importa módulo
                    module = importlib.import_module(module_name)

                    # Busca classes que herdam de DashboardPlugin
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, DashboardPlugin) and obj != DashboardPlugin:
                            # Instancia plugin
                            plugin = obj()
                            self.plugins[plugin.name] = plugin

                except Exception as e:
                    print(f"Erro ao carregar plugin {module_name}: {e}")

    def get_plugin(self, name: str) -> DashboardPlugin:
        """Retorna plugin por nome"""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """Lista nomes de todos os plugins"""
        return list(self.plugins.keys())

    def reload_plugin(self, name: str):
        """Recarrega plugin (hot-reload)"""
        if name in self.plugins:
            module_name = self.plugins[name].__class__.__module__
            module = importlib.reload(importlib.import_module(module_name))

            # Re-instancia
            for cls_name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, DashboardPlugin) and obj != DashboardPlugin:
                    if obj().name == name:
                        self.plugins[name] = obj()
                        break
```

---

#### Exemplo de Plugin

```python
# plugins/network_traffic_dashboard.py

from core.plugin_system import DashboardPlugin
from rich.panel import Panel
from rich.table import Table
import psutil

class NetworkTrafficDashboard(DashboardPlugin):
    """Dashboard de tráfego de rede"""

    @property
    def name(self) -> str:
        return "network_traffic"

    @property
    def description(self) -> str:
        return "Monitora tráfego de rede em tempo real"

    def __init__(self):
        self.data = {}

    def collect_data(self):
        """Coleta dados de rede"""
        io = psutil.net_io_counters(pernic=True)

        self.data = {
            'interfaces': {
                iface: {
                    'bytes_sent': counters.bytes_sent,
                    'bytes_recv': counters.bytes_recv,
                    'packets_sent': counters.packets_sent,
                    'packets_recv': counters.packets_recv
                }
                for iface, counters in io.items()
            }
        }

    def render(self) -> Panel:
        """Renderiza dashboard"""
        table = Table(title="Network Traffic")
        table.add_column("Interface")
        table.add_column("↓ Received")
        table.add_column("↑ Sent")

        for iface, data in self.data['interfaces'].items():
            table.add_row(
                iface,
                f"{data['bytes_recv'] / (1024**2):.2f} MB",
                f"{data['bytes_sent'] / (1024**2):.2f} MB"
            )

        return Panel(table, title=self.description)

    def get_config_schema(self) -> Dict:
        """Schema de configuração"""
        return {
            'refresh_rate_ms': 1000,
            'show_loopback': False,
            'interfaces': ['wlan0', 'eth0']  # Lista de interfaces para monitorar
        }
```

---

#### Uso do Plugin System

```python
# main.py

from core.plugin_system import PluginManager

# Cria gerenciador
manager = PluginManager(plugin_dir='plugins')

# Descobre plugins
manager.discover_plugins()

# Lista plugins disponíveis
print("Plugins disponíveis:")
for plugin_name in manager.list_plugins():
    plugin = manager.get_plugin(plugin_name)
    print(f"  - {plugin_name}: {plugin.description}")

# Carrega plugin específico
network_dash = manager.get_plugin('network_traffic')

# Coleta e renderiza
network_dash.collect_data()
panel = network_dash.render()

console.print(panel)

# Hot-reload (recarrega código sem reiniciar)
manager.reload_plugin('network_traffic')
```

---

<a name="composite"></a>
### 1.2 COMPOSITE PATTERN

#### Conceito

Permite **compor** dashboards complexos a partir de dashboards simples.

**Use case:** Dashboard agregado que combina múltiplos dashboards individuais.

---

#### Implementação

```python
# core/composite_dashboard.py

from typing import List
from rich.layout import Layout
from rich.panel import Panel

class CompositeDashboard(DashboardPlugin):
    """Dashboard que agrega outros dashboards"""

    def __init__(self, children: List[DashboardPlugin], layout_config: Dict):
        """
        Args:
            children: Lista de dashboards filhos
            layout_config: Configuração de layout
        """
        self.children = children
        self.layout_config = layout_config

    @property
    def name(self) -> str:
        return "composite_dashboard"

    @property
    def description(self) -> str:
        child_names = ", ".join([c.name for c in self.children])
        return f"Dashboard agregado: {child_names}"

    def collect_data(self):
        """Coleta dados de todos os filhos"""
        for child in self.children:
            child.collect_data()

    def render(self) -> Layout:
        """
        Renderiza todos os dashboards filhos em layout configurado

        layout_config exemplo:
        {
            'type': 'split_column',
            'children': [
                {'plugin': 'network_traffic', 'size': 10},
                {'plugin': 'system_monitor', 'ratio': 1}
            ]
        }
        """
        layout = Layout()

        # Parse layout config e cria estrutura
        self._build_layout(layout, self.layout_config)

        # Popula com renderizações dos filhos
        for child in self.children:
            layout[child.name].update(child.render())

        return layout

    def _build_layout(self, parent: Layout, config: Dict):
        """Constrói layout recursivamente"""
        if config['type'] == 'split_column':
            children_layouts = []

            for child_config in config['children']:
                child_layout = Layout(name=child_config['plugin'])

                if 'size' in child_config:
                    child_layout.size = child_config['size']
                elif 'ratio' in child_config:
                    child_layout.ratio = child_config['ratio']

                children_layouts.append(child_layout)

            parent.split_column(*children_layouts)

        elif config['type'] == 'split_row':
            children_layouts = []

            for child_config in config['children']:
                child_layout = Layout(name=child_config['plugin'])

                if 'size' in child_config:
                    child_layout.size = child_config['size']
                elif 'ratio' in child_config:
                    child_layout.ratio = child_config['ratio']

                children_layouts.append(child_layout)

            parent.split_row(*children_layouts)

    def get_config_schema(self) -> Dict:
        """Schema combina schemas dos filhos"""
        return {
            'layout': self.layout_config,
            'children_configs': {
                child.name: child.get_config_schema()
                for child in self.children
            }
        }
```

---

#### Uso do Composite

```python
# Cria dashboards individuais
network_dash = manager.get_plugin('network_traffic')
system_dash = manager.get_plugin('system_monitor')
wifi_dash = manager.get_plugin('wifi_analysis')

# Configura layout
layout_config = {
    'type': 'split_column',
    'children': [
        {
            'type': 'split_row',
            'children': [
                {'plugin': 'network_traffic', 'ratio': 1},
                {'plugin': 'system_monitor', 'ratio': 1}
            ],
            'size': 20
        },
        {
            'plugin': 'wifi_analysis',
            'ratio': 1
        }
    ]
}

# Cria dashboard composto
composite = CompositeDashboard(
    children=[network_dash, system_dash, wifi_dash],
    layout_config=layout_config
)

# Usa como qualquer outro dashboard
composite.collect_data()
layout = composite.render()

with Live(layout, refresh_per_second=4) as live:
    while True:
        composite.collect_data()
        live.update(composite.render())
        time.sleep(0.25)
```

---

<a name="observer"></a>
### 1.3 OBSERVER PATTERN

#### Conceito

Dashboards **observam** mudanças nos dados e reagem automaticamente.

**Use case:** Atualização reativa quando dados mudam.

---

#### Implementação

```python
# core/observable.py

from typing import Callable, List

class Observable:
    """Objeto observável (Subject)"""

    def __init__(self):
        self._observers: List[Callable] = []

    def attach(self, observer: Callable):
        """Adiciona observador"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Callable):
        """Remove observador"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        """Notifica todos os observadores"""
        for observer in self._observers:
            observer(*args, **kwargs)


class DataSource(Observable):
    """Fonte de dados observável"""

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        """Quando dados mudam, notifica observadores"""
        old_value = self._data
        self._data = value

        # Notifica mudança
        self.notify(old_value=old_value, new_value=value)


# Exemplo: Dashboard como Observer

class NetworkDashboard(DashboardPlugin):
    """Dashboard que observa dados de rede"""

    def __init__(self, data_source: DataSource):
        self.data_source = data_source
        self.cached_render = None

        # Registra como observer
        self.data_source.attach(self._on_data_changed)

    def _on_data_changed(self, old_value, new_value):
        """Callback quando dados mudam"""
        # Invalida cache
        self.cached_render = None

        # Poderia fazer processamento adicional aqui
        if new_value and 'bandwidth' in new_value:
            if new_value['bandwidth'] > 100:  # MB/s
                print("⚠️  High bandwidth detected!")

    def collect_data(self):
        """Coleta dados e atualiza data source"""
        io = psutil.net_io_counters()

        # Atualizar data source automaticamente notifica observers
        self.data_source.data = {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
            'bandwidth': calculate_bandwidth()
        }

    def render(self) -> Panel:
        """Renderiza (usa cache se disponível)"""
        if self.cached_render is None:
            # Re-renderiza
            self.cached_render = self._build_panel()

        return self.cached_render

    def _build_panel(self) -> Panel:
        """Constrói panel do zero"""
        # ... lógica de renderização
        pass
```

---

<a name="mvc-tui"></a>
### 1.4 MVC FOR TUI

#### Conceito

Separação de responsabilidades:
- **Model:** Dados e lógica de negócio
- **View:** Renderização visual
- **Controller:** Coordenação e input handling

---

#### Implementação

```python
# mvc/model.py

class NetworkModel:
    """Model: Dados e lógica de rede"""

    def __init__(self):
        self._bandwidth = 0
        self._connections = []
        self._observers = []

    def update(self):
        """Atualiza dados do modelo"""
        # Coleta dados reais
        self._bandwidth = self._calculate_bandwidth()
        self._connections = self._get_connections()

        # Notifica views
        self._notify_observers()

    def get_bandwidth(self) -> float:
        """Retorna bandwidth atual"""
        return self._bandwidth

    def get_connections(self) -> List:
        """Retorna conexões ativas"""
        return self._connections

    def _calculate_bandwidth(self) -> float:
        """Calcula bandwidth (lógica de negócio)"""
        # ... implementação
        pass

    def _get_connections(self) -> List:
        """Obtém conexões (lógica de negócio)"""
        # ... implementação
        pass

    def attach_observer(self, observer):
        """Adiciona observer (View)"""
        self._observers.append(observer)

    def _notify_observers(self):
        """Notifica views sobre mudanças"""
        for observer in self._observers:
            observer.on_model_changed()


# mvc/view.py

class NetworkView:
    """View: Renderização visual"""

    def __init__(self, model: NetworkModel):
        self.model = model
        self.model.attach_observer(self)

    def on_model_changed(self):
        """Callback quando modelo muda"""
        # View pode decidir se re-renderiza ou não
        pass

    def render(self) -> Panel:
        """Renderiza view baseado no modelo"""
        bandwidth = self.model.get_bandwidth()
        connections = self.model.get_connections()

        # Cria visualização
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Bandwidth", f"{bandwidth:.2f} MB/s")
        table.add_row("Connections", str(len(connections)))

        return Panel(table, title="Network Stats")


# mvc/controller.py

class NetworkController:
    """Controller: Coordenação e input"""

    def __init__(self, model: NetworkModel, view: NetworkView):
        self.model = model
        self.view = view

    def update(self):
        """Atualiza modelo (periodicamen
te)"""
        self.model.update()

    def handle_input(self, key: str):
        """Processa input do usuário"""
        if key == 'r':
            # Reset
            self.model.reset()
        elif key == 'f':
            # Filter
            self.model.set_filter(...)
        # ...

    def get_view(self) -> Panel:
        """Retorna view renderizada"""
        return self.view.render()


# Uso MVC

model = NetworkModel()
view = NetworkView(model)
controller = NetworkController(model, view)

# Loop
with Live(controller.get_view(), refresh_per_second=4) as live:
    while True:
        controller.update()
        live.update(controller.get_view())

        # Handle input (simplificado)
        # key = get_keypress()
        # controller.handle_input(key)

        time.sleep(0.25)
```

---

<a name="event-driven"></a>
### 1.5 EVENT-DRIVEN ARCHITECTURE

#### Conceito

Sistema baseado em **eventos** e **event handlers**.

**Vantagens:**
- Baixo acoplamento
- Fácil adicionar novos handlers
- Assíncrono

---

#### Implementação

```python
# core/event_system.py

from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class Event:
    """Evento base"""
    type: str
    data: Dict
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventBus:
    """Bus de eventos central"""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        """Inscreve handler para tipo de evento"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable):
        """Remove handler"""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    def publish(self, event: Event):
        """Publica evento (síncrono)"""
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                handler(event)

    async def publish_async(self, event: Event):
        """Publica evento (assíncrono)"""
        if event.type in self._handlers:
            tasks = [
                asyncio.create_task(handler(event))
                for handler in self._handlers[event.type]
            ]
            await asyncio.gather(*tasks)


# Exemplo de uso

class NetworkMonitor:
    """Monitor que publica eventos"""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def check_bandwidth(self):
        """Verifica bandwidth e publica eventos"""
        current_bw = self._get_bandwidth()

        # Publica evento
        self.event_bus.publish(Event(
            type='bandwidth_measured',
            data={'bandwidth_mbps': current_bw}
        ))

        # Publica alerta se necessário
        if current_bw > 100:
            self.event_bus.publish(Event(
                type='high_bandwidth_alert',
                data={'bandwidth_mbps': current_bw}
            ))


class BandwidthLogger:
    """Handler que loga bandwidth"""

    def __init__(self, event_bus: EventBus):
        # Inscreve-se em eventos
        event_bus.subscribe('bandwidth_measured', self.on_bandwidth_measured)

    def on_bandwidth_measured(self, event: Event):
        """Handler de evento"""
        bw = event.data['bandwidth_mbps']
        print(f"[{event.timestamp}] Bandwidth: {bw:.2f} MB/s")


class AlertDashboard:
    """Dashboard que mostra alertas"""

    def __init__(self, event_bus: EventBus):
        self.alerts = []
        event_bus.subscribe('high_bandwidth_alert', self.on_alert)

    def on_alert(self, event: Event):
        """Handler de alerta"""
        self.alerts.append(event)
        # Atualiza UI
        self.render()

    def render(self):
        """Renderiza alertas"""
        for alert in self.alerts[-10:]:  # Últimos 10
            print(f"⚠️  {alert.data}")


# Setup
event_bus = EventBus()

monitor = NetworkMonitor(event_bus)
logger = BandwidthLogger(event_bus)
alert_dash = AlertDashboard(event_bus)

# Simula monitoramento
while True:
    monitor.check_bandwidth()
    time.sleep(1)
```

---

<a name="python-libs"></a>
## 2. PYTHON LIBRARIES PARA TUI

<a name="rich"></a>
### 2.1 RICH - TERMINAL RENDERING

**GitHub:** https://github.com/Textualize/rich
**Docs:** https://rich.readthedocs.io/

#### Overview

**Rich** é uma biblioteca Python para renderização avançada em terminal.

**Features:**
- Renderização de tabelas, painéis, árvores
- Syntax highlighting
- Progress bars
- Live display (auto-refresh)
- Markdown rendering
- Logging com cores

**Já usamos Rich no projeto atual!**

---

#### Features Avançadas

**1. Live Display:**

```python
from rich.live import Live
from rich.table import Table
import time

def generate_table():
    table = Table()
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("CPU", f"{psutil.cpu_percent()}%")
    table.add_row("Memory", f"{psutil.virtual_memory().percent}%")

    return table

with Live(generate_table(), refresh_per_second=4) as live:
    while True:
        time.sleep(0.25)
        live.update(generate_table())
```

**2. Console Groups (Múltiplos Renderables):**

```python
from rich.console import Group

# Agrupa múltiplos renderables
group = Group(
    Panel("Panel 1"),
    Table(...),
    Text("Some text"),
    Panel("Panel 2")
)

console.print(group)
```

**3. Syntax Highlighting:**

```python
from rich.syntax import Syntax

code = '''
def hello():
    print("Hello World")
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

**4. Progress Bars:**

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=100)

    for i in range(100):
        time.sleep(0.1)
        progress.update(task, advance=1)
```

**5. Logging:**

```python
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")
log.error("Something went wrong!")
```

---

<a name="textual"></a>
### 2.2 TEXTUAL - TUI FRAMEWORK

**GitHub:** https://github.com/Textualize/textual
**Docs:** https://textual.textualize.io/

#### Overview

**Textual** é um framework completo para criar TUIs complexas, criado pelos mesmos autores do Rich.

**Features:**
- Widgets reativos (botões, inputs, tabelas)
- CSS-like styling
- Layout flexível
- Event handling
- Mouse support
- Animações
- Hot-reload (dev mode)

---

#### Arquitetura Textual

```
Textual App
├── Widgets (componentes reativos)
│   ├── Button
│   ├── Input
│   ├── DataTable
│   ├── Static (texto estático)
│   └── Custom Widgets
├── Screens (telas/views)
├── CSS Styling
└── Reactive Attributes
```

---

#### Exemplo Completo

```python
# textual_dashboard.py

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
import psutil

class SystemStats(Static):
    """Widget de stats do sistema (reativo)"""

    cpu_percent = reactive(0.0)
    mem_percent = reactive(0.0)

    def compose(self) -> ComposeResult:
        yield Static(id="cpu")
        yield Static(id="mem")

    def on_mount(self) -> None:
        """Quando widget é montado"""
        self.update_timer = self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        """Atualiza stats (chamado a cada 1s)"""
        self.cpu_percent = psutil.cpu_percent()
        self.mem_percent = psutil.virtual_memory().percent

    def watch_cpu_percent(self, value: float) -> None:
        """Callback quando cpu_percent muda (reactive!)"""
        self.query_one("#cpu").update(f"CPU: {value:.1f}%")

    def watch_mem_percent(self, value: float) -> None:
        """Callback quando mem_percent muda"""
        self.query_one("#mem").update(f"Memory: {value:.1f}%")


class NetworkTable(DataTable):
    """Tabela de rede"""

    def on_mount(self) -> None:
        self.add_column("Interface")
        self.add_column("Sent")
        self.add_column("Received")

        self.update_timer = self.set_interval(2, self.update_data)

    def update_data(self) -> None:
        """Atualiza dados da tabela"""
        self.clear()

        io = psutil.net_io_counters(pernic=True)
        for iface, counters in io.items():
            self.add_row(
                iface,
                f"{counters.bytes_sent / (1024**2):.2f} MB",
                f"{counters.bytes_recv / (1024**2):.2f} MB"
            )


class DashboardApp(App):
    """App principal"""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
    }

    SystemStats {
        border: solid green;
        padding: 1;
    }

    NetworkTable {
        border: solid cyan;
    }

    Button {
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        """Compõe UI"""
        yield Header()
        yield SystemStats()
        yield NetworkTable()
        yield Footer()

    def action_quit(self) -> None:
        """Action: quit"""
        self.exit()

    def action_refresh(self) -> None:
        """Action: refresh"""
        # Força refresh de todos os widgets
        for widget in self.query(SystemStats):
            widget.update_stats()

if __name__ == "__main__":
    app = DashboardApp()
    app.run()
```

---

#### Reactive Attributes

**Conceito chave do Textual:**

```python
from textual.reactive import reactive

class MyWidget(Widget):
    # Atributo reativo
    counter = reactive(0)

    def watch_counter(self, old_value, new_value):
        """Chamado automaticamente quando counter muda"""
        self.update(f"Counter: {new_value}")

    def on_button_pressed(self):
        # Incrementar counter automaticamente chama watch_counter
        self.counter += 1
```

---

<a name="urwid"></a>
### 2.3 URWID - EVENT LOOP TUI

**Website:** https://urwid.org/
**GitHub:** https://github.com/urwid/urwid

#### Overview

**urwid** é uma biblioteca madura para TUIs com event loop integrado.

**Features:**
- Event-driven
- Widgets diversos (text, buttons, lists, etc.)
- Layout flexível
- Mouse support
- Diversos backends (raw, curses, etc.)

---

#### Exemplo

```python
import urwid

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)

    def open_menu(button):
        return contents

    return menu_button([caption, "..."], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = menu_button(u'Ok', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response, done]))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Main Menu', [
    sub_menu(u'Applications', [
        menu_button(u'Textual Dashboard', item_chosen),
        menu_button(u'Network Monitor', item_chosen),
    ]),
    menu_button(u'Exit', exit_program),
])

main = urwid.Padding(menu_top, left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)

urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
```

---

<a name="lib-comparison"></a>
### 2.4 COMPARATIVO TÉCNICO

| Feature | Rich | Textual | urwid |
|---------|------|---------|-------|
| **Tipo** | Rendering | Framework | Framework |
| **Curva de Aprendizado** | Baixa | Média | Alta |
| **Widgets** | ❌ (apenas rendering) | ✅ Reativos | ✅ Tradicionais |
| **Event Handling** | ❌ | ✅ | ✅ |
| **Mouse Support** | ❌ | ✅ | ✅ |
| **Live Updates** | ✅ (manual) | ✅ (reativo) | ✅ (event loop) |
| **Styling** | Inline | CSS-like | Palette |
| **Hot-Reload** | ❌ | ✅ (dev mode) | ❌ |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Documentação** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Comunidade** | Grande | Crescendo | Estabelecida |

**Recomendações:**

- **Rich:** Ideal para dashboards simples, rendering rápido, já conhecemos
- **Textual:** Melhor para UIs complexas, interativas, reatividade
- **urwid:** Para apps tradicionais TUI, maior controle low-level

**Nossa escolha:**
- **Continuar com Rich** para dashboards individuais (simples, rápido)
- **Migrar para Textual** para dashboard agregado (interativo, features avançadas)

---

<a name="features"></a>
## 3. FEATURES PRIORIZADAS

<a name="p0-features"></a>
### 3.1 P0 - CRÍTICAS (MVP)

Features essenciais para lançamento inicial.

#### 1. Network Traffic Dashboard

**Descrição:** Dashboard dedicado a análise de tráfego de rede.

**Features:**
- Real-time bandwidth monitoring (download/upload)
- Top talkers (IPs que mais consomem)
- Protocol distribution (TCP, UDP, ICMP, %)
- Connection table (source → dest, port, state)
- Packet count
- Historical graphs (últimos 60s)

**Implementação:**
```python
# plugins/network_traffic_dashboard.py
# - Usa psutil para bandwidth
# - Usa scapy para packet analysis
# - Gráficos com plotext
# - Tabelas com Rich
```

---

#### 2. System Monitor Dashboard (Expandir Atual)

**Descrição:** Expandir dashboard de sistema atual.

**Adicionar:**
- CPU per-core breakdown
- Temperatura detalhada (múltiplos sensores)
- Disk I/O (read/write MB/s)
- Network interfaces stats
- Top processes (CPU e Memory consumers)

**Implementação:**
```python
# Expandir dashboard_ui.py atual
# - psutil.cpu_percent(percpu=True)
# - psutil.sensors_temperatures()
# - psutil.disk_io_counters()
```

---

#### 3. WiFi Analysis Dashboard (Expandir Atual)

**Descrição:** Análise profunda de WiFi.

**Adicionar:**
- Signal strength history graph
- Channel analysis (congestion)
- Security audit (WPA2/WPA3 check)
- Connected devices deep dive
- Nearby networks scan

**Implementação:**
```python
# Usar iw/iwconfig
# Gráfico de signal strength com plotext
# Scan de redes com airodump-ng (educational mode)
```

---

#### 4. Dashboard Agregado

**Descrição:** Dashboard que combina todos os dashboards individuais.

**Features:**
- Layout configurável
- Switch entre dashboards (tabs)
- Overview mode (todos visíveis)
- Focus mode (apenas um dashboard)

**Implementação:**
```python
# Usar CompositeDashboard
# Layout config via YAML
# Teclas 1-9 para switch
```

---

<a name="p1-features"></a>
### 3.2 P1 - IMPORTANTES

Features importantes mas não bloqueantes.

#### 1. Application Monitor Dashboard

**Descrição:** Monitora aplicações específicas.

**Features:**
- Per-app bandwidth usage
- Protocol breakdown per app
- Connection tracking per app
- Whitelist/blacklist
- App detection (YouTube, Netflix, Spotify, etc.)

**Implementação:**
```python
# Combinar psutil (processos) + scapy (pacotes)
# Matching de porta → processo → app
```

---

#### 2. Filtragem Avançada

**Descrição:** Sistema de filtros tipo Wireshark.

**Features:**
- Query language (`port == 443 and protocol == tcp`)
- Filtros salvos/favoritos
- Filter builder UI
- Export filtered data

**Implementação:**
```python
# Parser de query (pyparsing)
# Aplicar filtros em DataFrames (pandas)
```

---

#### 3. Alertas e Notificações

**Descrição:** Sistema de alertas configurável.

**Features:**
- Threshold-based alerts (CPU > 90%, bandwidth > 100MB/s)
- Pattern-based alerts (port scan detected)
- Visual indicators
- Sound alerts (beep)
- Desktop notifications (notify-send)
- Log de alertas

**Implementação:**
```python
# Event system
# Thresholds em config YAML
# notif y-send para desktop notifications
```

---

#### 4. Export e Logging

**Descrição:** Exportar dados e logs.

**Features:**
- CSV export
- JSON export
- Continuous logging
- Replay mode (replay de logs)

**Implementação:**
```python
# pandas.to_csv()
# json.dump()
# Rotate logs (logging.handlers.RotatingFileHandler)
```

---

<a name="p2-features"></a>
### 3.3 P2 - NICE-TO-HAVE

Features desejáveis mas não prioritárias.

#### 1. Security Dashboard

**Descrição:** Análise de segurança.

**Features:**
- Anomaly detection (ML-based)
- Port scan detection
- Unusual traffic patterns
- Security score
- Recommendations

---

#### 2. Historical Analysis

**Descrição:** Análise histórica de longo prazo.

**Features:**
- Database backend (SQLite)
- Trending (diário, semanal, mensal)
- Reports automáticos
- Comparação de períodos

---

#### 3. Remote Monitoring

**Descrição:** Monitorar múltiplos hosts.

**Features:**
- Agent-server architecture
- Central dashboard
- Multi-host view

---

<a name="roadmap"></a>
### 3.4 ROADMAP DE IMPLEMENTAÇÃO

#### Sprint 1 (2 semanas) - Infrastructure

**Goals:**
- ✅ Plugin system completo
- ✅ Composite dashboard
- ✅ Event system
- ✅ Config YAML loading

**Deliverables:**
- Core architecture funcionando
- 1-2 plugins de exemplo

---

#### Sprint 2 (2 semanas) - Network Traffic Dashboard

**Goals:**
- ✅ Real-time bandwidth
- ✅ Top talkers
- ✅ Protocol distribution
- ✅ Connection table

**Deliverables:**
- Network Traffic Dashboard completo
- Testes básicos

---

#### Sprint 3 (2 semanas) - System + WiFi Dashboards

**Goals:**
- ✅ Expandir System Monitor
- ✅ Expandir WiFi Analysis
- ✅ Integração com novo sistema

**Deliverables:**
- 2 dashboards refatorados
- Migração completa para novo sistema

---

#### Sprint 4 (2 semanas) - Dashboard Agregado

**Goals:**
- ✅ Layout manager
- ✅ Tab switching
- ✅ Overview + Focus modes
- ✅ Config YAML

**Deliverables:**
- Dashboard agregado funcional
- Aula 2 completa!

---

#### Sprint 5 (1-2 semanas) - Application Monitor + Filters

**Goals:**
- ✅ Application Monitor dashboard
- ✅ Query language parser
- ✅ Filter UI

**Deliverables:**
- Features P1 principais

---

#### Sprint 6 (1 semana) - Polish + Alertas

**Goals:**
- ✅ Sistema de alertas
- ✅ Export/logging
- ✅ Polimento visual
- ✅ Documentação

**Deliverables:**
- Versão 2.0 release-ready!

---

<a name="design-patterns"></a>
## 4. PADRÕES DE DESIGN PARA DASHBOARDS

<a name="yaml-config"></a>
### 4.1 SISTEMA DE CONFIGURAÇÃO YAML

#### Estrutura de Config

```yaml
# config/dashboard.yml

# Configuração global
global:
  refresh_rate_ms: 250
  theme: "dark"
  log_level: "INFO"

# Plugins disponíveis
plugins:
  - name: "network_traffic"
    enabled: true
    config:
      interface: "wlan0"
      show_loopback: false
      top_talkers_count: 10

  - name: "system_monitor"
    enabled: true
    config:
      show_per_core: true
      temperature_unit: "celsius"

  - name: "wifi_analysis"
    enabled: true
    config:
      scan_interval_sec: 30
      show_nearby_networks: true

# Layouts
layouts:
  - name: "default"
    description: "Layout padrão com todos os dashboards"
    structure:
      type: "split_column"
      children:
        - type: "split_row"
          size: 20
          children:
            - plugin: "network_traffic"
              ratio: 1
            - plugin: "system_monitor"
              ratio: 1

        - plugin: "wifi_analysis"
          ratio: 1

  - name: "network_focused"
    description: "Foco em análise de rede"
    structure:
      plugin: "network_traffic"

# Alertas
alerts:
  - name: "high_cpu"
    condition: "cpu_percent > 90"
    actions:
      - type: "visual"
        color: "red"
      - type: "sound"
        frequency: 800
        duration: 300
      - type: "log"
        message: "High CPU detected: {cpu_percent}%"

  - name: "high_bandwidth"
    condition: "bandwidth_mbps > 100"
    actions:
      - type: "notification"
        title: "High Bandwidth"
        message: "Bandwidth: {bandwidth_mbps} MB/s"

# Filtros salvos
filters:
  - name: "https_only"
    query: "port == 443 or port == 8443"

  - name: "youtube_traffic"
    query: "host contains youtube.com or host contains googlevideo.com"
```

---

#### Config Loader

```python
# core/config_loader.py

import yaml
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class GlobalConfig:
    refresh_rate_ms: int
    theme: str
    log_level: str

@dataclass
class PluginConfig:
    name: str
    enabled: bool
    config: Dict

@dataclass
class LayoutConfig:
    name: str
    description: str
    structure: Dict

@dataclass
class AlertConfig:
    name: str
    condition: str
    actions: List[Dict]

@dataclass
class DashboardConfig:
    global_config: GlobalConfig
    plugins: List[PluginConfig]
    layouts: List[LayoutConfig]
    alerts: List[AlertConfig]
    filters: Dict[str, str]


class ConfigLoader:
    """Carrega e valida configuração YAML"""

    @staticmethod
    def load(config_path: str) -> DashboardConfig:
        """
        Carrega config de arquivo YAML

        Returns:
            DashboardConfig object
        """
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        # Parse sections
        global_config = GlobalConfig(**data['global'])

        plugins = [
            PluginConfig(**plugin)
            for plugin in data['plugins']
        ]

        layouts = [
            LayoutConfig(**layout)
            for layout in data['layouts']
        ]

        alerts = [
            AlertConfig(**alert)
            for alert in data['alerts']
        ]

        filters = data.get('filters', {})

        return DashboardConfig(
            global_config=global_config,
            plugins=plugins,
            layouts=layouts,
            alerts=alerts,
            filters=filters
        )

    @staticmethod
    def save(config: DashboardConfig, config_path: str):
        """Salva config em arquivo YAML"""
        data = {
            'global': {
                'refresh_rate_ms': config.global_config.refresh_rate_ms,
                'theme': config.global_config.theme,
                'log_level': config.global_config.log_level
            },
            'plugins': [
                {
                    'name': p.name,
                    'enabled': p.enabled,
                    'config': p.config
                }
                for p in config.plugins
            ],
            # ... resto
        }

        with open(config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
```

---

<a name="hot-reload"></a>
### 4.2 HOT-RELOAD DE COMPONENTES

#### Implementação

```python
# core/hot_reload.py

import importlib
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PluginReloadHandler(FileSystemEventHandler):
    """Handler para detectar mudanças em plugins"""

    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager

    def on_modified(self, event):
        """Quando arquivo é modificado"""
        if event.src_path.endswith('.py'):
            # Extrai nome do módulo
            module_name = event.src_path.split('/')[-1][:-3]

            # Recarrega plugin
            try:
                self.plugin_manager.reload_plugin(module_name)
                print(f"✅ Plugin '{module_name}' reloaded successfully")
            except Exception as e:
                print(f"❌ Error reloading '{module_name}': {e}")


class HotReloader:
    """Sistema de hot-reload"""

    def __init__(self, plugin_manager, watch_dir='plugins'):
        self.plugin_manager = plugin_manager
        self.watch_dir = watch_dir
        self.observer = None

    def start(self):
        """Inicia watching"""
        event_handler = PluginReloadHandler(self.plugin_manager)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        print(f"🔥 Hot-reload enabled for '{self.watch_dir}'")

    def stop(self):
        """Para watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()

# Uso
hot_reloader = HotReloader(plugin_manager)
hot_reloader.start()

# Agora, qualquer mudança em plugins/ recarrega automaticamente!
```

---

<a name="dependency-injection"></a>
### 4.3 DEPENDENCY INJECTION

#### Implementação

```python
# core/dependency_injection.py

from typing import Dict, Type, Any

class ServiceContainer:
    """Container de serviços (DI)"""

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}

    def register(self, name: str, service: Any):
        """Registra serviço (singleton)"""
        self._services[name] = service

    def register_factory(self, name: str, factory: callable):
        """Registra factory (cria nova instância a cada get)"""
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        """Obtém serviço"""
        # Verifica se já existe singleton
        if name in self._services:
            return self._services[name]

        # Verifica se tem factory
        if name in self._factories:
            return self._factories[name]()

        raise KeyError(f"Service '{name}' not found")

    def inject(self, cls: Type) -> Any:
        """
        Injeta dependências automaticamente

        Busca por type hints no __init__
        """
        import inspect

        # Obtém signature do __init__
        sig = inspect.signature(cls.__init__)

        # Injeta parâmetros
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue

            # Tenta obter serviço
            if param.annotation != inspect.Parameter.empty:
                service_name = param.annotation.__name__.lower()
                if service_name in self._services or service_name in self._factories:
                    kwargs[param_name] = self.get(service_name)

        return cls(**kwargs)


# Uso

# Setup container
container = ServiceContainer()

# Registra serviços
container.register('config', config_loader.load('config.yml'))
container.register('event_bus', EventBus())
container.register_factory('database', lambda: Database())

# Plugin com DI
class NetworkDashboard(DashboardPlugin):
    def __init__(self, config: Config, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
    # ...

# Injeta automaticamente!
dashboard = container.inject(NetworkDashboard)
```

---

<a name="state-management"></a>
### 4.4 STATE MANAGEMENT

#### Implementação (Redux-like)

```python
# core/state_management.py

from typing import Dict, Callable, Any
from dataclasses import dataclass
import copy

@dataclass
class Action:
    """Ação que modifica state"""
    type: str
    payload: Dict = None

class Store:
    """Store central de state (Redux-like)"""

    def __init__(self, initial_state: Dict, reducer: Callable):
        """
        Args:
            initial_state: State inicial
            reducer: Função (state, action) -> new_state
        """
        self._state = copy.deepcopy(initial_state)
        self._reducer = reducer
        self._subscribers = []

    def get_state(self) -> Dict:
        """Retorna state atual (read-only)"""
        return copy.deepcopy(self._state)

    def dispatch(self, action: Action):
        """Dispara ação que modifica state"""
        # Aplica reducer
        new_state = self._reducer(self._state, action)

        # Atualiza state
        self._state = new_state

        # Notifica subscribers
        self._notify_subscribers()

    def subscribe(self, callback: Callable):
        """Inscreve callback para mudanças de state"""
        self._subscribers.append(callback)

    def _notify_subscribers(self):
        """Notifica todos os subscribers"""
        for callback in self._subscribers:
            callback(self._state)


# Reducer
def dashboard_reducer(state: Dict, action: Action) -> Dict:
    """
    Reducer principal

    State shape:
    {
        'network': {
            'bandwidth_mbps': 0.0,
            'connections': [],
            ...
        },
        'system': {
            'cpu_percent': 0.0,
            'mem_percent': 0.0,
            ...
        },
        'ui': {
            'active_dashboard': 'network_traffic',
            'filter_query': '',
            ...
        }
    }
    """
    new_state = copy.deepcopy(state)

    if action.type == 'UPDATE_BANDWIDTH':
        new_state['network']['bandwidth_mbps'] = action.payload['bandwidth_mbps']

    elif action.type == 'UPDATE_CPU':
        new_state['system']['cpu_percent'] = action.payload['cpu_percent']

    elif action.type == 'SWITCH_DASHBOARD':
        new_state['ui']['active_dashboard'] = action.payload['dashboard_name']

    elif action.type == 'SET_FILTER':
        new_state['ui']['filter_query'] = action.payload['query']

    # ... outros actions

    return new_state


# Uso

initial_state = {
    'network': {'bandwidth_mbps': 0.0, 'connections': []},
    'system': {'cpu_percent': 0.0, 'mem_percent': 0.0},
    'ui': {'active_dashboard': 'network_traffic', 'filter_query': ''}
}

store = Store(initial_state, dashboard_reducer)

# Subscribe
def on_state_change(state):
    print(f"State changed: {state}")

store.subscribe(on_state_change)

# Dispatch actions
store.dispatch(Action('UPDATE_BANDWIDTH', {'bandwidth_mbps': 50.5}))
store.dispatch(Action('SWITCH_DASHBOARD', {'dashboard_name': 'system_monitor'}))

# Get state
current_state = store.get_state()
print(f"Current dashboard: {current_state['ui']['active_dashboard']}")
```

---

<a name="implementacao-pratica"></a>
## 5. IMPLEMENTAÇÃO PRÁTICA

<a name="project-structure"></a>
### 5.1 ESTRUTURA DE PROJETO

```
wifi_security_education/
├── main.py                          # Entry point
├── config/
│   └── dashboard.yml                # Configuração principal
├── core/
│   ├── __init__.py
│   ├── plugin_system.py             # Sistema de plugins
│   ├── composite_dashboard.py       # Composite pattern
│   ├── event_system.py              # Event bus
│   ├── config_loader.py             # YAML loader
│   ├── hot_reload.py                # Hot-reload
│   ├── dependency_injection.py      # DI container
│   └── state_management.py          # State store
├── plugins/
│   ├── __init__.py
│   ├── network_traffic_dashboard.py
│   ├── system_monitor_dashboard.py
│   ├── wifi_analysis_dashboard.py
│   └── application_monitor_dashboard.py
├── renderers/
│   ├── __init__.py
│   ├── chart_renderer.py            # Gráficos (plotext)
│   ├── table_renderer.py            # Tabelas (Rich)
│   └── progress_renderer.py         # Progress bars
├── data_collectors/
│   ├── __init__.py
│   ├── network_collector.py         # Coleta dados de rede
│   ├── system_collector.py          # Coleta dados de sistema
│   └── wifi_collector.py            # Coleta dados WiFi
├── models/
│   ├── __init__.py
│   ├── network_snapshot.py          # Data models
│   └── config_models.py
├── utils/
│   ├── __init__.py
│   ├── filters.py                   # Query language parser
│   └── alerts.py                    # Sistema de alertas
└── tests/
    ├── test_plugins.py
    ├── test_collectors.py
    └── test_filters.py
```

---

<a name="exemplo-completo"></a>
### 5.2 EXEMPLO COMPLETO

#### main.py

```python
#!/usr/bin/env python3
"""
WiFi Security Education Dashboard v2.0
Aula 2: Dashboard Profissional com Sistema Modular

Juan-Dev - Soli Deo Gloria ✝️
"""

import sys
from rich.console import Console
from rich.live import Live
import signal

from core.plugin_system import PluginManager
from core.composite_dashboard import CompositeDashboard
from core.config_loader import ConfigLoader
from core.dependency_injection import ServiceContainer
from core.event_system import EventBus
from core.hot_reload import HotReloader

console = Console()

class DashboardApp:
    """Aplicação principal"""

    def __init__(self, config_path='config/dashboard.yml'):
        # Carrega config
        self.config = ConfigLoader.load(config_path)

        # Setup DI container
        self.container = ServiceContainer()
        self.container.register('config', self.config)
        self.container.register('event_bus', EventBus())
        self.container.register('console', console)

        # Setup plugin manager
        self.plugin_manager = PluginManager(plugin_dir='plugins')
        self.plugin_manager.discover_plugins()
        self.container.register('plugin_manager', self.plugin_manager)

        # Setup hot-reload (dev mode)
        if '--dev' in sys.argv:
            self.hot_reloader = HotReloader(self.plugin_manager)
            self.hot_reloader.start()

        # Cria dashboard agregado
        self.dashboard = self._create_dashboard()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)

    def _create_dashboard(self) -> CompositeDashboard:
        """Cria dashboard baseado em config"""
        # Carrega plugins enabled
        plugins = []
        for plugin_config in self.config.plugins:
            if plugin_config.enabled:
                plugin = self.plugin_manager.get_plugin(plugin_config.name)
                if plugin:
                    plugins.append(plugin)

        # Usa layout padrão
        default_layout = next(
            (l for l in self.config.layouts if l.name == 'default'),
            None
        )

        if not default_layout:
            raise ValueError("No default layout found in config!")

        # Cria composite
        return CompositeDashboard(
            children=plugins,
            layout_config=default_layout.structure
        )

    def run(self):
        """Loop principal"""
        console.print("[cyan]🚀 WiFi Security Education Dashboard v2.0[/cyan]")
        console.print("[cyan]   Press 'q' to quit[/cyan]\n")

        with Live(
            self.dashboard.render(),
            console=console,
            screen=True,
            refresh_per_second=self.config.global_config.refresh_rate_ms / 1000
        ) as live:

            while self.running:
                try:
                    # Atualiza dados
                    self.dashboard.collect_data()

                    # Re-renderiza
                    live.update(self.dashboard.render())

                    # Sleep
                    time.sleep(self.config.global_config.refresh_rate_ms / 1000)

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")

    def _signal_handler(self, signum, frame):
        """Handler para Ctrl+C"""
        console.print("\n[cyan]Shutting down...[/cyan]")
        sys.exit(0)


def main():
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    main()
```

---

## 📚 CONCLUSÃO GERAL

Nesta terceira e última parte cobrimos:

✅ **Arquiteturas Modulares:**
- Plugin Architecture para extensibilidade
- Composite Pattern para dashboards agregados
- Observer Pattern para reatividade
- MVC para separação de responsabilidades
- Event-Driven Architecture para baixo acoplamento

✅ **Python Libraries:**
- Rich (rendering, já usamos)
- Textual (framework completo, reativo)
- urwid (tradicional, event loop)
- Comparativo e recomendações

✅ **Features Priorizadas:**
- P0 (MVP): Network Traffic, System Monitor, WiFi Analysis, Dashboard Agregado
- P1 (Importantes): Application Monitor, Filtros, Alertas, Export
- P2 (Nice-to-have): Security Dashboard, Historical Analysis, Remote Monitoring
- Roadmap de 6 sprints

✅ **Padrões de Design:**
- Sistema de configuração YAML completo
- Hot-reload de componentes
- Dependency Injection
- State Management (Redux-like)

✅ **Implementação Prática:**
- Estrutura de projeto completa
- Exemplo funcional de main.py

---

**PRÓXIMOS DOCUMENTOS:**

1. **SAMPLER_DEEP_DIVE.md** - Análise profunda do Sampler com exemplos YAML
2. **REFERENCES.md** - Lista organizada de referências
3. **REFACTORING_PLAN.md** - Plano detalhado de refatoração

---

**Juan-Dev - Soli Deo Gloria ✝️**
