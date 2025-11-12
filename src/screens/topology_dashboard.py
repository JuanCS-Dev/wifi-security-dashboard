"""
Network Topology Dashboard

Displays discovered devices in network with visual table.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive


class TopologyDashboard(Screen):
    """
    Network Topology visualization dashboard.
    
    Shows:
    - Gateway info
    - Device count
    - Device table (IP, MAC, Hostname, Vendor)
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    TopologyDashboard {
        background: #000000;
    }
    
    #topology-header {
        background: #000000;
        color: #00cc66;
        height: 5;
        border: round #00aa55;
        padding: 1 2;
        margin: 1 2;
    }
    
    #device-table {
        height: 100%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 2 1 2;
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gateway_ip = "N/A"
        self.subnet = "N/A"
        self.device_count = 0
    
    def compose(self) -> ComposeResult:
        """Compose topology dashboard layout."""
        yield Header()
        
        with Vertical():
            yield Static("", id="topology-header")
            yield DataTable(id="device-table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup table and start refresh timer."""
        # Configure table
        table = self.query_one("#device-table", DataTable)
        table.add_columns("IP", "MAC Address", "Hostname", "Vendor", "Status")
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update topology data from plugin."""
        try:
            data = self.app.get_plugin_data('topology')
            
            if not data:
                return
            
            self.gateway_ip = data.get('gateway_ip', 'N/A')
            self.subnet = data.get('subnet', 'N/A')
            self.device_count = data.get('device_count', 0)
            devices = data.get('devices', [])
            
            # Update header
            self._update_header()
            
            # Update table
            self._update_table(devices)
            
        except Exception as e:
            self.app.notify(f"Topology refresh error: {e}", severity="error")
    
    def _update_header(self) -> None:
        """Update header with gateway info."""
        header = self.query_one("#topology-header", Static)
        
        content = f"""[bold #00cc66]NETWORK TOPOLOGY MAPPER[/]
[#00aa55]Gateway:[/] [#00cc66]{self.gateway_ip}[/]  [#00aa55]Subnet:[/] [#00cc66]{self.subnet}[/]  [#00aa55]Devices:[/] [bold #00cc66]{self.device_count}[/]"""
        
        header.update(content)
    
    def _update_table(self, devices: list) -> None:
        """Update device table."""
        table = self.query_one("#device-table", DataTable)
        
        # Clear existing rows
        table.clear()
        
        # Add devices
        for device in devices:
            ip = device.get('ip', 'N/A')
            mac = device.get('mac', 'N/A')
            hostname = device.get('hostname', 'Unknown')
            vendor = device.get('vendor', 'Unknown')
            
            # Status: check if gateway
            status = "🌐 Gateway" if ip == self.gateway_ip else "✓ Online"
            
            table.add_row(ip, mac, hostname, vendor, status)
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("Topology refreshed", severity="information")
    
    def action_switch_consolidated(self) -> None:
        """Switch to consolidated dashboard."""
        self.app.action_switch_screen('consolidated')
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.action_quit()
