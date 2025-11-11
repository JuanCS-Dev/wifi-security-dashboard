#!/usr/bin/env python3
"""
Grid Layout Validator - Air Gap and Overlap Detector
=====================================================

Validates dashboard grid layouts for:
- Air gaps (empty spaces between components)
- Overlaps (components covering same space)
- Out-of-bounds (components exceeding grid dimensions)
- Alignment issues

Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 6 (Integration & Validation)
"""

import yaml
import sys
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass


@dataclass
class Component:
    """Component with position and dimensions"""
    name: str
    type: str
    x: int
    y: int
    width: int
    height: int

    @property
    def x_end(self) -> int:
        return self.x + self.width

    @property
    def y_end(self) -> int:
        return self.y + self.height

    def overlaps(self, other: 'Component') -> bool:
        """Check if this component overlaps with another"""
        return not (
            self.x_end <= other.x or  # This is left of other
            self.x >= other.x_end or  # This is right of other
            self.y_end <= other.y or  # This is above other
            self.y >= other.y_end  # This is below other
        )

    def get_cells(self) -> Set[Tuple[int, int]]:
        """Get all grid cells occupied by this component"""
        cells = set()
        for x in range(self.x, self.x_end):
            for y in range(self.y, self.y_end):
                cells.add((x, y))
        return cells


class GridValidator:
    """Validates grid layouts"""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.components: List[Component] = []
        self.grid_width = 160
        self.grid_height = 60

    def load_config(self) -> bool:
        """Load and parse config file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Parse grid dimensions
            if 'settings' in config and 'terminal_size' in config['settings']:
                self.grid_width = config['settings']['terminal_size']['width']
                self.grid_height = config['settings']['terminal_size']['height']

            # Parse components
            for comp in config.get('components', []):
                pos = comp['position']
                self.components.append(Component(
                    name=comp['title'],
                    type=comp['type'],
                    x=pos['x'],
                    y=pos['y'],
                    width=pos['width'],
                    height=pos['height']
                ))

            return True
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return False

    def validate(self) -> Dict[str, any]:
        """Run all validations"""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }

        # Check out-of-bounds
        for comp in self.components:
            if comp.x < 0 or comp.y < 0:
                results['errors'].append(
                    f"❌ {comp.name}: Negative coordinates ({comp.x}, {comp.y})"
                )
                results['valid'] = False

            if comp.x_end > self.grid_width:
                results['errors'].append(
                    f"❌ {comp.name}: Exceeds grid width (x_end={comp.x_end} > {self.grid_width})"
                )
                results['valid'] = False

            if comp.y_end > self.grid_height:
                results['errors'].append(
                    f"❌ {comp.name}: Exceeds grid height (y_end={comp.y_end} > {self.grid_height})"
                )
                results['valid'] = False

        # Check overlaps
        for i, comp1 in enumerate(self.components):
            for comp2 in self.components[i+1:]:
                if comp1.overlaps(comp2):
                    results['errors'].append(
                        f"❌ OVERLAP: {comp1.name} overlaps {comp2.name}"
                    )
                    results['valid'] = False

        # Check air gaps
        air_gaps = self._detect_air_gaps()
        if air_gaps:
            results['warnings'].extend([
                f"⚠️  AIR GAP: {gap}" for gap in air_gaps
            ])

        # Coverage analysis
        coverage = self._calculate_coverage()
        results['info'].append(
            f"📊 Grid Coverage: {coverage['used_cells']}/{coverage['total_cells']} cells ({coverage['percentage']:.1f}%)"
        )

        if coverage['percentage'] < 70:
            results['warnings'].append(
                f"⚠️  Low coverage ({coverage['percentage']:.1f}%) - Consider filling more space"
            )

        return results

    def _detect_air_gaps(self) -> List[str]:
        """Detect significant air gaps between components"""
        gaps = []

        # Get all occupied cells
        occupied = set()
        for comp in self.components:
            occupied.update(comp.get_cells())

        # Define expected coverage areas (heuristic: should cover most of grid)
        # For now, check for large contiguous empty regions

        # Check horizontal gaps (columns with no components)
        empty_cols = []
        for x in range(self.grid_width):
            if not any((x, y) in occupied for y in range(self.grid_height)):
                empty_cols.append(x)

        # Group consecutive empty columns
        if empty_cols:
            gaps_grouped = []
            start = empty_cols[0]
            end = empty_cols[0]
            for col in empty_cols[1:]:
                if col == end + 1:
                    end = col
                else:
                    if end - start + 1 >= 5:  # At least 5 columns
                        gaps_grouped.append((start, end))
                    start = col
                    end = col
            if end - start + 1 >= 5:
                gaps_grouped.append((start, end))

            for start, end in gaps_grouped:
                width = end - start + 1
                gaps.append(f"Vertical gap at x={start}-{end} (width={width} cols)")

        # Check vertical gaps (rows with no components)
        empty_rows = []
        for y in range(self.grid_height):
            if not any((x, y) in occupied for x in range(self.grid_width)):
                empty_rows.append(y)

        # Group consecutive empty rows
        if empty_rows:
            gaps_grouped = []
            start = empty_rows[0]
            end = empty_rows[0]
            for row in empty_rows[1:]:
                if row == end + 1:
                    end = row
                else:
                    if end - start + 1 >= 3:  # At least 3 rows
                        gaps_grouped.append((start, end))
                    start = row
                    end = row
            if end - start + 1 >= 3:
                gaps_grouped.append((start, end))

            for start, end in gaps_grouped:
                height = end - start + 1
                gaps.append(f"Horizontal gap at y={start}-{end} (height={height} rows)")

        return gaps

    def _calculate_coverage(self) -> Dict[str, any]:
        """Calculate grid coverage percentage"""
        occupied = set()
        for comp in self.components:
            occupied.update(comp.get_cells())

        total_cells = self.grid_width * self.grid_height
        used_cells = len(occupied)
        percentage = (used_cells / total_cells * 100) if total_cells > 0 else 0

        return {
            'total_cells': total_cells,
            'used_cells': used_cells,
            'percentage': percentage
        }

    def print_report(self, results: Dict[str, any]) -> None:
        """Print validation report"""
        print("=" * 70)
        print("GRID LAYOUT VALIDATION REPORT")
        print("=" * 70)
        print(f"Config: {self.config_path}")
        print(f"Grid Size: {self.grid_width}x{self.grid_height}")
        print(f"Components: {len(self.components)}")
        print()

        # Component list
        print("Components:")
        for i, comp in enumerate(self.components, 1):
            print(f"  {i}. {comp.name} ({comp.type})")
            print(f"     Position: ({comp.x}, {comp.y})")
            print(f"     Size: {comp.width}x{comp.height}")
            print(f"     Coverage: ({comp.x}, {comp.y}) → ({comp.x_end-1}, {comp.y_end-1})")
            print()

        print("=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)

        # Errors
        if results['errors']:
            print("\n🚨 ERRORS:")
            for error in results['errors']:
                print(f"  {error}")
        else:
            print("\n✅ No errors found!")

        # Warnings
        if results['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in results['warnings']:
                print(f"  {warning}")
        else:
            print("\n✅ No warnings!")

        # Info
        if results['info']:
            print("\n📊 INFO:")
            for info in results['info']:
                print(f"  {info}")

        print("\n" + "=" * 70)
        if results['valid']:
            print("✅ LAYOUT VALIDATION: PASSED")
        else:
            print("❌ LAYOUT VALIDATION: FAILED")
        print("=" * 70)

    def visualize_grid(self) -> None:
        """Print ASCII visualization of grid"""
        print("\n" + "=" * 70)
        print("GRID VISUALIZATION (Scaled)")
        print("=" * 70)

        # Scale down for terminal display (4x2 cells → 1 character)
        scale_x = 4
        scale_y = 2
        viz_width = self.grid_width // scale_x
        viz_height = self.grid_height // scale_y

        # Create visualization grid
        grid = [[' ' for _ in range(viz_width)] for _ in range(viz_height)]

        # Mark component positions
        chars = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, comp in enumerate(self.components):
            char = chars[i % len(chars)]
            x_start = comp.x // scale_x
            x_end = comp.x_end // scale_x
            y_start = comp.y // scale_y
            y_end = comp.y_end // scale_y

            for y in range(y_start, min(y_end, viz_height)):
                for x in range(x_start, min(x_end, viz_width)):
                    grid[y][x] = char

        # Print grid
        print("+" + "-" * viz_width + "+")
        for row in grid:
            print("|" + "".join(row) + "|")
        print("+" + "-" * viz_width + "+")

        # Legend
        print("\nLegend:")
        for i, comp in enumerate(self.components):
            char = chars[i % len(chars)]
            print(f"  {char} = {comp.name} ({comp.type})")


def main():
    """Entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 validate_grid_layout.py <config.yml>")
        sys.exit(1)

    config_path = sys.argv[1]

    validator = GridValidator(config_path)

    print("Loading configuration...")
    if not validator.load_config():
        sys.exit(1)

    print(f"✅ Loaded {len(validator.components)} components\n")

    # Run validation
    results = validator.validate()

    # Print report
    validator.print_report(results)

    # Print visualization
    validator.visualize_grid()

    # Exit code
    sys.exit(0 if results['valid'] else 1)


if __name__ == "__main__":
    main()
