"""
NetworkDashboard - Dashboard detalhado de métricas de rede

Dashboard focado exclusivamente em métricas de rede: Bandwidth, Connections, Packets.
Inclui gráficos em tempo real e estatísticas detalhadas.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive
from src.widgets import NetworkChart


class NetworkStatsDetailWidget(Static):
    """Detailed network statistics widget."""
    bandwidth_rx = reactive(0.0)
    bandwidth_tx = reactive(0.0)
    bytes_recv = reactive(0)
    bytes_sent = reactive(0)
    packets_recv = reactive(0)
    packets_sent = reactive(0)
    connections_established = reactive(0)
    connections_total = reactive(0)
    errors_in = reactive(0)
    errors_out = reactive(0)

    def watch_bandwidth_rx(self, new_value: float) -> None:
        self._refresh_display()

    def watch_bandwidth_tx(self, new_value: float) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        bytes_recv_mb = self.bytes_recv / (1024 * 1024)
        bytes_sent_mb = self.bytes_sent / (1024 * 1024)
        
        total_errors = self.errors_in + self.errors_out
        
        if total_errors == 0:
            error_dot = "[green]●[/green]"
        elif total_errors < 10:
            error_dot = "[yellow]●[/yellow]"
        else:
            error_dot = "[red]●[/red]"

        self.update(
            f"[bold white]🌐 NETWORK STATS[/bold white]\n\n"
            f"[bold cyan]{self.bandwidth_rx:.2f}[/bold cyan] Mbps ↓\n"
            f"[dim]Received: {bytes_recv_mb:.1f} MB\n"
            f"Packets: {self.packets_recv:,}[/dim]\n\n"
            f"[bold yellow]{self.bandwidth_tx:.2f}[/bold yellow] Mbps ↑\n"
            f"[dim]Sent: {bytes_sent_mb:.1f} MB\n"
            f"Packets: {self.packets_sent:,}[/dim]\n\n"
            f"[bold]{self.connections_established}[/bold] {error_dot}\n"
            f"[dim]Active Connections\n"
            f"Total: {self.connections_total} • Errors: {total_errors}[/dim]"
        )


class NetworkDashboard(Screen):
    """
    Dashboard detalhado de rede.

    Mostra métricas de rede com visualização:
    - Gráfico de bandwidth RX/TX em tempo real
    - Estatísticas detalhadas (bytes, packets, connections, errors)
    """

    CSS = """
    NetworkDashboard {
        background: $surface;
    }

    #network-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #chart-panel {
        width: 2fr;
        height: 100%;
    }

    #stats-panel {
        width: 1fr;
        height: 100%;
    }

    NetworkChart {
        height: 100%;
        border: solid #00aa00;
        margin: 0 1 0 0;
        background: $panel;
    }

    NetworkStatsDetailWidget {
        height: 100%;
        border: solid #00aa00;
        padding: 0 1;
        margin: 0 0 0 1;
        background: $panel;
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
        """Compose the network dashboard layout."""
        yield Header(show_clock=True)

        with Horizontal(id="network-container"):
            with Vertical(id="chart-panel"):
                yield NetworkChart(id="network-chart")
            with Vertical(id="stats-panel"):
                yield NetworkStatsDetailWidget(id="network-stats")

        yield Footer()

    def update_metrics(self, network_data):
        """
        Update all widgets with fresh network data.

        Args:
            network_data: Dict from NetworkPlugin
        """
        # Update chart
        network_chart = self.query_one("#network-chart", NetworkChart)
        network_chart.update_data({'network': network_data})

        # Update stats
        stats_widget = self.query_one("#network-stats", NetworkStatsDetailWidget)
        stats_widget.bandwidth_rx = network_data.get('bandwidth_rx_mbps', 0.0)
        stats_widget.bandwidth_tx = network_data.get('bandwidth_tx_mbps', 0.0)
        stats_widget.bytes_recv = network_data.get('bytes_recv', 0)
        stats_widget.bytes_sent = network_data.get('bytes_sent', 0)
        stats_widget.packets_recv = network_data.get('packets_recv', 0)
        stats_widget.packets_sent = network_data.get('packets_sent', 0)
        stats_widget.connections_established = network_data.get('connections_established', 0)
        stats_widget.connections_total = network_data.get('connections_total', 0)
        stats_widget.errors_in = network_data.get('errors_in', 0)
        stats_widget.errors_out = network_data.get('errors_out', 0)
