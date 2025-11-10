# Contributing Quick Start

Get started contributing to WiFi Security Dashboard in 10 minutes.

## Prerequisites

- Git installed
- Python 3.10+
- GitHub account

## Quick Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/wifi_security_education.git
cd wifi_security_education

# 2. Setup development environment
bash scripts/setup.sh

# 3. Create feature branch
git checkout -b feature/my-contribution

# 4. Make changes, write tests
# ... edit code ...
pytest tests/

# 5. Run quality checks
make validate  # Black, isort, flake8, mypy

# 6. Commit (detailed message required)
git add .
git commit -m "feat: Add [feature] following P1-P6 principles

Detailed description...

Soli Deo Gloria ✝️"

# 7. Push and create PR
git push origin feature/my-contribution
# Then open PR on GitHub
```

## P1-P6 Principles (Must Follow)

**P1: Completude Obrigatória** - No TODOs, all code complete
**P2: Validação Preventiva** - Validate dependencies before use
**P3: Ceticismo Crítico** - Test all assumptions
**P4: Rastreabilidade Total** - Document all decisions
**P5: Consciência Sistêmica** - Maintain system consistency
**P6: Eficiência de Token** - Fix issues in ≤2 iterations

## Quality Targets

- **Test Coverage**: ≥98%
- **FPC (First-Pass Correctness)**: ≥95%
- **LEI (Lazy Execution Index)**: <1.0
- **CRS (Context Retention Score)**: ≥95%

## Common Contributions

### Add a Plugin

See [PLUGIN_API.md](./PLUGIN_API.md) for complete guide.

```python
# src/plugins/my_plugin.py
from src.core.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self, mock_mode=True):
        super().__init__(name="my_plugin", update_rate_ms=1000)
        self.mock_mode = mock_mode

    def collect_data(self):
        return {"value": 42}  # Replace with actual logic
```

### Fix a Bug

1. Find issue on GitHub
2. Create branch: `git checkout -b fix/issue-123`
3. Fix bug + add regression test
4. Run `make test` (must pass)
5. Commit with "fix:" prefix
6. Open PR referencing issue

### Improve Documentation

1. Find doc gap or error
2. Edit relevant .md file
3. Follow markdown style (markdownlint)
4. Commit with "docs:" prefix
5. Open PR

## Pre-commit Hooks (Recommended)

```bash
pip install pre-commit
pre-commit install
# Now hooks run automatically on commit
```

## Need Help?

- **Full Guide**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **FAQ**: [FAQ.md](./FAQ.md)
- **Support**: [.github/SUPPORT.md](../.github/SUPPORT.md)
- **GitHub Issues**: Ask questions with `[Question]` tag

---

**Framework**: Constituição Vértice v3.0 (P1-P6)

**Soli Deo Gloria** ✝️
