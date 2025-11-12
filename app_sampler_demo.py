"""
Sampler Style Demo - Test new professional design
Quick demo to showcase the Sampler-inspired layout

Author: Juan-Dev - Soli Deo Gloria ✝️
"""

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Header, Footer
from src.widgets.system_widgets import (
    CPUWidget,
    RAMWidget,
    DiskWidget,
    NetworkStatsWidget,
    WiFiWidget,
    PacketStatsWidget
)


class SamplerDemo(App):
    """Demo app showcasing Sampler-style widgets."""
    
    CSS = """
    Screen {
        background: #000000;
    }
    
    Grid {
        grid-size: 3 2;
        grid-gutter: 1 2;
        height: 100%;
    }
    
    CPUWidget, RAMWidget, DiskWidget,
    NetworkStatsWidget, WiFiWidget, PacketStatsWidget {
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        padding: 1 2;
        height: 100%;
    }
    
    Header {
        background: #000000;
        color: #00cc66;
    }
    
    Footer {
        background: #000000;
        color: #00aa55;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose Sampler-style demo."""
        yield Header()
        
        with Grid():
            self.cpu_widget = CPUWidget()
            self.ram_widget = RAMWidget()
            self.disk_widget = DiskWidget()
            self.network_widget = NetworkStatsWidget()
            self.wifi_widget = WiFiWidget()
            self.packets_widget = PacketStatsWidget()
            
            yield self.cpu_widget
            yield self.ram_widget
            yield self.disk_widget
            yield self.network_widget
            yield self.wifi_widget
            yield self.packets_widget
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup mock data for demo."""
        self.set_interval(1.0, self.update_mock_data)
        self.update_mock_data()
    
    def update_mock_data(self) -> None:
        """Update widgets with mock data."""
        import random
        
        # CPU
        self.cpu_widget.cpu_percent = 65.0 + random.uniform(-10, 10)
        self.cpu_widget.cores = [
            45 + random.uniform(-10, 10),
            89 + random.uniform(-5, 5),
            72 + random.uniform(-10, 10),
            58 + random.uniform(-10, 10)
        ]
        
        # RAM
        self.ram_widget.percent = 68.5 + random.uniform(-5, 5)
        self.ram_widget.used_gb = 10.8 + random.uniform(-0.5, 0.5)
        self.ram_widget.total_gb = 16.0
        
        # Disk
        self.disk_widget.percent = 45.2 + random.uniform(-2, 2)
        self.disk_widget.used_gb = 225 + random.uniform(-10, 10)
        self.disk_widget.total_gb = 500
        
        # Network
        self.network_widget.upload_mbps = 1.2 + random.uniform(-0.5, 0.5)
        self.network_widget.download_mbps = 3.4 + random.uniform(-1, 1)
        self.network_widget.connections = 42 + random.randint(-5, 5)
        
        # WiFi
        self.wifi_widget.ssid = "HomeNetwork"
        self.wifi_widget.signal_dbm = -45 + random.randint(-5, 5)
        self.wifi_widget.security = "WPA2-PSK"
        
        # Packets
        self.packets_widget.total_packets = self.packets_widget.total_packets + random.randint(10, 50)
        self.packets_widget.http_count = self.packets_widget.http_count + random.randint(1, 5)
        self.packets_widget.https_count = self.packets_widget.https_count + random.randint(5, 15)
        self.packets_widget.dns_count = self.packets_widget.dns_count + random.randint(2, 8)


if __name__ == "__main__":
    app = SamplerDemo()
    app.run()
