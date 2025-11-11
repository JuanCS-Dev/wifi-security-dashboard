# ⚡ REFERÊNCIA RÁPIDA - Migração py_cui

## 🎯 OBJETIVO
Migrar dashboard de Rich → py_cui para pixel-perfect rendering.
**Status:** 25% (Sprint 2/8 completo)

## ✅ FUNCIONANDO
- Infraestrutura: CoordinateConverter, PyCUIRenderer, ComponentAdapter
- **Sparkline adapter** → `python3 test_pycui_minimal.py` ✅

## ❌ QUEBRADO
- Dashboard completo (componentes não migrados)
- Runchart, PacketTable, Barchart, Textbox

## 🚨 ERROS CRÍTICOS CORRIGIDOS
1. **BlockLabel NÃO tem set_text()** → Use `TextBlock`
2. **Plugin API:** `get_all_plugin_data()` (não get_all_data)
3. **Custom widgets:** Difícil demais → Use built-in + lógica no adapter

## 📝 TEMPLATE ADAPTER

```python
from typing import Any
import py_cui
from src.adapters.component_adapter import ComponentAdapter

COLOR_MAP = {
    'green': py_cui.GREEN_ON_BLACK,
    'yellow': py_cui.YELLOW_ON_BLACK,
    'red': py_cui.RED_ON_BLACK,
}

class MyAdapter(ComponentAdapter):
    def create_widget(self, pycui_root, row, col, row_span, col_span):
        widget = pycui_root.add_text_block(  # ou add_label
            self.component.config.title,
            row, col,
            row_span=row_span,
            column_span=col_span
        )
        self.widget = widget
        return widget

    def update_widget(self, plugin_data: dict):
        plugin_name = self.component.config.plugin
        data_field = self.component.config.data_field
        value = plugin_data[plugin_name][data_field]
        self.widget.set_text(str(value))  # TextBlock
        # ou
        self.widget.set_title(str(value))  # Label
```

## 📦 WIDGETS py_cui

| Widget | Método update | Uso |
|--------|--------------|-----|
| `TextBlock` | `set_text(str)` | ✅ Multi-line, dinâmico |
| `Label` | `set_title(str)` | ✅ Single-line |
| `BlockLabel` | ❌ Nenhum | ❌ NÃO USAR |

## 🔧 COMANDOS

```bash
# Teste isolado
python3 test_pycui_minimal.py

# Sparkline funcionando
python3 main_v2.py --config config/test_sparkline_pycui.yml --pycui-mode --mock

# Dashboard completo (objetivo final)
python3 main_v2.py --config config/dashboard_grid_complex.yml --pycui-mode --mock
```

## 📂 ARQUIVOS IMPORTANTES

- `MIGRATION_STATUS.md` → Status detalhado, problemas, próximos passos
- `NEXT_STEPS_CODE.md` → Código pronto para copiar (Sprints 3-5)
- `src/adapters/sparkline_adapter.py` → Exemplo funcionando

## 🎯 PRÓXIMO PASSO

**Sprint 3:** Textbox adapter (30min)
→ Código pronto em `NEXT_STEPS_CODE.md`
→ Copiar `textbox_adapter.py` e testar

## ⏱️ ESTIMATIVA

- Sprint 3: 30min (Textbox - fácil)
- Sprint 4: 2-3h (Runchart - plotext spike)
- Sprint 5: 4-6h (PacketTable - tabulate)
- Sprint 6: 1-2h (Barchart - similar Runchart)
- Sprint 7: 2-3h (Integração completa)
- **Total:** 10-15 horas

## 🔥 REGRA DE OURO

**NÃO COMEMORAR ATÉ dashboard_grid_complex.yml FUNCIONAR 100%**

Soli Deo Gloria ✝️
