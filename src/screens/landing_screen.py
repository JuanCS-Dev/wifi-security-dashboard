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
        """Renderiza banner minimalista e profissional responsivo."""
        banner_text = Text()
        
        # Get terminal width for responsive design
        try:
            from textual.app import App
            app = App.get_running_app()
            terminal_width = app.console.width if app else 80
        except:
            terminal_width = 80
        
        # Adjust banner based on width
        if terminal_width < 80:
            # Small screen - compact
            banner_text.append("\n", style="#000000")
            banner_text.append("WiFi Security Education", style="bold #00cc66")
            banner_text.append("\n", style="#000000")
            banner_text.append("v3.0.0", style="#00aa55")
            banner_text.append("\n", style="#000000")
        else:
            # Normal/Large screen - full
            banner_text.append("\n", style="#000000")
            banner_text.append("WiFi Security Education Dashboard", style="bold #00cc66")
            banner_text.append("\n", style="#000000")
            banner_text.append("v3.0.0", style="#00aa55")
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
        """Renderiza menu de opções - estilo profissional responsivo."""
        mode_color = "#00cc66" if self.current_mode == "mock" else "#cc8800"
        mode_icon = "●"
        mode_label = "MOCK" if self.current_mode == "mock" else "REAL"

        # Get terminal size for responsive layout
        try:
            from textual.app import App
            app = App.get_running_app()
            terminal_width = app.console.width if app else 80
            terminal_height = app.console.height if app else 24
        except:
            terminal_width = 80
            terminal_height = 24

        menu_text = Text()
        
        # Compact mode for small screens
        compact = terminal_width < 80 or terminal_height < 30

        # Modo atual - compacto
        menu_text.append("\n MODE: ", style="#00aa55")
        menu_text.append(f"{mode_icon} {mode_label}", style=f"bold {mode_color}")
        menu_text.append("\n" if compact else "\n\n", style="#000000")

        # Dashboards - ultra limpo, sem linhas
        menu_text.append(" DASHBOARDS\n", style="bold #00cc66")
        if not compact:
            menu_text.append("\n", style="#000000")
        
        # Compact descriptions for small screens
        desc_style = "#008855" if not compact else "#006644"
        spacing = "    " if not compact else "  "
        
        menu_text.append("  0 ", style="#00aa55")
        menu_text.append("Consolidated", style="#00cc66")
        if not compact:
            menu_text.append(f"{spacing}All metrics\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")

        menu_text.append("  1 ", style="#00aa55")
        menu_text.append("System", style="#00cc66")
        if not compact:
        else:
            menu_text.append("\n", style="#000000")

        menu_text.append("  2 ", style="#00aa55")
        menu_text.append("Network", style="#00cc66")

        menu_text.append("  3 ", style="#00aa55")
        menu_text.append("WiFi", style="#00cc66")

        menu_text.append("  4 ", style="#00aa55")
        menu_text.append("Packets", style="#00cc66")
        
        menu_text.append("  5 ", style="#00aa55")
        menu_text.append("Topology", style="#00cc66")
        menu_text.append("        Network devices\n", style="#008855")
        
        menu_text.append("  6 ", style="#00aa55")
        menu_text.append("ARP Detector", style="#00cc66")
        menu_text.append("    Spoofing monitor\n", style="#008855")
        
        menu_text.append("  7 ", style="#00aa55")
        menu_text.append("Traffic Stats", style="#00cc66")
        menu_text.append("    Bandwidth per device\n", style="#008855")
        
        menu_text.append("  8 ", style="#00aa55")
        menu_text.append("DNS Monitor", style="#00cc66")
        if not compact:
            menu_text.append("     Query tracking\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")
        
        menu_text.append("  9 ", style="#00aa55")
        menu_text.append("HTTP Sniffer", style="#ff6666")
        if not compact:
            menu_text.append("    ⚠️ Ethical use only\n", style="#ff4444")
        else:
            menu_text.append(" ⚠️\n", style="#ff4444")
        
        menu_text.append("  a ", style="#00aa55")
        menu_text.append("Rogue AP", style="#00cc66")
        if not compact:
            menu_text.append("        Evil twin detector\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")
        
        menu_text.append("  b ", style="#00aa55")
        menu_text.append("Handshake", style="#ff6666")
        if not compact:
            menu_text.append("      ⚖️ Legal use only\n", style="#ff4444")
        else:
            menu_text.append(" ⚖️\n", style="#ff4444")

        # Controles - ultra limpo
        menu_text.append("\n CONTROLS\n", style="bold #00cc66")
        if not compact:
            menu_text.append("\n", style="#000000")
        
        menu_text.append("  m ", style="#00aa55")
        menu_text.append("Toggle mode", style="#00cc66")
        if not compact:
            menu_text.append("     Mock ↔ Real\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")

        menu_text.append("  h ", style="#00aa55")
        menu_text.append("Help", style="#00cc66")
        if not compact:
            menu_text.append("             Keybindings\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")

        menu_text.append("  q ", style="#00aa55")
        menu_text.append("Quit", style="#00cc66")
        if not compact:
            menu_text.append("             Exit\n", style=desc_style)
        else:
            menu_text.append("\n", style="#000000")
        
        if not compact:
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
        width: 100%;
        height: 100%;
        background: #000000;
        border: none;
        padding: 1 2;
        overflow-y: auto;
    }

    BannerWidget {
        height: auto;
        width: 100%;
        margin: 0 0 1 0;
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
        ("6", "launch_dashboard('arp_detector')", "ARP Detector"),
        ("7", "launch_dashboard('traffic')", "Traffic Stats"),
        ("8", "launch_dashboard('dns_monitor')", "DNS Monitor"),
        ("9", "launch_dashboard('http_sniffer')", "HTTP Sniffer"),
        ("a", "launch_dashboard('rogue_ap')", "Rogue AP"),
        ("b", "launch_dashboard('handshake')", "Handshake"),
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
                "Press 0-6 to launch • m=toggle mode • q=quit • Author: Professor JuanCS-Dev",
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
