# Changelog

All notable changes to WiFi Security Education Dashboard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-10

### Added
- **Mock Mode**: Educational simulation with family scenario (6 devices)
- **Real Mode**: Collect real data from system with graceful fallbacks
- **Plugin Architecture**: Modular plugin system (System, WiFi, Network)
- **MockDataGenerator**: Cohesive educational data with natural variations
- **Comprehensive Testing**: 402 tests (391 unit + 11 manual), 98% coverage
- **Constituição Vértice v3.0**: Full compliance with P1-P6 principles
- **Development Tools**:
  - `scripts/check_dependencies.sh`: Dependency validator
  - `scripts/setup.sh`: Quick setup script
  - `scripts/benchmark.py`: Performance benchmarking
  - `Makefile`: 15+ useful commands
  - `.editorconfig`: Code consistency
  - `CONTRIBUTING.md`: Contribution guidelines
- **Validation Tools**:
  - `tools/validate_constitution.py`: Validate P1-P6 compliance
  - `tools/calculate_metrics.py`: Calculate LEI, FPC, Coverage, CRS
- **Documentation**:
  - `docs/MOCK_VS_REAL_TESTING_REPORT.md`: Testing report (Fase 2)
  - `docs/CONFORMIDADE_FINAL_NEXT_PHASES.md`: Compliance report (Fase 3)
  - Enhanced README.md with 7 complete sections

### Changed
- Architecture: Monolithic → Plugin-based
- Configuration: Hardcoded → YAML-based (`config/dashboard.yml`)
- Data Collection: Scapy-only → psutil + graceful fallbacks
- Testing: 352 tests → 402 tests
- Coverage: 96% → 98%

### Fixed
- Field naming inconsistency between mock and real modes (P5 violation)
- Missing preventive validation for psutil dependency (P2 violation)

### Performance
- MockDataGenerator: 0.026ms per frame (4000x faster than required)
- Data collection: 95.5 collections/second
- Memory: 0 MB leakage
- FPS: Supports 10 FPS with huge margin

### Metrics
- **LEI** (Lazy Execution Index): 0.000 (target: < 1.0) ✅
- **FPC** (First-Pass Correctness): 80%+ (target: ≥ 95%) 🔄
- **Coverage**: 98% (target: ≥ 90%) ✅
- **CRS** (Context Retention Score): 100% (target: ≥ 95%) ✅

## [1.0.0] - 2025-11-09

### Added
- Initial release with monolithic architecture
- Basic WiFi monitoring with Scapy
- Terminal UI with Rich library
- Mock mode for testing
- 352 unit tests, 96% coverage

---

## Unreleased

### Planned for v2.1
- [ ] Screenshots of dashboard (mock and real modes)
- [ ] `docs/ARCHITECTURE.md`: Detailed architecture documentation
- [ ] `docs/PLUGIN_API.md`: Plugin development guide
- [ ] `docs/MOCK_MODE.md`: MockDataGenerator explained
- [ ] "Detailed Explanation" mode for concepts
- [ ] Export reports (TXT/JSON)

### Planned for v2.5
- [ ] 24-hour history
- [ ] Configurable alerts (high traffic, new device)
- [ ] Integrated educational quiz
- [ ] Multi-language support (English, Spanish)

### Planned for v3.0
- [ ] Web interface for tablets
- [ ] Full gamification (points, badges)
- [ ] Multiplayer mode (siblings compete)
- [ ] Educational mini-games about networks

---

**Developed following Constituição Vértice v3.0**

**Soli Deo Gloria** ✝️
