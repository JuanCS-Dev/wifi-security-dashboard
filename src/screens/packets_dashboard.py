"""
PacketsDashboard - Dashboard detalhado de análise de pacotes

Dashboard focado exclusivamente em análise de pacotes de rede.
Estilo Wireshark com tabela de pacotes e estatísticas de protocolos.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive
from src.widgets import PacketTable


class PacketStatsDetailWidget(Static):
    """Detailed packet statistics widget."""
    packet_count = reactive(0)
    packet_rate = reactive(0.0)
    top_protocols = reactive({})
    top_sources = reactive({})
    top_destinations = reactive({})
    backend = reactive("unknown")

    def watch_packet_count(self, new_value: int) -> None:
        self._refresh_display()

    def watch_top_protocols(self, new_value: dict) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        # Backend indicator
        if self.backend == "scapy":
            backend_icon = "⚡"
            backend_color = "green"
            backend_label = "Scapy (High Performance)"
        elif self.backend == "pyshark":
            backend_icon = "🦈"
            backend_color = "cyan"
            backend_label = "PyShark (Wireshark)"
        elif self.backend == "mock":
            backend_icon = "🎓"
            backend_color = "yellow"
            backend_label = "Mock (Educational)"
        else:
            backend_icon = "❓"
            backend_color = "dim"
            backend_label = "Unknown"

        output = (
            f"[bold bright_white]📊 PACKET STATISTICS[/bold bright_white]\n\n"
            f"[bold]Capture Info:[/bold]\n"
            f"  Total Packets: [bold]{self.packet_count:,}[/bold]\n"
            f"  Packet Rate:   [bold]{self.packet_rate:.1f}[/bold] pkt/s\n"
            f"  Backend:       {backend_icon} [{backend_color}]{backend_label}[/{backend_color}]\n\n"
        )

        # Top protocols
        if self.top_protocols:
            output += "[bold cyan]Top Protocols:[/bold cyan]\n"
            for proto, count in list(self.top_protocols.items())[:5]:
                # Protocol-specific icons
                if proto == "HTTPS" or proto == "TLS":
                    icon = "🔒"
                elif proto == "HTTP":
                    icon = "⚠️ "
                elif proto == "DNS":
                    icon = "🌐"
                elif proto == "SSH":
                    icon = "🔑"
                else:
                    icon = "📦"

                output += f"  {icon} {proto:<10} [dim]{count:,} packets[/dim]\n"
        else:
            output += "[dim]No protocols detected yet...[/dim]\n"

        output += "\n"

        # Top sources
        if self.top_sources:
            output += "[bold green]Top Sources:[/bold green]\n"
            for ip, count in list(self.top_sources.items())[:3]:
                output += f"  {ip:<15} [dim]{count:,} packets[/dim]\n"
        else:
            output += "[dim]No sources detected yet...[/dim]\n"

        output += "\n"

        # Top destinations
        if self.top_destinations:
            output += "[bold yellow]Top Destinations:[/bold yellow]\n"
            for ip, count in list(self.top_destinations.items())[:3]:
                output += f"  {ip:<15} [dim]{count:,} packets[/dim]\n"
        else:
            output += "[dim]No destinations detected yet...[/dim]"

        self.update(output)


class EducationalTipsWidget(Static):
    """Educational tips widget about packet analysis."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update(
            f"[bold bright_yellow]🎓 EDUCATIONAL TIPS[/bold bright_yellow]\n\n"
            f"[bold]Protocol Security:[/bold]\n"
            f"  [green]🔒 HTTPS/TLS[/green]  - Encrypted, SAFE\n"
            f"  [red]⚠️  HTTP[/red]      - Plain text, UNSAFE!\n"
            f"  [cyan]🌐 DNS[/cyan]       - Name lookups\n"
            f"  [green]🔑 SSH[/green]       - Secure remote access\n\n"
            f"[bold]What to Watch:[/bold]\n"
            f"  • High HTTP traffic = potential data leak\n"
            f"  • Many different IPs = normal browsing\n"
            f"  • One IP dominating = video streaming\n"
            f"  • Many DNS queries = starting new apps\n\n"
            f"[dim italic]In mock mode, data is simulated\n"
            f"for safe educational learning![/dim italic]"
        )


class PacketsDashboard(Screen):
    """
    Dashboard detalhado de pacotes.

    Mostra análise de pacotes de rede:
    - Tabela de pacotes recentes (Wireshark-style)
    - Estatísticas detalhadas (protocols, sources, destinations)
    - Educational tips sobre segurança de protocolos
    """

    CSS = """
    PacketsDashboard {
        background: $surface;
    }

    #packets-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #left-panel {
        width: 2fr;
        height: 100%;
    }

    #right-panel {
        width: 1fr;
        height: 100%;
    }

    PacketTable {
        height: 1fr;
        border: solid magenta;
        margin: 0 1 0 1;
        padding: 0 1;
        background: $panel;
    }

    PacketStatsDetailWidget {
        height: 1fr;
        border: solid magenta;
        padding: 1 2;
        margin: 0 1 1 1;
        background: $panel;
    }

    EducationalTipsWidget {
        height: 1fr;
        border: solid yellow;
        padding: 1 2;
        margin: 0 1 0 1;
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
        """Compose the packets dashboard layout."""
        yield Header(show_clock=True)

        with Horizontal(id="packets-container"):
            with Vertical(id="left-panel"):
                yield PacketTable(id="packet-table")

            with Vertical(id="right-panel"):
                yield PacketStatsDetailWidget(id="packet-stats")
                yield EducationalTipsWidget(id="educational-tips")

        yield Footer()

    def update_metrics(self, packet_data):
        """
        Update all widgets with fresh packet data.

        Args:
            packet_data: Dict from PacketAnalyzerPlugin
        """
        # Update table
        packet_table = self.query_one("#packet-table", PacketTable)
        packet_table.update_data({'packet_analyzer': packet_data})

        # Update stats
        stats_widget = self.query_one("#packet-stats", PacketStatsDetailWidget)
        stats_widget.packet_count = packet_data.get('total_packets', 0)
        stats_widget.packet_rate = packet_data.get('packet_rate', 0.0)
        stats_widget.top_protocols = packet_data.get('top_protocols', {})
        stats_widget.top_sources = packet_data.get('top_sources', {})
        stats_widget.top_destinations = packet_data.get('top_destinations', {})
        stats_widget.backend = packet_data.get('backend', 'unknown')
