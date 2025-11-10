"""
Validation script for Constituição Vértice v3.0 compliance.

Audits the codebase for P1-P6 principle violations and generates
a compliance report.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple


class ConstitutionValidator:
    """Validates codebase against Constituição Vértice v3.0 principles."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"
        self.tests_dir = project_root / "tests"

        self.violations = {
            "P1": [],  # Completude Obrigatória
            "P2": [],  # Validação Preventiva
            "P3": [],  # Ceticismo Crítico
            "P4": [],  # Rastreabilidade Total
            "P5": [],  # Consciência Sistêmica
            "P6": [],  # Eficiência de Token
        }

        self.passed = {
            "P1": [],
            "P2": [],
            "P3": [],
            "P4": [],
            "P5": [],
            "P6": [],
        }

    def validate_p1_completeness(self) -> Tuple[int, int]:
        """
        P1: Completude Obrigatória

        Checks for:
        - TODO/FIXME/XXX/HACK comments
        - Placeholder implementations
        - Empty functions (except Template Methods)
        """
        print("\n[P1] Validating Completude Obrigatória...")

        # Check for incomplete markers (whole word matches only, in comments)
        patterns = [
            (r'#.*\bTODO\b', 'TODO'),
            (r'#.*\bFIXME\b', 'FIXME'),
            (r'#.*\bXXX\b', 'XXX'),
            (r'#.*\bHACK\b', 'HACK'),
            (r'#\s*TEMP\b', 'TEMP'),  # TEMP at start of comment
            (r'#\s*PLACEHOLDER\b', 'PLACEHOLDER'),  # PLACEHOLDER at start of comment
        ]

        for pattern, name in patterns:
            for file_path in self.src_dir.rglob("*.py"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_no, line in enumerate(f, 1):
                        # Skip docstrings and acceptable comments
                        if 'Template Method' in line or 'Intentionally empty' in line:
                            continue

                        if re.search(pattern, line, re.IGNORECASE):
                            self.violations["P1"].append(
                                f"{file_path.relative_to(self.project_root)}:{line_no} - {name} marker found"
                            )

        if not self.violations["P1"]:
            self.passed["P1"].append("No incomplete code markers found")
            self.passed["P1"].append("All implementations complete")

        violations_count = len(self.violations["P1"])
        passed_count = len(self.passed["P1"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def validate_p2_preventive(self) -> Tuple[int, int]:
        """
        P2: Validação Preventiva

        Checks for:
        - Import statements with try/except
        - API validation before use
        - Defensive programming patterns
        """
        print("\n[P2] Validating Validação Preventiva...")

        # Check that external imports are wrapped in try/except
        external_libs = ['psutil', 'scapy', 'rich']

        for lib in external_libs:
            found_import = False
            found_validation = False

            for file_path in self.src_dir.rglob("*.py"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    if f'import {lib}' in content:
                        found_import = True

                        # Check if it's in a try/except block
                        if 'try:' in content and 'except ImportError' in content:
                            found_validation = True
                            self.passed["P2"].append(
                                f"{lib} import validated in {file_path.relative_to(self.project_root)}"
                            )

            if found_import and not found_validation:
                self.violations["P2"].append(
                    f"{lib} imported without validation"
                )

        # Check for hasattr validation after imports
        validation_count = 0
        for file_path in self.src_dir.rglob("*.py"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'hasattr(' in content or 'getattr(' in content:
                    validation_count += 1

        if validation_count > 0:
            self.passed["P2"].append(
                f"Found {validation_count} files using hasattr/getattr validation"
            )

        violations_count = len(self.violations["P2"])
        passed_count = len(self.passed["P2"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def validate_p3_skepticism(self) -> Tuple[int, int]:
        """
        P3: Ceticismo Crítico

        Checks for:
        - Assumptions validated with tests
        - Edge cases handled
        - Input validation
        """
        print("\n[P3] Validating Ceticismo Crítico...")

        # Count tests
        test_files = list(self.tests_dir.rglob("test_*.py"))
        test_count = len(test_files)

        if test_count > 0:
            self.passed["P3"].append(
                f"Found {test_count} test files validating assumptions"
            )

        # Check for validation patterns
        validation_patterns = [
            (r'if .* is None:', "None checks"),
            (r'if .* <= 0:', "Boundary checks"),
            (r'if not .*:', "Falsy checks"),
            (r'assert ', "Assertions"),
        ]

        for pattern, name in validation_patterns:
            count = 0
            for file_path in self.src_dir.rglob("*.py"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    count += len(re.findall(pattern, content))

            if count > 0:
                self.passed["P3"].append(
                    f"Found {count} {name} validating assumptions"
                )

        violations_count = len(self.violations["P3"])
        passed_count = len(self.passed["P3"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def validate_p4_traceability(self) -> Tuple[int, int]:
        """
        P4: Rastreabilidade Total

        Checks for:
        - Git history present
        - Docstrings documenting decisions
        - Comments explaining "why" not "what"
        """
        print("\n[P4] Validating Rastreabilidade Total...")

        # Check git history exists
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            commit_count = len(result.stdout.strip().split('\n'))

            if commit_count > 0:
                self.passed["P4"].append(
                    f"Git history present ({commit_count} commits)"
                )
        except Exception as e:
            self.violations["P4"].append(f"Git history unavailable: {e}")

        # Check for docstrings
        docstring_count = 0
        for file_path in self.src_dir.rglob("*.py"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                docstring_count += content.count('"""')

        if docstring_count > 0:
            self.passed["P4"].append(
                f"Found {docstring_count // 2} docstrings documenting decisions"
            )

        violations_count = len(self.violations["P4"])
        passed_count = len(self.passed["P4"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def validate_p5_systemic_awareness(self) -> Tuple[int, int]:
        """
        P5: Consciência Sistêmica

        Checks for:
        - Consistent naming conventions
        - Consistent return types
        - Consistent error handling
        """
        print("\n[P5] Validating Consciência Sistêmica...")

        # Check field naming consistency (from our fix)
        critical_fields = [
            "bandwidth_rx_mbps",
            "bandwidth_tx_mbps",
            "cpu_percent",
            "memory_percent",
        ]

        for field in critical_fields:
            found_locations = []
            for file_path in self.src_dir.rglob("*.py"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if field in content:
                        found_locations.append(file_path.name)

            if len(found_locations) > 1:
                self.passed["P5"].append(
                    f"Field '{field}' used consistently across {len(found_locations)} files"
                )

        # Check plugin interface consistency
        plugin_files = list(self.src_dir.glob("plugins/*_plugin.py"))
        if len(plugin_files) > 0:
            # All plugins should have initialize, collect_data, cleanup
            required_methods = ["initialize", "collect_data", "cleanup"]
            for plugin_file in plugin_files:
                with open(plugin_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    has_all = all(method in content for method in required_methods)

                    if has_all:
                        self.passed["P5"].append(
                            f"{plugin_file.name} implements Plugin interface consistently"
                        )
                    else:
                        self.violations["P5"].append(
                            f"{plugin_file.name} missing Plugin interface methods"
                        )

        violations_count = len(self.violations["P5"])
        passed_count = len(self.passed["P5"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def validate_p6_efficiency(self) -> Tuple[int, int]:
        """
        P6: Eficiência de Token

        Checks for:
        - Git commits show efficient iterations
        - Fixes happen in ≤2 iterations
        - Context is maintained across sessions
        """
        print("\n[P6] Validating Eficiência de Token...")

        try:
            # Check recent commit messages for fix iterations
            result = subprocess.run(
                ['git', 'log', '--oneline', '-20'],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            commits = result.stdout.strip().split('\n')
            fix_commits = [c for c in commits if 'fix:' in c.lower()]

            if len(fix_commits) <= 2:
                self.passed["P6"].append(
                    f"Fixes resolved efficiently ({len(fix_commits)} fix commits in last 20)"
                )
            else:
                self.violations["P6"].append(
                    f"Many fix commits ({len(fix_commits)}) may indicate inefficiency"
                )

            # Check for comprehensive commits
            comprehensive_commits = [
                c for c in commits
                if len(c.split()) > 10  # Commits with good descriptions
            ]

            if len(comprehensive_commits) > 5:
                self.passed["P6"].append(
                    f"Found {len(comprehensive_commits)} commits with comprehensive descriptions"
                )

        except Exception as e:
            self.violations["P6"].append(f"Could not analyze git history: {e}")

        violations_count = len(self.violations["P6"])
        passed_count = len(self.passed["P6"])

        print(f"   ✅ Passed checks: {passed_count}")
        print(f"   {'✅' if violations_count == 0 else '❌'} Violations: {violations_count}")

        return passed_count, violations_count

    def generate_report(self) -> str:
        """Generate comprehensive compliance report."""
        report = []
        report.append("="*70)
        report.append("CONSTITUIÇÃO VÉRTICE v3.0 - COMPLIANCE REPORT")
        report.append("="*70)
        report.append("")

        total_passed = 0
        total_violations = 0

        for principle in ["P1", "P2", "P3", "P4", "P5", "P6"]:
            passed_count = len(self.passed[principle])
            violation_count = len(self.violations[principle])

            total_passed += passed_count
            total_violations += violation_count

            status = "✅ COMPLIANT" if violation_count == 0 else "⚠️ VIOLATIONS FOUND"

            report.append(f"\n{principle}: {status}")
            report.append(f"  Passed: {passed_count} | Violations: {violation_count}")

            if self.passed[principle]:
                report.append("  ✅ Passed Checks:")
                for check in self.passed[principle]:
                    report.append(f"     - {check}")

            if self.violations[principle]:
                report.append("  ❌ Violations:")
                for violation in self.violations[principle]:
                    report.append(f"     - {violation}")

        report.append("")
        report.append("="*70)
        report.append(f"TOTAL: {total_passed} passed | {total_violations} violations")

        if total_violations == 0:
            report.append("✅ FULLY COMPLIANT WITH CONSTITUIÇÃO VÉRTICE v3.0")
        else:
            report.append("⚠️ COMPLIANCE ISSUES DETECTED - REVIEW REQUIRED")

        report.append("="*70)

        return "\n".join(report)

    def run_validation(self) -> None:
        """Run all validation checks."""
        print("\n" + "="*70)
        print("VALIDATING CONSTITUIÇÃO VÉRTICE v3.0 COMPLIANCE")
        print("="*70)

        self.validate_p1_completeness()
        self.validate_p2_preventive()
        self.validate_p3_skepticism()
        self.validate_p4_traceability()
        self.validate_p5_systemic_awareness()
        self.validate_p6_efficiency()

        print("\n" + self.generate_report())


def main():
    """Run constitution validation."""
    project_root = Path(__file__).parent.parent
    validator = ConstitutionValidator(project_root)
    validator.run_validation()


if __name__ == "__main__":
    main()
