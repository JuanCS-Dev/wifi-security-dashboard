"""
Tooltip Widget - Educational contextual tips

Reusable tooltip component that can be attached to any widget
to show educational information on hover or focus.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.widgets import Static
from textual.reactive import reactive
from typing import Optional


class Tooltip(Static):
    """
    Educational tooltip widget.
    
    Shows contextual help and learning tips.
    Can be positioned near any widget.
    """
    
    visible = reactive(False)
    content = reactive("")
    
    CSS = """
    Tooltip {
        display: none;
        layer: overlay;
        background: $panel;
        border: solid $accent;
        padding: 1 2;
        max-width: 60;
        color: $text;
    }
    
    Tooltip.visible {
        display: block;
    }
    """
    
    def watch_visible(self, is_visible: bool) -> None:
        """Toggle visibility class."""
        if is_visible:
            self.add_class("visible")
        else:
            self.remove_class("visible")
    
    def watch_content(self, new_content: str) -> None:
        """Update content when changed."""
        self.update(new_content)
    
    def show_tip(self, tip_content: str) -> None:
        """Show tooltip with content."""
        self.content = tip_content
        self.visible = True
    
    def hide_tip(self) -> None:
        """Hide tooltip."""
        self.visible = False


class EducationalTip(Static):
    """
    Static educational tip widget.
    
    Always visible tips for specific contexts.
    Clean design matching dashboard style.
    """
    
    tip_type = reactive("info")
    
    CSS = """
    EducationalTip {
        border: solid $primary;
        background: $panel;
        padding: 1 2;
        margin: 1 0;
    }
    
    EducationalTip.info {
        border: solid cyan;
    }
    
    EducationalTip.warning {
        border: solid yellow;
    }
    
    EducationalTip.success {
        border: solid green;
    }
    
    EducationalTip.error {
        border: solid red;
    }
    """
    
    def __init__(self, content: str, tip_type: str = "info", **kwargs):
        """
        Initialize educational tip.
        
        Args:
            content: Tip text content (supports Rich markup)
            tip_type: Type of tip (info, warning, success, error)
        """
        super().__init__(content, **kwargs)
        self.tip_type = tip_type
    
    def watch_tip_type(self, new_type: str) -> None:
        """Update classes when type changes."""
        # Remove all type classes
        for t in ["info", "warning", "success", "error"]:
            self.remove_class(t)
        # Add new type class
        self.add_class(new_type)


# Common educational tips library
SECURITY_TIPS = {
    "https": (
        "[bold green]🔒 HTTPS - Secure[/bold green] [green]●[/green]\n\n"
        "[dim]HTTPS encrypts data between your browser and websites.\n"
        "Always look for the padlock icon when entering passwords\n"
        "or credit card information.[/dim]"
    ),
    "http": (
        "[bold red]⚠️  HTTP - Insecure[/bold red] [red]●[/red]\n\n"
        "[dim]HTTP sends data in plain text - anyone monitoring your\n"
        "network can see it! Avoid using HTTP for:\n"
        "• Logging into websites\n"
        "• Online shopping\n"
        "• Sensitive information[/dim]"
    ),
    "dns": (
        "[bold cyan]🌐 DNS - Name Resolution[/bold cyan] [cyan]●[/cyan]\n\n"
        "[dim]DNS translates domain names (like google.com) into\n"
        "IP addresses (like 142.250.180.46) that computers use.\n"
        "It's like the internet's phonebook![/dim]"
    ),
    "ssh": (
        "[bold green]🔑 SSH - Secure Shell[/bold green] [green]●[/green]\n\n"
        "[dim]SSH allows secure remote access to servers.\n"
        "All communication is encrypted, making it safe for:\n"
        "• Remote server management\n"
        "• Secure file transfers\n"
        "• Running commands remotely[/dim]"
    ),
    "wifi_signal": (
        "[bold yellow]📶 WiFi Signal Strength[/bold yellow]\n\n"
        "[dim]Signal strength affects your connection:\n"
        "[green]●[/green] 70-100% - Excellent (streaming, gaming)\n"
        "[yellow]●[/yellow] 40-69% - Good (browsing)\n"
        "[red]●[/red] 0-39% - Poor (slow, unstable)[/dim]"
    ),
    "wifi_security": (
        "[bold green]🔒 WiFi Security[/bold green]\n\n"
        "[dim]Protection levels:\n"
        "[green]●[/green] WPA3 - Best (newest, most secure)\n"
        "[green]●[/green] WPA2 - Good (widely compatible)\n"
        "[red]●[/red] WEP - Bad (easily cracked!)\n"
        "[red]●[/red] Open - Dangerous (no encryption!)[/dim]"
    ),
    "bandwidth": (
        "[bold cyan]📊 Bandwidth[/bold cyan]\n\n"
        "[dim]Bandwidth measures how much data moves through\n"
        "your network:\n"
        "• RX (↓) - Download (receiving data)\n"
        "• TX (↑) - Upload (sending data)\n"
        "Measured in Mbps (megabits per second)[/dim]"
    ),
    "cpu_usage": (
        "[bold blue]💻 CPU Usage[/bold blue]\n\n"
        "[dim]Shows how hard your processor is working:\n"
        "[green]●[/green] 0-50% - Normal (light tasks)\n"
        "[yellow]●[/yellow] 51-80% - High (heavy processing)\n"
        "[red]●[/red] 81-100% - Critical (may slow down)[/dim]"
    ),
    "ram_usage": (
        "[bold magenta]📊 RAM Usage[/bold magenta]\n\n"
        "[dim]RAM (memory) stores data for running programs:\n"
        "[green]●[/green] 0-60% - Normal\n"
        "[yellow]●[/yellow] 61-85% - High (may be slow)\n"
        "[red]●[/red] 86-100% - Critical (system may freeze)\n\n"
        "Close unused programs to free memory![/dim]"
    ),
}


def get_tip(tip_name: str) -> Optional[str]:
    """
    Get educational tip by name.
    
    Args:
        tip_name: Name of tip from SECURITY_TIPS dict
        
    Returns:
        Tip content string or None if not found
    """
    return SECURITY_TIPS.get(tip_name)
