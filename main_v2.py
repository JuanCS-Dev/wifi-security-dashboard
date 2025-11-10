#!/usr/bin/env python3
"""
WiFi Security Education Dashboard v2.0 - Entry Point

This is the main entry point for the v2.0 dashboard with modular architecture.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09

Usage:
    python main_v2.py                    # Use default config
    python main_v2.py --config custom.yml  # Use custom config
    python main_v2.py --help             # Show help
"""

import sys
import argparse
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.dashboard import Dashboard
from src.core.config_loader import ConfigLoader


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="WiFi Security Education Dashboard v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_v2.py                           # Use default config
  python main_v2.py --config custom.yml       # Use custom config
  python main_v2.py --validate                # Validate config only

Author: Juan-Dev - Soli Deo Gloria ✝️
        """
    )

    parser.add_argument(
        '--config',
        '-c',
        default='config/dashboard.yml',
        help='Path to YAML configuration file (default: config/dashboard.yml)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate configuration and exit'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version and exit'
    )

    return parser.parse_args()


def show_version():
    """Show version information"""
    console = Console()
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]WiFi Security Education Dashboard[/bold cyan]\n"
            "[yellow]Version:[/yellow] 2.0.0-alpha (Sprint 3)\n"
            "[yellow]Author:[/yellow] Juan-Dev\n"
            "[yellow]License:[/yellow] Educational Use\n\n"
            "[dim]Soli Deo Gloria ✝️[/dim]"
        ),
        title="Dashboard v2.0",
        border_style="cyan"
    ))


def show_juan_banner():
    """
    Mostra o banner JUAN colorido com gradient verde → amarelo → azul

    Banner ASCII art com o nome JUAN em letras grandes,
    cada linha em uma cor diferente criando um efeito gradient.
    """
    console = Console()

    banner_lines = [
        "     ██╗██╗   ██╗ █████╗ ███╗   ██╗",
        "     ██║██║   ██║██╔══██╗████╗  ██║",
        "     ██║██║   ██║███████║██╔██╗ ██║",
        "██   ██║██║   ██║██╔══██║██║╚██╗██║",
        "╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║",
        " ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝",
    ]

    # Gradient verde → amarelo → azul
    colors = ['bright_green', 'green', 'yellow', 'bright_yellow', 'cyan', 'bright_cyan']

    console.print()

    # Imprime cada linha com sua cor
    for i, line in enumerate(banner_lines):
        console.print(Align.center(Text(line, style=colors[i % len(colors)])))

    console.print()
    console.print(Align.center(Text("🎓 WiFi Security Education Dashboard v2.0 🎓", style="bold bright_yellow")))
    console.print(Align.center(Text("Soli Deo Gloria ✝️", style="bold bright_white")))
    console.print()


def validate_config(config_path: str) -> bool:
    """
    Validate configuration file

    Args:
        config_path: Path to config file

    Returns:
        True if valid, False otherwise
    """
    console = Console()

    try:
        console.print(f"[cyan]Validating config:[/cyan] {config_path}")
        config = ConfigLoader.load(config_path)

        console.print("[green]✓[/green] Configuration is valid!")
        console.print(f"\n[cyan]Dashboard:[/cyan] {config.title}")
        console.print(f"[cyan]Plugins:[/cyan] {len(config.plugins)}")
        console.print(f"[cyan]Components:[/cyan] {len(config.components)}")

        return True

    except FileNotFoundError as e:
        console.print(f"[red]✗ Config file not found:[/red] {e}")
        return False

    except Exception as e:
        console.print(f"[red]✗ Validation failed:[/red]")
        console.print(str(e))
        return False


def main():
    """Main entry point"""
    args = parse_args()
    console = Console()

    # Show JUAN banner (always)
    show_juan_banner()

    # Show version
    if args.version:
        show_version()
        return 0

    # Validate only
    if args.validate:
        success = validate_config(args.config)
        return 0 if success else 1

    # Check config exists
    config_path = Path(args.config)
    if not config_path.exists():
        console.print(f"[red]Error:[/red] Config file not found: {args.config}")
        console.print("\n[yellow]Hint:[/yellow] Use --config to specify config file")
        return 1

    # Show startup info (clean, after banner)
    console.print(f"[cyan]📋 Config:[/cyan] {args.config}")
    console.print(f"[cyan]🎮 Controls:[/cyan] Press 'q' to quit, '?' for help\n")

    # Create and run dashboard
    try:
        dashboard = Dashboard(str(config_path))

        # Note: Dashboard.run() is blocking - will run until quit
        dashboard.run()

        return 0

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 0

    except Exception as e:
        console.print(f"\n[red]Fatal error:[/red] {e}")
        import traceback
        console.print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
