"""
Rogue AP Detector Dashboard

Monitors for fake/evil twin access points.
Educational tool demonstrating AP spoofing attacks.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-13
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import datetime


class RogueAPDashboard(Screen):
    """
    Rogue AP Detector Dashboard.
    
    Shows:
    - Baseline learning status
    - All detected APs (table)
    - Rogue AP alerts (critical section)
    - Educational security tips
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("b", "show_baseline", "Show Baseline"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    RogueAPDashboard {
        background: #000000;
    }
    
    #rogue-stats-header {
        background: #000000;
        color: #00cc66;
        height: 7;
        border: round #00aa55;
        padding: 1 2;
        margin: 1 2;
    }
    
    #ap-table {
        height: 50%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 2 1 2;
    }
    
    #bottom-section {
        height: 35%;
        margin: 0 2 1 2;
    }
    
    #alert-table {
        width: 60%;
        border: heavy #ff0000;
        background: #110000;
        color: #ff6666;
    }
    
    #educational-tips {
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
        self.baseline_learned = False
    
    def compose(self) -> ComposeResult:
        """Compose rogue AP dashboard layout."""
        yield Header()
        
        with Vertical():
            # Stats header
            yield Static("", id="rogue-stats-header")
            
            # AP table (all detected APs)
            yield DataTable(id="ap-table")
            
            # Bottom section: Alerts + Educational
            with Horizontal(id="bottom-section"):
                yield DataTable(id="alert-table")
                yield Static("", id="educational-tips")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup tables and start refresh timer."""
        # Configure AP table
        ap_table = self.query_one("#ap-table", DataTable)
        ap_table.add_columns("SSID", "BSSID", "Ch", "Signal", "Encryption", "Vendor", "Beacons", "Status")
        ap_table.cursor_type = "row"
        
        # Configure alert table
        alert_table = self.query_one("#alert-table", DataTable)
        alert_table.add_columns("Time", "SSID", "Rogue BSSID", "Severity", "Reason")
        alert_table.cursor_type = "row"
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update rogue AP data from plugin."""
        try:
            data = self.app.get_plugin_data('rogue_ap')
            
            if not data:
                return
            
            self._update_stats_header(data)
            self._update_ap_table(data)
            self._update_alert_table(data)
            self._update_educational_tips(data)
            
        except Exception as e:
            self.app.notify(f"Rogue AP refresh error: {e}", severity="error")
    
    def _update_stats_header(self, data: dict) -> None:
        """Update statistics header."""
        header = self.query_one("#rogue-stats-header", Static)
        
        stats = data.get('stats', {})
        monitoring = data.get('monitoring', False)
        baseline_learned = data.get('baseline_learned', False)
        tip = data.get('educational_tip', '')
        
        status_color = "#00cc66" if monitoring else "#ff0000"
        status_text = "ACTIVE" if monitoring else "STOPPED"
        
        baseline_color = "#00cc66" if baseline_learned else "#ffaa00"
        baseline_text = "LEARNED" if baseline_learned else "LEARNING..."
        
        rogue_count = stats.get('rogue_aps_confirmed', 0)
        rogue_color = "#ff0000" if rogue_count > 0 else "#00cc66"
        
        content = f"""[bold #00cc66]ROGUE AP DETECTOR[/]
[#00aa55]Status:[/] [{status_color}]{status_text}[/]  [#00aa55]Baseline:[/] [{baseline_color}]{baseline_text}[/]  [#00aa55]Total APs:[/] [#00cc66]{stats.get('total_aps_detected', 0)}[/]  [#00aa55]Rogue APs:[/] [{rogue_color}]{rogue_count}[/]  [#00aa55]Beacons:[/] [#00cc66]{stats.get('beacons_captured', 0)}[/]
[#00aa55]💡 Status:[/] [#008855]{tip}[/]"""
        
        header.update(content)
    
    def _update_ap_table(self, data: dict) -> None:
        """Update access points table."""
        table = self.query_one("#ap-table", DataTable)
        
        # Get APs
        aps = data.get('access_points', [])
        baseline_aps = data.get('baseline_aps', {})
        rogue_alerts = data.get('rogue_alerts', [])
        
        # Get rogue BSSIDs for highlighting
        rogue_bssids = {alert['rogue_bssid'] for alert in rogue_alerts}
        
        # Clear and repopulate
        table.clear()
        
        # Sort by signal strength (strongest first)
        aps_sorted = sorted(aps, key=lambda x: x.get('signal_strength', -100), reverse=True)
        
        for ap in aps_sorted:
            ssid = ap.get('ssid', 'N/A')
            bssid = ap.get('bssid', 'N/A')
            channel = ap.get('channel', 0)
            signal = ap.get('signal_strength', -100)
            encryption = ap.get('encryption', 'Unknown')
            vendor = ap.get('vendor', 'Unknown')
            beacons = ap.get('beacon_count', 0)
            
            # Determine status
            if bssid in rogue_bssids:
                status = "[bold #ff0000]🚨 ROGUE[/]"
            elif ssid in baseline_aps and baseline_aps[ssid] == bssid:
                status = "[#00cc66]✓ Baseline[/]"
            else:
                status = "[#ffaa00]? Unknown[/]"
            
            # Truncate long values
            if len(ssid) > 20:
                ssid = ssid[:17] + "..."
            if len(bssid) > 17:
                bssid = bssid[:14] + "..."
            if len(vendor) > 15:
                vendor = vendor[:12] + "..."
            
            # Format signal strength
            if signal > -50:
                signal_display = f"[#00cc66]{signal} dBm[/]"  # Strong
            elif signal > -70:
                signal_display = f"[#ffaa00]{signal} dBm[/]"  # Medium
            else:
                signal_display = f"[#666666]{signal} dBm[/]"  # Weak
            
            # Format encryption
            if encryption == "Open":
                enc_display = f"[#ff6666]{encryption}[/]"  # Dangerous
            elif "WPA2" in encryption or "WPA3" in encryption:
                enc_display = f"[#00cc66]{encryption}[/]"  # Secure
            else:
                enc_display = f"[#ffaa00]{encryption}[/]"  # Weak
            
            table.add_row(
                ssid,
                bssid,
                str(channel),
                f"{signal} dBm",
                encryption,
                vendor,
                str(beacons),
                status
            )
    
    def _update_alert_table(self, data: dict) -> None:
        """Update rogue AP alerts table."""
        table = self.query_one("#alert-table", DataTable)
        
        # Get alerts
        alerts = data.get('rogue_alerts', [])
        
        # Clear and repopulate
        table.clear()
        
        if not alerts:
            table.add_row(
                "[#00cc66]No rogue APs[/]",
                "[#00cc66]detected![/]",
                "[#00cc66]✓ Network[/]",
                "[#00cc66]looks[/]",
                "[#00cc66]clean[/]"
            )
            return
        
        for alert in reversed(alerts[-10:]):  # Last 10, most recent first
            timestamp = alert.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            
            ssid = alert.get('ssid', 'N/A')
            rogue_bssid = alert.get('rogue_bssid', 'N/A')
            severity = alert.get('severity', 'UNKNOWN')
            reason = alert.get('reason', 'UNKNOWN')
            
            # Truncate long values
            if len(ssid) > 15:
                ssid = ssid[:12] + "..."
            if len(rogue_bssid) > 17:
                rogue_bssid = rogue_bssid[:14] + "..."
            
            # Color severity
            if severity == "CRITICAL":
                severity_display = f"[bold #ff0000]{severity}[/]"
            elif severity == "HIGH":
                severity_display = f"[#ff6666]{severity}[/]"
            elif severity == "MEDIUM":
                severity_display = f"[#ffaa00]{severity}[/]"
            else:
                severity_display = f"[#ffcc66]{severity}[/]"
            
            # Format reason
            reason_map = {
                'SSID_COLLISION': '🎭 Evil Twin',
                'STRONG_SIGNAL': '📡 Strong Signal',
                'SUSPICIOUS_OPEN': '🍯 Honeypot',
            }
            reason_display = reason_map.get(reason, reason)
            
            table.add_row(
                time_str,
                ssid,
                rogue_bssid,
                severity_display,
                reason_display
            )
    
    def _update_educational_tips(self, data: dict) -> None:
        """Update educational tips panel."""
        widget = self.query_one("#educational-tips", Static)
        
        stats = data.get('stats', {})
        rogue_count = stats.get('rogue_aps_confirmed', 0)
        baseline_learned = data.get('baseline_learned', False)
        
        content = "[bold #00cc66]🎓 Evil Twin Protection[/]\n\n"
        
        # Lesson 1: What are Evil Twins?
        content += "[#00aa55]What is an Evil Twin?[/]\n"
        content += "[#008855]• Fake AP with same name as real one\n"
        content += "• Tricks devices into connecting\n"
        content += "• Attacker captures ALL your data\n"
        content += "• Very dangerous attack!\n\n"
        
        # Lesson 2: How to protect
        content += "[#00aa55]How to Protect Yourself:[/]\n"
        content += "[#008855]• Verify AP MAC address (BSSID)\n"
        content += "• Check signal strength\n"
        content += "• Use VPN on public WiFi\n"
        content += "• Prefer WPA3 networks\n"
        content += "• Forget network when leaving\n\n"
        
        # Lesson 3: Warning signs
        content += "[#00aa55]Warning Signs:[/]\n"
        content += "[#008855]• Duplicate network names\n"
        content += "• Sudden connection drop/reconnect\n"
        content += "• Unusually strong signal\n"
        content += "• Open network in secure area\n\n"
        
        # Current status
        if rogue_count > 0:
            content += f"[bold #ff0000]⚠️ ALERT![/]\n"
            content += f"[#ff6666]{rogue_count} rogue AP(s) detected!\n"
            content += "Do NOT connect to suspicious APs.\n"
            content += "Verify with network admin![/]\n\n"
        elif baseline_learned:
            content += "[bold #00cc66]✓ Status:[/]\n"
            content += "[#00aa55]No evil twins detected.\n"
            content += "Network appears legitimate.\n"
            content += "Stay vigilant![/]\n\n"
        else:
            content += "[#ffaa00]🔄 Learning baseline...[/]\n"
            content += "[#ffcc66]Please wait 60 seconds.\n"
            content += "Detector is memorizing\n"
            content += "legitimate APs.[/]\n\n"
        
        # Final tip
        content += "[bold #00cc66]Remember:[/]\n"
        content += "[#00aa55]Evil twins are the most dangerous\n"
        content += "WiFi attack. Always verify APs![/]"
        
        widget.update(content)
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("Rogue AP data refreshed", severity="information")
    
    def action_show_baseline(self) -> None:
        """Show baseline APs."""
        try:
            data = self.app.get_plugin_data('rogue_ap')
            baseline = data.get('baseline_aps', {})
            
            if baseline:
                msg = "Baseline APs:\n" + "\n".join([f"{ssid}: {bssid}" for ssid, bssid in baseline.items()])
                self.app.notify(msg, severity="information", timeout=5)
            else:
                self.app.notify("Baseline not learned yet", severity="warning")
        except Exception as e:
            self.app.notify(f"Error: {e}", severity="error")
    
    def action_switch_consolidated(self) -> None:
        """Switch to consolidated dashboard."""
        self.app.action_switch_screen('consolidated')
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.action_quit()
