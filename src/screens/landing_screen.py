"""
LandingScreen - Tela inicial com banner JUAN e menu interativo

Landing page estilo retro com banner ASCII colorido e menu de navegação.
Permite selecionar dashboard ou modo de operação.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Center
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align


class BannerWidget(Static):
    """Widget com banner JUAN colorido em ASCII art."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._render_banner()

    def _render_banner(self):
        """Renderiza banner JUAN - Matrix style (verde em escala)."""
        # Banner JUAN com blocos preenchidos
        banner_lines = [
            "     ██╗██╗   ██╗ █████╗ ███╗   ██╗",
            "     ██║██║   ██║██╔══██╗████╗  ██║",
            "     ██║██║   ██║███████║██╔██╗ ██║",
            "██   ██║██║   ██║██╔══██║██║╚██╗██║",
            "╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║",
            " ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝",
        ]

        # Matrix style: escala de verdes (bright → dim)
        # Usando RGB direto para controle preciso
        green_scale = [
            '#00ff00',  # Bright green (top)
            '#00ee00',  
            '#00dd00',  
            '#00cc00',  
            '#00bb00',  
            '#00aa00',  # Dim green (bottom)
        ]

        banner_text = Text()
        for i, line in enumerate(banner_lines):
            banner_text.append(line + "\n", style=green_scale[i])

        # Subtítulo em verde matrix
        banner_text.append("\n")
        banner_text.append("  WiFi Security Education Dashboard v3.0\n", style="bold #00ff00")
        banner_text.append("  🎓 Educational Network Monitoring Tool\n", style="#00aa00")
        banner_text.append("  Soli Deo Gloria ✝️\n", style="italic #00aa00")

        self.update(Align.center(banner_text))


class MenuWidget(Static):
    """Widget com menu interativo de dashboards."""

    current_mode = reactive("mock")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._render_menu()

    def watch_current_mode(self, new_value: str):
        """Atualiza display quando modo muda."""
        self._render_menu()

    def _render_menu(self):
        """Renderiza menu de opções."""
        mode_color = "green" if self.current_mode == "mock" else "yellow"
        mode_icon = "🎓" if self.current_mode == "mock" else "⚡"
        mode_label = "MOCK MODE (Educational)" if self.current_mode == "mock" else "REAL MODE (Live Data)"

        menu_text = Text()

        # Modo atual
        menu_text.append("━" * 60 + "\n", style="dim")
        menu_text.append(f"  Current Mode: ", style="bold")
        menu_text.append(f"{mode_icon} {mode_label}\n", style=f"bold {mode_color}")
        menu_text.append("━" * 60 + "\n\n", style="dim")

        # Dashboards
        menu_text.append("  📊 DASHBOARDS:\n\n", style="bold cyan")
        menu_text.append("    [0]  ", style="white")
        menu_text.append("Consolidated Overview", style="cyan")
        menu_text.append("  (All metrics at once)\n", style="dim")

        menu_text.append("    [1]  ", style="white")
        menu_text.append("System Dashboard", style="green")
        menu_text.append("      (CPU, RAM, Disk details)\n", style="dim")

        menu_text.append("    [2]  ", style="white")
        menu_text.append("Network Dashboard", style="yellow")
        menu_text.append("     (Bandwidth + Stats)\n", style="dim")

        menu_text.append("    [3]  ", style="white")
        menu_text.append("WiFi Dashboard", style="magenta")
        menu_text.append("        (Signal + Security)\n", style="dim")

        menu_text.append("    [4]  ", style="white")
        menu_text.append("Packets Dashboard", style="red")
        menu_text.append("     (Wireshark-style)\n\n", style="dim")

        # Opções
        menu_text.append("  ⚙️  OPTIONS:\n\n", style="bold yellow")
        menu_text.append("    [m]  ", style="white")
        menu_text.append("Toggle Mock/Real Mode\n", style="cyan")

        menu_text.append("    [h]  ", style="white")
        menu_text.append("Help Screen\n", style="cyan")

        menu_text.append("    [q]  ", style="white")
        menu_text.append("Quit\n\n", style="red")

        menu_text.append("━" * 60 + "\n", style="dim")
        menu_text.append("  Press any number key to launch dashboard\n", style="italic dim")
        menu_text.append("━" * 60, style="dim")

        self.update(Align.center(menu_text))


class LandingScreen(Screen):
    """
    Landing page com banner JUAN e menu interativo.

    Features:
    - Banner ASCII colorido (gradient verde → amarelo → azul)
    - Menu interativo com todos os dashboards
    - Indicador de modo atual (Mock/Real)
    - Navegação por teclas 0-4
    - Toggle de modo com 'm'
    """

    CSS = """
    LandingScreen {
        background: $surface;
        align: center middle;
    }

    #landing-container {
        width: 95%;
        min-width: 120;
        max-width: 180;
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 2;
    }

    BannerWidget {
        height: auto;
        margin: 0 0 2 0;
    }

    MenuWidget {
        height: auto;
        margin: 1 0;
    }

    #footer-info {
        height: 3;
        margin: 2 0 0 0;
        border-top: solid $accent;
        padding-top: 1;
    }
    """

    BINDINGS = [
        ("0", "launch_dashboard('consolidated')", "Consolidated"),
        ("1", "launch_dashboard('system')", "System"),
        ("2", "launch_dashboard('network')", "Network"),
        ("3", "launch_dashboard('wifi')", "WiFi"),
        ("4", "launch_dashboard('packets')", "Packets"),
        ("m", "toggle_mode", "Toggle Mode"),
        ("h", "show_help", "Help"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, current_mode: str = "mock", **kwargs):
        super().__init__(**kwargs)
        self.current_mode = current_mode

    def compose(self) -> ComposeResult:
        """Compose landing page layout."""
        with Container(id="landing-container"):
            yield BannerWidget(id="banner")
            yield MenuWidget(id="menu")
            yield Static(
                "[dim italic]Tip: Press numbers 0-4 to launch dashboards, 'm' to toggle mode, 'q' to quit[/dim italic]",
                id="footer-info"
            )

    def on_mount(self) -> None:
        """Update menu with current mode."""
        menu_widget = self.query_one("#menu", MenuWidget)
        menu_widget.current_mode = self.current_mode

    def action_launch_dashboard(self, dashboard_name: str) -> None:
        """
        Launch specific dashboard.

        Args:
            dashboard_name: Name of dashboard to launch
        """
        # Notify parent app to switch screen
        self.app.action_switch_screen(dashboard_name)

    def action_toggle_mode(self) -> None:
        """Toggle between mock and real mode."""
        # Toggle mode in app
        self.app.mock_mode = not self.app.mock_mode
        new_mode = "mock" if self.app.mock_mode else "real"

        # Update menu display
        menu_widget = self.query_one("#menu", MenuWidget)
        menu_widget.current_mode = new_mode

        # Reinitialize plugins with new mode
        self.app._initialize_plugins()

        # Notify user
        mode_label = "MOCK (Educational)" if self.app.mock_mode else "REAL (Live Data)"
        self.app.notify(
            f"Switched to {mode_label}",
            title="🔄 Mode Changed",
            severity="information"
        )

    def action_show_help(self) -> None:
        """Show help screen."""
        self.app.push_screen("help")

    def action_quit(self) -> None:
        """Quit application."""
        self.app.action_quit()
