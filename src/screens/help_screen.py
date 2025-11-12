"""
Help Screen Modal - Keyboard shortcuts and usage guide

Educational overlay showing all available commands and features.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Static, Button


class HelpScreen(ModalScreen):
    """
    Help overlay modal showing keyboard shortcuts and usage guide.

    Features:
    - Keyboard shortcuts reference
    - Widget descriptions
    - Educational mode explanation
    - Dismissible with ESC or Close button
    """

    CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        border: thick #00ff00;
        background: #2d2d2d;
        padding: 1 2;
    }

    #help-content {
        height: auto;
        width: 100%;
    }

    #help-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1 0;
    }

    #shortcuts {
        border: solid #00aa00;
        padding: 1;
        margin: 1 0;
    }

    #widgets-info {
        border: solid #00aa00;
        padding: 1;
        margin: 1 0;
    }
    
    #educational-info {
        border: solid #00aa00;
        padding: 1;
        margin: 1 0;
    }

    Button {
        width: 20;
        margin: 1 auto;
    }
    """

    BINDINGS = [
        ("escape", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the help modal layout."""
        with Container(id="help-dialog"):
            with Vertical(id="help-content"):
                yield Static(
                    "🎓 WiFi Security Dashboard - Help",
                    id="help-title"
                )

                yield Static(
                    "[bold cyan]⌨️  KEYBOARD SHORTCUTS[/bold cyan]\n\n"
                    "[bold yellow]q[/bold yellow]        Quit dashboard\n"
                    "[bold yellow]0-4[/bold yellow]      Switch dashboards\n"
                    "[bold yellow]h / ?[/bold yellow]    Show this help\n"
                    "[bold yellow]ESC[/bold yellow]      Close modals\n\n"
                    "[dim]Navigation:[/dim]\n"
                    "[yellow]0[/yellow] Consolidated • [yellow]1[/yellow] System • [yellow]2[/yellow] Network\n"
                    "[yellow]3[/yellow] WiFi • [yellow]4[/yellow] Packets",
                    id="shortcuts"
                )

                yield Static(
                    "[bold green]📊 DASHBOARD GUIDE[/bold green]\n\n"
                    "[bold cyan]0 • Consolidated[/bold cyan]\n"
                    "[dim]Overview of all metrics\n\n"
                    "[bold cyan]1 • System[/bold cyan]\n"
                    "[dim]CPU, RAM, Disk monitoring\n\n"
                    "[bold cyan]2 • Network[/bold cyan]\n"
                    "[dim]Bandwidth & connections\n\n"
                    "[bold cyan]3 • WiFi[/bold cyan]\n"
                    "[dim]Signal, security, speed\n\n"
                    "[bold cyan]4 • Packets[/bold cyan]\n"
                    "[dim]Protocol analysis & tips\n\n"
                    "[bold]Status Indicators:[/bold]\n"
                    "[green]●[/green] Normal  [yellow]●[/yellow] High  [red]●[/red] Critical",
                    id="widgets-info"
                )

                yield Static(
                    "[bold yellow]🎓 SECURITY GUIDE[/bold yellow]\n\n"
                    "[green]🔒 HTTPS/TLS[/green] [green]●[/green]\n"
                    "[dim]Encrypted & safe for passwords\n\n"
                    "[red]⚠️  HTTP[/red] [red]●[/red]\n"
                    "[dim]Plain text - avoid for sensitive data!\n\n"
                    "[cyan]🌐 DNS[/cyan] [cyan]●[/cyan]\n"
                    "[dim]Translates domain names to IPs\n\n"
                    "[green]🔑 SSH[/green] [green]●[/green]\n"
                    "[dim]Secure remote server access\n\n"
                    "[bold]Learn by watching:[/bold]\n"
                    "[dim]See real protocols in Packets dashboard (press 4)[/dim]",
                    id="educational-info"
                )

                yield Button("Close (ESC)", variant="primary", id="close-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close-button":
            self.dismiss()

    def action_dismiss(self) -> None:
        """Close the help screen."""
        self.dismiss()
