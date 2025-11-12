"""
WiFiDashboard - Dashboard detalhado de métricas WiFi

Dashboard focado exclusivamente em métricas WiFi: Signal, SSID, Security, Channel, Bitrate.
Fornece análise detalhada da conexão WiFi.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive


class WiFiSignalWidget(Static):
    """Detailed WiFi signal widget with visual representation."""
    signal_strength_percent = reactive(0)
    signal_dbm = reactive(-100)
    link_quality = reactive(0)

    def watch_signal_strength_percent(self, new_value: int) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        if self.signal_strength_percent >= 70:
            color = "green"
            bars = "📶"
            status = "EXCELLENT"
            quality = "Perfect for streaming"
        elif self.signal_strength_percent >= 50:
            color = "green"
            bars = "📶"
            status = "GOOD"
            quality = "Good for browsing"
        elif self.signal_strength_percent >= 30:
            color = "yellow"
            bars = "📶"
            status = "FAIR"
            quality = "May have lag"
        elif self.signal_strength_percent > 0:
            color = "red"
            bars = "📶"
            status = "WEAK"
            quality = "Connection issues"
        else:
            color = "dim"
            bars = "📵"
            status = "NO SIGNAL"
            quality = "Disconnected"

        # Large visual bar
        bar_length = 40
        filled = int(bar_length * self.signal_strength_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Signal strength visualization
        bars_visual = ""
        if self.signal_strength_percent > 0:
            num_bars = min(5, self.signal_strength_percent // 20 + 1)
            bars_visual = ("▂" * min(num_bars, 1) +
                          "▄" * max(0, min(num_bars - 1, 1)) +
                          "▆" * max(0, min(num_bars - 2, 1)) +
                          "█" * max(0, min(num_bars - 3, 1)) +
                          "█" * max(0, num_bars - 4))

        # Status dot
        status_dot = f"[{color}]●[/{color}]"
        
        self.update(
            f"[bold white]{bars} WIFI SIGNAL[/bold white]\n\n"
            f"[bold {color}]{self.signal_strength_percent}%[/bold {color}] {status_dot}\n"
            f"[{color}]{bar}[/{color}]\n\n"
            f"[bold]{self.signal_dbm}[/bold] dBm\n"
            f"[dim]Signal Strength\n\n"
            f"[bold]{self.link_quality}%[/bold]\n"
            f"[dim]Link Quality\n\n"
            f"[dim italic]{quality}[/dim italic]"
        )


class WiFiInfoWidget(Static):
    """Detailed WiFi connection info widget."""
    ssid = reactive("N/A")
    bssid = reactive("N/A")
    security = reactive("N/A")
    channel = reactive(0)
    frequency_mhz = reactive(0)
    bitrate_mbps = reactive(0.0)
    interface = reactive("N/A")

    def watch_ssid(self, new_value: str) -> None:
        self._refresh_display()

    def watch_security(self, new_value: str) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        # Security color coding
        if "WPA3" in self.security:
            sec_color = "green"
            sec_icon = "🔒"
            sec_status = "Secure (WPA3)"
        elif "WPA2" in self.security:
            sec_color = "green"
            sec_icon = "🔒"
            sec_status = "Secure (WPA2)"
        elif "WPA" in self.security:
            sec_color = "yellow"
            sec_icon = "⚠️ "
            sec_status = "Moderate (WPA)"
        elif "WEP" in self.security:
            sec_color = "red"
            sec_icon = "⚠️ "
            sec_status = "Weak (WEP - INSECURE!)"
        elif "Open" in self.security or self.security == "N/A":
            sec_color = "red"
            sec_icon = "🔓"
            sec_status = "OPEN - NO ENCRYPTION!"
        else:
            sec_color = "dim"
            sec_icon = "❓"
            sec_status = "Unknown"

        # Frequency band
        if self.frequency_mhz >= 5000:
            band = "5 GHz (Fast)"
            band_color = "cyan"
        elif self.frequency_mhz >= 2400:
            band = "2.4 GHz (Compatible)"
            band_color = "yellow"
        else:
            band = "Unknown"
            band_color = "dim"

        # Security status dot
        sec_dot = f"[{sec_color}]●[/{sec_color}]"
        
        self.update(
            f"[bold white]📡 CONNECTION INFO[/bold white]\n\n"
            f"[bold cyan]{self.ssid}[/bold cyan]\n"
            f"[dim]Network Name\n\n"
            f"{sec_icon} [{sec_color}]{sec_status}[/{sec_color}] {sec_dot}\n"
            f"[dim]Security Protocol\n\n"
            f"[bold]{self.channel}[/bold] • [{band_color}]{self.frequency_mhz} MHz[/{band_color}]\n"
            f"[dim]Channel & Frequency ({band})\n\n"
            f"[bold]{self.bitrate_mbps:.1f}[/bold] Mbps\n"
            f"[dim]Connection Speed\n\n"
            f"[dim]{self.interface} • {self.bssid}[/dim]"
        )


class WiFiDashboard(Screen):
    """
    Dashboard detalhado de WiFi.

    Mostra métricas de WiFi com análise:
    - Signal strength (visual detalhado)
    - Connection info (SSID, security, channel, frequency)
    - Educational security warnings
    """

    CSS = """
    WiFiDashboard {
        background: $surface;
    }

    #wifi-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    WiFiSignalWidget {
        height: 1fr;
        border: solid #00aa00;
        padding: 0 1;
        margin: 0 1 0 1;
        background: $panel;
    }

    WiFiInfoWidget {
        height: 1fr;
        border: solid #00aa00;
        padding: 0 1;
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
        """Compose the WiFi dashboard layout."""
        yield Header(show_clock=True)

        with Horizontal(id="wifi-container"):
            yield WiFiSignalWidget(id="wifi-signal")
            yield WiFiInfoWidget(id="wifi-info")

        yield Footer()

    def update_metrics(self, wifi_data):
        """
        Update all widgets with fresh WiFi data.

        Args:
            wifi_data: Dict from WiFiPlugin
        """
        # Update signal widget
        signal_widget = self.query_one("#wifi-signal", WiFiSignalWidget)
        signal_widget.signal_strength_percent = wifi_data.get('signal_strength_percent', 0)
        signal_widget.signal_dbm = wifi_data.get('signal_strength_dbm', -100)
        signal_widget.link_quality = wifi_data.get('link_quality', 0)

        # Update info widget
        info_widget = self.query_one("#wifi-info", WiFiInfoWidget)
        info_widget.ssid = wifi_data.get('ssid', 'Not Connected')
        info_widget.bssid = wifi_data.get('bssid', 'N/A')
        info_widget.security = wifi_data.get('security', 'N/A')
        info_widget.channel = wifi_data.get('channel', 0)
        info_widget.frequency_mhz = wifi_data.get('frequency_mhz', 0)
        info_widget.bitrate_mbps = wifi_data.get('bitrate_mbps', 0.0)
        info_widget.interface = wifi_data.get('interface', 'N/A')
