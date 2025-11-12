"""
ConsolidatedDashboard v2 - Sampler Style
Professional overview dashboard inspired by sqshq/sampler

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widgets import Header, Footer

from ..widgets import (
    CPUWidget,
    RAMWidget,
    DiskWidget,
    NetworkStatsWidget,
    WiFiWidget,
    PacketStatsWidget
)


class ConsolidatedDashboardV2(Screen):
    """
    Consolidated overview - Sampler style.
    Clean, professional layout with all metrics.
    """
    
    BINDINGS = [
        ("1", "switch_system", "System"),
        ("2", "switch_network", "Network"),
        ("3", "switch_wifi", "WiFi"),
        ("4", "switch_packets", "Packets"),
        ("t", "toggle_mode", "Toggle Mode"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    ConsolidatedDashboardV2 {
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
    
    def __init__(self, plugin_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = plugin_manager
        
        # Widgets
        self.cpu_widget = CPUWidget()
        self.ram_widget = RAMWidget()
        self.disk_widget = DiskWidget()
        self.network_widget = NetworkStatsWidget()
        self.wifi_widget = WiFiWidget()
        self.packets_widget = PacketStatsWidget()
    
    def compose(self) -> ComposeResult:
        """Compose Sampler-style grid layout."""
        yield Header()
        
        with Grid():
            yield self.cpu_widget
            yield self.ram_widget
            yield self.disk_widget
            yield self.network_widget
            yield self.wifi_widget
            yield self.packets_widget
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup auto-refresh timer."""
        self.set_interval(1.0, self.refresh_metrics)
        self.refresh_metrics()
    
    def refresh_metrics(self) -> None:
        """Update all widgets with latest data."""
        try:
            # System Plugin
            system_data = self.plugin_manager.get_plugin_data('system')
            if system_data:
                self.cpu_widget.cpu_percent = system_data.get('cpu_percent', 0.0)
                self.cpu_widget.cores = system_data.get('cpu_per_core', [])
                
                memory = system_data.get('memory', {})
                self.ram_widget.percent = memory.get('percent', 0.0)
                self.ram_widget.used_gb = memory.get('used', 0) / (1024**3)
                self.ram_widget.total_gb = memory.get('total', 0) / (1024**3)
                
                disk = system_data.get('disk', {})
                self.disk_widget.percent = disk.get('percent', 0.0)
                self.disk_widget.used_gb = disk.get('used', 0) / (1024**3)
                self.disk_widget.total_gb = disk.get('total', 0) / (1024**3)
            
            # Network Plugin
            network_data = self.plugin_manager.get_plugin_data('network')
            if network_data:
                self.network_widget.upload_mbps = network_data.get('bytes_sent_per_sec', 0) / (1024**2)
                self.network_widget.download_mbps = network_data.get('bytes_recv_per_sec', 0) / (1024**2)
                self.network_widget.connections = network_data.get('connections', 0)
            
            # WiFi Plugin
            wifi_data = self.plugin_manager.get_plugin_data('wifi')
            if wifi_data and wifi_data.get('networks'):
                network = wifi_data['networks'][0]  # First network
                self.wifi_widget.ssid = network.get('ssid', 'Unknown')
                self.wifi_widget.signal_dbm = network.get('signal_strength', -100)
                self.wifi_widget.security = network.get('security', 'Unknown')
            
            # Packet Analyzer Plugin
            packet_data = self.plugin_manager.get_plugin_data('packet_analyzer')
            if packet_data:
                self.packets_widget.total_packets = packet_data.get('total_packets', 0)
                protocols = packet_data.get('protocols', {})
                self.packets_widget.http_count = protocols.get('HTTP', 0)
                self.packets_widget.https_count = protocols.get('HTTPS', 0)
                self.packets_widget.dns_count = protocols.get('DNS', 0)
        
        except Exception as e:
            self.log(f"Error refreshing metrics: {e}")
    
    def action_switch_system(self) -> None:
        """Switch to system dashboard."""
        self.app.pop_screen()
        self.app.push_screen("system")
    
    def action_switch_network(self) -> None:
        """Switch to network dashboard."""
        self.app.pop_screen()
        self.app.push_screen("network")
    
    def action_switch_wifi(self) -> None:
        """Switch to WiFi dashboard."""
        self.app.pop_screen()
        self.app.push_screen("wifi")
    
    def action_switch_packets(self) -> None:
        """Switch to packets dashboard."""
        self.app.pop_screen()
        self.app.push_screen("packets")
    
    def action_toggle_mode(self) -> None:
        """Toggle between mock and real mode."""
        self.app.toggle_mode()
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.exit()
