"""
LandingScreen - Tela inicial com banner JUAN e menu interativo

Landing page estilo retro com banner ASCII colorido e menu de navegação.
Permite selecionar dashboard ou modo de operação.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
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
        """Renderiza banner minimalista e profissional."""
        banner_text = Text()
        
        # Header ultra simples - sem bordas
        banner_text.append("\n", style="#000000")
        banner_text.append("  WiFi Security Education Dashboard", style="bold #00cc66")
        banner_text.append("\n", style="#000000")
        banner_text.append("  v3.0.0", style="#00aa55")
        banner_text.append("\n\n", style="#000000")

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
        """Renderiza menu de opções - estilo profissional."""
        mode_color = "#00cc66" if self.current_mode == "mock" else "#cc8800"
        mode_icon = "●"
        mode_label = "MOCK" if self.current_mode == "mock" else "REAL"

        menu_text = Text()

        # Modo atual - compacto
        menu_text.append("\n MODE: ", style="#00aa55")
        menu_text.append(f"{mode_icon} {mode_label}", style=f"bold {mode_color}")
        menu_text.append("\n\n", style="#000000")

        # Dashboards - ultra limpo, sem linhas
        menu_text.append(" DASHBOARDS\n", style="bold #00cc66")
        menu_text.append("\n", style="#000000")
        
        menu_text.append("  0 ", style="#00aa55")
        menu_text.append("Consolidated", style="#00cc66")
        menu_text.append("    All metrics\n", style="#008855")

        menu_text.append("  1 ", style="#00aa55")
        menu_text.append("System", style="#00cc66")
        menu_text.append("          CPU, RAM, Disk\n", style="#008855")

        menu_text.append("  2 ", style="#00aa55")
        menu_text.append("Network", style="#00cc66")
        menu_text.append("         Bandwidth, connections\n", style="#008855")

        menu_text.append("  3 ", style="#00aa55")
        menu_text.append("WiFi", style="#00cc66")
        menu_text.append("            Signal, security\n", style="#008855")

        menu_text.append("  4 ", style="#00aa55")
        menu_text.append("Packets", style="#00cc66")
        menu_text.append("         Protocol analysis\n", style="#008855")
        
        menu_text.append("  5 ", style="#00aa55")
        menu_text.append("Topology", style="#00cc66")
        menu_text.append("        Network devices\n", style="#008855")

        # Controles - ultra limpo
        menu_text.append("\n CONTROLS\n", style="bold #00cc66")
        menu_text.append("\n", style="#000000")
        
        menu_text.append("  m ", style="#00aa55")
        menu_text.append("Toggle mode", style="#00cc66")
        menu_text.append("     Mock ↔ Real\n", style="#008855")

        menu_text.append("  h ", style="#00aa55")
        menu_text.append("Help", style="#00cc66")
        menu_text.append("             Keybindings\n", style="#008855")

        menu_text.append("  q ", style="#00aa55")
        menu_text.append("Quit", style="#00cc66")
        menu_text.append("             Exit\n", style="#008855")
        
        menu_text.append("\n", style="#000000")

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
        background: #000000;
        align: center middle;
    }

    #landing-container {
        width: 95%;
        min-width: 120;
        max-width: 180;
        height: auto;
        background: #000000;
        border: none;
        padding: 2;
    }

    BannerWidget {
        height: auto;
        margin: 0 0 2 0;
        background: #000000;
    }

    MenuWidget {
        height: auto;
        margin: 1 0;
        background: #000000;
    }

    #footer-info {
        height: 3;
        margin: 2 0 0 0;
        border: none;
        padding-top: 1;
        background: #000000;
        color: #00aa55;
    }
    """

    BINDINGS = [
        ("0", "launch_dashboard('consolidated')", "Consolidated"),
        ("1", "launch_dashboard('system')", "System"),
        ("2", "launch_dashboard('network')", "Network"),
        ("3", "launch_dashboard('wifi')", "WiFi"),
        ("4", "launch_dashboard('packets')", "Packets"),
        ("5", "launch_dashboard('topology')", "Topology"),
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
                "[#008855]Press 0-4 to launch • m=toggle mode • q=quit • Author: Professor JuanCS-Dev[/#008855]",
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
