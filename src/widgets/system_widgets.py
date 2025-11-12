"""
System Widgets - Sampler Style
Professional CPU, RAM, Disk widgets inspired by sqshq/sampler

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.progress_bar import ProgressBar


class CPUWidget(Static):
    """CPU usage widget - Sampler style."""
    
    cpu_percent = reactive(0.0)
    cores = reactive([])
    
    def watch_cpu_percent(self, value: float):
        """Update display when CPU changes."""
        self.render_display()
    
    def watch_cores(self, value: list):
        """Update display when cores change."""
        self.render_display()
    
    def render_display(self):
        """Render CPU widget - Sampler style."""
        text = Text()
        
        # Title
        text.append("CPU\n", style="bold #00cc66")
        
        # Overall percentage with bar
        bar_length = 15
        filled = int((self.cpu_percent / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        text.append(f" {self.cpu_percent:5.1f}%  ", style="#00cc66")
        text.append(bar + "\n", style="#00aa55")
        
        # Core details (compact)
        if self.cores:
            text.append("\n", style="#00aa55")
            for i, core_percent in enumerate(self.cores[:4], 1):  # Max 4 cores
                text.append(f" Core {i}: ", style="dim #008855")
                text.append(f"{core_percent:4.0f}%\n", style="#00cc66")
        
        self.update(text)


class RAMWidget(Static):
    """RAM usage widget - Sampler style."""
    
    used_gb = reactive(0.0)
    total_gb = reactive(0.0)
    percent = reactive(0.0)
    
    def watch_percent(self, value: float):
        """Update display when RAM changes."""
        self.render_display()
    
    def render_display(self):
        """Render RAM widget - Sampler style."""
        text = Text()
        
        # Title
        text.append("RAM\n", style="bold #00cc66")
        
        # Usage with bar
        bar_length = 15
        filled = int((self.percent / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        text.append(f" {self.percent:5.1f}%  ", style="#00cc66")
        text.append(bar + "\n", style="#00aa55")
        
        # Details
        text.append(f"\n {self.used_gb:.1f} GB ", style="#00cc66")
        text.append("/ ", style="dim #008855")
        text.append(f"{self.total_gb:.1f} GB\n", style="#00aa55")
        
        self.update(text)


class DiskWidget(Static):
    """Disk usage widget - Sampler style."""
    
    used_gb = reactive(0.0)
    total_gb = reactive(0.0)
    percent = reactive(0.0)
    
    def watch_percent(self, value: float):
        """Update display when disk changes."""
        self.render_display()
    
    def render_display(self):
        """Render Disk widget - Sampler style."""
        text = Text()
        
        # Title
        text.append("DISK\n", style="bold #00cc66")
        
        # Usage with bar
        bar_length = 15
        filled = int((self.percent / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        text.append(f" {self.percent:5.1f}%  ", style="#00cc66")
        text.append(bar + "\n", style="#00aa55")
        
        # Details
        text.append(f"\n {self.used_gb:.0f} GB ", style="#00cc66")
        text.append("/ ", style="dim #008855")
        text.append(f"{self.total_gb:.0f} GB\n", style="#00aa55")
        
        self.update(text)


class NetworkStatsWidget(Static):
    """Network statistics widget - Sampler style."""
    
    upload_mbps = reactive(0.0)
    download_mbps = reactive(0.0)
    connections = reactive(0)
    
    def watch_upload_mbps(self, value: float):
        """Update display when network changes."""
        self.render_display()
    
    def watch_download_mbps(self, value: float):
        """Update display when network changes."""
        self.render_display()
    
    def render_display(self):
        """Render Network stats - Sampler style."""
        text = Text()
        
        # Title
        text.append("NETWORK\n", style="bold #00cc66")
        
        # Upload
        text.append("\n ↑ ", style="#00aa55")
        text.append(f"{self.upload_mbps:6.2f} MB/s", style="#00cc66")
        
        # Mini sparkline (simple)
        up_bar = self._make_mini_bar(self.upload_mbps, 10.0)
        text.append(f"  {up_bar}\n", style="#00aa55")
        
        # Download
        text.append(" ↓ ", style="#00aa55")
        text.append(f"{self.download_mbps:6.2f} MB/s", style="#00cc66")
        
        down_bar = self._make_mini_bar(self.download_mbps, 10.0)
        text.append(f"  {down_bar}\n", style="#00aa55")
        
        # Connections
        text.append(f"\n Connections: ", style="dim #008855")
        text.append(f"{self.connections}\n", style="#00cc66")
        
        self.update(text)
    
    def _make_mini_bar(self, value: float, max_value: float) -> str:
        """Create mini bar indicator."""
        bars = "▁▂▃▄▅▆▇█"
        index = int((value / max_value) * (len(bars) - 1))
        index = min(index, len(bars) - 1)
        return bars[index] * 3


class WiFiWidget(Static):
    """WiFi signal widget - Sampler style."""
    
    ssid = reactive("No WiFi")
    signal_dbm = reactive(-100)
    security = reactive("Unknown")
    
    def watch_ssid(self, value: str):
        """Update display when WiFi changes."""
        self.render_display()
    
    def watch_signal_dbm(self, value: int):
        """Update display when signal changes."""
        self.render_display()
    
    def render_display(self):
        """Render WiFi widget - Sampler style."""
        text = Text()
        
        # Title
        text.append("WIFI SIGNAL\n", style="bold #00cc66")
        
        # SSID
        text.append(f"\n {self.ssid}\n", style="#00cc66")
        
        # Signal strength
        signal_percent = self._dbm_to_percent(self.signal_dbm)
        bar_length = 10
        filled = int((signal_percent / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        text.append(f" {self.signal_dbm} dBm  ", style="#00aa55")
        text.append(bar + "\n", style="#00cc66")
        
        # Security
        text.append(f" {self.security}\n", style="dim #008855")
        
        self.update(text)
    
    def _dbm_to_percent(self, dbm: int) -> float:
        """Convert dBm to percentage."""
        if dbm >= -50:
            return 100.0
        elif dbm <= -100:
            return 0.0
        else:
            return ((dbm + 100) / 50) * 100


class PacketStatsWidget(Static):
    """Packet statistics widget - Sampler style."""
    
    total_packets = reactive(0)
    http_count = reactive(0)
    https_count = reactive(0)
    dns_count = reactive(0)
    
    def watch_total_packets(self, value: int):
        """Update display when packets change."""
        self.render_display()
    
    def render_display(self):
        """Render Packet stats - Sampler style."""
        text = Text()
        
        # Title
        text.append("PACKETS\n", style="bold #00cc66")
        
        # Total
        text.append(f"\n Total: ", style="dim #008855")
        text.append(f"{self.total_packets}\n", style="#00cc66")
        
        # Protocol breakdown
        text.append(f"\n HTTP:  ", style="dim #008855")
        text.append(f"{self.http_count}\n", style="#00aa55")
        
        text.append(f" HTTPS: ", style="dim #008855")
        text.append(f"{self.https_count}\n", style="#00cc66")
        
        text.append(f" DNS:   ", style="dim #008855")
        text.append(f"{self.dns_count}\n", style="#00aa55")
        
        self.update(text)
