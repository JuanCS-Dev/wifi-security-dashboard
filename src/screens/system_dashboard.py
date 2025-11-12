"""
SystemDashboard - Dashboard detalhado de métricas do sistema

Dashboard focado exclusivamente em métricas de sistema: CPU, RAM, Disk, Load, Uptime.
Fornece visualização detalhada com histórico e estatísticas.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from collections import deque
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive


class DetailedCPUWidget(Static):
    """Detailed CPU widget with per-core breakdown."""
    cpu_percent = reactive(0.0)
    cpu_count = reactive(0)
    cpu_per_core = reactive([])

    def watch_cpu_percent(self, new_value: float) -> None:
        self._refresh_display()

    def watch_cpu_per_core(self, new_value: list) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        # Clean status indicator
        if self.cpu_percent < 70:
            status_icon = "[green]●[/green]"
        elif self.cpu_percent < 90:
            status_icon = "[yellow]●[/yellow]"
        else:
            status_icon = "[red]●[/red]"

        # Overall bar (clean, 40 chars)
        bar_length = 40
        filled = int(bar_length * self.cpu_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        output = (
            f"[bold white]💻 CPU USAGE[/bold white]\n\n"
            f"[bold]{self.cpu_percent:.1f}%[/bold] {status_icon}\n"
            f"{bar}\n"
            f"[dim]Cores: {self.cpu_count}[/dim]\n\n"
        )

        # Per-core breakdown (clean)
        if self.cpu_per_core:
            output += "\n[bold]Per-Core:[/bold]\n"
            for i, usage in enumerate(self.cpu_per_core[:8]):  # Max 8 cores
                mini_bar_len = 15
                mini_filled = int(mini_bar_len * usage / 100)
                mini_bar = "█" * mini_filled + "░" * (mini_bar_len - mini_filled)

                if usage < 70:
                    dot = "[green]●[/green]"
                elif usage < 90:
                    dot = "[yellow]●[/yellow]"
                else:
                    dot = "[red]●[/red]"

                output += f"  [dim]Core {i}:[/dim] {mini_bar} [bold]{usage:.0f}%[/bold] {dot}\n"

        self.update(output)


class DetailedRAMWidget(Static):
    """Detailed RAM widget with usage breakdown."""
    memory_percent = reactive(0.0)
    memory_used_mb = reactive(0.0)
    memory_total_mb = reactive(0.0)

    def watch_memory_percent(self, new_value: float) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        # Clean status
        if self.memory_percent < 70:
            status_icon = "[green]●[/green]"
        elif self.memory_percent < 90:
            status_icon = "[yellow]●[/yellow]"
        else:
            status_icon = "[red]●[/red]"

        bar_length = 40
        filled = int(bar_length * self.memory_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        used_gb = self.memory_used_mb / 1024
        total_gb = self.memory_total_mb / 1024
        free_gb = total_gb - used_gb

        self.update(
            f"[bold white]📊 MEMORY[/bold white]\n\n"
            f"[bold]{used_gb:.1f} / {total_gb:.1f} GB[/bold] {status_icon}\n"
            f"{bar}\n"
            f"[dim]{self.memory_percent:.1f}% Used[/dim]\n\n"
            f"[dim]Free: {free_gb:.1f} GB[/dim]"
        )


class DetailedDiskWidget(Static):
    """Detailed Disk widget with usage breakdown."""
    disk_percent = reactive(0.0)
    disk_used_gb = reactive(0.0)
    disk_total_gb = reactive(0.0)

    def watch_disk_percent(self, new_value: float) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        if self.disk_percent < 70:
            color = "cyan"
            status = "GOOD"
        elif self.disk_percent < 90:
            color = "yellow"
            status = "WARNING"
        else:
            color = "red"
            status = "CRITICAL"

        bar_length = 40
        filled = int(bar_length * self.disk_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        free_gb = self.disk_total_gb - self.disk_used_gb

        self.update(
            f"[bold white]💾 DISK USAGE - DETAILED[/bold white]\n\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{self.disk_percent:.1f}%[/bold {color}] [{color}]{status}[/{color}]\n\n"
            f"[bold]Disk Breakdown:[/bold]\n"
            f"[green]Used:[/green]  {self.disk_used_gb:.1f} GB\n"
            f"[cyan]Free:[/cyan]   {free_gb:.1f} GB\n"
            f"[dim]Total:[/dim]  {self.disk_total_gb:.1f} GB"
        )


class SystemInfoWidget(Static):
    """System information widget (uptime, load average)."""
    uptime_seconds = reactive(0)
    load_avg_1m = reactive(0.0)
    load_avg_5m = reactive(0.0)
    load_avg_15m = reactive(0.0)

    def watch_uptime_seconds(self, new_value: int) -> None:
        self._refresh_display()

    def watch_load_avg_1m(self, new_value: float) -> None:
        self._refresh_display()

    def _refresh_display(self) -> None:
        # Convert uptime to human readable
        days = self.uptime_seconds // 86400
        hours = (self.uptime_seconds % 86400) // 3600
        minutes = (self.uptime_seconds % 3600) // 60

        uptime_str = f"{days}d {hours}h {minutes}m"

        self.update(
            f"[bold white]⏱️  SYSTEM INFO[/bold white]\n\n"
            f"[bold]Uptime:[/bold] [green]{uptime_str}[/green]\n\n"
            f"[bold]Load Average:[/bold]\n"
            f"[cyan]1 min:[/cyan]  {self.load_avg_1m:.2f}\n"
            f"[cyan]5 min:[/cyan]  {self.load_avg_5m:.2f}\n"
            f"[cyan]15 min:[/cyan] {self.load_avg_15m:.2f}"
        )


class SystemDashboard(Screen):
    """
    Dashboard detalhado de sistema.

    Mostra métricas de sistema com detalhamento:
    - CPU (overall + per-core)
    - RAM (used/free breakdown)
    - Disk (used/free breakdown)
    - System info (uptime, load average)
    """

    CSS = """
    SystemDashboard {
        background: $surface;
    }

    #system-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #left-column {
        width: 1fr;
        height: 100%;
    }

    #right-column {
        width: 1fr;
        height: 100%;
    }

    /* Unified terminal-native borders */
    DetailedCPUWidget, DetailedRAMWidget, DetailedDiskWidget, SystemInfoWidget {
        border: solid #00aa00;
        padding: 0 1;
        margin: 0 1 1 1;
        background: $panel;
        height: 1fr;
    }
    """

    BINDINGS = [
        ("0", "switch_screen('consolidated')", "Consolidated"),
        ("1", "switch_screen('system')", "System"),
        ("2", "switch_screen('network')", "Network"),
        ("3", "switch_screen('wifi')", "WiFi"),
        ("4", "switch_screen('packets')", "Packets"),
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the system dashboard layout."""
        yield Header(show_clock=True)

        with Horizontal(id="system-container"):
            with Vertical(id="left-column"):
                yield DetailedCPUWidget(id="cpu-detailed")
                yield SystemInfoWidget(id="system-info")

            with Vertical(id="right-column"):
                yield DetailedRAMWidget(id="ram-detailed")
                yield DetailedDiskWidget(id="disk-detailed")

        yield Footer()

    def update_metrics(self, system_data):
        """
        Update all widgets with fresh system data.

        Args:
            system_data: Dict from SystemPlugin
        """
        # Update CPU
        cpu_widget = self.query_one("#cpu-detailed", DetailedCPUWidget)
        cpu_widget.cpu_percent = system_data.get('cpu_percent', 0.0)
        cpu_widget.cpu_count = system_data.get('cpu_count', 0)
        cpu_widget.cpu_per_core = system_data.get('cpu_percent_per_core', [])

        # Update RAM
        ram_widget = self.query_one("#ram-detailed", DetailedRAMWidget)
        ram_widget.memory_percent = system_data.get('memory_percent', 0.0)
        ram_widget.memory_used_mb = system_data.get('memory_used_mb', 0.0)
        ram_widget.memory_total_mb = system_data.get('memory_total_mb', 0.0)

        # Update Disk
        disk_widget = self.query_one("#disk-detailed", DetailedDiskWidget)
        disk_widget.disk_percent = system_data.get('disk_percent', 0.0)
        disk_widget.disk_used_gb = system_data.get('disk_used_gb', 0.0)
        disk_widget.disk_total_gb = system_data.get('disk_total_gb', 0.0)

        # Update System Info
        info_widget = self.query_one("#system-info", SystemInfoWidget)
        info_widget.uptime_seconds = system_data.get('uptime_seconds', 0)
        info_widget.load_avg_1m = system_data.get('load_avg_1m', 0.0)
        info_widget.load_avg_5m = system_data.get('load_avg_5m', 0.0)
        info_widget.load_avg_15m = system_data.get('load_avg_15m', 0.0)
