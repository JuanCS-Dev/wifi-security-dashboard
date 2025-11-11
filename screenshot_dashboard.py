#!/usr/bin/env python3
"""
Capture clean screenshot of dashboard for visual validation.
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.dashboard import Dashboard
from src.core.grid_renderer import GridDashboardRenderer


def strip_ansi(text):
    """Remove ANSI codes for clean visualization."""
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*[mHJKhlABCDEFG]')
    return ansi_pattern.sub('', text)


def main():
    # Create dashboard
    dashboard = Dashboard('config/dashboard_grid_complex.yml', mock_mode=True)

    # Update components once
    dashboard.update_components()

    # Create grid renderer
    grid_renderer = GridDashboardRenderer(width=160, height=60)

    # Add all components
    for component in dashboard.components:
        grid_renderer.add_from_component(component)

    # Render
    output = grid_renderer.render()

    # Strip ANSI for clean view
    clean_output = strip_ansi(output)

    # Print line by line with line numbers
    lines = clean_output.split('\n')

    print("="*160)
    print("DASHBOARD VISUAL SCREENSHOT (Clean - No ANSI)")
    print("="*160)
    print()

    for i, line in enumerate(lines[:60], 1):  # First 60 lines
        # Show line number and content
        print(f"{i:3d} | {line}")

    print()
    print("="*160)
    print(f"Total lines: {len(lines)}")
    print("="*160)


if __name__ == "__main__":
    main()
