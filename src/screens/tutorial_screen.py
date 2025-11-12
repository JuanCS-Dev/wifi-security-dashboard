"""
Tutorial Screen - First-run interactive tutorial

Shows on first launch to guide users through dashboard features.
Can be dismissed and won't show again (flag file created).

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.reactive import reactive
from pathlib import Path


class TutorialScreen(ModalScreen):
    """
    First-run tutorial modal.
    
    Features:
    - Multi-step walkthrough
    - Skip or complete tutorial
    - Creates flag file on completion
    - Clean, minimal design
    """
    
    current_step = reactive(0)
    total_steps = 4
    
    CSS = """
    TutorialScreen {
        align: center middle;
    }
    
    #tutorial-dialog {
        width: 90;
        height: auto;
        max-height: 90%;
        border: thick #00ff00;
        background: #2d2d2d;
        padding: 2;
    }
    
    #tutorial-header {
        text-align: center;
        text-style: bold;
        color: #00ff00;
        padding: 0 0 1 0;
    }
    
    #tutorial-progress {
        text-align: center;
        color: #808080;
        padding: 0 0 2 0;
    }
    
    #tutorial-content {
        border: solid #00aa00;
        padding: 2;
        margin: 1 0;
        min-height: 20;
    }
    
    #tutorial-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0 0 0;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        ("escape", "skip_tutorial", "Skip"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the tutorial modal layout."""
        with Container(id="tutorial-dialog"):
            yield Static(
                "🎓 Welcome to WiFi Security Dashboard!",
                id="tutorial-header"
            )
            yield Static("", id="tutorial-progress")
            yield Static("", id="tutorial-content")
            
            with Horizontal(id="tutorial-buttons"):
                yield Button("Skip", variant="default", id="skip-btn")
                yield Button("Previous", variant="default", id="prev-btn")
                yield Button("Next", variant="primary", id="next-btn")
    
    def on_mount(self) -> None:
        """Initialize tutorial on mount."""
        self.update_content()
    
    def watch_current_step(self, new_step: int) -> None:
        """Update content when step changes."""
        self.update_content()
    
    def update_content(self) -> None:
        """Update tutorial content based on current step."""
        # Update progress
        progress = self.query_one("#tutorial-progress", Static)
        progress.update(f"[dim]Step {self.current_step + 1} of {self.total_steps}[/dim]")
        
        # Update content
        content = self.query_one("#tutorial-content", Static)
        
        if self.current_step == 0:
            content.update(
                "[bold cyan]📊 Dashboard Overview[/bold cyan]\n\n"
                "This dashboard helps you learn about network security by\n"
                "monitoring real-time network activity.\n\n"
                "[bold]Five dashboards available:[/bold]\n\n"
                "[cyan]0[/cyan] [bold]Consolidated[/bold] - Overview of everything\n"
                "[dim]Quick glance at all metrics\n\n"
                "[cyan]1[/cyan] [bold]System[/bold] - CPU, RAM, Disk\n"
                "[dim]Hardware resource monitoring\n\n"
                "[cyan]2[/cyan] [bold]Network[/bold] - Bandwidth & connections\n"
                "[dim]Network traffic analysis\n\n"
                "[cyan]3[/cyan] [bold]WiFi[/bold] - Signal & security\n"
                "[dim]Wireless connection details\n\n"
                "[cyan]4[/cyan] [bold]Packets[/bold] - Protocol analysis\n"
                "[dim]Learn about HTTP, HTTPS, DNS, SSH"
            )
        
        elif self.current_step == 1:
            content.update(
                "[bold green]🎮 Navigation[/bold green]\n\n"
                "[bold]Keyboard shortcuts:[/bold]\n\n"
                "[yellow]0-4[/yellow]     Switch between dashboards\n"
                "[yellow]h or ?[/yellow]  Show help screen anytime\n"
                "[yellow]q[/yellow]       Quit dashboard\n"
                "[yellow]ESC[/yellow]     Close modals\n\n"
                "[bold]Tips:[/bold]\n"
                "[dim]• Press [yellow]h[/yellow] anytime for full shortcuts list\n"
                "• Use number keys for quick navigation\n"
                "• Mouse works too! Click and scroll[/dim]"
            )
        
        elif self.current_step == 2:
            content.update(
                "[bold yellow]🎓 Learning Mode[/bold yellow]\n\n"
                "[bold]Status indicators explained:[/bold]\n\n"
                "[green]●[/green] [bold]Normal[/bold]\n"
                "[dim]Everything is working fine\n\n"
                "[yellow]●[/yellow] [bold]High/Warning[/bold]\n"
                "[dim]Pay attention - resource usage elevated\n\n"
                "[red]●[/red] [bold]Critical[/bold]\n"
                "[dim]Potential issue - investigate\n\n"
                "[bold]Security indicators:[/bold]\n\n"
                "[green]🔒 HTTPS[/green] = Safe encrypted connection\n"
                "[red]⚠️  HTTP[/red] = Insecure - avoid for passwords!\n"
                "[cyan]🌐 DNS[/cyan] = Domain name lookups\n"
                "[green]🔑 SSH[/green] = Secure remote access"
            )
        
        elif self.current_step == 3:
            content.update(
                "[bold magenta]🚀 Ready to Explore![/bold magenta]\n\n"
                "[bold]Recommended learning path:[/bold]\n\n"
                "[cyan]1.[/cyan] Start with [bold]Consolidated[/bold] (press [yellow]0[/yellow])\n"
                "[dim]   Get familiar with the layout\n\n"
                "[cyan]2.[/cyan] Check [bold]System[/bold] dashboard (press [yellow]1[/yellow])\n"
                "[dim]   See how your computer uses resources\n\n"
                "[cyan]3.[/cyan] Explore [bold]Packets[/bold] (press [yellow]4[/yellow])\n"
                "[dim]   Learn about HTTP vs HTTPS security\n\n"
                "[cyan]4.[/cyan] Press [yellow]h[/yellow] anytime for help\n\n"
                "[bold green]✅ You're all set![/bold green]\n\n"
                "[dim italic]Click 'Finish' to start exploring.\n"
                "This tutorial won't show again.[/dim italic]"
            )
        
        # Update buttons
        prev_btn = self.query_one("#prev-btn", Button)
        next_btn = self.query_one("#next-btn", Button)
        
        prev_btn.disabled = (self.current_step == 0)
        
        if self.current_step == self.total_steps - 1:
            next_btn.label = "Finish"
            next_btn.variant = "success"
        else:
            next_btn.label = "Next"
            next_btn.variant = "primary"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "skip-btn":
            self.action_skip_tutorial()
        elif event.button.id == "prev-btn":
            if self.current_step > 0:
                self.current_step -= 1
        elif event.button.id == "next-btn":
            if self.current_step < self.total_steps - 1:
                self.current_step += 1
            else:
                self.action_finish_tutorial()
    
    def action_skip_tutorial(self) -> None:
        """Skip tutorial without creating flag file."""
        self.dismiss(completed=False)
    
    def action_finish_tutorial(self) -> None:
        """Finish tutorial and create flag file."""
        self.create_completion_flag()
        self.dismiss(completed=True)
    
    def create_completion_flag(self) -> None:
        """Create flag file to mark tutorial as completed."""
        try:
            flag_file = Path.home() / ".wifi_security_dashboard" / "tutorial_completed"
            flag_file.parent.mkdir(exist_ok=True)
            flag_file.touch()
        except Exception as e:
            # Silently fail - tutorial will just show again next time
            pass
    
    @staticmethod
    def should_show_tutorial() -> bool:
        """Check if tutorial should be shown (first run)."""
        flag_file = Path.home() / ".wifi_security_dashboard" / "tutorial_completed"
        return not flag_file.exists()
