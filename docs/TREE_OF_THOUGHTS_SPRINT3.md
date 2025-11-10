# 🌳 TREE OF THOUGHTS - SPRINT 3: Component Migration

**Projeto:** WiFi Security Education Dashboard v2.0
**Sprint:** 3 - Component Migration
**Framework:** DETER-AGENT (Constituição Vértice v3.0)
**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09

---

## 📋 CONTEXTO

**Sprint Anterior (Sprint 2):**
- ✅ Plugin System completo (SystemPlugin, NetworkPlugin, WiFiPlugin)
- ✅ 258 testes, 96.16% coverage
- ✅ 100% conformidade constitucional
- ✅ Repositório público criado

**Objetivo Sprint 3:**
Implementar componentes visuais (Runchart, Sparkline, Barchart, Textbox) conectando plugins ao Dashboard com renderização terminal usando Rich + Plotext.

**Restrições Constitucionais:**
- P1: Zero TODOs, código completo
- P2: Validar APIs Rich/Plotext antes de usar
- P6: Max 2 iterações com diagnóstico
- Padrão Pagani: Coverage ≥90%, LEI <1.0

---

## 🎯 ANÁLISE DE REQUISITOS

### Componentes a Implementar (4 tipos)

1. **Runchart** - Gráfico de linhas temporal
   - Biblioteca: `plotext`
   - Uso: WiFi signal, Network traffic
   - Data: Time series (histórico 60s)

2. **Sparkline** - Mini-gráfico inline
   - Biblioteca: Unicode chars (`▁▂▃▄▅▆▇█`)
   - Uso: CPU per-core, Memory trend
   - Data: Array pequeno (8-16 valores)

3. **Barchart** - Gráfico de barras
   - Biblioteca: `plotext` ou Rich Progress
   - Uso: Disk usage, Bandwidth por interface
   - Data: Categorical (labels + valores)

4. **Textbox** - Painel de texto formatado
   - Biblioteca: Rich Panel + Text
   - Uso: System info, WiFi SSID/Security
   - Data: Key-value pairs

### Definition of Done
- ✅ 4 componentes herdando de `Component` base class
- ✅ `render()` implementado retornando Rich renderables
- ✅ Rate-based updates funcionando
- ✅ Tests unitários ≥90% coverage cada
- ✅ Dashboard renderizando 3 painéis principais
- ✅ Config YAML controlando layout

---

## 🌳 TREE OF THOUGHTS (5 Abordagens)

### 🌿 ABORDAGEM 1: "Big Bang" - Implementar Tudo de Uma Vez

**Descrição:**
Implementar todos 4 componentes + integração Dashboard em uma única iteração massiva.

**Prós:**
- ✅ Visualização completa do sistema final rapidamente
- ✅ Otimização global (evita refactoring posterior)
- ✅ Menos commits intermediários

**Contras:**
- ❌ Alto risco de bugs difíceis de isolar
- ❌ Difícil debugar (muitas variáveis)
- ❌ Viola P6 (eficiência) - pode gerar ciclos de correção
- ❌ Testing complexo (muitas dependências)

**Conformidade Constitucional:**
- P1 (Completude): ⚠️ Risco de código incompleto por complexidade
- P6 (Eficiência): ❌ VIOLAÇÃO - alta chance de >2 iterações
- Padrão Pagani: ⚠️ Difícil atingir 90% coverage

**Avaliação:** ❌ **REJEITADA** - Viola P6, alto risco

---

### 🌿 ABORDAGEM 2: "Incremental Linear" - Um Componente por Vez

**Descrição:**
Implementar componentes sequencialmente: Textbox → Sparkline → Barchart → Runchart.
Cada componente 100% completo (código + tests + integração) antes do próximo.

**Ordem Justificada:**
1. **Textbox** (mais simples) - Apenas Rich Panel
2. **Sparkline** (Unicode) - Lógica de conversão numérica
3. **Barchart** (plotext básico) - Introduz plotext
4. **Runchart** (plotext avançado) - Time series + buffering

**Prós:**
- ✅ Baixo risco (isola problemas)
- ✅ Feedback rápido (commits incrementais)
- ✅ Fácil debugar
- ✅ Respeita P6 (diagnóstico focado)
- ✅ TDD natural (testa cada peça)

**Contras:**
- ⚠️ Dashboard visual só no final
- ⚠️ Possível refactoring de abstrações

**Conformidade Constitucional:**
- P1 (Completude): ✅ Cada componente 100% antes de avançar
- P6 (Eficiência): ✅ Erros isolados, max 2 iterações viável
- Padrão Pagani: ✅ 90% coverage incremental

**Avaliação:** ✅ **FORTE CANDIDATO** - Baixo risco, alta conformidade

---

### 🌿 ABORDAGEM 3: "Vertical Slice" - Feature Completa por Vez

**Descrição:**
Implementar fatias verticais completas (Plugin → Component → Dashboard → Test).
Exemplo: WiFi Panel completo (WiFiPlugin + Runchart + Dashboard integration + tests).

**Fatias:**
1. **WiFi Signal Panel:** WiFiPlugin → Runchart → Dashboard
2. **System CPU Panel:** SystemPlugin → Sparkline → Dashboard
3. **Network Traffic Panel:** NetworkPlugin → Runchart → Dashboard
4. **System Info Box:** SystemPlugin → Textbox → Dashboard

**Prós:**
- ✅ Valor entregue rapidamente (painel funcional)
- ✅ Testa integração real desde início
- ✅ Feedback visual imediato
- ✅ Alinhado com DDD (domínios isolados)

**Contras:**
- ⚠️ Possível duplicação de código (Runchart usado 2x)
- ⚠️ Refactoring posterior para DRY
- ⚠️ Complexidade moderada (3 camadas simultâneas)

**Conformidade Constitucional:**
- P1 (Completude): ✅ Fatia completa end-to-end
- P5 (Consciência Sistêmica): ✅ Testa impacto no sistema
- P6 (Eficiência): ⚠️ Pode ter refactoring extra

**Avaliação:** ✅ **CANDIDATO VIÁVEL** - Bom feedback, risco moderado

---

### 🌿 ABORDAGEM 4: "TDD Extremo" - Testes Primeiro, Sempre

**Descrição:**
Escrever TODOS os testes de TODOS os componentes ANTES de qualquer implementação.
Depois implementar até todos testes passarem.

**Sequência:**
1. Escrever: `test_textbox.py`, `test_sparkline.py`, `test_barchart.py`, `test_runchart.py`
2. Implementar: `textbox.py`, `sparkline.py`, `barchart.py`, `runchart.py`
3. Integrar: Dashboard + config YAML

**Prós:**
- ✅ 100% conformidade com TDD (Camada 2 DETER-AGENT)
- ✅ Design de API pensado antes
- ✅ Cobertura 100% garantida
- ✅ Zero código morto

**Contras:**
- ❌ Difícil escrever testes sem protótipo
- ❌ Pode gerar over-specification
- ❌ Iterações de ajuste entre test/code
- ❌ Workflow não natural

**Conformidade Constitucional:**
- P1 (Completude): ✅ Testes garantem completude
- P6 (Eficiência): ❌ RISCO - muitas iterações test/code
- Padrão Pagani: ✅ Coverage garantido

**Avaliação:** ⚠️ **CANDIDATO MODERADO** - TDD puro difícil sem exploração

---

### 🌿 ABORDAGEM 5: "Hybrid TDD" - Spike + Test + Implement

**Descrição:**
Combinar exploração rápida (spike) com TDD rigoroso.

**Sequência por Componente:**
1. **Spike (30min):** Protótipo descartável em script isolado
   - Validar API Rich/Plotext (P2)
   - Explorar edge cases
   - Descobrir gotchas
2. **Test (1h):** Escrever tests baseados em spike
   - Mock plugin data
   - Test boundary conditions
3. **Implement (2h):** Código production com TDD
   - Seguir tests
   - Completude obrigatória (P1)
4. **Integrate (30min):** Dashboard + config
5. **Audit (30min):** Conformidade P1-P6

**Ordem:**
Textbox → Sparkline → Barchart → Runchart (simples → complexo)

**Prós:**
- ✅ Valida APIs antes (P2)
- ✅ TDD informado (não cego)
- ✅ Baixo risco (spike descobre problemas)
- ✅ Eficiente (spike evita iterações P6)
- ✅ Incrementos pequenos e testáveis

**Contras:**
- ⚠️ Spike pode ser desperdício se API simples
- ⚠️ Requer disciplina (descartar spike, não reaproveitar)

**Conformidade Constitucional:**
- P1 (Completude): ✅ TDD garante completude
- P2 (Validação): ✅ Spike valida APIs
- P6 (Eficiência): ✅ Spike evita ciclos cegos
- Padrão Pagani: ✅ Coverage ≥90% por TDD

**Avaliação:** ✅ **FAVORITO** - Equilibra exploração + rigor

---

## 🏆 DECISÃO: Hybrid TDD (Abordagem 5)

**Justificativa:**

1. **Conformidade P2 (Validação):**
   - Spike valida Rich/Plotext ANTES de comprometer
   - Descobre APIs quebradas/deprecadas cedo

2. **Conformidade P6 (Eficiência):**
   - Spike economiza tokens (evita 3+ iterações)
   - Descobre gotchas em ambiente isolado

3. **Padrão Pagani:**
   - TDD garante coverage ≥90%
   - Spike garante FPC ≥80% (First-Pass Correctness)

4. **Baixo Risco:**
   - Incrementos pequenos (1 componente/vez)
   - Spike descartável (não contamina prod)

5. **Rastreabilidade (P4):**
   - Spike documenta APIs usadas
   - Testes documentam comportamento esperado

**Red Team (Auto-Crítica):**
- ⚠️ Spike pode virar código production por preguiça → **Mitigação:** Git branch separada para spikes, DELETE após test
- ⚠️ Over-engineering em testes → **Mitigação:** Foco em behavior, não implementation

---

## 📐 ARQUITETURA DE COMPONENTES

### Hierarquia de Classes

```python
Component (ABC)                    # Já existe (Sprint 1)
├── config: ComponentConfig
├── data: Any
├── should_update() → bool
├── update(plugin_data: Dict)
└── render() → Renderable         # ABC method

├── Textbox(Component)             # NOVO Sprint 3
│   └── render() → Panel
│
├── Sparkline(Component)           # NOVO Sprint 3
│   ├── _values: List[float]
│   ├── _to_unicode(values) → str
│   └── render() → Panel
│
├── Barchart(Component)            # NOVO Sprint 3
│   ├── _labels: List[str]
│   ├── _values: List[float]
│   └── render() → Panel (with plotext)
│
└── Runchart(Component)            # NOVO Sprint 3
    ├── _history: Deque[float]
    ├── _timestamps: Deque[float]
    ├── _max_points: int = 60
    └── render() → Panel (with plotext)
```

### Responsabilidades

| Camada | Responsabilidade | Exemplo |
|--------|------------------|---------|
| **Plugin** | Coleta dados raw | `{"signal_strength_dbm": -45}` |
| **Component** | Extrai field, formata | `self.data = -45` |
| **Component.render()** | Gera visual Rich | `Panel(plotext.build())` |
| **Dashboard** | Orquestra layout | `Layout([runchart, sparkline])` |

---

## 📋 PLANO DE EXECUÇÃO (Hybrid TDD)

### Fase 1: Textbox Component (4h)

**1.1 Spike (30min)**
```python
# spike_textbox.py
from rich.panel import Panel
from rich.text import Text

# Testar:
# - Rich Panel borders/styles
# - Text formatting (bold, colors)
# - Key-value layout
# - Emoji support
```

**1.2 Tests (1h)**
```python
# tests/unit/test_textbox.py
- test_textbox_initialization
- test_textbox_update_extracts_data
- test_textbox_render_returns_panel
- test_textbox_format_key_value
- test_textbox_empty_data_handling
- test_textbox_rate_based_update
```

**1.3 Implementation (2h)**
```python
# src/components/textbox.py
class Textbox(Component):
    def render(self) -> Panel:
        # Implementação completa (P1)
        # Sem TODOs
```

**1.4 Integration (30min)**
```yaml
# config/dashboard.yml
components:
  - type: textbox
    title: "System Info"
    plugin: system
    data_field: uptime_seconds
```

---

### Fase 2: Sparkline Component (4h)

**2.1 Spike (30min)**
```python
# spike_sparkline.py
# Testar:
# - Unicode block chars: ▁▂▃▄▅▆▇█
# - Normalização 0-100 → 0-7 (8 chars)
# - Edge cases: all zeros, negatives
# - Color gradients (Rich)
```

**2.2 Tests (1h)**
```python
# tests/unit/test_sparkline.py
- test_sparkline_unicode_conversion
- test_sparkline_normalization
- test_sparkline_empty_array
- test_sparkline_single_value
- test_sparkline_all_same_values
- test_sparkline_render_with_colors
```

**2.3 Implementation (2h)**
```python
# src/components/sparkline.py
class Sparkline(Component):
    CHARS = "▁▂▃▄▅▆▇█"

    def _to_unicode(self, values: List[float]) -> str:
        # Normalização + conversão (P1)

    def render(self) -> Panel:
        # Rich Panel com sparkline (P1)
```

**2.4 Integration (30min)**

---

### Fase 3: Barchart Component (5h)

**3.1 Spike (1h)**
```python
# spike_barchart.py
import plotext as plt

# Testar:
# - plotext.bar() API
# - Terminal size handling
# - Color schemes
# - Label truncation
```

**3.2 Tests (1.5h)**
```python
# tests/unit/test_barchart.py
- test_barchart_plotext_integration
- test_barchart_empty_data
- test_barchart_single_bar
- test_barchart_many_bars (20+)
- test_barchart_negative_values
- test_barchart_label_truncation
```

**3.3 Implementation (2h)**
```python
# src/components/barchart.py
class Barchart(Component):
    def render(self) -> Panel:
        # plotext → string → Panel (P1)
```

**3.4 Integration (30min)**

---

### Fase 4: Runchart Component (6h)

**4.1 Spike (1h)**
```python
# spike_runchart.py
import plotext as plt
from collections import deque

# Testar:
# - Time series plotting
# - Deque circular buffer
# - Multi-line plots
# - X-axis time formatting
```

**4.2 Tests (2h)**
```python
# tests/unit/test_runchart.py
- test_runchart_buffer_management
- test_runchart_max_points_limit
- test_runchart_time_series_plot
- test_runchart_empty_history
- test_runchart_single_point
- test_runchart_buffer_overflow
- test_runchart_multiple_series
```

**4.3 Implementation (2.5h)**
```python
# src/components/runchart.py
class Runchart(Component):
    def __init__(self, config):
        super().__init__(config)
        self._history = deque(maxlen=60)
        self._timestamps = deque(maxlen=60)

    def update(self, plugin_data):
        # Append to history (P1)

    def render(self) -> Panel:
        # plotext line chart (P1)
```

**4.4 Integration (30min)**

---

### Fase 5: Dashboard Integration (3h)

**5.1 Config YAML (1h)**
```yaml
# config/dashboard.yml
components:
  - type: runchart
    title: "WiFi Signal Strength"
    plugin: wifi
    data_field: signal_strength_dbm
    position: {x: 0, y: 0, width: 60, height: 20}

  - type: sparkline
    title: "CPU Cores"
    plugin: system
    data_field: cpu_per_core
    position: {x: 60, y: 0, width: 60, height: 10}

  - type: textbox
    title: "System Info"
    plugin: system
    data_field: uptime_seconds
    position: {x: 60, y: 10, width: 60, height: 10}
```

**5.2 Dashboard.render_layout() (1h)**
```python
# src/core/dashboard.py
def render_layout(self) -> Layout:
    # Instanciar componentes do config
    # Posicionar com Rich Layout
    # Rate-based updates (já existe)
```

**5.3 Integration Tests (1h)**
```python
# tests/integration/test_dashboard_render.py
- test_dashboard_renders_all_components
- test_dashboard_layout_positioning
- test_dashboard_updates_components
```

---

### Fase 6: Auditoria Conformidade (2h)

**6.1 Coverage Check**
```bash
pytest --cov=src/components --cov-report=term-missing
# Target: ≥90% cada componente
```

**6.2 Checklist P1-P6**
- [ ] P1: Zero TODOs em componentes
- [ ] P2: APIs Rich/Plotext validadas
- [ ] P3: Design questionado (red team)
- [ ] P4: Código rastreável (docs citadas)
- [ ] P5: Impacto sistêmico avaliado
- [ ] P6: Max 2 iterações respeitado

**6.3 Padrão Pagani**
- [ ] LEI < 1.0 (zero lazy code)
- [ ] Coverage ≥90% (4 componentes + integration)
- [ ] FPC ≥80% (testes passam first-pass)

---

## 📊 MÉTRICAS PROJETADAS

### Coverage Estimado
```
src/components/textbox.py      95%  ✅
src/components/sparkline.py    93%  ✅
src/components/barchart.py     91%  ✅
src/components/runchart.py     92%  ✅
src/core/dashboard.py          85%  ✅ (↑ from 80%)

OVERALL: 94% (↑ from 96.16%)
```

### Tests Estimados
```
test_textbox.py         8 testes
test_sparkline.py       9 testes
test_barchart.py       10 testes
test_runchart.py       12 testes
test_dashboard_render   6 testes

TOTAL: +45 testes (258 → 303)
```

### Tempo Estimado
```
Textbox:     4h
Sparkline:   4h
Barchart:    5h
Runchart:    6h
Integration: 3h
Auditoria:   2h

TOTAL: 24h (vs estimativa 30h - buffer 6h)
```

---

## 🎯 RISCOS E MITIGAÇÕES

### Risco 1: Plotext API Breaking Changes
**Probabilidade:** Baixa
**Impacto:** Alto
**Mitigação:**
- Spike valida API antes (P2)
- Pin version em requirements: `plotext==5.2.8`

### Risco 2: Terminal Size Variável
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:**
- Testes com múltiplos tamanhos (80x24, 120x46, 160x50)
- Rich Layout responsivo

### Risco 3: Unicode Rendering em Terminais Antigos
**Probabilidade:** Média
**Impacto:** Baixo
**Mitigação:**
- Fallback ASCII para Sparkline: `[###---]`
- Detectar capabilities do terminal

### Risco 4: Performance (60 FPS?)
**Probabilidade:** Média
**Impacto:** Alto
**Mitigação:**
- Rate-based updates (já implementado)
- Buffer plotext renders (cache)
- Profile com `cProfile`

---

## ✅ DEFINITION OF DONE (Sprint 3)

### Funcional
- [ ] 4 componentes visuais funcionando (Textbox, Sparkline, Barchart, Runchart)
- [ ] Dashboard renderiza 3 painéis principais
- [ ] Rate-based updates em produção
- [ ] Config YAML controla layout

### Qualidade
- [ ] Coverage ≥90% (4 componentes + integration)
- [ ] 45+ novos testes passando
- [ ] Zero TODOs, zero placeholders (P1)
- [ ] LEI < 1.0 (Padrão Pagani)

### Conformidade
- [ ] P1-P6 validados (checklist)
- [ ] Spike branches deletadas
- [ ] Documentação atualizada (README)
- [ ] Tag git `v2.0-sprint3-complete`

### Entrega
- [ ] Commit descritivo
- [ ] Push para GitHub
- [ ] Relatório conformidade `CONFORMIDADE_FINAL_SPRINT3.md`

---

## 📚 REFERÊNCIAS TÉCNICAS

### Rich Library
- Docs: https://rich.readthedocs.io/
- Panel: https://rich.readthedocs.io/en/stable/panel.html
- Layout: https://rich.readthedocs.io/en/stable/layout.html
- Text: https://rich.readthedocs.io/en/stable/text.html

### Plotext
- Docs: https://github.com/piccolomo/plotext
- Bar charts: `plt.bar(labels, values)`
- Line plots: `plt.plot(x, y)`
- Terminal sizing: `plt.plotsize(width, height)`

### Unicode Block Chars
- Sparkline: `▁▂▃▄▅▆▇█` (U+2581 to U+2588)
- Braille: `⠀⠁⠂⠃⠄⠅⠆⠇` (alta densidade)

---

## 🎓 LIÇÕES DO SPRINT 2 APLICADAS

1. **Lazy Loading:** Imports dinâmicos em `render()` se necessário
2. **Mock Strategy:** Fixtures para plugin data
3. **Auto-Recovery:** Componentes resilientes a dados vazios
4. **Documentation First:** Docstrings antes do código

---

**Próxima Ação:** Executar Fase 1 (Textbox Component)

**Soli Deo Gloria ✝️**
**Constituição Vértice v3.0 - Framework DETER-AGENT**
