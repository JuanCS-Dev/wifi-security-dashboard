"""
Traffic Statistics Dashboard - Sampler Style

Real-time network traffic monitoring per device.
Professional grid layout inspired by sqshq/sampler.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import timedelta


class TrafficDashboard(Screen):
    """
    Traffic Statistics Dashboard - Sampler style.
    
    Grid layout with:
    - Global stats (top-left)
    - Top talkers (top-right)
    - Device table (bottom, full-width)
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("s", "sort_bandwidth", "Sort by Bandwidth"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    TrafficDashboard {
        background: #000000;
    }
    
    #stats-grid {
        grid-size: 2 1;
        grid-gutter: 1 2;
        height: 12;
        margin: 1 2;
    }
    
    #global-stats, #top-talkers {
        background: #000000;
        color: #00cc66;
        border: round #00aa55;
        padding: 1 2;
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
        self.monitoring = False
        self.device_count = 0
        self.sort_by = 'bandwidth'  # bandwidth, packets, hostname
    
    def compose(self) -> ComposeResult:
        """Compose Sampler-style grid layout."""
        yield Header()
        
        with Vertical():
            # Top row: Global stats + Top talkers (Grid 2x1)
            with Grid(id="stats-grid"):
                yield Static("", id="global-stats")
                yield Static("", id="top-talkers")
            
            # Bottom row: Device table (full width)
            yield DataTable(id="device-table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup table and start refresh timer."""
        # Configure device table
        table = self.query_one("#device-table", DataTable)
        table.add_columns(
            "Hostname",
            "IP Address",
            "↑ Sent",
            "↓ Received",
            "Total",
            "Bandwidth",
            "Packets"
        )
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update traffic statistics from plugin."""
        try:
            data = self.app.get_plugin_data('traffic_stats')
            
            if not data:
                return
            
            self.monitoring = data.get('monitoring', False)
            self.device_count = data.get('device_count', 0)
            global_stats = data.get('global_stats', {})
            top_talkers = data.get('top_talkers', [])
            devices = data.get('devices', [])
            uptime = data.get('uptime', 0)
            
            # Update widgets
            self._update_global_stats(global_stats, uptime)
            self._update_top_talkers(top_talkers)
            self._update_device_table(devices)
            
        except Exception as e:
            self.app.notify(f"Traffic stats refresh error: {e}", severity="error")
    
    def _update_global_stats(self, stats: dict, uptime: float) -> None:
        """Update global statistics widget (Sampler style)."""
        widget = self.query_one("#global-stats", Static)
        
        # Format uptime
        uptime_str = str(timedelta(seconds=int(uptime)))
        
        # Format total bytes
        total_bytes = stats.get('total_bytes', 0)
        total_gb = total_bytes / (1024**3)
        
        # Format bandwidth
        bandwidth_mbps = stats.get('bandwidth_mbps', 0.0)
        
        # Protocols
        protocols = stats.get('protocols', {})
        protocol_str = ", ".join([f"{k}:{v}" for k, v in list(protocols.items())[:3]])
        
        # Status indicator
        if self.monitoring:
            status_icon = "[bold green]●[/bold green] MONITORING"
        else:
            status_icon = "[bold red]●[/bold red] STOPPED"
        
        content = f"""[bold #00cc66]GLOBAL STATISTICS[/bold #00cc66]

[#00aa55]Status:[/] {status_icon}
[#00aa55]Uptime:[/] [#00cc66]{uptime_str}[/]
[#00aa55]Devices:[/] [bold #00cc66]{self.device_count}[/bold #00cc66]
[#00aa55]Total:[/] [#00cc66]{total_gb:.2f} GB[/]
[#00aa55]Bandwidth:[/] [bold #00cc66]{bandwidth_mbps:.2f}[/bold #00cc66] [#00aa55]Mbps[/]
[#00aa55]Protocols:[/] [dim]{protocol_str or 'None'}[/dim]"""
        
        widget.update(content)
    
    def _update_top_talkers(self, top_talkers: list) -> None:
        """Update top talkers widget (Sampler style)."""
        widget = self.query_one("#top-talkers", Static)
        
        content = "[bold #00cc66]TOP 5 BANDWIDTH HOGS[/bold #00cc66]\n\n"
        
        if not top_talkers:
            content += "[dim]No devices detected yet[/dim]"
        else:
            # Emoji indicators for rank
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            
            for i, device in enumerate(top_talkers[:5]):
                hostname = device.get('hostname', 'Unknown')[:12]  # Truncate
                total_mb = device.get('total_bytes', 0) / (1024**2)
                bandwidth = device.get('bandwidth', 0.0)
                
                # Bar indicator (relative to top device)
                if i == 0:
                    max_bandwidth = bandwidth if bandwidth > 0 else 1
                bar_length = int((bandwidth / max_bandwidth) * 10) if i == 0 else int((bandwidth / (top_talkers[0].get('bandwidth', 1) or 1)) * 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                
                content += f"{medals[i]} [#00cc66]{hostname}[/]\n"
                content += f"   {bar} [bold]{total_mb:.1f}[/bold] [dim]MB[/dim]\n"
        
        widget.update(content)
    
    def _update_device_table(self, devices: list) -> None:
        """Update device table with traffic stats."""
        table = self.query_one("#device-table", DataTable)
        
        # Clear existing rows
        table.clear()
        
        if not devices:
            # Friendly message
            table.add_row(
                "No devices",
                "---",
                "---",
                "---",
                "---",
                "0 Mbps",
                "0"
            )
            return
        
        # Sort devices
        if self.sort_by == 'bandwidth':
            devices = sorted(devices, key=lambda d: d.get('total_bytes', 0), reverse=True)
        elif self.sort_by == 'packets':
            devices = sorted(devices, key=lambda d: d.get('total_packets', 0), reverse=True)
        elif self.sort_by == 'hostname':
            devices = sorted(devices, key=lambda d: d.get('hostname', 'Unknown'))
        
        # Add device rows
        for device in devices:
            hostname = device.get('hostname', 'Unknown')[:20]  # Truncate
            ip = device.get('ip', 'N/A')
            bytes_sent = device.get('bytes_sent', 0)
            bytes_recv = device.get('bytes_received', 0)
            total_bytes = device.get('total_bytes', 0)
            total_packets = device.get('total_packets', 0)
            
            # Format sizes
            sent_mb = bytes_sent / (1024**2)
            recv_mb = bytes_recv / (1024**2)
            total_mb = total_bytes / (1024**2)
            
            # Calculate bandwidth (rough estimate)
            bandwidth = 0.0  # Would need time delta for accurate calculation
            
            # Color coding based on traffic volume
            if total_mb > 100:
                total_display = f"[bold red]{total_mb:.1f} MB[/bold red]"
            elif total_mb > 10:
                total_display = f"[bold yellow]{total_mb:.1f} MB[/bold yellow]"
            else:
                total_display = f"[#00cc66]{total_mb:.1f} MB[/]"
            
            table.add_row(
                hostname,
                ip,
                f"{sent_mb:.1f} MB",
                f"{recv_mb:.1f} MB",
                total_display,
                f"{bandwidth:.2f} Mbps",
                str(total_packets)
            )
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("Traffic statistics refreshed", severity="information")
    
    def action_sort_bandwidth(self) -> None:
        """Toggle sort mode."""
        sort_modes = ['bandwidth', 'packets', 'hostname']
        current_idx = sort_modes.index(self.sort_by)
        self.sort_by = sort_modes[(current_idx + 1) % len(sort_modes)]
        self.refresh_data()
        self.app.notify(f"Sorted by {self.sort_by}", severity="information")
    
    def action_switch_consolidated(self) -> None:
        """Switch to consolidated dashboard."""
        self.app.action_switch_screen('consolidated')
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.action_quit()
