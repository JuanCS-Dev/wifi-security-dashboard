"""
Main dashboard orchestrator.

This module contains the Dashboard class that coordinates all system components:
- Config loading
- Plugin management
- Component rendering
- Event handling
- Main update loop

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import List, Dict, Optional, Any
import time
import sys

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from .config_loader import ConfigLoader, DashboardConfig
from .event_bus import EventBus, Event, EventType
from .component import Component
from .plugin_manager import PluginManager


class Dashboard:
    """
    Main dashboard controller.

    Orchestrates the entire dashboard system including:
    - Loading configuration
    - Managing plugins (Sprint 2)
    - Creating and updating components
    - Rendering layout
    - Handling events

    Example:
        >>> dashboard = Dashboard("config/dashboard.yml")
        >>> dashboard.run()
    """

    def __init__(self, config_path: str, mock_mode: bool = False, grid_mode: bool = False, pycui_mode: bool = False):
        """
        Initialize dashboard.

        Args:
            config_path: Path to YAML configuration file
            mock_mode: Run with simulated data (educational mode)
            grid_mode: Use grid positioning (2D absolute coordinates) - DEPRECATED, use pycui_mode
            pycui_mode: Use py_cui for pixel-perfect grid positioning (RECOMMENDED)

        Raises:
            FileNotFoundError: If config file not found
            ValidationError: If config invalid
        """
        self.console = Console()
        self.mock_mode = mock_mode
        self.grid_mode = grid_mode
        self.pycui_mode = pycui_mode

        # Load configuration
        try:
            self.config = ConfigLoader.load(config_path)
        except Exception as e:
            self.console.print(f"[bold red]Error loading configuration:[/bold red] {e}")
            sys.exit(1)

        # Initialize event bus with configured history limit
        self.event_bus = EventBus(max_history=self.config.settings.max_event_history)

        # Initialize state
        self._running = False
        self._paused = False

        # Components
        self.components: List[Component] = []

        # Initialize plugin manager
        self.plugin_manager = PluginManager(self.config.plugins, self.event_bus, mock_mode=mock_mode)
        try:
            self.plugin_manager.initialize_all()
        except Exception as e:
            self.console.print(f"[bold yellow]Warning:[/bold yellow] Plugin initialization error: {e}")

        # Initialize components from config
        self._initialize_components()

        # Setup event handlers
        self._setup_event_handlers()

        # Publish startup event
        self.event_bus.publish(Event(
            type=EventType.DASHBOARD_STARTED.value,
            source="dashboard",
            data={"config_path": config_path}
        ))

    def _setup_event_handlers(self) -> None:
        """Setup internal event handlers"""
        # Handle component errors
        self.event_bus.subscribe(
            EventType.COMPONENT_ERROR,
            self._on_component_error
        )

    def _on_component_error(self, event: Event) -> None:
        """
        Handle component errors by logging to console.

        Args:
            event: Error event with data containing error details

        Note:
            Future enhancements (Sprint 5+) may include:
            - Logging to file
            - Sending alerts/notifications
            - Error recovery strategies
        """
        error_data = event.data or {}
        component_name = event.source
        error_msg = error_data.get('error', 'Unknown error')

        # Log error to console with Rich formatting
        self.console.print(
            f"[red]⚠ Component Error:[/red] [yellow]{component_name}[/yellow]",
            style="bold"
        )
        self.console.print(f"  {error_msg}", style="dim red")

    def add_component(self, component: Component) -> None:
        """
        Add a component to the dashboard.

        Args:
            component: Component instance to add
        """
        self.components.append(component)

    def _initialize_components(self) -> None:
        """
        Initialize components from configuration.

        Creates component instances based on dashboard.yml configuration.
        Each component type is dynamically instantiated from src.components module.

        Note:
            Components are created in the order they appear in config.
            Failed component initialization is logged but doesn't stop dashboard.
        """
        from src.components import Textbox, Sparkline, Barchart, Runchart, PacketTable
        from src.core.component import ComponentConfig, Position, ComponentType

        # Map component types to classes
        component_classes = {
            'textbox': Textbox,
            'sparkline': Sparkline,
            'barchart': Barchart,
            'runchart': Runchart,
            'packettable': PacketTable,
        }

        for comp_config_model in self.config.components:
            try:
                # Convert Pydantic model to ComponentConfig dataclass
                component_config = ComponentConfig(
                    type=ComponentType(comp_config_model.type),
                    title=comp_config_model.title,
                    position=Position(
                        x=comp_config_model.position.x,
                        y=comp_config_model.position.y,
                        width=comp_config_model.position.width,
                        height=comp_config_model.position.height
                    ),
                    rate_ms=comp_config_model.rate_ms,
                    plugin=comp_config_model.plugin,
                    data_field=comp_config_model.data_field,
                    color=comp_config_model.color,
                    triggers=[],  # Triggers Sprint 5
                    extra=comp_config_model.extra
                )

                # Get component class
                component_class = component_classes.get(comp_config_model.type)

                if component_class is None:
                    self.console.print(
                        f"[yellow]Warning:[/yellow] Unknown component type '{comp_config_model.type}', skipping"
                    )
                    continue

                # Instantiate component
                component = component_class(component_config)

                # Add to dashboard
                self.add_component(component)

                self.console.print(
                    f"[green]✓[/green] Component loaded: [cyan]{comp_config_model.title}[/cyan] "
                    f"({comp_config_model.type})"
                )

            except Exception as e:
                self.console.print(
                    f"[red]✗ Failed to load component:[/red] {comp_config_model.title}"
                )
                self.console.print(f"  Error: {e}", style="dim red")

    def update_components(self) -> None:
        """
        Update all components that need updating based on their rate_ms.

        This method:
        1. Checks each component's should_update()
        2. Fetches data from associated plugin
        3. Updates the component
        4. Publishes update event
        """
        for component in self.components:
            if not component.should_update():
                continue

            try:
                # Get data from plugin manager
                plugin_data = self.plugin_manager.get_plugin_data(component.config.plugin)

                # Update component
                component.update(plugin_data)

                # Publish event
                self.event_bus.publish(Event(
                    type=EventType.COMPONENT_UPDATED.value,
                    source=component.config.title,
                    data={"value": component.data}
                ))

            except Exception as e:
                # Publish error event
                self.event_bus.publish(Event(
                    type=EventType.COMPONENT_ERROR.value,
                    source=component.config.title,
                    data={"error": str(e)}
                ))

    def render_layout(self) -> Layout:
        """
        Render complete dashboard layout.

        Returns:
            Rich Layout object with all components positioned

        Note:
            Proper grid layout implementation comes in Sprint 4.
            For now, using simple vertical stacking.
        """
        # Create main layout
        layout = Layout()

        # Header
        header = Panel(
            Text(self.config.title, justify="center", style="bold cyan"),
            border_style="cyan"
        )

        # If no components, show welcome message
        if not self.components:
            content = Panel(
                "[yellow]No components configured.[/yellow]\n\n"
                "Add components to your config file to get started.",
                title="Dashboard Empty",
                border_style="yellow"
            )
            layout.split_column(
                Layout(header, size=3),
                Layout(content)
            )
            return layout

        # Render components
        # Sprint 1: Simple vertical layout
        # Grid positioning with (x,y,w,h) coordinates implemented in Sprint 4
        component_panels = [comp.render() for comp in self.components]

        # Create vertical stack layout
        if component_panels:
            # Stack all component panels vertically
            main_content = Layout()
            for panel in component_panels:
                main_content.split_column(Layout(panel))

            layout.split_column(
                Layout(header, size=3),
                main_content
            )
        else:
            # No renderable components
            layout.split_column(
                Layout(header, size=3),
                Layout(Panel(
                    "[dim]Components configured but not rendering yet[/dim]",
                    title="Main Area"
                ))
            )

        return layout

    def run(self) -> None:
        """
        Run dashboard main loop.

        This is the primary entry point that:
        1. Initializes the display
        2. Enters update loop
        3. Handles keyboard input
        4. Renders at configured refresh rate

        Chooses between pycui mode (py_cui pixel-perfect), grid mode
        (ANSI positioning - deprecated), or vertical stack mode.
        """
        if self.pycui_mode:
            self._run_pycui_mode()
        elif self.grid_mode:
            self._run_grid_mode()
        else:
            self._run_vertical_mode()

    def _run_vertical_mode(self) -> None:
        """Run dashboard with vertical stacking layout (default)"""
        self._running = True
        refresh_rate = self.config.settings.refresh_rate_ms / 1000

        try:
            with Live(
                self.render_layout(),
                console=self.console,
                screen=True,
                auto_refresh=False,
                refresh_per_second=1 / refresh_rate
            ) as live:
                while self._running:
                    # Skip update if paused
                    if self._paused:
                        time.sleep(refresh_rate)
                        continue

                    # Update components
                    self.update_components()

                    # Render
                    layout = self.render_layout()
                    live.update(layout, refresh=True)

                    # Sleep for refresh interval
                    time.sleep(refresh_rate)

        except KeyboardInterrupt:
            self._running = False
            self.console.print("\n[yellow]Dashboard stopped by user[/yellow]")

        finally:
            # Cleanup plugins
            self.plugin_manager.cleanup_all()

            # Publish shutdown event
            self.event_bus.publish(Event(
                type=EventType.DASHBOARD_STOPPED.value,
                source="dashboard"
            ))

    def _run_grid_mode(self) -> None:
        """Run dashboard with 2D grid positioning (ANSI absolute positioning)"""
        from src.core.grid_renderer import GridDashboardRenderer

        self._running = True
        refresh_rate = self.config.settings.refresh_rate_ms / 1000

        # Create grid renderer with terminal size from config
        grid_renderer = GridDashboardRenderer(
            width=self.config.settings.terminal_size.width,
            height=self.config.settings.terminal_size.height
        )

        try:
            # Clear screen once at start
            self.console.clear()

            while self._running:
                # Skip update if paused
                if self._paused:
                    time.sleep(refresh_rate)
                    continue

                # Update components
                self.update_components()

                # Clear grid renderer
                grid_renderer.clear()

                # Add all components to grid renderer
                for component in self.components:
                    grid_renderer.add_from_component(component)

                # Render grid and print
                grid_output = grid_renderer.render()
                print(grid_output, end='', flush=True)

                # Sleep for refresh interval
                time.sleep(refresh_rate)

        except KeyboardInterrupt:
            self._running = False
            self.console.print("\n[yellow]Dashboard stopped by user[/yellow]")

        finally:
            # Cleanup plugins
            self.plugin_manager.cleanup_all()

            # Publish shutdown event
            self.event_bus.publish(Event(
                type=EventType.DASHBOARD_STOPPED.value,
                source="dashboard"
            ))

    def _run_pycui_mode(self) -> None:
        """Run dashboard with py_cui pixel-perfect grid positioning"""
        from src.core.pycui_renderer import PyCUIDashboardRenderer

        self._running = True

        # Create py_cui renderer with terminal size from config
        pycui_renderer = PyCUIDashboardRenderer(
            width=self.config.settings.terminal_size.width,
            height=self.config.settings.terminal_size.height
        )

        # Set plugin manager for data updates
        pycui_renderer.set_plugin_manager(self.plugin_manager)

        # Set update callback
        pycui_renderer.set_update_callback(self.update_components)

        # Set refresh rate
        pycui_renderer.set_refresh_rate(self.config.settings.refresh_rate_ms)

        try:
            # Add all components with adapters
            # TODO: Create adapter factory in Sprint 2
            # For now, components without adapters will be skipped
            for component in self.components:
                try:
                    # Get adapter for this component type
                    adapter = self._create_adapter_for_component(component)
                    if adapter:
                        pycui_renderer.add_from_component(component, adapter)
                except Exception as e:
                    self.console.print(f"[yellow]Warning:[/yellow] Could not add component {component.config.title}: {e}")

            # Start py_cui event loop (blocking until quit)
            pycui_renderer.start()

        except KeyboardInterrupt:
            self._running = False
            self.console.print("\n[yellow]Dashboard stopped by user[/yellow]")

        finally:
            # Cleanup plugins
            self.plugin_manager.cleanup_all()

            # Publish shutdown event
            self.event_bus.publish(Event(
                type=EventType.DASHBOARD_STOPPED.value,
                source="dashboard"
            ))

    def _create_adapter_for_component(self, component: Any):
        """
        Factory method to create appropriate adapter for component type.

        Args:
            component: Component instance

        Returns:
            ComponentAdapter instance or None if type not supported yet

        Note:
            Implementation will be added in Sprint 2-6 as we migrate each component type.
        """
        component_type = component.config.type

        # Sprint 2: Sparkline adapter
        if component_type == "sparkline":
            try:
                from src.adapters.sparkline_adapter import SparklineAdapter
                return SparklineAdapter(component)
            except ImportError:
                return None

        # Sprint 3: Textbox adapter
        if component_type == "textbox":
            try:
                from src.adapters.textbox_adapter import TextboxAdapter
                return TextboxAdapter(component)
            except ImportError:
                return None

        # Sprint 4: Runchart adapter
        if component_type == "runchart":
            try:
                from src.adapters.runchart_adapter import RunchartAdapter
                return RunchartAdapter(component)
            except ImportError:
                return None

        # Sprint 5: PacketTable adapter
        if component_type == "packettable":
            try:
                from src.adapters.packet_table_adapter import PacketTableAdapter
                return PacketTableAdapter(component)
            except ImportError:
                return None

        # Sprint 6: Barchart adapter
        if component_type == "barchart":
            try:
                from src.adapters.barchart_adapter import BarchartAdapter
                return BarchartAdapter(component)
            except ImportError:
                return None

        # Unknown or not migrated yet
        return None

    def pause(self) -> None:
        """Pause dashboard updates"""
        self._paused = True
        self.event_bus.publish(Event(
            type=EventType.DASHBOARD_PAUSED.value,
            source="dashboard"
        ))

    def resume(self) -> None:
        """Resume dashboard updates"""
        self._paused = False
        self.event_bus.publish(Event(
            type=EventType.DASHBOARD_RESUMED.value,
            source="dashboard"
        ))

    def stop(self) -> None:
        """Stop dashboard"""
        self._running = False

    @property
    def is_running(self) -> bool:
        """Check if dashboard is running"""
        return self._running

    @property
    def is_paused(self) -> bool:
        """Check if dashboard is paused"""
        return self._paused

    def __repr__(self) -> str:
        return (
            f"Dashboard("
            f"title='{self.config.title}', "
            f"components={len(self.components)}, "
            f"running={self._running})"
        )
