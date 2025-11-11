#!/usr/bin/env python3
"""
Debug test: Verificar se nossa integração funciona.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.coordinate_converter import CoordinateConverter, Position
import py_cui

# Test coordinate conversion
converter = CoordinateConverter(
    terminal_width=80,
    terminal_height=24,
    grid_rows=24,  # Use same as terminal for 1:1 mapping
    grid_cols=80
)

# Config position: x=5, y=5, width=60, height=8
pos = Position(x=5, y=5, width=60, height=8)
grid_pos = converter.to_grid(pos)

print("=" * 80)
print("COORDINATE CONVERSION DEBUG")
print("=" * 80)
print(f"Input (character-based):  x={pos.x}, y={pos.y}, width={pos.width}, height={pos.height}")
print(f"Output (grid-based):     row={grid_pos.row}, col={grid_pos.col}, row_span={grid_pos.row_span}, col_span={grid_pos.col_span}")
print(f"Converter: {converter}")
print("=" * 80)

# Create py_cui with same grid
root = py_cui.PyCUI(24, 80)
root.set_title('Debug: Grid Position Test')

# Add widget at converted position
widget = root.add_block_label(
    '💻 CPU Test',
    row=grid_pos.row,
    column=grid_pos.col,
    row_span=grid_pos.row_span,
    column_span=grid_pos.col_span,
    center=False
)
widget.set_text('CPU: ▁▂▃▄▅▆▇█ (45%)')

print(f"Widget created: {widget}")
print(f"Widget position: row={widget._start_row}, col={widget._start_col}")
print(f"Widget size: row_span={widget._row_span}, col_span={widget._column_span}")
print(f"Total widgets in root: {len(root.get_widgets())}")
print("=" * 80)
print("Starting py_cui... (press 'q' to quit)")
print("=" * 80)

# Start
root.start()
