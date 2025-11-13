"""
WiFi Handshake Capturer Dashboard

Educational tool demonstrating WPA/WPA2 handshake capture.
⚠️ LEGAL WARNING: Only use on YOUR networks with permission.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-13
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import datetime


class HandshakeDashboard(Screen):
    """
    WiFi Handshake Capturer Dashboard.
    
    ⚠️ CRITICAL LEGAL REQUIREMENTS:
    - Only YOUR OWN networks
    - WRITTEN PERMISSION required
    - Educational demonstration ONLY
    
    Shows:
    - Legal warnings (prominent)
    - Target networks (WPA/WPA2)
    - Captured handshakes
    - Password strength analysis
    - Educational security lessons
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("w", "show_warnings", "Legal Warnings"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    HandshakeDashboard {
        background: #000000;
    }
    
    #legal-warning {
        background: #330000;
        color: #ff0000;
        height: 9;
        border: heavy #ff0000;
        padding: 1 2;
        margin: 1 2;
    }
    
    #handshake-stats-header {
        background: #000000;
        color: #00cc66;
        height: 6;
        border: round #00aa55;
        padding: 1 2;
        margin: 0 2 1 2;
    }
    
    #networks-table {
        height: 35%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 2 1 2;
    }
    
    #bottom-section {
        height: 40%;
        margin: 0 2 1 2;
    }
    
    #handshakes-table {
        width: 60%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
    }
    
    #educational-panel {
        width: 40%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        padding: 1 2;
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
        self.ethical_consent = False
    
    def compose(self) -> ComposeResult:
        """Compose handshake dashboard layout."""
        yield Header()
        
        with Vertical():
            # LEGAL WARNING - Most prominent
            yield Static("", id="legal-warning")
            
            # Stats header
            yield Static("", id="handshake-stats-header")
            
            # Target networks table
            yield DataTable(id="networks-table")
            
            # Bottom section: Handshakes + Educational
            with Horizontal(id="bottom-section"):
                yield DataTable(id="handshakes-table")
                yield Static("", id="educational-panel")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup tables and start refresh timer."""
        # Configure networks table
        networks_table = self.query_one("#networks-table", DataTable)
        networks_table.add_columns("SSID", "BSSID", "Ch", "Signal", "Encryption", "Clients", "Status")
        networks_table.cursor_type = "row"
        
        # Configure handshakes table
        handshakes_table = self.query_one("#handshakes-table", DataTable)
        handshakes_table.add_columns("Time", "SSID", "Client", "Packets", "Strength")
        handshakes_table.cursor_type = "row"
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update handshake data from plugin."""
        try:
            data = self.app.get_plugin_data('handshake')
            
            if not data:
                return
            
            self._update_legal_warning(data)
            self._update_stats_header(data)
            self._update_networks_table(data)
            self._update_handshakes_table(data)
            self._update_educational_panel(data)
            
        except Exception as e:
            self.app.notify(f"Handshake refresh error: {e}", severity="error")
    
    def _update_legal_warning(self, data: dict) -> None:
        """Update legal warning banner."""
        warning = self.query_one("#legal-warning", Static)
        
        consent = data.get('ethical_consent', False)
        
        if not consent:
            content = """[bold #ff0000 blink]⚖️  LEGAL CONSENT REQUIRED  ⚖️[/]

[#ff6666]Capturing WPA handshakes without authorization is ILLEGAL.
ONLY use on networks you OWN with WRITTEN PERMISSION.
Unauthorized access is a FEDERAL CRIME in most countries.[/]

[#ffaa00]To enable: Set ethical_consent=True for YOUR network only[/]"""
        else:
            content = """[bold #ffaa00]⚠️  LEGAL & EDUCATIONAL USE ONLY  ⚠️[/]

[#ffcc66]This tool is for YOUR network security education.
Demonstrates why strong passwords (20+ chars) are critical.
Never use on networks you don't own![/]

[#00cc66]Legal consent given - Educational mode active[/]"""
        
        warning.update(content)
    
    def _update_stats_header(self, data: dict) -> None:
        """Update statistics header."""
        header = self.query_one("#handshake-stats-header", Static)
        
        stats = data.get('stats', {})
        monitoring = data.get('monitoring', False)
        warning_msg = data.get('educational_warning', '')
        
        status_color = "#00cc66" if monitoring else "#ff0000"
        status_text = "ACTIVE" if monitoring else "STOPPED"
        
        handshakes = stats.get('complete_handshakes', 0)
        handshake_color = "#00cc66" if handshakes > 0 else "#ffaa00"
        
        content = f"""[bold #00cc66]HANDSHAKE CAPTURER[/]
[#00aa55]Status:[/] [{status_color}]{status_text}[/]  [#00aa55]Networks:[/] [#00cc66]{stats.get('networks_detected', 0)}[/]  [#00aa55]EAPOL Packets:[/] [#00cc66]{stats.get('eapol_packets', 0)}[/]  [#00aa55]Handshakes:[/] [{handshake_color}]{handshakes}[/]
[#00aa55]📡 Status:[/] [#008855]{warning_msg}[/]"""
        
        header.update(content)
    
    def _update_networks_table(self, data: dict) -> None:
        """Update target networks table."""
        table = self.query_one("#networks-table", DataTable)
        
        # Get networks
        networks = data.get('target_networks', [])
        handshakes = data.get('handshakes', [])
        
        # Get BSSIDs with captured handshakes
        captured_bssids = {h['bssid'] for h in handshakes if h.get('is_complete')}
        
        # Clear and repopulate
        table.clear()
        
        if not networks:
            table.add_row(
                "[#666666]No WPA/WPA2[/]",
                "[#666666]networks[/]",
                "[#666666]detected[/]",
                "[#666666]yet[/]",
                "[#666666]...[/]",
                "[#666666]-[/]",
                "[#666666]Scanning...[/]"
            )
            return
        
        # Sort by signal strength
        networks_sorted = sorted(networks, key=lambda x: x.get('signal_strength', -100), reverse=True)
        
        for net in networks_sorted:
            ssid = net.get('ssid', 'N/A')
            bssid = net.get('bssid', 'N/A')
            channel = net.get('channel', 0)
            signal = net.get('signal_strength', -100)
            encryption = net.get('encryption', 'Unknown')
            clients = net.get('clients_count', 0)
            
            # Determine status
            if bssid in captured_bssids:
                status = "[bold #00cc66]✓ Captured[/]"
            else:
                status = "[#ffaa00]⏳ Waiting[/]"
            
            # Truncate long values
            if len(ssid) > 20:
                ssid = ssid[:17] + "..."
            if len(bssid) > 17:
                bssid = bssid[:14] + "..."
            
            # Format signal
            if signal > -50:
                signal_display = f"[#00cc66]{signal} dBm[/]"
            elif signal > -70:
                signal_display = f"[#ffaa00]{signal} dBm[/]"
            else:
                signal_display = f"[#666666]{signal} dBm[/]"
            
            table.add_row(
                ssid,
                bssid,
                str(channel),
                f"{signal} dBm",
                encryption,
                str(clients),
                status
            )
    
    def _update_handshakes_table(self, data: dict) -> None:
        """Update captured handshakes table."""
        table = self.query_one("#handshakes-table", DataTable)
        
        # Get handshakes
        handshakes = data.get('handshakes', [])
        
        # Clear and repopulate
        table.clear()
        
        if not handshakes:
            table.add_row(
                "[#666666]No handshakes[/]",
                "[#666666]captured yet[/]",
                "[#666666]...[/]",
                "[#666666]-[/]",
                "[#666666]Waiting[/]"
            )
            return
        
        for hs in reversed(handshakes[-10:]):  # Last 10, most recent first
            timestamp = hs.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            
            ssid = hs.get('ssid', 'N/A')
            client = hs.get('client_mac', 'N/A')
            packets = hs.get('packets_captured', 0)
            strength = hs.get('password_strength', 'Unknown')
            
            # Truncate long values
            if len(ssid) > 15:
                ssid = ssid[:12] + "..."
            if len(client) > 17:
                client = client[:14] + "..."
            
            # Color strength
            if strength == "WEAK":
                strength_display = f"[bold #ff0000]{strength}[/]"
            elif strength == "MEDIUM":
                strength_display = f"[#ffaa00]{strength}[/]"
            elif strength == "STRONG":
                strength_display = f"[#00cc66]{strength}[/]"
            else:
                strength_display = f"[#666666]{strength}[/]"
            
            table.add_row(
                time_str,
                ssid,
                client,
                str(packets),
                strength_display
            )
    
    def _update_educational_panel(self, data: dict) -> None:
        """Update educational information panel."""
        widget = self.query_one("#educational-panel", Static)
        
        stats = data.get('stats', {})
        handshakes = stats.get('complete_handshakes', 0)
        
        content = "[bold #00cc66]🎓 Handshake Education[/]\n\n"
        
        # Lesson 1: What is a handshake?
        content += "[#00aa55]WPA Handshake Process:[/]\n"
        content += "[#008855]1. Client asks to connect\n"
        content += "2. AP sends challenge (ANonce)\n"
        content += "3. Client responds (SNonce + MIC)\n"
        content += "4. AP confirms connection\n\n"
        
        content += "[#ffaa00]This 4-way exchange can be\n"
        content += "captured and used to test\n"
        content += "password strength offline.[/]\n\n"
        
        # Lesson 2: Password security
        content += "[#00aa55]Password Strength:[/]\n"
        content += "[#ff6666]WEAK:[/] [#ff8888]< 8 chars, dictionary\n"
        content += "        Cracked in hours\n\n"
        content += "[#ffaa00]MEDIUM:[/] [#ffcc66]8-15 chars, mixed\n"
        content += "          Cracked in days/weeks\n\n"
        content += "[#00cc66]STRONG:[/] [#00ff00]20+ chars, random\n"
        content += "          Takes YEARS to crack[/]\n\n"
        
        # Lesson 3: Protection
        content += "[#00aa55]How to Protect:[/]\n"
        content += "[#008855]• Use 20+ character passwords\n"
        content += "• Random characters (no words)\n"
        content += "• Change default router password\n"
        content += "• Use WPA3 if available\n"
        content += "• Monitor for deauth attacks\n\n"
        
        # Current status
        if handshakes > 0:
            content += f"[bold #00cc66]✓ Education Complete![/]\n"
            content += f"[#00aa55]{handshakes} handshake(s) captured.\n"
            content += "You now understand why strong\n"
            content += "passwords are CRITICAL![/]\n\n"
        else:
            content += "[#ffaa00]📡 Monitoring...[/]\n"
            content += "[#ffcc66]Waiting for handshake capture.\n"
            content += "Connect a device to target\n"
            content += "network to trigger exchange.[/]\n\n"
        
        # Final message
        content += "[bold #00cc66]Remember:[/]\n"
        content += "[#00aa55]This demonstrates WHY security matters.\n"
        content += "Always use STRONG passwords![/]"
        
        widget.update(content)
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("Handshake data refreshed", severity="information")
    
    def action_show_warnings(self) -> None:
        """Show legal warnings."""
        self.app.notify(
            "⚖️ LEGAL WARNING: Only capture handshakes on YOUR network with permission!",
            severity="warning",
            timeout=5
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
