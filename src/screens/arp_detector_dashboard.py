"""
ARP Spoofing Detector Dashboard

Monitors network for ARP spoofing attacks (Man-in-the-Middle).
Educational tool to demonstrate network security threats.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import datetime


class ARPDetectorDashboard(Screen):
    """
    ARP Spoofing Detection Dashboard.
    
    Shows:
    - Monitor status (ON/OFF)
    - Detection statistics
    - Recent alerts table
    - Educational security tips
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("c", "clear_alerts", "Clear Alerts"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    ARPDetectorDashboard {
        background: #000000;
    }
    
    #arp-status-header {
        background: #000000;
        color: #00cc66;
        height: auto; min-height: auto; min-height: 3;
        border: round #00aa55;
        padding: 1;
        margin: 0 1 1 1;
    }
    
    #alerts-table {
        height: auto; min-height: 12;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 1 1 1;
    }
    
    #educational-tip {
        background: #000000;
        color: #00aa55;
        height: auto; min-height: 3;
        border: round #00aa55;
        padding: 1;
        margin: 0 1 1 1;
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
        self.alert_count = 0
        self.arp_cache_size = 0
    
    def compose(self) -> ComposeResult:
        """Compose ARP detector dashboard layout."""
        yield Header()
        
        with Vertical():
            yield Static("", id="arp-status-header")
            yield DataTable(id="alerts-table")
            yield Static("", id="educational-tip")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup table and start refresh timer."""
        # Configure alerts table
        table = self.query_one("#alerts-table", DataTable)
        table.add_columns(
            "Time",
            "IP Address",
            "Old MAC",
            "New MAC",
            "Severity",
            "Description"
        )
        
        # Update educational tip
        self._update_educational_tip()
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update ARP detection data from plugin."""
        try:
            data = self.app.get_plugin_data('arp_detector')
            
            if not data:
                return
            
            self.monitoring = data.get('monitoring', False)
            self.alert_count = data.get('alert_count', 0)
            self.arp_cache_size = data.get('arp_cache_size', 0)
            stats = data.get('stats', {})
            recent_alerts = data.get('recent_alerts', [])
            
            # Update header
            self._update_header(stats)
            
            # Update alerts table
            self._update_alerts_table(recent_alerts)
            
        except Exception as e:
            self.app.notify(f"ARP detector refresh error: {e}", severity="error")
    
    def _update_header(self, stats: dict) -> None:
        """Update status header with monitoring info."""
        header = self.query_one("#arp-status-header", Static)
        
        # Monitor status indicator
        if self.monitoring:
            status_icon = "[bold green]●[/bold green] MONITORING"
            status_color = "#00cc66"
        else:
            status_icon = "[bold red]●[/bold red] STOPPED"
            status_color = "#cc6600"
        
        # Alert severity indicator
        critical_alerts = stats.get('critical_alerts', 0)
        if critical_alerts > 0:
            alert_indicator = f"[bold red]⚠ {critical_alerts} CRITICAL[/bold red]"
        elif self.alert_count > 0:
            alert_indicator = f"[bold yellow]⚠ {self.alert_count} warnings[/bold yellow]"
        else:
            alert_indicator = "[bold green]✓ No threats[/bold green]"
        
        content = f"""[bold #00cc66]ARP SPOOFING DETECTOR[/bold #00cc66]

[#{status_color}]Status:[/] {status_icon}  [#00aa55]Cache Size:[/] [#00cc66]{self.arp_cache_size}[/]  [#00aa55]Total Packets:[/] [#00cc66]{stats.get('arp_packets', 0)}[/]
{alert_indicator}  [#00aa55]MAC Changes:[/] [#00cc66]{stats.get('mac_changes', 0)}[/]"""
        
        header.update(content)
    
    def _update_alerts_table(self, alerts: list) -> None:
        """Update alerts table with recent detections."""
        table = self.query_one("#alerts-table", DataTable)
        
        # Clear existing rows
        table.clear()
        
        if not alerts:
            # Show friendly message if no alerts
            table.add_row(
                "---",
                "No alerts detected",
                "---",
                "---",
                "✓ SAFE",
                "Network is clean"
            )
            return
        
        # Add alerts (most recent first)
        for alert in reversed(alerts):
            timestamp = alert.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            
            ip = alert.get('ip', 'Unknown')
            old_mac = alert.get('old_mac', 'N/A')
            new_mac = alert.get('new_mac', 'N/A')
            severity = alert.get('severity', 'LOW')
            description = alert.get('description', '')
            
            # Severity indicator
            if severity == 'CRITICAL':
                severity_display = "[bold red]🔴 CRITICAL[/bold red]"
            elif severity == 'HIGH':
                severity_display = "[bold yellow]🟡 HIGH[/bold yellow]"
            elif severity == 'MEDIUM':
                severity_display = "[yellow]🟠 MEDIUM[/yellow]"
            else:
                severity_display = "[dim]🔵 LOW[/dim]"
            
            table.add_row(
                time_str,
                ip,
                old_mac[:17],  # Truncate MAC if too long
                new_mac[:17],
                severity_display,
                description[:40]  # Truncate description
            )
    
    def _update_educational_tip(self) -> None:
        """Update educational security tip."""
        tip_widget = self.query_one("#educational-tip", Static)
        
        tip = (
            "[bold #00cc66]💡 SECURITY TIP:[/bold #00cc66] "
            "[#00aa55]ARP spoofing is a Man-in-the-Middle attack where an attacker "
            "impersonates another device by sending fake ARP messages. "
            "This allows them to intercept, modify, or block data. "
            "Always use encrypted connections (HTTPS, VPN) on untrusted networks![/]"
        )
        
        tip_widget.update(tip)
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("ARP detector refreshed", severity="information")
    
    def action_clear_alerts(self) -> None:
        """Clear all alerts (educational mode)."""
        # In real implementation, this would call plugin.clear_alerts()
        self.app.notify(
            "Alerts cleared (educational mode)",
            title="⚠️ Educational Feature",
            severity="information"
        )
    
    def action_switch_consolidated(self) -> None:
        """Switch to consolidated dashboard."""
        self.app.action_switch_screen('consolidated')
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.action_quit()
