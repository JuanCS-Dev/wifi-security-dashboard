"""
Coordinate Converter for Grid Positioning.

Converts character-based coordinates (x, y, width, height) used in config YML
to cell-based coordinates (row, col, row_span, col_span) used by py_cui.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Position:
    """Character-based position (config YML format)."""
    x: int
    y: int
    width: int
    height: int


@dataclass
class GridPosition:
    """Cell-based position (py_cui format)."""
    row: int
    col: int
    row_span: int
    col_span: int


class CoordinateConverter:
    """
    Converts between character-based and cell-based coordinate systems.

    Character-based (Rich/ANSI):
        - Origin (0,0) = top-left corner
        - Units: terminal characters (columns) and lines (rows)
        - Example: x=40, y=16, width=120, height=28

    Cell-based (py_cui/curses):
        - Origin (0,0) = top-left cell
        - Units: grid cells
        - Example: row=16, col=40, row_span=28, col_span=120

    Strategy: Use FINE grid (1 cell = 1 character) for maximum precision.

    Example:
        >>> converter = CoordinateConverter(terminal_width=160, terminal_height=60)
        >>> pos = Position(x=40, y=16, width=120, height=28)
        >>> grid_pos = converter.to_grid(pos)
        >>> print(grid_pos)
        GridPosition(row=16, col=40, row_span=28, col_span=120)
    """

    def __init__(
        self,
        terminal_width: int = 160,
        terminal_height: int = 60,
        grid_rows: int = 60,
        grid_cols: int = 160
    ):
        """
        Initialize converter with terminal and grid dimensions.

        Args:
            terminal_width: Terminal width in characters
            terminal_height: Terminal height in lines
            grid_rows: Number of grid rows (py_cui)
            grid_cols: Number of grid columns (py_cui)

        Note:
            For pixel-perfect positioning, use grid_rows=terminal_height
            and grid_cols=terminal_width (1 cell = 1 character).
        """
        if terminal_width <= 0 or terminal_height <= 0:
            raise ValueError(f"Terminal dimensions must be > 0, got ({terminal_width}x{terminal_height})")

        if grid_rows <= 0 or grid_cols <= 0:
            raise ValueError(f"Grid dimensions must be > 0, got ({grid_rows}x{grid_cols})")

        self.terminal_width = terminal_width
        self.terminal_height = terminal_height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        # Calculate cell dimensions (chars per cell)
        self.chars_per_row = terminal_height / grid_rows
        self.chars_per_col = terminal_width / grid_cols

    def to_grid(self, position: Position) -> GridPosition:
        """
        Convert character-based position to grid-based position.

        Args:
            position: Character-based position (x, y, width, height)

        Returns:
            GridPosition with (row, col, row_span, col_span)

        Algorithm:
            row = floor(y / chars_per_row)
            col = floor(x / chars_per_col)
            row_span = max(1, floor(height / chars_per_row))
            col_span = max(1, floor(width / chars_per_col))

        Note:
            Minimum span is 1 cell to prevent zero-size widgets.
        """
        row = int(position.y / self.chars_per_row)
        col = int(position.x / self.chars_per_col)
        row_span = max(1, int(position.height / self.chars_per_row))
        col_span = max(1, int(position.width / self.chars_per_col))

        # Clamp to grid bounds
        row = max(0, min(row, self.grid_rows - 1))
        col = max(0, min(col, self.grid_cols - 1))

        # Ensure span doesn't exceed grid
        row_span = min(row_span, self.grid_rows - row)
        col_span = min(col_span, self.grid_cols - col)

        return GridPosition(
            row=row,
            col=col,
            row_span=row_span,
            col_span=col_span
        )

    def to_character(self, grid_pos: GridPosition) -> Position:
        """
        Convert grid-based position to character-based position.

        Args:
            grid_pos: Grid-based position (row, col, row_span, col_span)

        Returns:
            Position with (x, y, width, height)

        Algorithm:
            x = col * chars_per_col
            y = row * chars_per_row
            width = col_span * chars_per_col
            height = row_span * chars_per_row
        """
        x = int(grid_pos.col * self.chars_per_col)
        y = int(grid_pos.row * self.chars_per_row)
        width = int(grid_pos.col_span * self.chars_per_col)
        height = int(grid_pos.row_span * self.chars_per_row)

        return Position(x=x, y=y, width=width, height=height)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"CoordinateConverter("
            f"terminal={self.terminal_width}x{self.terminal_height}, "
            f"grid={self.grid_cols}x{self.grid_rows}, "
            f"cell_size={self.chars_per_col:.2f}x{self.chars_per_row:.2f})"
        )
