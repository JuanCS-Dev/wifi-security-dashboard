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
        border: thick $accent;
        background: $surface;
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
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }

    #widgets-info {
        border: solid $secondary;
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
                    "[bold bright_cyan]📋 KEYBOARD SHORTCUTS[/bold bright_cyan]\n\n"
                    "[yellow]q[/yellow]       - Quit dashboard\n"
                    "[yellow]p[/yellow]       - Pause/Resume updates\n"
                    "[yellow]h or ?[/yellow]  - Show this help screen\n"
                    "[yellow]r[/yellow]       - Reset/clear all charts and tables\n"
                    "[yellow]e[/yellow]       - Toggle educational mode\n"
                    "[yellow]ESC[/yellow]     - Close modal dialogs\n",
                    id="shortcuts"
                )

                yield Static(
                    "[bold bright_green]📊 WIDGETS[/bold bright_green]\n\n"
                    "[cyan]💻 CPU Widget[/cyan]      - Shows CPU usage percentage\n"
                    "[cyan]📊 RAM Widget[/cyan]      - Shows memory usage (GB)\n"
                    "[cyan]💽 Disk Widget[/cyan]     - Shows disk usage\n"
                    "[cyan]📡 WiFi Widget[/cyan]     - Shows WiFi signal strength\n"
                    "[cyan]📈 Network Chart[/cyan]   - RX/TX bandwidth over time\n"
                    "[cyan]📦 Packet Table[/cyan]    - Recent network packets\n\n"
                    "[dim]Color codes: [green]GREEN[/green]=Normal, [yellow]YELLOW[/yellow]=High, [red]RED[/red]=Critical[/dim]",
                    id="widgets-info"
                )

                yield Static(
                    "[bold bright_yellow]🎓 EDUCATIONAL MODE[/bold bright_yellow]\n\n"
                    "When enabled, the dashboard shows educational flags:\n"
                    "[green]🔒 HTTPS[/green]     - Secure encrypted connection\n"
                    "[yellow]⚠️ HTTP[/yellow]      - Insecure connection (warning!)\n"
                    "[blue]🌐 DNS[/blue]       - Domain name system query\n\n"
                    "[dim]This mode helps you learn about network security![/dim]",
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
