# 🚧 MIGRAÇÃO py_cui - STATUS SNAPSHOT
**Data:** 2025-11-11
**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Objetivo:** Migrar dashboard de Rich → py_cui para rendering pixel-perfect

---

## ⚠️ STATUS ATUAL: INCOMPLETO

### ✅ O QUE FUNCIONA

1. **Infraestrutura base criada:**
   - `src/utils/coordinate_converter.py` - Converte (x,y,w,h) → (row,col,span)
   - `src/adapters/component_adapter.py` - Classe base para adapters
   - `src/core/pycui_renderer.py` - Renderer py_cui
   - `src/widgets/` - Diretório criado
   - CLI: `--pycui-mode` flag adicionado

2. **Sparkline MIGRADO E FUNCIONANDO:**
   - `src/adapters/sparkline_adapter.py` ✅
   - Usa `TextBlock` (NÃO BlockLabel - esse não tem set_text!)
   - Teste: `python3 test_pycui_minimal.py` → FUNCIONA
   - Unicode chars: ▁▂▃▄▅▆▇█ renderizam corretamente
   - Atualização dinâmica funciona

### ❌ O QUE ESTÁ QUEBRADO

1. **Dashboard completo NÃO funciona:**
   - `python3 main_v2.py --config config/dashboard_grid_complex.yml --pycui-mode --mock`
   - Tela preta, nada renderiza (exceto título/status bar)

2. **Componentes NÃO migrados:**
   - ❌ Runchart (usa plotext - complexo)
   - ❌ PacketTable (tabela custom - muito complexo)
   - ❌ Barchart (usa plotext - complexo)
   - ❌ Textbox (simples - usa Label)

3. **Grid mode ANTIGO quebrado:**
   - `grid_renderer.py` tinha bugs de ANSI/borders
   - Foi a RAZÃO da migração para py_cui

---

## 📁 ARQUIVOS CRIADOS/MODIFICADOS

### Criados:
```
src/
├── utils/
│   └── coordinate_converter.py          # NEW - Conversão coordenadas
├── adapters/
│   ├── __init__.py                       # NEW
│   ├── component_adapter.py              # NEW - Base abstrata
│   └── sparkline_adapter.py              # NEW - Sparkline → TextBlock
├── widgets/
│   ├── __init__.py                       # NEW
│   └── sparkline_widget.py               # NEW - Não usado! (custom widget falhou)
└── core/
    └── pycui_renderer.py                 # NEW - Renderer principal

config/
└── test_sparkline_pycui.yml              # NEW - Config teste

Testes:
├── test_pycui_minimal.py                 # NEW - Teste py_cui isolado
└── test_pycui_debug.py                   # NEW - Debug coordenadas
```

### Modificados:
```
src/core/dashboard.py                     # Adicionado _run_pycui_mode()
main_v2.py                                # Adicionado --pycui-mode flag
```

---

## 🐛 PROBLEMAS ENCONTRADOS (Lições Aprendidas)

### Problema 1: BlockLabel NÃO tem set_text()
**Erro:** `AttributeError: 'BlockLabel' object has no attribute 'set_text'`
**Solução:** Usar `TextBlock` ao invés de `BlockLabel`
**Código correto:**
```python
widget = pycui_root.add_text_block(title, row, col, row_span, column_span)
widget.set_text("Dynamic text here")  # Funciona!
```

### Problema 2: Custom widgets complexos demais
**Tentativa:** Criar `SparklineWidget` herdando `py_cui.widgets.Widget`
**Problema:** API complicada, `add_custom_widget()` recebe CLASSE não instância
**Solução:** Usar widgets built-in do py_cui (TextBlock, Label, etc) + lógica no adapter

### Problema 3: Fine grid (1:1 mapping)
**Decisão:** Grid de 160x60 = Terminal de 160x60 (1 cell = 1 char)
**Motivo:** Máxima precisão para pixel-perfect
**Funciona:** Sim, CoordinateConverter faz conversão correta

---

## 📋 PRÓXIMOS PASSOS (Em Ordem)

### Sprint 3: Migrar Textbox (FÁCIL - 30min)
**Objetivo:** Componente mais simples, valida Labels
**Implementação:**
```python
# src/adapters/textbox_adapter.py
class TextboxAdapter(ComponentAdapter):
    def create_widget(self, pycui_root, row, col, row_span, col_span):
        widget = pycui_root.add_label(
            self.component.config.title,
            row, col
        )
        return widget

    def update_widget(self, plugin_data):
        # Extract value from plugin
        value = plugin_data[plugin_name][data_field]
        # Update label
        self.widget.set_title(f"{label}: {value}")
```

### Sprint 4: Migrar Runchart (DIFÍCIL - 2-3h)
**Desafio:** plotext pode não funcionar com curses
**Opções:**
1. **Tentar plotext + TextBlock:**
   ```python
   chart_str = plt.build()  # Gera ASCII
   widget.set_text(chart_str)
   ```
2. **Fallback ASCII manual:** Se plotext não funcionar, fazer chart simples

**Spike necessário:**
```python
# test_plotext_pycui.py
import plotext as plt
import py_cui

root = py_cui.PyCUI(20, 80)
text_block = root.add_text_block('Chart', 0, 0, 15, 70)

plt.clf()
plt.plotsize(60, 10)
plt.plot([1,2,3,4], [1,4,2,3])
chart_str = plt.build()

text_block.set_text(chart_str)
root.start()
```

### Sprint 5: Migrar PacketTable (MUITO DIFÍCIL - 4-6h)
**Desafio:** Rich Table → ASCII table manual
**Solução:** Usar biblioteca `tabulate`:
```python
from tabulate import tabulate

headers = ['Time', 'Source', 'Dest', 'Protocol', 'Info']
rows = [
    ['12:30:45', '192.168.1.1', '8.8.8.8', 'HTTPS', 'Encrypted'],
    ...
]
table_str = tabulate(rows, headers=headers, tablefmt='grid')
widget.set_text(table_str)
```

### Sprint 6: Migrar Barchart (MÉDIO - 1-2h)
**Similar a Runchart** - Reutilizar aprendizado

### Sprint 7: Dashboard Completo (CRÍTICO - 2-3h)
**Objetivo:** `dashboard_grid_complex.yml` funcionando
**Config atual:** 7 componentes (2 sparklines, 2 runcharts, 1 packettable, 1 barchart, 1 textbox)
**Validação:**
- [ ] TODOS componentes visíveis
- [ ] Posições pixel-perfect
- [ ] Borders alinhados
- [ ] Atualização real-time
- [ ] 0 crashes

---

## 🔧 COMANDOS ÚTEIS

### Testes isolados:
```bash
# Teste 1: py_cui básico (valida instalação)
python3 test_pycui_minimal.py

# Teste 2: Conversão coordenadas (valida CoordinateConverter)
python3 test_pycui_debug.py

# Teste 3: Sparkline isolado (valida adapter)
python3 main_v2.py --config config/test_sparkline_pycui.yml --pycui-mode --mock
```

### Dashboard completo:
```bash
# Grid mode ANTIGO (quebrado, não usar)
python3 main_v2.py --grid --mock

# py_cui mode NOVO (em progresso)
python3 main_v2.py --pycui-mode --mock

# Config complexo
python3 main_v2.py --config config/dashboard_grid_complex.yml --pycui-mode --mock
```

---

## 📚 REFERÊNCIAS IMPORTANTES

### py_cui API:
- **Widgets com set_text():** TextBlock, ScrollTextBlock
- **Widgets SEM set_text():** BlockLabel, Label (usa set_title)
- **Signature:** `add_text_block(title, row, col, row_span, column_span, padx, pady)`

### Color mapping:
```python
COLOR_MAP = {
    'green': py_cui.GREEN_ON_BLACK,
    'yellow': py_cui.YELLOW_ON_BLACK,
    'red': py_cui.RED_ON_BLACK,
    'cyan': py_cui.CYAN_ON_BLACK,
    'blue': py_cui.BLUE_ON_BLACK,
    'magenta': py_cui.MAGENTA_ON_BLACK,
}
```

### Unicode sparkline:
```python
SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"
```

---

## 💡 INSIGHTS CRÍTICOS

1. **NÃO criar custom widgets complexos** - Usar built-in widgets + lógica no adapter
2. **TextBlock é o widget mais versátil** - Aceita multi-line, set_text() dinâmico
3. **Fine grid funciona** - 1 cell = 1 char para precisão
4. **py_cui SÓ funciona em TTY real** - Não testa via background/timeout
5. **Plugin API:** `plugin_manager.get_all_plugin_data()` (não get_all_data!)

---

## 🎯 ESTIMATIVA DE CONCLUSÃO

**Tempo restante:** 10-15 horas
**Sprints pendentes:** 3, 4, 5, 6, 7, 8
**Complexidade maior:** PacketTable (Sprint 5)
**Risco maior:** plotext incompatível com curses (Sprint 4)

---

## 📞 COMO CONTINUAR

### 1. Validar Sparkline funcionando:
```bash
python3 main_v2.py --config config/test_sparkline_pycui.yml --pycui-mode --mock
# Deve mostrar: CPU: ▁▂▃▄▅▆▇█ (45%)
```

### 2. Continuar Sprint 3 (Textbox):
- Criar `src/adapters/textbox_adapter.py`
- Usar `add_label()` com `set_title()` para atualizar
- Testar com config simples

### 3. Spike plotext (Sprint 4):
- Criar `test_plotext_pycui.py` (veja código acima)
- Verificar se plotext output funciona em TextBlock
- Se NÃO → implementar ASCII chart manual

### 4. NÃO comemorar até dashboard_grid_complex.yml funcionar 100%

---

## 🔥 ERROS A NÃO REPETIR

1. ❌ Usar BlockLabel achando que tem set_text()
2. ❌ Comemorar antes de terminar
3. ❌ Não validar API antes de implementar
4. ❌ Criar código sem testar isoladamente primeiro
5. ❌ Assumir que "funcionou no teste = está pronto"

---

**Status:** 25% completo (2/8 sprints)
**Próximo passo:** Sprint 3 - Textbox adapter
**Meta:** Dashboard pixel-perfect sem NENHUM pixel fora do lugar

Soli Deo Gloria ✝️
