"""
Grid-based absolute positioning renderer for terminal UI.

This module provides a GridRenderer that allows positioning Rich components
at absolute (x, y) coordinates with specified (width, height), similar to
Sampler's grid system.

Uses ANSI escape codes for precise cursor control combined with Rich rendering.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from io import StringIO

from rich.console import Console, RenderableType
from rich.segment import Segment
from rich.style import Style


@dataclass
class RenderedComponent:
    """
    A component rendered at a specific grid position.

    Attributes:
        renderable: Rich renderable object (Panel, Table, etc.)
        x: Column position (0-based, left edge)
        y: Row position (0-based, top edge)
        width: Width in characters
        height: Height in lines
    """
    renderable: RenderableType
    x: int
    y: int
    width: int
    height: int


class GridRenderer:
    """
    Renders components at absolute grid positions using ANSI positioning.

    This renderer provides Sampler-style grid positioning where each component
    has explicit (x, y, width, height) coordinates. It works by:

    1. Rendering each component to a string buffer
    2. Splitting into lines
    3. Positioning each line at absolute terminal coordinates using ANSI

    Example:
        >>> from rich.panel import Panel
        >>> renderer = GridRenderer(width=120, height=40)
        >>> renderer.add_component(
        ...     Panel("Hello"),
        ...     x=0, y=0, width=30, height=5
        ... )
        >>> output = renderer.render()
        >>> print(output, end='')

    Performance:
        - O(n) where n = total lines across all components
        - Efficient for dashboards with 5-20 components
        - Uses string concatenation (optimized in Python 3.6+)

    Technical Notes:
        - Uses ANSI escape code `\\033[{y};{x}H` for cursor positioning
        - Terminal coordinates are 1-based (not 0-based) in ANSI
        - Clipping ensures components don't exceed terminal bounds
    """

    def __init__(self, width: int, height: int):
        """
        Initialize grid renderer with terminal dimensions.

        Args:
            width: Terminal width in characters
            height: Terminal height in lines

        Raises:
            ValueError: If width or height <= 0
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Terminal dimensions must be > 0, got ({width}, {height})")

        self.width = width
        self.height = height
        self._components: List[RenderedComponent] = []

        # Create console for rendering components
        # Use record=True to capture output without printing
        self._console = Console(
            width=width,
            height=height,
            force_terminal=True,
            force_interactive=False,
            legacy_windows=False
        )

    def add_component(
        self,
        renderable: RenderableType,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> None:
        """
        Add a component to be rendered at specified position.

        Args:
            renderable: Rich renderable (Panel, Table, etc.)
            x: Column position (0-based)
            y: Row position (0-based)
            width: Component width in characters
            height: Component height in lines

        Note:
            Components are rendered in the order they're added.
            Later components will overlay earlier ones if they overlap.

            Enforces minimum dimensions (like Sampler):
            - Min width: 3 characters
            - Min height: 3 lines
        """
        # Enforce minimum dimensions (Sampler-style)
        MIN_DIMENSION = 3
        width = max(width, MIN_DIMENSION)
        height = max(height, MIN_DIMENSION)

        # Clamp to terminal bounds
        width = min(width, self.width - x)
        height = min(height, self.height - y)

        self._components.append(RenderedComponent(
            renderable=renderable,
            x=x,
            y=y,
            width=width,
            height=height
        ))

    def clear_components(self) -> None:
        """Remove all components from renderer."""
        self._components.clear()

    def render(self) -> str:
        """
        Render all components with absolute positioning.

        Returns:
            String containing ANSI-positioned terminal output

        Algorithm:
            1. Clear screen with ANSI code
            2. For each component:
                a. Render component to string using Rich
                b. Split into lines
                c. Position each line at (x, y+line_offset)
            3. Move cursor to bottom (cleanup)

        ANSI Codes Used:
            - \\033[2J: Clear entire screen
            - \\033[H: Move cursor to home (1,1)
            - \\033[{y};{x}H: Move cursor to (x, y)
            - \\033[0m: Reset all attributes
        """
        output_lines: List[str] = []

        # Clear screen and move to home
        output_lines.append("\033[2J\033[H")

        for comp in self._components:
            # Render component to string using Rich
            rendered_lines = self._render_component(
                comp.renderable,
                comp.width,
                comp.height
            )

            # Position each line at absolute coordinates
            for line_offset, line in enumerate(rendered_lines):
                # Calculate terminal row (1-based in ANSI)
                terminal_row = comp.y + line_offset + 1
                terminal_col = comp.x + 1

                # Skip if outside terminal bounds
                if terminal_row > self.height or terminal_row < 1:
                    continue

                # Position cursor and write line
                output_lines.append(f"\033[{terminal_row};{terminal_col}H{line}")

        # Move cursor to bottom of screen (cleanup)
        output_lines.append(f"\033[{self.height};1H")

        return ''.join(output_lines)

    def _render_component(
        self,
        renderable: RenderableType,
        width: int,
        height: int
    ) -> List[str]:
        """
        Render a Rich component to list of strings.

        Args:
            renderable: Rich renderable object
            width: Maximum width for rendering
            height: Maximum height for rendering

        Returns:
            List of strings, one per line (max height lines)

        Note:
            Uses StringIO to capture Rich output without printing.
            Strips ANSI codes that would interfere with positioning.
        """
        # Create string buffer
        buffer = StringIO()

        # Create console that writes to buffer
        temp_console = Console(
            file=buffer,
            width=width,
            height=height,
            force_terminal=True,
            force_interactive=False,
            legacy_windows=False
        )

        # Render component
        temp_console.print(renderable)

        # Extract lines
        output = buffer.getvalue()
        lines = output.split('\n')

        # Clip to height
        if len(lines) > height:
            lines = lines[:height]

        # Pad with empty lines if needed
        while len(lines) < height:
            lines.append(' ' * width)

        # Ensure each line is exactly width characters
        lines = [self._pad_or_clip(line, width) for line in lines]

        return lines

    def _pad_or_clip(self, line: str, width: int) -> str:
        """
        Ensure line is exactly width characters (VISIBLE chars, not counting ANSI).

        Args:
            line: Input line (may contain ANSI codes)
            width: Target visible width

        Returns:
            Line padded or clipped to EXACT width

        Note:
            Uses Rich Console to accurately measure visible length,
            preserving ANSI codes while ensuring pixel-perfect width.
        """
        import re

        # Strip ANSI escape codes to measure visible length
        # Pattern matches: ESC [ ... m (color codes) and ESC [ ... H (cursor positioning)
        ansi_pattern = re.compile(r'\x1b\[[0-9;]*[mHJKhlABCDEFG]')
        visible_text = ansi_pattern.sub('', line)
        visible_len = len(visible_text)

        if visible_len < width:
            # Pad with spaces to EXACT width
            padding = ' ' * (width - visible_len)
            return line + padding
        elif visible_len > width:
            # Clip to EXACT width (preserve ANSI codes at start)
            # Find position where visible chars reach width
            char_count = 0
            result = []
            i = 0
            while i < len(line) and char_count < width:
                if line[i:i+2] == '\x1b[':
                    # ANSI escape sequence - find end
                    end = i + 2
                    while end < len(line) and line[end] not in 'mHJKhlABCDEFG':
                        end += 1
                    result.append(line[i:end+1])
                    i = end + 1
                else:
                    # Regular character
                    result.append(line[i])
                    char_count += 1
                    i += 1

            # Add reset code if we clipped
            if char_count >= width:
                result.append('\x1b[0m')

            return ''.join(result)
        else:
            return line

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"GridRenderer("
            f"size=({self.width}x{self.height}), "
            f"components={len(self._components)})"
        )


class GridDashboardRenderer:
    """
    High-level renderer for dashboard with grid positioning.

    Wraps GridRenderer with dashboard-specific features:
    - Automatic terminal size detection
    - Component management from config
    - Integration with Dashboard class

    Example:
        >>> from src.core.component import Component, Position
        >>> renderer = GridDashboardRenderer()
        >>> for component in dashboard.components:
        ...     renderer.add_from_component(component)
        >>> output = renderer.render()
    """

    def __init__(self, width: Optional[int] = None, height: Optional[int] = None):
        """
        Initialize dashboard renderer.

        Args:
            width: Terminal width (None = auto-detect)
            height: Terminal height (None = auto-detect)
        """
        # Auto-detect terminal size if not provided
        if width is None or height is None:
            console = Console()
            width = width or console.width
            height = height or console.height

        self.renderer = GridRenderer(width, height)

    def add_from_component(self, component) -> None:
        """
        Add component using its Position config.

        Args:
            component: Component instance with config.position
        """
        pos = component.config.position
        rendered = component.render()

        self.renderer.add_component(
            renderable=rendered,
            x=pos.x,
            y=pos.y,
            width=pos.width,
            height=pos.height
        )

    def render(self) -> str:
        """
        Render all components with grid positioning.

        Returns:
            ANSI-formatted terminal output string
        """
        return self.renderer.render()

    def clear(self) -> None:
        """Clear all components."""
        self.renderer.clear_components()
