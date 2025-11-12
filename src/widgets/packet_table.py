"""
PacketTable Widget - Wireshark-style packet display

Real-time packet monitoring table with educational safety flags.
Displays recent network packets with protocol analysis.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from collections import deque
from typing import Dict, Any, List

from textual.widgets import DataTable
from textual.reactive import reactive


class PacketTable(DataTable):
    """
    Wireshark-style packet table widget.

    Features:
    - Real-time packet display (last 50 packets)
    - Educational safety flags:
      - 🔒 HTTPS (secure)
      - ⚠️ HTTP (insecure)
      - 🌐 DNS queries
    - Color-coded protocols
    - Auto-scroll to latest
    """

    # Reactive attribute for packet count
    packet_count = reactive(0)

    def __init__(self, **kwargs):
        """Initialize PacketTable widget."""
        super().__init__(**kwargs)

        # Circular buffer for packets (max 50)
        self.packet_buffer = deque(maxlen=50)

        # Configure DataTable
        self.zebra_stripes = True  # Alternating row colors
        self.cursor_type = "row"  # Highlight full row
        self.show_header = True
        self.fixed_columns = 0

    def on_mount(self) -> None:
        """Initialize table columns when widget is mounted."""
        # Add columns
        self.add_column("Time", key="time", width=10)
        self.add_column("Source", key="source", width=18)
        self.add_column("Dest", key="dest", width=18)
        self.add_column("Protocol", key="protocol", width=10)
        self.add_column("Info", key="info", width=None)  # Flex width

    def update_data(self, plugin_data: Dict[str, Any]) -> None:
        """
        Update table with packet analyzer plugin data.

        Args:
            plugin_data: Dict from PacketAnalyzerPlugin with key:
                - packet_analyzer: Dict with 'recent_packets' list
        """
        if 'packet_analyzer' not in plugin_data:
            return

        analyzer_data = plugin_data['packet_analyzer']
        recent_packets = analyzer_data.get('recent_packets', [])

        if not recent_packets:
            return

        # Add new packets to buffer
        for packet in recent_packets:
            # Skip if packet already in buffer (by timestamp)
            timestamp = packet.get('timestamp', '')
            if any(p.get('timestamp') == timestamp for p in self.packet_buffer):
                continue

            self.packet_buffer.append(packet)

        # Update packet count
        self.packet_count = len(self.packet_buffer)

        # Refresh table display
        self._refresh_table()

    def _refresh_table(self) -> None:
        """Refresh DataTable with current packet buffer."""
        # Clear existing rows
        self.clear()

        # Add rows from buffer (newest first)
        for packet in reversed(self.packet_buffer):
            time_str = self._format_timestamp(packet.get('timestamp', ''))
            source = self._truncate(packet.get('src', 'N/A'), 18)
            dest = self._truncate(packet.get('dst', 'N/A'), 18)
            protocol = packet.get('protocol', 'N/A')
            info = self._format_info(packet, protocol)

            # Add row with educational styling
            self.add_row(
                time_str,
                source,
                dest,
                protocol,
                info,
                key=packet.get('timestamp', '')
            )

        # Auto-scroll to top (newest packet)
        if self.row_count > 0:
            self.move_cursor(row=0)

    def _format_timestamp(self, timestamp: str) -> str:
        """
        Format timestamp to HH:MM:SS.

        Args:
            timestamp: ISO timestamp or empty string

        Returns:
            Formatted time string (HH:MM:SS)
        """
        if not timestamp:
            return "00:00:00"

        try:
            # Extract time component if ISO format
            if 'T' in timestamp:
                time_part = timestamp.split('T')[1].split('.')[0]
                return time_part
            else:
                return timestamp[:8]
        except (IndexError, AttributeError):
            return "00:00:00"

    def _truncate(self, text: str, max_length: int) -> str:
        """
        Truncate text to max_length with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum character length

        Returns:
            Truncated string
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    def _format_info(self, packet: Dict[str, Any], protocol: str) -> str:
        """
        Format packet info with educational safety flags.

        Args:
            packet: Packet data dict
            protocol: Protocol name (HTTP, HTTPS, DNS, etc.)

        Returns:
            Formatted info string with educational flags
        """
        info = packet.get('info', '')

        # Educational safety flags
        if protocol == 'HTTPS':
            return f"🔒 {info}"  # Secure
        elif protocol == 'HTTP':
            return f"⚠️ {info} (INSECURE!)"  # Warning
        elif protocol == 'DNS':
            return f"🌐 {info}"  # DNS query
        elif protocol == 'TLS' or protocol == 'SSL':
            return f"🔒 {info}"  # Encrypted
        else:
            return info

    def clear_packets(self) -> None:
        """Clear all packets from buffer and table."""
        self.packet_buffer.clear()
        self.clear()
        self.packet_count = 0
