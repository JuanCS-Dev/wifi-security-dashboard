# Versioning Strategy

WiFi Security Dashboard follows **Semantic Versioning 2.0.0** (SemVer).

## Format: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes (API incompatible)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Current Version: 2.0.0

- **2** (MAJOR): v2.0 rewrite with plugin architecture (breaks v1.0 API)
- **0** (MINOR): No new features since v2.0 release
- **0** (PATCH): No bug fixes since v2.0 release

## Version History

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 2.0.0 | 2025-11-10 | MAJOR | Plugin architecture, mock mode, 98% coverage |
| 1.0.0 | 2025-XX-XX | MAJOR | Initial release |

## Breaking Changes Policy

**Breaking changes** only in MAJOR versions:
- v1.x → v2.0: Plugin API introduced
- v2.x → v3.0: Rich → Textual framework (planned Q1 2027)

**Plugin API stability**:
- v2.0 → v2.1: 100% backward compatible
- v2.x: All minor versions compatible
- v3.0: New UI but plugin API preserved

## Version Update Rules

**PATCH (2.0.0 → 2.0.1)**:
- Bug fixes
- Security patches
- Documentation fixes
- Performance improvements (no API changes)

**MINOR (2.0.0 → 2.1.0)**:
- New plugins
- New features (backward compatible)
- Deprecations (with warnings)
- New optional parameters

**MAJOR (2.0.0 → 3.0.0)**:
- Remove deprecated features
- Change plugin API signature
- Breaking UI changes
- Python version requirement change

## Pre-release Versions

**Format**: MAJOR.MINOR.PATCH-PRERELEASE

Examples:
- `2.1.0-alpha.1`: First alpha of v2.1
- `2.1.0-beta.1`: First beta of v2.1
- `2.1.0-rc.1`: Release candidate 1

## VERSION File

Central version source: `VERSION` file (single line)

```bash
# Read version
cat VERSION
# Output: 2.0.0
```

Used by:
- `setup.py` (if added)
- `main_v2.py --version`
- CITATION.cff
- Docker tags

## Git Tags

Versions tagged in Git:

```bash
# Tag release
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0

# List tags
git tag -l "v*"
```

## See Also

- **CHANGELOG.md**: Detailed change history
- **ROADMAP.md**: Planned versions (v2.1, v3.0, v4.0)
- **VERSION**: Current version file

---

**Framework**: Constituição Vértice v3.0 (P4 - Rastreabilidade Total)

**Soli Deo Gloria** ✝️
