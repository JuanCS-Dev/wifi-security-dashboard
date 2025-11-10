# 🏗️ REFACTORING PLAN - WiFi Security Education Dashboard v2.0

**Projeto:** WiFi Security Education Dashboard
**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Versão Atual:** v1.0 (Mock funcional)
**Versão Alvo:** v2.0 (Arquitetura modular inspirada em Sampler)

---

## 📑 Índice

1. [Executive Summary](#1-executive-summary)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target Architecture](#3-target-architecture)
4. [Migration Strategy](#4-migration-strategy)
5. [Sprint Breakdown](#5-sprint-breakdown)
6. [Detailed Implementation Tasks](#6-detailed-implementation-tasks)
7. [Risk Analysis](#7-risk-analysis)
8. [Testing Strategy](#8-testing-strategy)
9. [Success Metrics](#9-success-metrics)
10. [Rollback Plan](#10-rollback-plan)

---

## 1. Executive Summary

### 1.1 Objetivo

Refatorar o WiFi Security Education Dashboard de uma aplicação monolítica para uma arquitetura modular, extensível e configurável via YAML, inspirada no **Sampler**.

### 1.2 Motivação

**Problemas atuais (v1.0):**
- ❌ Código monolítico hardcoded em `main.py` (~1500+ linhas)
- ❌ Componentes acoplados (difícil adicionar novo painel)
- ❌ Lógica de atualização manual (sem rate-based updates)
- ❌ Sem sistema de configuração (tudo no código)
- ❌ Difícil testar componentes isoladamente
- ❌ Sem sistema de plugins/extensões

**Benefícios esperados (v2.0):**
- ✅ Arquitetura modular baseada em plugins
- ✅ Configuração declarativa via YAML
- ✅ Rate-based updates independentes por componente
- ✅ Sistema de triggers/alertas
- ✅ Fácil adicionar novos painéis sem tocar código existente
- ✅ Testável e manutenível
- ✅ Educational mode com dicas contextuais

### 1.3 Timeline

**Duração total:** 6 sprints (~12 semanas)
- Sprint 1-2: Core Architecture (4 semanas)
- Sprint 3-4: Components & Features (4 semanas)
- Sprint 5-6: Polish & Educational Features (4 semanas)

### 1.4 Esforço Estimado

| Fase | Complexidade | Horas Estimadas | Risk Level |
|------|--------------|-----------------|------------|
| Sprint 1 | Alta | 40h | Alto ⚠️ |
| Sprint 2 | Média | 30h | Médio |
| Sprint 3 | Média | 30h | Médio |
| Sprint 4 | Baixa | 25h | Baixo ✅ |
| Sprint 5 | Média | 30h | Médio |
| Sprint 6 | Baixa | 20h | Baixo ✅ |
| **TOTAL** | - | **175h** | - |

---

## 2. Current State Analysis

### 2.1 Estrutura de Arquivos Atual

```
wifi_security_education/
├── main.py                      # Aplicação monolítica (~1500 linhas)
├── test_visual.py               # Testes visuais
├── test_render.py               # Testes de renderização
├── test_dashboard_completo.py   # Teste dashboard completo
├── COMO_TESTAR.md
├── CORRECOES_VISUAIS.md
└── docs/                        # Documentação de pesquisa (criada agora)
    ├── RESEARCH_PART1_SAMPLER_AND_TOOLS.md
    ├── RESEARCH_PART2_PACKET_ANALYSIS.md
    ├── RESEARCH_PART3_ARCHITECTURE.md
    ├── SAMPLER_DEEP_DIVE.md
    ├── REFERENCES.md
    └── REFACTORING_PLAN.md (este arquivo)
```

### 2.2 Componentes Atuais (v1.0)

| Componente | Status | Linhas | Acoplamento | Testabilidade |
|------------|--------|--------|-------------|---------------|
| Header | ✅ Funcionando | ~30 | Baixo | ✅ Bom |
| WiFi Panel | ✅ Funcionando | ~40 | Alto | ⚠️ Médio |
| System Panel | ✅ Funcionando | ~50 | Alto | ⚠️ Médio |
| Traffic Chart | ✅ Funcionando | ~60 | Médio | ⚠️ Médio |
| Devices Panel | ✅ Funcionando | ~40 | Alto | ⚠️ Médio |
| Apps Panel | ✅ Funcionando | ~50 | Alto | ⚠️ Médio |
| Footer | ✅ Funcionando | ~30 | Baixo | ✅ Bom |

**Total:** 7 componentes, ~300 linhas de rendering + ~1200 linhas de lógica/mock

### 2.3 Dependências Atuais

```python
# requirements.txt (atual)
rich>=13.0.0
plotext>=5.0.0
psutil>=5.9.0
```

**Faltando:**
- PyYAML (para config)
- Scapy (para packet analysis)
- pydantic (para validação de config)

### 2.4 Pontos Fortes do v1.0

✅ **Visual funcionando perfeitamente:**
- Todos os painéis renderizam corretamente
- Cores e markup processados corretamente
- Layout 120x46 responsivo
- Mock mode funcional para demonstração

✅ **Código limpo em alguns aspectos:**
- `DashboardColors` - Sistema de cores dinâmicas
- `ProgressRenderer` - Renderização de barras de progresso
- `ChartRenderer` - Integração com plotext

✅ **Bem documentado:**
- `COMO_TESTAR.md` com instruções claras
- `CORRECOES_VISUAIS.md` documentando fixes
- Comentários no código

### 2.5 Pontos Fracos do v1.0

❌ **Arquitetura monolítica:**
```python
# main.py - Tudo em uma classe gigante
class EducationalDashboard:
    def _render_wifi_panel(self):  # 40 linhas
    def _render_system_panel(self):  # 50 linhas
    def _render_traffic_chart(self):  # 60 linhas
    # ... 7 métodos de renderização
    # ... Lógica de mock
    # ... Lógica de captura real
    # ... Tudo acoplado!
```

❌ **Lógica de atualização hardcoded:**
```python
# Todos os componentes atualizam sempre juntos!
def update_dashboard(self):
    self.update_wifi()
    self.update_system()
    self.update_traffic()
    # ... sem rate-based updates individuais
```

❌ **Sem configuração externa:**
```python
# Tudo hardcoded
DASHBOARD_WIDTH = 120
DASHBOARD_HEIGHT = 46
REFRESH_RATE = 0.1
# Impossível mudar sem editar código
```

❌ **Acoplamento alto:**
```python
# WiFi Panel conhece detalhes de mock vs real
def _render_wifi_panel(self):
    if self.mock_mode:
        wifi = self._get_mock_wifi()
    else:
        wifi = self._capture_real_wifi()
    # Viola Single Responsibility Principle
```

---

## 3. Target Architecture

### 3.1 Visão Geral v2.0

```
┌─────────────────────────────────────────────────────────────────┐
│                   DASHBOARD v2.0 ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 1. CONFIG LAYER (YAML)                                          │
│    - dashboard.yml (layout, components, triggers)               │
│    - plugins.yml (plugin configs)                               │
│    - themes.yml (color schemes)                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PLUGIN SYSTEM                                                │
│    ┌──────────────┬──────────────┬──────────────┐              │
│    │ WiFiPlugin   │ SystemPlugin │ NetworkPlugin│              │
│    │ (captures    │ (CPU, RAM,   │ (bandwidth,  │              │
│    │  WiFi data)  │  disk)       │  connections)│              │
│    └──────────────┴──────────────┴──────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. COMPONENT LAYER (Sampler-like)                               │
│    ┌──────────────┬──────────────┬──────────────┬─────────────┐│
│    │ Runchart     │ Sparkline    │ Barchart     │ Textbox     ││
│    │ (time series)│ (compact)    │ (comparison) │ (text/logs) ││
│    └──────────────┴──────────────┴──────────────┴─────────────┘│
│    - Rate-based updates (cada componente tem seu rate_ms)       │
│    - Trigger system (alertas visuais/sonoros)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. LAYOUT ENGINE                                                │
│    - GridLayout (x, y, w, h)                                    │
│    - Responsive resizing                                        │
│    - Multi-page support                                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. RENDER ENGINE                                                │
│    - Rich Live rendering                                        │
│    - Event system (keyboard, triggers)                          │
│    - Educational overlay system                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Estrutura de Diretórios v2.0

```
wifi_security_education/
├── config/                          # Configurações YAML
│   ├── dashboard.yml                # Config principal
│   ├── plugins.yml                  # Configuração de plugins
│   ├── themes/                      # Temas de cores
│   │   ├── default.yml
│   │   └── dark.yml
│   └── educational/                 # Dicas educacionais
│       └── tips.yml
│
├── src/                             # Código fonte
│   ├── __init__.py
│   │
│   ├── core/                        # Core system
│   │   ├── __init__.py
│   │   ├── component.py             # Base Component class
│   │   ├── config_loader.py         # YAML config parser
│   │   ├── plugin_manager.py        # Plugin discovery/loading
│   │   ├── event_bus.py             # Event system
│   │   └── dashboard.py             # Main Dashboard class
│   │
│   ├── components/                  # Componentes visuais
│   │   ├── __init__.py
│   │   ├── runchart.py              # Time series chart
│   │   ├── sparkline.py             # Compact sparkline
│   │   ├── barchart.py              # Bar chart
│   │   ├── gauge.py                 # Gauge/meter
│   │   ├── textbox.py               # Text display
│   │   └── table.py                 # Table display
│   │
│   ├── plugins/                     # Data collection plugins
│   │   ├── __init__.py
│   │   ├── base.py                  # Base Plugin class
│   │   ├── wifi_plugin.py           # WiFi data collection
│   │   ├── system_plugin.py         # System metrics
│   │   ├── network_plugin.py        # Network traffic
│   │   └── packet_plugin.py         # Packet analysis (Scapy)
│   │
│   ├── renderers/                   # Rendering utilities
│   │   ├── __init__.py
│   │   ├── colors.py                # Color schemes
│   │   ├── progress.py              # Progress bars
│   │   └── charts.py                # Chart rendering
│   │
│   ├── layout/                      # Layout system
│   │   ├── __init__.py
│   │   ├── grid.py                  # Grid positioning
│   │   └── responsive.py            # Responsive layout
│   │
│   ├── triggers/                    # Trigger/alert system
│   │   ├── __init__.py
│   │   ├── trigger.py               # Trigger base
│   │   ├── actions.py               # Trigger actions
│   │   └── conditions.py            # Condition evaluators
│   │
│   ├── educational/                 # Educational features
│   │   ├── __init__.py
│   │   ├── tips.py                  # Educational tips
│   │   ├── overlay.py               # Info overlays
│   │   └── explanations.py          # Protocol explanations
│   │
│   └── utils/                       # Utilities
│       ├── __init__.py
│       ├── shell.py                 # Shell command execution
│       ├── validators.py            # Config validation
│       └── logger.py                # Logging system
│
├── tests/                           # Tests
│   ├── __init__.py
│   ├── unit/                        # Unit tests
│   │   ├── test_components.py
│   │   ├── test_plugins.py
│   │   └── test_triggers.py
│   ├── integration/                 # Integration tests
│   │   ├── test_dashboard.py
│   │   └── test_layout.py
│   └── fixtures/                    # Test fixtures
│       ├── mock_data.py
│       └── sample_configs.yml
│
├── scripts/                         # Helper scripts
│   ├── get_wifi_info.sh             # WiFi data collector
│   ├── get_bandwidth.sh             # Bandwidth calculator
│   └── install_deps.sh              # Dependency installer
│
├── docs/                            # Documentation
│   ├── RESEARCH_PART1_SAMPLER_AND_TOOLS.md
│   ├── RESEARCH_PART2_PACKET_ANALYSIS.md
│   ├── RESEARCH_PART3_ARCHITECTURE.md
│   ├── SAMPLER_DEEP_DIVE.md
│   ├── REFERENCES.md
│   ├── REFACTORING_PLAN.md          # Este arquivo
│   ├── API.md                       # API documentation
│   ├── PLUGIN_DEVELOPMENT.md        # Como criar plugins
│   └── USER_GUIDE.md                # Guia do usuário
│
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── setup.py                         # Package setup
├── pyproject.toml                   # Project config
└── README.md                        # Project README
```

### 3.3 Exemplo de Config v2.0

```yaml
# config/dashboard.yml

# ============================================================================
# DASHBOARD CONFIG v2.0
# ============================================================================

version: 2.0
title: WiFi Security Education Dashboard

# Global settings
settings:
  refresh_rate_ms: 100      # UI refresh rate
  terminal_size:
    width: 120
    height: 46
  theme: default            # themes/default.yml
  educational_mode: true    # Mostra dicas educacionais

# ============================================================================
# PLUGINS
# ============================================================================

plugins:
  - name: wifi
    enabled: true
    module: src.plugins.wifi_plugin
    config:
      interface: wlan0
      update_interval: 1000  # ms

  - name: system
    enabled: true
    module: src.plugins.system_plugin
    config:
      update_interval: 2000

  - name: network
    enabled: true
    module: src.plugins.network_plugin
    config:
      interface: wlan0
      update_interval: 500

# ============================================================================
# COMPONENTS (Sampler-style)
# ============================================================================

components:
  # ROW 1: WiFi Signal Chart
  - type: runchart
    title: WiFi Signal Strength
    position: {x: 0, y: 0, width: 60, height: 12}
    plugin: wifi
    data_field: signal_strength
    rate_ms: 1000
    color: green
    triggers:
      - condition: "value < -70"
        actions:
          visual: true
          educational_tip: "signal_weak"

  # ROW 1: System Sparklines
  - type: sparkline
    title: System Resources
    position: {x: 60, y: 0, width: 60, height: 12}
    plugin: system
    data_fields:
      - cpu_percent
      - memory_percent
    rate_ms: 2000
    color: yellow

  # ROW 2: Network Traffic Chart
  - type: runchart
    title: Network Throughput (Mbps)
    position: {x: 0, y: 12, width: 120, height: 15}
    plugin: network
    data_fields:
      - bandwidth_rx
      - bandwidth_tx
    rate_ms: 500
    color: cyan

  # ROW 3: Connected Devices
  - type: table
    title: Connected Devices
    position: {x: 0, y: 27, width: 60, height: 10}
    plugin: network
    data_field: devices
    rate_ms: 5000

  # ROW 3: Top Apps
  - type: barchart
    title: Top Network Apps
    position: {x: 60, y: 27, width: 60, height: 10}
    plugin: network
    data_field: top_apps
    rate_ms: 3000
    color: blue

  # ROW 4: Educational Tips
  - type: textbox
    title: Educational Tip
    position: {x: 0, y: 37, width: 120, height: 6}
    plugin: educational
    data_field: current_tip
    rate_ms: 30000

# ============================================================================
# EDUCATIONAL MODE
# ============================================================================

educational:
  enabled: true
  tips_file: config/educational/tips.yml
  overlay_key: "?"          # Pressionar '?' mostra overlay educacional
  auto_rotate: true         # Roda dicas automaticamente
  rotation_interval: 30000  # ms

# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

keyboard:
  quit: "q"
  pause: "p"
  help: "?"
  next_page: "n"
  prev_page: "p"
  toggle_educational: "e"
```

---

## 4. Migration Strategy

### 4.1 Abordagem: Big Bang vs Incremental

**Decisão: INCREMENTAL ✅**

**Razão:**
- v1.0 está funcionando perfeitamente
- Risco menor de quebrar funcionalidade existente
- Permite testar cada módulo isoladamente
- Maximus e Penelope podem continuar usando v1.0 durante desenvolvimento

### 4.2 Fases de Migração

```
┌─────────────────────────────────────────────────────────────────┐
│                     MIGRATION PHASES                            │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: FOUNDATION (Sprint 1-2)
├── Criar nova estrutura de diretórios
├── Implementar Component base class
├── Implementar Plugin system
├── Implementar Config loader
└── Manter v1.0 intacto em main.py

PHASE 2: COMPONENT MIGRATION (Sprint 3-4)
├── Migrar WiFi Panel → WiFiPlugin + Runchart
├── Migrar System Panel → SystemPlugin + Sparkline
├── Migrar Traffic Chart → NetworkPlugin + Runchart
├── Migrar outros painéis
└── v1.0 e v2.0 coexistem (flag --v2)

PHASE 3: FEATURE PARITY (Sprint 5)
├── Implementar triggers
├── Implementar educational mode
├── Garantir que v2.0 tem TODAS features de v1.0
└── Beta testing com Maximus/Penelope

PHASE 4: CUTOVER (Sprint 6)
├── Tornar v2.0 padrão
├── Mover v1.0 para legacy/
├── Atualizar documentação
└── Celebração! 🎉
```

### 4.3 Compatibilidade Backwards

**Estratégia:**
```bash
# v1.0 (atual) - Mantém funcionando
python main.py --mock

# v2.0 (novo) - Novo entry point
python main.py --v2 --config config/dashboard.yml

# Após Sprint 6
python main.py  # usa v2.0 por padrão
python main.py --legacy  # usa v1.0 se necessário
```

---

## 5. Sprint Breakdown

### 5.1 Sprint Overview

| Sprint | Foco | Duração | Prioridade | Dependencies |
|--------|------|---------|------------|--------------|
| Sprint 1 | Core Architecture | 2 semanas | P0 | None |
| Sprint 2 | Plugin System | 2 semanas | P0 | Sprint 1 |
| Sprint 3 | Component Migration | 2 semanas | P0 | Sprint 2 |
| Sprint 4 | Advanced Components | 2 semanas | P1 | Sprint 3 |
| Sprint 5 | Educational Features | 2 semanas | P1 | Sprint 4 |
| Sprint 6 | Polish & Launch | 2 semanas | P2 | Sprint 5 |

### 5.2 Sprint 1: Core Architecture (P0)

**Objetivo:** Criar fundação do sistema v2.0

**Tasks:**
1. ✅ Setup estrutura de diretórios
2. ✅ Criar `Component` base class
3. ✅ Implementar `ConfigLoader` com PyYAML
4. ✅ Implementar `EventBus` para eventos
5. ✅ Criar `Dashboard` main class
6. ✅ Setup pytest e testes básicos

**Deliverables:**
- [ ] `src/core/component.py` com todos os métodos abstratos
- [ ] `src/core/config_loader.py` carregando YAML
- [ ] `src/core/event_bus.py` funcional
- [ ] `src/core/dashboard.py` com loop principal
- [ ] Tests: `tests/unit/test_component.py`

**Definition of Done:**
- ✅ Todos os testes passando
- ✅ Config YAML sendo parseado corretamente
- ✅ Dashboard vazio renderizando (sem componentes ainda)
- ✅ Code review aprovado

**Estimativa:** 40h
**Risk:** Alto ⚠️ (Nova arquitetura)

---

### 5.3 Sprint 2: Plugin System (P0)

**Objetivo:** Implementar sistema de plugins para coleta de dados

**Tasks:**
1. ✅ Criar `Plugin` base class
2. ✅ Implementar `PluginManager` com auto-discovery
3. ✅ Criar `WiFiPlugin` (migrar lógica de v1.0)
4. ✅ Criar `SystemPlugin` (CPU, RAM, Disk)
5. ✅ Criar `NetworkPlugin` (bandwidth, connections)
6. ✅ Implementar plugin hot-reload (opcional)

**Deliverables:**
- [ ] `src/plugins/base.py` com Plugin interface
- [ ] `src/plugins/wifi_plugin.py` coletando dados WiFi
- [ ] `src/plugins/system_plugin.py` com psutil
- [ ] `src/plugins/network_plugin.py` com bandwidth
- [ ] `src/core/plugin_manager.py` descobrindo plugins
- [ ] Tests: `tests/unit/test_plugins.py`

**Definition of Done:**
- ✅ Todos os plugins coletando dados reais
- ✅ PluginManager carregando plugins de config
- ✅ Mock data disponível para testing
- ✅ Documentação de como criar plugin

**Estimativa:** 30h
**Risk:** Médio

---

### 5.4 Sprint 3: Component Migration (P0)

**Objetivo:** Migrar componentes visuais de v1.0 para v2.0

**Tasks:**
1. ✅ Implementar `Runchart` component
2. ✅ Implementar `Sparkline` component
3. ✅ Implementar `Barchart` component
4. ✅ Implementar `Textbox` component
5. ✅ Migrar WiFi Panel para Runchart + WiFiPlugin
6. ✅ Migrar System Panel para Sparkline + SystemPlugin
7. ✅ Migrar Traffic Chart para Runchart + NetworkPlugin

**Deliverables:**
- [ ] `src/components/runchart.py` com plotext
- [ ] `src/components/sparkline.py` com unicode chars
- [ ] `src/components/barchart.py`
- [ ] `src/components/textbox.py`
- [ ] Dashboard v2.0 renderizando 3 painéis principais
- [ ] Tests: `tests/unit/test_components.py`

**Definition of Done:**
- ✅ Todos os 4 componentes funcionando
- ✅ Dashboard v2.0 com visual similar ao v1.0
- ✅ Rate-based updates funcionando
- ✅ Config YAML controlando componentes

**Estimativa:** 30h
**Risk:** Médio

---

### 5.5 Sprint 4: Advanced Components (P1)

**Objetivo:** Implementar componentes avançados e features adicionais

**Tasks:**
1. ✅ Implementar `Gauge` component
2. ✅ Implementar `Table` component (para devices)
3. ✅ Implementar `GridLayout` engine
4. ✅ Migrar Devices Panel
5. ✅ Migrar Apps Panel
6. ✅ Implementar responsive resizing

**Deliverables:**
- [ ] `src/components/gauge.py`
- [ ] `src/components/table.py`
- [ ] `src/layout/grid.py`
- [ ] Dashboard v2.0 com TODOS os painéis de v1.0
- [ ] Tests: `tests/integration/test_dashboard.py`

**Definition of Done:**
- ✅ Dashboard v2.0 = feature parity com v1.0
- ✅ Layout responsivo funcionando
- ✅ Todos os componentes testados

**Estimativa:** 25h
**Risk:** Baixo ✅

---

### 5.6 Sprint 5: Educational Features (P1)

**Objetivo:** Adicionar features educacionais únicas

**Tasks:**
1. ✅ Implementar `TriggerSystem`
2. ✅ Criar educational tips system
3. ✅ Implementar info overlay (pressionar '?')
4. ✅ Criar biblioteca de dicas sobre protocolos
5. ✅ Implementar packet explanation mode
6. ✅ Criar tutorial interativo

**Deliverables:**
- [ ] `src/triggers/trigger.py` com sistema de alertas
- [ ] `src/educational/tips.py` com dicas rotativas
- [ ] `src/educational/overlay.py` com help overlay
- [ ] `config/educational/tips.yml` com 50+ dicas
- [ ] Tutorial interativo para primeira execução
- [ ] Tests: `tests/unit/test_triggers.py`

**Definition of Done:**
- ✅ Triggers funcionando (visual, sound, bell)
- ✅ Educational mode com dicas contextuais
- ✅ Overlay de ajuda completo
- ✅ Tutorial testado com Maximus/Penelope

**Estimativa:** 30h
**Risk:** Médio

---

### 5.7 Sprint 6: Polish & Launch (P2)

**Objetivo:** Finalização, documentação e lançamento

**Tasks:**
1. ✅ Performance optimization
2. ✅ Error handling robusto
3. ✅ Logging system
4. ✅ Documentação completa
5. ✅ User guide
6. ✅ Plugin development guide
7. ✅ Demo video/screenshots
8. ✅ Cutover para v2.0 como padrão

**Deliverables:**
- [ ] Performance profiling report
- [ ] Exception handling em todos os módulos
- [ ] `docs/USER_GUIDE.md`
- [ ] `docs/PLUGIN_DEVELOPMENT.md`
- [ ] `docs/API.md`
- [ ] README.md atualizado
- [ ] Screenshots/demo
- [ ] v1.0 movido para `legacy/`

**Definition of Done:**
- ✅ Todos os testes passando (100% cobertura core)
- ✅ Documentação completa
- ✅ v2.0 é padrão (`python main.py`)
- ✅ Maximus e Penelope aprovam! 🎉

**Estimativa:** 20h
**Risk:** Baixo ✅

---

## 6. Detailed Implementation Tasks

### 6.1 Component Base Class

```python
# src/core/component.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
import time
from rich.panel import Panel

@dataclass
class Position:
    x: int
    y: int
    width: int
    height: int

@dataclass
class ComponentConfig:
    title: str
    position: Position
    rate_ms: int
    plugin: str
    data_field: str
    color: str = "white"

class Component(ABC):
    """
    Base class para todos os componentes visuais
    Inspirado no Sampler
    """

    def __init__(self, config: ComponentConfig):
        self.config = config
        self.last_update = 0
        self.data = None
        self.plugin_data = {}

    def should_update(self) -> bool:
        """Verifica se componente deve atualizar baseado em rate_ms"""
        now = time.time() * 1000
        elapsed = now - self.last_update
        return elapsed >= self.config.rate_ms

    def update(self, plugin_data: dict):
        """
        Atualiza dados do componente

        Args:
            plugin_data: Dados coletados pelo plugin
        """
        self.plugin_data = plugin_data
        self.data = plugin_data.get(self.config.data_field)
        self.last_update = time.time() * 1000

        # Hook para processamento adicional
        self.on_update()

    def on_update(self):
        """Hook chamado após update (subclasses podem override)"""
        pass

    @abstractmethod
    def render(self) -> Panel:
        """Renderiza componente visual"""
        pass

# Uso:
class Runchart(Component):
    def __init__(self, config: ComponentConfig):
        super().__init__(config)
        self.points = deque(maxlen=config.position.width - 4)

    def on_update(self):
        """Adiciona ponto ao buffer"""
        if self.data is not None:
            self.points.append(float(self.data))

    def render(self) -> Panel:
        # Renderiza gráfico com plotext
        # (código já implementado no SAMPLER_DEEP_DIVE.md)
        pass
```

### 6.2 Plugin Base Class

```python
# src/plugins/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any

class Plugin(ABC):
    """
    Base class para plugins de coleta de dados
    """

    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get('enabled', True)
        self.update_interval = config.get('update_interval', 1000)
        self.last_update = 0

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome único do plugin"""
        pass

    def should_update(self) -> bool:
        """Verifica se deve coletar novos dados"""
        import time
        now = time.time() * 1000
        elapsed = now - self.last_update
        return elapsed >= self.update_interval

    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """
        Coleta dados e retorna dicionário

        Returns:
            Dict com campos de dados (ex: {'cpu_percent': 45.2, 'memory_percent': 78.5})
        """
        pass

    def update(self) -> Dict[str, Any]:
        """Wrapper que chama collect_data e atualiza timestamp"""
        import time
        data = self.collect_data()
        self.last_update = time.time() * 1000
        return data

# Exemplo de uso:
class WiFiPlugin(Plugin):
    @property
    def name(self) -> str:
        return "wifi"

    def collect_data(self) -> Dict[str, Any]:
        interface = self.config.get('interface', 'wlan0')

        # Coleta dados WiFi (já implementado em v1.0)
        return {
            'ssid': self._get_ssid(interface),
            'signal_strength': self._get_signal(interface),
            'channel': self._get_channel(interface),
            'tx_power': self._get_tx_power(interface),
        }

    def _get_signal(self, interface):
        # Implementação já existe em v1.0
        pass
```

### 6.3 Config Loader

```python
# src/core/config_loader.py

import yaml
from pathlib import Path
from typing import List, Dict
from pydantic import BaseModel, ValidationError

class DashboardConfig(BaseModel):
    """Validação de config com pydantic"""
    version: str
    title: str
    settings: dict
    plugins: List[dict]
    components: List[dict]

class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> DashboardConfig:
        """
        Carrega e valida config YAML

        Args:
            config_path: Caminho para config.yml

        Returns:
            DashboardConfig validado

        Raises:
            FileNotFoundError: Se arquivo não existe
            ValidationError: Se config inválido
        """
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(path, 'r') as f:
            raw_config = yaml.safe_load(f)

        # Valida com pydantic
        try:
            config = DashboardConfig(**raw_config)
        except ValidationError as e:
            print(f"Invalid config: {e}")
            raise

        return config

# Uso:
config = ConfigLoader.load('config/dashboard.yml')
print(config.title)  # "WiFi Security Education Dashboard"
```

### 6.4 Main Dashboard

```python
# src/core/dashboard.py

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from typing import List

class Dashboard:
    def __init__(self, config_path: str):
        self.console = Console()
        self.config = ConfigLoader.load(config_path)

        # Initialize systems
        self.plugin_manager = PluginManager(self.config.plugins)
        self.component_factory = ComponentFactory()
        self.event_bus = EventBus()

        # Create components from config
        self.components = []
        for comp_config in self.config.components:
            component = self.component_factory.create(comp_config)
            self.components.append(component)

        # Setup layout
        self.layout_engine = GridLayout(
            width=self.config.settings['terminal_size']['width'],
            height=self.config.settings['terminal_size']['height']
        )

    def update_components(self):
        """Atualiza componentes que precisam"""
        for component in self.components:
            if component.should_update():
                # Pega dados do plugin
                plugin_data = self.plugin_manager.get_data(component.config.plugin)

                # Atualiza componente
                component.update(plugin_data)

    def render_layout(self) -> Layout:
        """Renderiza layout completo"""
        return self.layout_engine.render(self.components)

    def run(self):
        """Main loop"""
        refresh_rate = self.config.settings['refresh_rate_ms'] / 1000

        with Live(console=self.console, screen=True, auto_refresh=False) as live:
            while True:
                # Update plugins
                self.plugin_manager.update_all()

                # Update components
                self.update_components()

                # Render
                layout = self.render_layout()
                live.update(layout, refresh=True)

                # Sleep
                time.sleep(refresh_rate)

# Entry point
if __name__ == "__main__":
    dashboard = Dashboard("config/dashboard.yml")
    dashboard.run()
```

---

## 7. Risk Analysis

### 7.1 Technical Risks

| Risk | Probabilidade | Impacto | Mitigação |
|------|---------------|---------|-----------|
| **Complexidade da arquitetura plugin** | Média | Alto | - Começar simples (sem hot-reload no Sprint 2)<br>- Estudar arquitetura de plugins existentes<br>- Prototipar antes de implementar |
| **Performance degradation** | Baixa | Médio | - Profiling contínuo<br>- Manter rate_ms adequado<br>- Otimizar rendering |
| **Config YAML complexo demais** | Média | Médio | - Manter config simples no início<br>- Validação clara com pydantic<br>- Exemplos bem documentados |
| **Quebra de compatibilidade com v1.0** | Baixa | Alto | - Manter v1.0 funcionando<br>- Feature parity checklist<br>- Beta testing com usuários |
| **Scapy requiring root** | Alta | Médio | - Documentar requisitos claramente<br>- Fallback para mock mode<br>- Considerar alternativas (tcpdump) |

### 7.2 Schedule Risks

| Risk | Probabilidade | Impacto | Mitigação |
|------|---------------|---------|-----------|
| **Sprint 1 mais longo que estimado** | Média | Alto | - Buffer de 1 semana no planejamento<br>- Priorizar P0 features<br>- Cortar P2 se necessário |
| **Dificuldade em testar WiFi features** | Alta | Médio | - Mock data robusto<br>- VMs para testing<br>- Testing manual |
| **Documentação ficando para trás** | Alta | Baixo | - Documentar durante desenvolvimento<br>- Sprint 6 dedicado a polish<br>- Code comments obrigatórios |

### 7.3 User Risks

| Risk | Probabilidade | Impacto | Mitigação |
|------|---------------|---------|-----------|
| **v2.0 confuso para Maximus/Penelope** | Baixa | Alto | - Manter UX similar ao v1.0<br>- Tutorial interativo<br>- Educational mode ativo por padrão |
| **Perda de funcionalidade** | Baixa | Alto | - Feature parity checklist<br>- Beta testing<br>- Rollback plan claro |

---

## 8. Testing Strategy

### 8.1 Test Pyramid

```
                   ┌──────────────┐
                   │   E2E Tests  │  (10%)
                   │  Dashboard   │
                   └──────────────┘
              ┌─────────────────────────┐
              │  Integration Tests      │  (30%)
              │  Plugin + Component     │
              └─────────────────────────┘
         ┌────────────────────────────────────┐
         │       Unit Tests                   │  (60%)
         │  Components, Plugins, Utils        │
         └────────────────────────────────────┘
```

### 8.2 Unit Tests

**Target: 80% code coverage**

```python
# tests/unit/test_components.py

import pytest
from src.components.runchart import Runchart
from src.core.component import ComponentConfig, Position

def test_runchart_should_update():
    """Testa rate-based update logic"""
    config = ComponentConfig(
        title="Test Chart",
        position=Position(0, 0, 40, 10),
        rate_ms=1000,
        plugin="test",
        data_field="value"
    )

    chart = Runchart(config)

    # Should update immediately (first time)
    assert chart.should_update() == True

    # Update once
    chart.update({'value': 42})

    # Should NOT update immediately after
    assert chart.should_update() == False

    # Wait 1 second
    import time
    time.sleep(1.1)

    # Should update now
    assert chart.should_update() == True

def test_runchart_render():
    """Testa renderização"""
    # ... similar tests
```

### 8.3 Integration Tests

```python
# tests/integration/test_dashboard.py

def test_dashboard_loads_config():
    """Testa que dashboard carrega config YAML"""
    dashboard = Dashboard("tests/fixtures/test_config.yml")

    assert dashboard.config.title == "Test Dashboard"
    assert len(dashboard.components) == 2
    assert len(dashboard.plugin_manager.plugins) == 1

def test_dashboard_updates_components():
    """Testa que componentes são atualizados corretamente"""
    # ... test implementation
```

### 8.4 Mock Data

```python
# tests/fixtures/mock_data.py

class MockWiFiPlugin:
    """Mock plugin para testing sem hardware WiFi"""

    def collect_data(self):
        return {
            'ssid': 'Test_Network',
            'signal_strength': -45,
            'channel': 6,
            'tx_power': 20
        }
```

---

## 9. Success Metrics

### 9.1 Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Code coverage** | ≥80% | pytest-cov |
| **Performance** | UI refresh ≤100ms | Profiling |
| **Memory usage** | ≤200MB | psutil monitoring |
| **Startup time** | ≤2s | time command |
| **Config load time** | ≤100ms | Profiling |

### 9.2 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Linter errors** | 0 | pylint, flake8 |
| **Type coverage** | ≥90% | mypy |
| **Cyclomatic complexity** | ≤10 per function | radon |
| **Documentation** | 100% public APIs | pydoc |

### 9.3 User Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to first render** | ≤3s | User testing |
| **Setup difficulty** | "Easy" rating | User feedback |
| **Feature discoverability** | ≥80% features discovered | User testing |
| **Educational value** | ≥4/5 rating | User feedback |

---

## 10. Rollback Plan

### 10.1 Trigger Conditions

Rollback para v1.0 se:
- ❌ Critical bugs em v2.0
- ❌ Performance inaceitável (>500ms refresh)
- ❌ Perda de funcionalidade crítica
- ❌ Feedback negativo de usuários

### 10.2 Rollback Procedure

```bash
# 1. Stop v2.0
pkill -f "main.py --v2"

# 2. Checkout v1.0 branch
git checkout v1.0-stable

# 3. Reinstall dependencies
pip install -r requirements-v1.txt

# 4. Run v1.0
python main.py --mock

# 5. Investigate issue
# ... debug v2.0 em branch separada

# 6. Fix e re-deploy quando pronto
```

### 10.3 Data Preservation

- ✅ Configs YAML versionados em git
- ✅ v1.0 mantido em branch `v1.0-stable`
- ✅ No data loss (app é stateless)

---

## 🎯 Conclusion

Este plano de refatoração fornece um roadmap detalhado para evoluir o WiFi Security Education Dashboard de v1.0 para v2.0, implementando uma arquitetura modular inspirada no Sampler.

**Principais benefícios:**
1. ✅ Arquitetura extensível via plugins
2. ✅ Configuração declarativa via YAML
3. ✅ Rate-based updates independentes
4. ✅ Sistema de triggers educacionais
5. ✅ Fácil manutenção e testing

**Próximos passos imediatos:**
1. 🏁 Revisar este plano com stakeholders (Maximus/Penelope)
2. 🏁 Criar branch `v2.0-dev`
3. 🏁 Iniciar Sprint 1

**Status:** READY TO START 🚀

**Juan-Dev - Soli Deo Gloria ✝️**
