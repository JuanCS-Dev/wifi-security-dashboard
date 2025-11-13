"""
HTTP Data Sniffer Dashboard

⚠️ ETHICAL WARNING: Educational tool demonstrating HTTP security risks.
Only use on networks you own with explicit permission.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import datetime


class HTTPSnifferDashboard(Screen):
    """
    HTTP Data Sniffer Dashboard.
    
    ⚠️ CRITICAL ETHICAL REQUIREMENTS:
    - Only use on YOUR OWN network
    - Obtain WRITTEN PERMISSION
    - Educational demonstration ONLY
    - Never capture real user data
    
    Shows:
    - Ethical warnings (prominent)
    - HTTP requests captured
    - Credential exposure (redacted)
    - HTTPS vs HTTP statistics
    - Educational security lessons
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("w", "show_warnings", "Ethical Warnings"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    HTTPSnifferDashboard {
        background: #000000;
    }
    
    #ethical-warning {
        background: #330000;
        color: #ff0000;
        height: auto; min-height: 5;
        border: heavy #ff0000;
        padding: 1;
        margin: 0 1 1 1;
    }
    
    #http-stats-header {
        background: #000000;
        color: #00cc66;
        height: auto; min-height: 4;
        border: round #00aa55;
        padding: 1;
        margin: 0 1 1 1;
    }
    
    #http-requests-table {
        height: auto; min-height: 10;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 1 1 1;
    }
    
    #credentials-section {
        height: auto; min-height: 8;
        margin: 0 1 1 1;
    }
    
    #credentials-table {
        width: 60%;
        border: round #ff0000;
        background: #110000;
        color: #ff6666;
    }
    
    #educational-panel {
        width: 40%;
        border: round #00aa55;
        background: #000000;
        color: #00cc66;
        padding: 1;
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
        """Compose HTTP sniffer dashboard layout."""
        yield Header()
        
        with Vertical():
            # ETHICAL WARNING - Most prominent
            yield Static("", id="ethical-warning")
            
            # Stats header
            yield Static("", id="http-stats-header")
            
            # HTTP requests table
            yield DataTable(id="http-requests-table")
            
            # Bottom section: Credentials + Educational
            with Horizontal(id="credentials-section"):
                yield DataTable(id="credentials-table")
                yield ScrollableContainer(Static("", id="educational-panel"))
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup tables and start refresh timer."""
        # Configure requests table
        requests_table = self.query_one("#http-requests-table", DataTable)
        requests_table.add_columns("Time", "Source IP", "Method", "Host", "Path", "User-Agent")
        requests_table.cursor_type = "row"
        
        # Configure credentials table
        creds_table = self.query_one("#credentials-table", DataTable)
        creds_table.add_columns("Time", "Source", "Type", "Username", "URL")
        creds_table.cursor_type = "row"
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update HTTP sniffer data from plugin."""
        try:
            data = self.app.get_plugin_data('http_sniffer')
            
            if not data:
                return
            
            self._update_ethical_warning(data)
            self._update_stats_header(data)
            self._update_requests_table(data)
            self._update_credentials_table(data)
            self._update_educational_panel(data)
            
        except Exception as e:
            self.app.notify(f"HTTP sniffer refresh error: {e}", severity="error")
    
    def _update_ethical_warning(self, data: dict) -> None:
        """Update ethical warning banner."""
        warning = self.query_one("#ethical-warning", Static)
        
        consent = data.get('ethical_consent', False)
        
        if not consent:
            content = """[bold #ff0000 blink]⚠️  ETHICAL CONSENT REQUIRED  ⚠️[/]

[#ff6666]This tool demonstrates HTTP security vulnerabilities.
ONLY use on networks you OWN with WRITTEN PERMISSION.
Unauthorized use is ILLEGAL and UNETHICAL.[/]

[#ffaa00]To enable: Set ethical_consent=True in config[/]"""
        else:
            content = """[bold #ffaa00]⚠️  EDUCATIONAL USE ONLY  ⚠️[/]

[#ffcc66]Remember: This is for YOUR network only.
Demonstrates why HTTPS is critical for security.
Never capture real user credentials.[/]

[#00cc66]Consent given - Monitoring active[/]"""
        
        warning.update(content)
    
    def _update_stats_header(self, data: dict) -> None:
        """Update statistics header."""
        header = self.query_one("#http-stats-header", Static)
        
        stats = data.get('stats', {})
        monitoring = data.get('monitoring', False)
        warning_msg = data.get('educational_warning', '')
        
        status_color = "#00cc66" if monitoring else "#ff0000"
        status_text = "ACTIVE" if monitoring else "STOPPED"
        
        # Color warning based on severity
        if "CRITICAL" in warning_msg:
            warning_color = "#ff0000"
        elif "WARNING" in warning_msg:
            warning_color = "#ffaa00"
        else:
            warning_color = "#00cc66"
        
        content = f"""[bold #00cc66]HTTP DATA SNIFFER[/]
[#00aa55]Status:[/] [{status_color}]{status_text}[/]  [#00aa55]HTTP Requests:[/] [#00cc66]{stats.get('http_requests', 0)}[/]  [#00aa55]Credentials Found:[/] [#ff6666]{stats.get('credentials_found', 0)}[/]  [#00aa55]Unique Hosts:[/] [#00cc66]{stats.get('unique_hosts', 0)}[/]
[{warning_color}]{warning_msg}[/]"""
        
        header.update(content)
    
    def _update_requests_table(self, data: dict) -> None:
        """Update HTTP requests table."""
        table = self.query_one("#http-requests-table", DataTable)
        
        # Get recent requests
        requests = data.get('recent_requests', [])
        
        # Clear and repopulate
        table.clear()
        
        for request in reversed(requests):  # Most recent first
            timestamp = request.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            
            source_ip = request.get('source_ip', 'N/A')
            method = request.get('method', 'N/A')
            host = request.get('host', 'N/A')
            path = request.get('path', '/')
            user_agent = request.get('user_agent', '-')
            
            # Truncate long values
            if len(host) > 25:
                host = host[:22] + "..."
            if len(path) > 30:
                path = path[:27] + "..."
            if user_agent and len(user_agent) > 35:
                user_agent = user_agent[:32] + "..."
            
            # Color method
            if method == 'POST':
                method_display = f"[#ffaa00]{method}[/]"
            else:
                method_display = method
            
            table.add_row(
                time_str,
                source_ip,
                method,
                host,
                path,
                user_agent or '-'
            )
    
    def _update_credentials_table(self, data: dict) -> None:
        """Update credentials capture table."""
        table = self.query_one("#credentials-table", DataTable)
        
        # Get credential captures
        credentials = data.get('credential_captures', [])
        
        # Clear and repopulate
        table.clear()
        
        if not credentials:
            table.add_row("No credentials", "captured", "yet", "-", "-")
            return
        
        for cred in reversed(credentials[-10:]):  # Last 10, most recent first
            timestamp = cred.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            
            source = cred.get('source_ip', 'N/A')
            cred_type = cred.get('credential_type', 'unknown')
            username = cred.get('username', '-')
            url = cred.get('url', 'N/A')
            
            # Truncate URL
            if len(url) > 40:
                url = url[:37] + "..."
            
            # Redact username partially for privacy
            if username and username != '-':
                if len(username) > 3:
                    username = username[:2] + "***"
            
            table.add_row(
                time_str,
                source,
                cred_type.upper(),
                username,
                url
            )
    
    def _update_educational_panel(self, data: dict) -> None:
        """Update educational information panel."""
        container = self.query_one("#educational-panel", Static)
        
        stats = data.get('stats', {})
        creds_found = stats.get('credentials_found', 0)
        http_requests = stats.get('http_requests', 0)
        
        content = "[bold #00cc66]🎓 Educational Insights[/]\n\n"
        
        # Lesson 1: HTTP vs HTTPS
        content += "[#00aa55]HTTP vs HTTPS:[/]\n"
        content += "[#008855]• HTTP = Plain text (anyone can read)\n"
        content += "• HTTPS = Encrypted (secure)\n"
        content += "• Always use HTTPS for sensitive data\n\n"
        
        # Lesson 2: What attackers see
        content += "[#00aa55]What Attackers Can See:[/]\n"
        content += "[#008855]• Websites you visit\n"
        content += "• Login credentials\n"
        content += "• Personal information\n"
        content += "• API keys and tokens\n\n"
        
        # Lesson 3: Protection
        content += "[#00aa55]How to Protect Yourself:[/]\n"
        content += "[#008855]• Use HTTPS everywhere\n"
        content += "• Enable HTTPS-Only mode in browser\n"
        content += "• Use VPN on public WiFi\n"
        content += "• Check for lock icon in address bar\n\n"
        
        # Current findings
        if creds_found > 0:
            content += f"[bold #ff0000]⚠️ ALERT:[/] [#ff6666]{creds_found} credential(s) captured!\n"
            content += "This demonstrates the CRITICAL\n"
            content += "importance of HTTPS encryption![/]\n\n"
        
        if http_requests > 0:
            content += f"[#ffaa00]📊 Analysis:[/]\n"
            content += f"[#ffcc66]{http_requests} HTTP requests intercepted.\n"
            content += "All this data is visible to attackers\n"
            content += "on the same network.[/]\n\n"
        
        # Final message
        content += "[bold #00cc66]Remember:[/]\n"
        content += "[#00aa55]This tool shows WHY encryption matters.\n"
        content += "Always encrypt sensitive communications![/]"
        
        container.update(content)
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("HTTP sniffer data refreshed", severity="information")
    
    def action_show_warnings(self) -> None:
        """Show ethical warnings."""
        self.app.notify(
            "⚠️ ETHICAL USE ONLY: Only capture traffic on YOUR network with permission!",
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
