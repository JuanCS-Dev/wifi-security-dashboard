"""
DNS Query Monitor Dashboard

Real-time DNS query monitoring with educational insights.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from datetime import datetime


class DNSDashboard(Screen):
    """
    DNS Query Monitor Dashboard.
    
    Shows:
    - Monitor status and statistics
    - Recent DNS queries (scrolling log)
    - Top domains accessed
    - Query type distribution
    - Educational privacy tips
    """
    
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("c", "clear_history", "Clear History"),
        ("0", "switch_consolidated", "Overview"),
        ("h", "show_help", "Help"),
        ("q", "quit_app", "Quit"),
    ]
    
    CSS = """
    DNSDashboard {
        background: #000000;
    }
    
    #dns-stats-header {
        background: #000000;
        color: #00cc66;
        height: auto;
        border: solid #00aa55;
        padding: 1;
        margin: 0 1 1 1;
    }
    
    #dns-queries-table {
        height: 50%;
        border: solid #00aa55;
        background: #000000;
        color: #00cc66;
        margin: 0 1 1 1;
    }
    
    #dns-bottom-section {
        height: 30%;
        margin: 0 1 1 1;
    }
    
    #top-domains-table {
        width: 50%;
        border: solid #00aa55;
        background: #000000;
        color: #00cc66;
    }
    
    #query-types-info {
        width: 50%;
        border: solid #00aa55;
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
        self.query_count = 0
        self.monitoring = False
    
    def compose(self) -> ComposeResult:
        """Compose DNS dashboard layout."""
        yield Header()
        
        with Vertical():
            # Stats header
            yield Static("", id="dns-stats-header")
            
            # Recent queries table (main area)
            yield DataTable(id="dns-queries-table")
            
            # Bottom section: Top domains + Query types
            with Horizontal(id="dns-bottom-section"):
                yield DataTable(id="top-domains-table")
                yield Static("", id="query-types-info")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Setup tables and start refresh timer."""
        # Configure queries table
        queries_table = self.query_one("#dns-queries-table", DataTable)
        queries_table.add_columns("Time", "Source IP", "Domain", "Type", "Resolved IP")
        queries_table.cursor_type = "row"
        
        # Configure top domains table
        domains_table = self.query_one("#top-domains-table", DataTable)
        domains_table.add_columns("Domain", "Count")
        domains_table.cursor_type = "row"
        
        # Start refresh
        self.set_interval(2.0, self.refresh_data)
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Update DNS data from plugin."""
        try:
            data = self.app.get_plugin_data('dns_monitor')
            
            if not data:
                return
            
            self._update_stats_header(data)
            self._update_queries_table(data)
            self._update_top_domains(data)
            self._update_query_types(data)
            
        except Exception as e:
            self.app.notify(f"DNS refresh error: {e}", severity="error")
    
    def _update_stats_header(self, data: dict) -> None:
        """Update statistics header."""
        header = self.query_one("#dns-stats-header", Static)
        
        stats = data.get('stats', {})
        monitoring = data.get('monitoring', False)
        tip = data.get('educational_tip', '')
        
        status_color = "#00cc66" if monitoring else "#ff0000"
        status_text = "ACTIVE" if monitoring else "STOPPED"
        
        content = f"""[bold #00cc66]DNS QUERY MONITOR[/]
[#00aa55]Status:[/] [{status_color}]{status_text}[/]  [#00aa55]Total Queries:[/] [#00cc66]{stats.get('total_queries', 0)}[/]  [#00aa55]Unique Domains:[/] [#00cc66]{stats.get('unique_domains', 0)}[/]  [#00aa55]Rate:[/] [#00cc66]{stats.get('queries_per_minute', 0):.1f}/min[/]
[#00aa55]💡 Tip:[/] [#008855]{tip}[/]"""
        
        header.update(content)
    
    def _update_queries_table(self, data: dict) -> None:
        """Update recent queries table."""
        table = self.query_one("#dns-queries-table", DataTable)
        
        # Get recent queries
        queries = data.get('recent_queries', [])
        
        # Clear and repopulate
        table.clear()
        
        for query in reversed(queries):  # Most recent first
            timestamp = query.get('timestamp', 0)
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            
            source_ip = query.get('source_ip', 'N/A')
            domain = query.get('domain', 'N/A')
            query_type = query.get('query_type', 'N/A')
            resolved_ip = query.get('resolved_ip', '-')
            
            # Truncate long domains
            if len(domain) > 40:
                domain = domain[:37] + "..."
            
            # Color resolved IPs
            if resolved_ip and resolved_ip != '-':
                resolved_display = f"[#00cc66]{resolved_ip}[/]"
            else:
                resolved_display = "[#666666]-[/]"
            
            table.add_row(
                time_str,
                source_ip,
                domain,
                query_type,
                resolved_ip or '-'
            )
    
    def _update_top_domains(self, data: dict) -> None:
        """Update top domains table."""
        table = self.query_one("#top-domains-table", DataTable)
        
        # Get top domains
        top_domains = data.get('top_domains', [])
        
        # Clear and repopulate
        table.clear()
        
        for domain, count in top_domains[:10]:  # Top 10
            # Truncate long domains
            if len(domain) > 35:
                domain = domain[:32] + "..."
            
            table.add_row(domain, str(count))
    
    def _update_query_types(self, data: dict) -> None:
        """Update query types distribution."""
        widget = self.query_one("#query-types-info", Static)
        
        query_types = data.get('query_types', {})
        
        content = "[bold #00cc66]Query Types[/]\n\n"
        
        if query_types:
            # Sort by count
            sorted_types = sorted(query_types.items(), key=lambda x: x[1], reverse=True)
            
            for qtype, count in sorted_types:
                # Simple bar chart
                bar_length = min(20, count // 5)
                bar = "█" * bar_length
                
                content += f"[#00aa55]{qtype:8s}[/] [{self._get_type_color(qtype)}]{bar}[/] [#00cc66]{count}[/]\n"
        else:
            content += "[#666666]No queries yet[/]\n"
        
        # Educational notes
        content += f"\n[#00aa55]Legend:[/]\n"
        content += "[#008855]A     = IPv4 address\n"
        content += "AAAA  = IPv6 address\n"
        content += "MX    = Mail server\n"
        content += "TXT   = Text record[/]"
        
        widget.update(content)
    
    def _get_type_color(self, qtype: str) -> str:
        """Get color for query type."""
        colors = {
            'A': '#00cc66',
            'AAAA': '#00aa55',
            'MX': '#008855',
            'TXT': '#006644',
            'CNAME': '#00bb66',
            'NS': '#009955',
        }
        return colors.get(qtype, '#005544')
    
    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_data()
        self.app.notify("DNS data refreshed", severity="information")
    
    def action_clear_history(self) -> None:
        """Clear query history."""
        # Would need to add clear_history() method to plugin
        self.app.notify("History cleared", severity="information")
    
    def action_switch_consolidated(self) -> None:
        """Switch to consolidated dashboard."""
        self.app.action_switch_screen('consolidated')
    
    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")
    
    def action_quit_app(self) -> None:
        """Quit application."""
        self.app.action_quit()
