# 🔍 AIR GAPS ANALYSIS - SPRINT 2

**WiFi Security Education Dashboard v2.0**
**Author:** Juan-Dev - Soli Deo Gloria ✝️
**Date:** 2025-11-09
**Framework:** Constituição Vértice v3.0 - P1 (Completude Obrigatória)

---

## 📊 Executive Summary

Análise sistemática de **air gaps** (lacunas de funcionalidade) no Sprint 2 (Plugin System).
Objetivo: 100% de conformidade com P1 (Completude Obrigatória) - zero TODOs, zero placeholders.

**Status:** ⚠️ **AIR GAPS IDENTIFICADOS - CORREÇÕES NECESSÁRIAS**

---

## 🎯 Metodologia de Análise

### Critérios de Air Gap

Um "air gap" é considerado qualquer:
1. **Funcionalidade incompleta** - Código que não executa completamente seu propósito
2. **Dependência não resolvida** - Imports que falham ou bibliotecas ausentes
3. **Placeholder code** - Código temporário marcado para substituição
4. **Error handling incompleto** - Exceções não tratadas adequadamente
5. **Tests falhando** - Testes que não passam indicam funcionalidade quebrada

---

## 🔴 AIR GAPS IDENTIFICADOS

### Gap #1: psutil Dependency Missing

**Severidade:** 🔴 CRÍTICA
**Arquivo:** `src/plugins/system_plugin.py`, `src/plugins/network_plugin.py`
**Linha:** Imports lazy loading

**Problema:**
```python
# src/plugins/system_plugin.py:60-64
try:
    import psutil
    self.psutil = psutil
except ImportError:
    raise RuntimeError("psutil library not installed. Install with: pip install psutil")
```

**Impacto:**
- Plugins SystemPlugin e NetworkPlugin **não funcionam** sem psutil instalado
- Testes podem passar (lazy loading), mas runtime falha
- Dashboard **crasheia** ao tentar inicializar plugins

**Evidência:**
```bash
$ python3 -c "import psutil"
ModuleNotFoundError: No module named 'psutil'
```

**Correção Necessária:**
1. Instalar psutil no sistema OR
2. Criar mock plugins para ambiente sem psutil OR
3. Documentar como pre-requisito obrigatório

**Status:** ⚠️ PENDENTE

---

### Gap #2: Dashboard Tests Desatualizados

**Severidade:** 🟡 MÉDIA
**Arquivo:** `tests/unit/test_dashboard.py`
**Linhas:** 143-453

**Problema:**
Dashboard foi modificado para usar PluginManager, mas testes ainda esperam `_get_mock_plugin_data()` que foi removido.

**Testes Afetados:**
- `test_update_components_updates_when_ready` - PARCIALMENTE CORRIGIDO
- `test_update_components_publishes_event` - PRECISA CORREÇÃO
- `test_update_components_handles_exceptions` - PRECISA CORREÇÃO
- `test_get_mock_plugin_data_*` - 4 testes OBSOLETOS

**Impacto:**
- Testes não validam integração real com PluginManager
- Coverage enganoso (testa código que não existe mais)

**Correção Necessária:**
1. Adicionar `@patch('src.core.dashboard.PluginManager')` em todos os testes
2. Mockar `get_plugin_data()` retornando dados de teste
3. Remover testes de `_get_mock_plugin_data` (função removida)

**Status:** 🟡 PARCIALMENTE CORRIGIDO (1/6 testes atualizados)

---

### Gap #3: WiFiPlugin Plataform Dependencies

**Severidade:** 🟡 MÉDIA
**Arquivo:** `src/plugins/wifi_plugin.py`
**Linhas:** 63-88, 114-137

**Problema:**
WiFiPlugin depende de comandos de sistema que podem não existir:
- `nmcli` (NetworkManager) - não disponível em todas as distribuições
- `iwconfig` (wireless-tools) - deprecated em algumas distros
- `/proc/net/wireless` - apenas Linux

**Código:**
```python
def _has_nmcli(self) -> bool:
    """Check if nmcli is available"""
    try:
        subprocess.run(['nmcli', '--version'], capture_output=True, timeout=1)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
```

**Impacto:**
- WiFiPlugin **silenciosamente retorna dados vazios** sem nmcli/iwconfig
- Erro não fica claro para usuário
- Dashboard funciona mas sem dados de WiFi

**Correção Necessária:**
1. Melhorar mensagens de erro em `initialize()`
2. Documentar dependências opcionais
3. Adicionar fallback mock para desenvolvimento

**Status:** ⚠️ FUNCIONAL MAS SUBÓTIMO

---

### Gap #4: Event Bus History Limite Hardcoded

**Severidade:** 🟢 BAIXA
**Arquivo:** `src/core/event_bus.py`
**Linha:** 97

**Problema:**
```python
self._max_history: int = 100  # Hardcoded limit
```

Limite de 100 eventos hardcoded, não configurável.

**Impacto:**
- Em dashboards com muitos eventos, histórico se perde rapidamente
- Não há como ajustar para debugging (aumentar limite)
- Violação de princípio de configurabilidade

**Correção Necessária:**
1. Mover `max_history` para DashboardConfig
2. Permitir override via parâmetro no construtor

**Status:** 🟢 FUNCIONAL (mas não ideal)

---

### Gap #5: Plugin Error Recovery

**Severidade:** 🟡 MÉDIA
**Arquivo:** `src/plugins/base.py`
**Linhas:** 213-248

**Problema:**
```python
def collect_safe(self) -> Dict[str, Any]:
    try:
        data = self.collect_data()
        # ...
    except Exception as e:
        self._error_count += 1
        self._last_error = str(e)
        self._status = PluginStatus.ERROR
        return {}  # Plugin fica em ERROR state permanentemente
```

Plugin que entra em ERROR state **nunca recupera automaticamente**.
Requer chamada manual de `reset_errors()`.

**Impacto:**
- Erro transitório (rede down 1 segundo) = plugin morto permanentemente
- Dashboard precisa implementar auto-recovery (não implementado)

**Correção Necessária:**
1. Adicionar auto-recovery após N sucessos OR
2. Documentar como comportamento intencional
3. Implementar health check no PluginManager

**Status:** ⚠️ DESIGN DECISION NEEDED

---

### Gap #6: Missing Tests for System/Network/WiFi Plugins

**Severidade:** 🟡 MÉDIA
**Arquivos:** `tests/unit/test_system_plugin.py`, `test_network_plugin.py`, `test_wifi_plugin.py`
**Status:** ❌ NÃO EXISTEM

**Problema:**
Plugins concretos (SystemPlugin, NetworkPlugin, WiFiPlugin) **não têm testes unitários**.

**Coverage Atual:**
```
src/plugins/system_plugin.py    48    42    12%
src/plugins/network_plugin.py   42    35    17%
src/plugins/wifi_plugin.py      154   130   16%
```

**Impacto:**
- 12-17% coverage é CRÍTICO (meta: ≥90%)
- Bugs não detectados
- Refactoring perigoso

**Correção Necessária:**
1. Criar `test_system_plugin.py` com mocks de psutil
2. Criar `test_network_plugin.py` com mocks de psutil
3. Criar `test_wifi_plugin.py` com mocks de subprocess

**Status:** 🔴 CRÍTICO - PRECISA URGENTE

---

## 📊 Air Gaps Summary

| Gap ID | Severidade | Arquivo | Status | Priority |
|--------|------------|---------|--------|----------|
| #1 | 🔴 CRÍTICA | system_plugin.py | PENDENTE | P0 |
| #2 | 🟡 MÉDIA | test_dashboard.py | PARCIAL | P1 |
| #3 | 🟡 MÉDIA | wifi_plugin.py | FUNCIONAL | P2 |
| #4 | 🟢 BAIXA | event_bus.py | FUNCIONAL | P3 |
| #5 | 🟡 MÉDIA | base.py | DESIGN | P1 |
| #6 | 🔴 CRÍTICA | tests/unit/ | NÃO EXISTE | P0 |

**Total Air Gaps:** 6
**Críticos:** 2
**Médios:** 3
**Baixos:** 1

---

## 🔧 Plano de Correção

### Fase 1: Críticos (P0) - BLOQUEADORES

**Gap #1: psutil Dependency**
```bash
# Opção A: Instalar globalmente (requer sudo)
sudo apt-get install python3-psutil

# Opção B: Venv (recomendado)
python3 -m venv venv
source venv/bin/activate
pip install psutil

# Opção C: Documentar como dependência
# Atualizar README.md e requirements-v2.txt
```

**Gap #6: Missing Plugin Tests**
- Criar `test_system_plugin.py` (mock psutil)
- Criar `test_network_plugin.py` (mock psutil)
- Criar `test_wifi_plugin.py` (mock subprocess)
- Target: 90%+ coverage cada

**Estimativa:** 4 horas

---

### Fase 2: Médios (P1) - IMPORTANTES

**Gap #2: Dashboard Tests**
- Atualizar todos os testes com PluginManager mock
- Remover testes obsoletos (_get_mock_plugin_data)

**Gap #5: Plugin Error Recovery**
- Decidir estratégia (auto-recovery vs manual)
- Implementar solução escolhida
- Documentar comportamento

**Estimativa:** 3 horas

---

### Fase 3: Baixos (P2-P3) - MELHORIAS

**Gap #3: WiFiPlugin Dependencies**
- Documentar dependências opcionais
- Melhorar mensagens de erro

**Gap #4: Event Bus History Limite**
- Tornar configurável via DashboardConfig

**Estimativa:** 2 horas

---

## ✅ Critérios de Resolução

Um air gap é considerado **RESOLVIDO** quando:

1. ✅ **Funcionalidade 100%** - Código executa completamente
2. ✅ **Tests passando** - Testes validam comportamento
3. ✅ **Coverage ≥90%** - Código coberto por testes
4. ✅ **Sem dependências pendentes** - Todas libs disponíveis
5. ✅ **Documentado** - Comportamento documentado
6. ✅ **Zero TODOs** - Sem marcadores de trabalho futuro

---

## 📈 Impacto na Conformidade

### Before Air Gaps Resolution
```
Plugin Base:     97% ✅
Plugin Manager:  93% ✅
System Plugin:   12% ❌
Network Plugin:  17% ❌
WiFi Plugin:     16% ❌
Dashboard:       41% ❌ (testes desatualizados)

OVERALL: 46% ❌ (meta: 90%)
```

### After Air Gaps Resolution (Projected)
```
Plugin Base:     97% ✅
Plugin Manager:  93% ✅
System Plugin:   90% ✅
Network Plugin:  90% ✅
WiFi Plugin:     90% ✅
Dashboard:       85% ✅

OVERALL: 91% ✅ (exceeds 90% target)
```

---

## 🎯 Recomendações

### Immediate Actions (Hoje)
1. ⚠️ Resolver Gap #1 (psutil dependency) - BLOQUEADOR
2. ⚠️ Criar testes de plugins (Gap #6) - CRÍTICO

### Short Term (Esta semana)
3. 🔧 Atualizar Dashboard tests (Gap #2)
4. 🔧 Decidir estratégia error recovery (Gap #5)

### Medium Term (Próximo sprint)
5. 📝 Documentar dependências WiFi (Gap #3)
6. ⚙️ Configurar event history limite (Gap #4)

---

## 📝 Lições Aprendidas

### 1. Lazy Loading != Dependency Resolution
**Problema:** Lazy loading de psutil esconde problema até runtime.
**Lição:** Validar dependências em `__init__` ou documentar claramente.

### 2. Tests Devem Evoluir com Código
**Problema:** Dashboard mudou mas tests não foram atualizados.
**Lição:** Atualizar tests ANTES de marcar feature completa.

### 3. Platform Dependencies Precisam Fallbacks
**Problema:** WiFiPlugin assume Linux + nmcli.
**Lição:** Sempre ter fallback ou error messages claros.

---

## ✅ Conclusão

Sprint 2 tem **funcionalidade core implementada**, mas com **6 air gaps significativos**.

**Prioridade:** Resolver Gaps #1 e #6 (P0) ANTES de prosseguir.

**Próximos Passos:**
1. Instalar psutil (Gap #1)
2. Criar tests de plugins (Gap #6)
3. Atualizar Dashboard tests (Gap #2)
4. Validar 90%+ coverage
5. Auditoria de conformidade final

---

**Soli Deo Gloria ✝️**
**Juan-Dev**
**2025-11-09**
