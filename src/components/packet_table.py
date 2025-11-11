"""
PacketTable Component - Display packet analysis data (Wireshark-style)

Displays packet analyzer data including protocols, sources, and recent packets
with educational safety flags.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import Dict, List, Any, Optional
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group

from src.core.component import Component, ComponentConfig


class PacketTable(Component):
    """
    PacketTable component renders packet analysis data.

    Displays network packet information in a tabular format similar to Wireshark,
    with educational safety indicators for HTTP vs HTTPS traffic.

    Example config (dashboard.yml):
        components:
          - type: packettable
            title: "Packet Analyzer (Wireshark-style)"
            position: {x: 0, y: 43, width: 120, height: 18}
            rate_ms: 2000
            plugin: "packet_analyzer"
            data_field: "all"  # Special: fetch entire plugin data
            color: "red"
            extra:
              show_protocols: true
              show_recent: true
              max_protocols: 6
              max_recent: 5

    Renders as:
        ╭───────── Packet Analyzer (Wireshark-style) ─────────╮
        │ Top Protocols:                                       │
        │   HTTPS ████████ 450 pkts (55%)                     │
        │   DNS   ██ 89 pkts (11%)                            │
        │   HTTP  █ 32 pkts (4%) ⚠️ Unencrypted!              │
        │                                                      │
        │ Recent Packets:                                      │
        │ ┌──────────┬────────────────┬──────────┬──────────┐ │
        │ │ Time     │ Source         │ Protocol │ Info     │ │
        │ ├──────────┼────────────────┼──────────┼──────────┤ │
        │ │ 14:32:15 │ 192.168.1.102  │ HTTPS    │ Gmail ✅ │ │
        │ │ 14:32:15 │ 192.168.1.104  │ HTTP     │ ⚠️ Unsafe│ │
        │ └──────────┴────────────────┴──────────┴──────────┘ │
        ╰──────────────────────────────────────────────────────╯
    """

    def __init__(self, config: ComponentConfig):
        """
        Initialize PacketTable component.

        Args:
            config: ComponentConfig dataclass
                Required:
                - type: "packettable"
                - title: str - Panel title
                - plugin: str - "packet_analyzer"
                - data_field: str - "all" (fetch entire plugin data)

                Optional (via config.extra):
                - show_protocols: bool - Show protocol distribution (default: True)
                - show_recent: bool - Show recent packets table (default: True)
                - max_protocols: int - Max protocols to show (default: 6)
                - max_recent: int - Max recent packets (default: 5)
        """
        super().__init__(config)

        # Extract PacketTable-specific config
        self.show_protocols: bool = config.extra.get("show_protocols", True)
        self.show_recent: bool = config.extra.get("show_recent", True)
        self.max_protocols: int = config.extra.get("max_protocols", 6)
        self.max_recent: int = config.extra.get("max_recent", 5)

    def render(self) -> Panel:
        """
        Render PacketTable as Rich Panel.

        Returns:
            Rich Panel with packet analysis data
        """
        content = self._build_content()

        panel = Panel(
            content,
            title=f"[bold]{self.config.title}[/bold]",
            border_style=self.config.color,
            padding=(1, 2)
        )

        return panel

    def _build_content(self) -> Group:
        """
        Build content with protocols and recent packets.

        Returns:
            Rich Group with multiple renderables
        """
        if self.data is None:
            return Group(Text("No packet data yet", style="dim italic"))

        renderables = []

        # Add packet rate summary
        packet_rate = self.data.get('packet_rate', 0)
        total_packets = self.data.get('total_packets', 0)
        backend = self.data.get('backend', 'unknown')

        summary = Text()
        summary.append(f"📊 Rate: ", style="bold cyan")
        summary.append(f"{packet_rate:.1f} pkts/s", style="yellow")
        summary.append(f"  |  Total: ", style="bold cyan")
        summary.append(f"{total_packets}", style="yellow")
        summary.append(f"  |  Backend: ", style="bold cyan")
        summary.append(f"{backend}", style="green" if backend == "scapy" else "yellow")

        renderables.append(summary)
        renderables.append(Text())  # Spacing

        # Show protocols if enabled
        if self.show_protocols:
            protocols_section = self._render_protocols()
            if protocols_section:
                renderables.append(protocols_section)
                renderables.append(Text())  # Spacing

        # Show recent packets if enabled
        if self.show_recent:
            recent_section = self._render_recent_packets()
            if recent_section:
                renderables.append(recent_section)

        return Group(*renderables)

    def _render_protocols(self) -> Optional[Text]:
        """
        Render top protocols section.

        Returns:
            Text with protocol distribution
        """
        top_protocols = self.data.get('top_protocols', {})

        if not top_protocols:
            return Text("No protocol data", style="dim italic")

        # Sort by count and limit
        sorted_protocols = sorted(
            top_protocols.items(),
            key=lambda x: x[1],
            reverse=True
        )[:self.max_protocols]

        # Calculate total for percentages
        total = sum(top_protocols.values())

        # Build text
        result = Text()
        result.append("🔝 Top Protocols:\n", style="bold cyan")

        for protocol, count in sorted_protocols:
            percentage = (count / total * 100) if total > 0 else 0

            # Bar visualization (simple)
            bar_length = int(percentage / 10)  # 10% = 1 char
            bar = "█" * bar_length

            # Color based on protocol
            if protocol == "HTTP":
                color = "red"
                warning = " ⚠️ Unencrypted!"
            elif protocol == "HTTPS":
                color = "green"
                warning = ""
            else:
                color = "white"
                warning = ""

            result.append(f"  {protocol:8} ", style="bold")
            result.append(bar, style=color)
            result.append(f" {count} pkts ({percentage:.0f}%)", style=color)
            result.append(warning, style="red bold")
            result.append("\n")

        return result

    def _render_recent_packets(self) -> Optional[Table]:
        """
        Render recent packets table.

        Returns:
            Rich Table with recent packets
        """
        recent_packets = self.data.get('recent_packets', [])

        if not recent_packets:
            return None

        # Limit to max_recent
        packets = recent_packets[:self.max_recent]

        # Create table
        table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="dim",
            title="📦 Recent Packets",
            title_style="bold magenta",
            expand=False
        )

        table.add_column("Time", style="dim", width=12)
        table.add_column("Source", style="cyan", width=16)
        table.add_column("Destination", style="blue", width=16)
        table.add_column("Protocol", style="yellow", width=10)
        table.add_column("Info", style="white", width=30)

        # Add rows
        for pkt in packets:
            time = pkt.get('time', '')
            src = pkt.get('src', '')
            dst = pkt.get('dst', '')
            protocol = pkt.get('protocol', '')
            info = pkt.get('info', '')
            safe = pkt.get('safe', True)

            # Color based on safety
            if not safe:
                protocol_style = "red bold"
                info_style = "red"
            else:
                protocol_style = "green"
                info_style = "white"

            table.add_row(
                time,
                src,
                dst,
                Text(protocol, style=protocol_style),
                Text(info, style=info_style)
            )

        return table
