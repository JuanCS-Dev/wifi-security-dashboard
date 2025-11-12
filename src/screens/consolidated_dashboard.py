"""
ConsolidatedDashboard - Overview completo de todos os sistemas

Dashboard principal que mostra TODAS as métricas em uma única tela.
Fornece visão holística do sistema, rede, WiFi e packets.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive


class CPUWidget(Static):
    """CPU usage widget for consolidated view."""
    cpu_percent = reactive(0.0)

    def watch_cpu_percent(self, new_value: float) -> None:
        if new_value < 70:
            color = "green"
            status = "NORMAL"
        elif new_value < 90:
            color = "yellow"
            status = "HIGH"
        else:
            color = "red"
            status = "CRITICAL"

        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        self.update(
            f"[bold bright_white]💻 CPU[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]"
        )


class RAMWidget(Static):
    """RAM usage widget for consolidated view."""
    memory_percent = reactive(0.0)
    memory_used_mb = reactive(0.0)
    memory_total_mb = reactive(0.0)

    def watch_memory_percent(self, new_value: float) -> None:
        if new_value < 70:
            color = "green"
            status = "NORMAL"
        elif new_value < 90:
            color = "yellow"
            status = "HIGH"
        else:
            color = "red"
            status = "CRITICAL"

        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        used_gb = self.memory_used_mb / 1024
        total_gb = self.memory_total_mb / 1024

        self.update(
            f"[bold bright_white]📊 RAM[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{used_gb:.1f}/{total_gb:.1f} GB[/dim]"
        )


class DiskWidget(Static):
    """Disk usage widget for consolidated view."""
    disk_percent = reactive(0.0)
    disk_used_gb = reactive(0.0)
    disk_total_gb = reactive(0.0)

    def watch_disk_percent(self, new_value: float) -> None:
        if new_value < 70:
            color = "cyan"
            status = "GOOD"
        elif new_value < 90:
            color = "yellow"
            status = "WARNING"
        else:
            color = "red"
            status = "CRITICAL"

        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        self.update(
            f"[bold bright_white]💾 DISK[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{self.disk_used_gb:.0f}/{self.disk_total_gb:.0f} GB[/dim]"
        )


class WiFiWidget(Static):
    """WiFi signal widget for consolidated view."""
    signal_strength_percent = reactive(0)
    ssid = reactive("N/A")
    signal_dbm = reactive(-100)

    def watch_signal_strength_percent(self, new_value: int) -> None:
        if new_value >= 70:
            color = "green"
            bars = "📶"
            status = "EXCELLENT"
        elif new_value >= 50:
            color = "green"
            bars = "📶"
            status = "GOOD"
        elif new_value >= 30:
            color = "yellow"
            bars = "📶"
            status = "FAIR"
        elif new_value > 0:
            color = "red"
            bars = "📶"
            status = "WEAK"
        else:
            color = "dim"
            bars = "📵"
            status = "NO SIGNAL"

        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        self.update(
            f"[bold bright_white]{bars} WIFI[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{self.ssid} ({self.signal_dbm} dBm)[/dim]"
        )


class NetworkStatsWidget(Static):
    """Network statistics widget for consolidated view."""
    bandwidth_rx = reactive(0.0)
    bandwidth_tx = reactive(0.0)
    connections = reactive(0)

    def watch_bandwidth_rx(self, new_value: float) -> None:
        self._refresh_display()

    def watch_bandwidth_tx(self, new_value: float) -> None:
        self._refresh_display()

    def watch_connections(self, new_value: int) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        self.update(
            f"[bold bright_white]🌐 NETWORK[/bold bright_white]\n"
            f"[cyan]↓ RX:[/cyan] [bold]{self.bandwidth_rx:.2f}[/bold] Mbps\n"
            f"[yellow]↑ TX:[/yellow] [bold]{self.bandwidth_tx:.2f}[/bold] Mbps\n"
            f"[dim]Connections: {self.connections}[/dim]"
        )


class PacketStatsWidget(Static):
    """Packet statistics widget for consolidated view."""
    packet_count = reactive(0)
    packet_rate = reactive(0.0)
    top_protocol = reactive("N/A")

    def watch_packet_count(self, new_value: int) -> None:
        self._refresh_display()

    def watch_packet_rate(self, new_value: float) -> None:
        self._refresh_display()

    def watch_top_protocol(self, new_value: str) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        self.update(
            f"[bold bright_white]📦 PACKETS[/bold bright_white]\n"
            f"[green]Count:[/green] [bold]{self.packet_count}[/bold]\n"
            f"[yellow]Rate:[/yellow] [bold]{self.packet_rate:.1f}[/bold] pkt/s\n"
            f"[dim]Top: {self.top_protocol}[/dim]"
        )


class ConsolidatedDashboard(Screen):
    """
    Dashboard consolidado - Visão completa de TODOS os sistemas.

    Mostra em uma única tela:
    - System metrics (CPU, RAM, Disk)
    - Network metrics (RX/TX, Connections)
    - WiFi metrics (Signal, SSID)
    - Packet metrics (Count, Rate, Protocol)

    Layout: Grid 2x3 (6 widgets)
    """

    CSS = """
    ConsolidatedDashboard {
        background: $surface;
    }

    #widgets-grid {
        width: 100%;
        height: 100%;
        grid-size: 3 2;
        grid-gutter: 1 2;
        padding: 1;
    }

    CPUWidget, RAMWidget, DiskWidget, WiFiWidget, NetworkStatsWidget, PacketStatsWidget {
        border: solid $primary;
        padding: 1 2;
        background: $panel;
        height: 100%;
    }

    CPUWidget {
        border: solid green;
    }

    RAMWidget {
        border: solid green;
    }

    DiskWidget {
        border: solid cyan;
    }

    WiFiWidget {
        border: solid yellow;
    }

    NetworkStatsWidget {
        border: solid cyan;
    }

    PacketStatsWidget {
        border: solid magenta;
    }
    """

    BINDINGS = [
        ("0", "switch_screen('consolidated')", "Consolidated"),
        ("1", "switch_screen('system')", "System"),
        ("2", "switch_screen('network')", "Network"),
        ("3", "switch_screen('wifi')", "WiFi"),
        ("4", "switch_screen('packets')", "Packets"),
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the consolidated dashboard layout."""
        yield Header(show_clock=True)

        with Grid(id="widgets-grid"):
            yield CPUWidget(id="cpu-widget")
            yield RAMWidget(id="ram-widget")
            yield DiskWidget(id="disk-widget")
            yield WiFiWidget(id="wifi-widget")
            yield NetworkStatsWidget(id="network-widget")
            yield PacketStatsWidget(id="packet-widget")

        yield Footer()

    def update_metrics(self, system_data, wifi_data, network_data, packet_data):
        """
        Update all widgets with fresh data from plugins.

        Args:
            system_data: Dict from SystemPlugin
            wifi_data: Dict from WiFiPlugin
            network_data: Dict from NetworkPlugin
            packet_data: Dict from PacketAnalyzerPlugin
        """
        # Update CPU
        cpu_widget = self.query_one("#cpu-widget", CPUWidget)
        cpu_widget.cpu_percent = system_data.get('cpu_percent', 0.0)

        # Update RAM
        ram_widget = self.query_one("#ram-widget", RAMWidget)
        ram_widget.memory_percent = system_data.get('memory_percent', 0.0)
        ram_widget.memory_used_mb = system_data.get('memory_used_mb', 0.0)
        ram_widget.memory_total_mb = system_data.get('memory_total_mb', 0.0)

        # Update Disk
        disk_widget = self.query_one("#disk-widget", DiskWidget)
        disk_widget.disk_percent = system_data.get('disk_percent', 0.0)
        disk_widget.disk_used_gb = system_data.get('disk_used_gb', 0.0)
        disk_widget.disk_total_gb = system_data.get('disk_total_gb', 0.0)

        # Update WiFi
        wifi_widget = self.query_one("#wifi-widget", WiFiWidget)
        wifi_widget.signal_strength_percent = wifi_data.get('signal_strength_percent', 0)
        wifi_widget.ssid = wifi_data.get('ssid', 'Not Connected')
        wifi_widget.signal_dbm = wifi_data.get('signal_strength_dbm', -100)

        # Update Network
        network_widget = self.query_one("#network-widget", NetworkStatsWidget)
        network_widget.bandwidth_rx = network_data.get('bandwidth_rx_mbps', 0.0)
        network_widget.bandwidth_tx = network_data.get('bandwidth_tx_mbps', 0.0)
        network_widget.connections = network_data.get('connections_established', 0)

        # Update Packets
        packet_widget = self.query_one("#packet-widget", PacketStatsWidget)
        packet_widget.packet_count = packet_data.get('total_packets', 0)
        packet_widget.packet_rate = packet_data.get('packet_rate', 0.0)

        # Get top protocol
        top_protocols = packet_data.get('top_protocols', {})
        if top_protocols:
            packet_widget.top_protocol = list(top_protocols.keys())[0]
        else:
            packet_widget.top_protocol = "N/A"
