# 🚀 PRÓXIMOS PASSOS - CÓDIGO PRONTO PARA COPIAR

---

## Sprint 3: Textbox Adapter (COPIE E COLE)

### Arquivo: `src/adapters/textbox_adapter.py`
```python
"""
Textbox Component Adapter for py_cui.

Adapter that converts Textbox component to py_cui Label.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

from typing import Any
import py_cui

from src.adapters.component_adapter import ComponentAdapter


# Color mapping
COLOR_MAP = {
    'green': py_cui.GREEN_ON_BLACK,
    'yellow': py_cui.YELLOW_ON_BLACK,
    'red': py_cui.RED_ON_BLACK,
    'cyan': py_cui.CYAN_ON_BLACK,
    'blue': py_cui.BLUE_ON_BLACK,
    'magenta': py_cui.MAGENTA_ON_BLACK,
    'white': py_cui.WHITE_ON_BLACK,
}


class TextboxAdapter(ComponentAdapter):
    """
    Adapter for Textbox component → py_cui Label.

    Simple key-value display using Label widget.
    """

    def __init__(self, component: Any):
        super().__init__(component)
        self.label_text = self.component.config.extra.get('label', 'Value')

    def create_widget(
        self,
        pycui_root: py_cui.PyCUI,
        row: int,
        col: int,
        row_span: int,
        col_span: int
    ) -> Any:
        """Create py_cui Label for textbox display."""
        title = self.component.config.title
        color_name = self.component.config.color

        # Use Label (single line text)
        widget = pycui_root.add_label(
            title,
            row,
            col,
            row_span=row_span,
            column_span=col_span,
            padx=1,
            pady=0
        )

        # Set color
        pycui_color = COLOR_MAP.get(color_name, py_cui.GREEN_ON_BLACK)
        widget.set_color(pycui_color)

        # Store widget
        self.widget = widget

        return widget

    def update_widget(self, plugin_data: dict) -> None:
        """Update label text with plugin data."""
        if not self.widget:
            return

        # Get data
        plugin_name = self.component.config.plugin
        data_field = self.component.config.data_field

        if plugin_name not in plugin_data:
            return

        plugin_values = plugin_data[plugin_name]
        if data_field not in plugin_values:
            return

        value = plugin_values[data_field]

        # Update label title (Label não tem set_text, usa set_title)
        display_text = f"{self.label_text}: {value}"
        self.widget.set_title(display_text)
```

### Config teste: `config/test_textbox_pycui.yml`
```yaml
version: '2.0'
title: 'Textbox Test'

settings:
  refresh_rate_ms: 1000
  terminal_size:
    width: 80
    height: 24

plugins:
  - name: system
    enabled: true
    module: src.plugins.system_plugin
    rate_ms: 1000

components:
  - type: textbox
    title: 'System Info'
    position: {x: 10, y: 5, width: 30, height: 3}
    rate_ms: 1000
    plugin: system
    data_field: cpu_percent
    color: yellow
    extra:
      label: "CPU"
```

### Teste:
```bash
python3 main_v2.py --config config/test_textbox_pycui.yml --pycui-mode --mock
```

---

## Sprint 4: Runchart Adapter - SPIKE PRIMEIRO!

### Spike: `test_plotext_pycui.py`
```python
#!/usr/bin/env python3
"""
Spike: Testar se plotext funciona com py_cui TextBlock.
"""
import py_cui
import plotext as plt
import time

# Create py_cui
root = py_cui.PyCUI(20, 80)
root.set_title('Plotext + py_cui Spike')

# Create TextBlock for chart
text_block = root.add_text_block(
    'Chart Test',
    row=2,
    column=5,
    row_span=15,
    column_span=70
)

# Generate plotext chart
def update_chart():
    """Update chart with random data."""
    import random

    plt.clf()
    plt.plotsize(60, 10)

    # Sample data
    x = list(range(20))
    y = [random.randint(10, 100) for _ in range(20)]

    plt.plot(x, y, marker='dot')
    plt.title('Test Chart')

    # Build ASCII output
    chart_str = plt.build()

    # Update widget
    text_block.set_text(chart_str)

# Set draw callback
root.set_on_draw_update_func(update_chart)
root.set_refresh_timeout(1)  # 1 second refresh

# Start
root.start()
```

### Teste spike:
```bash
python3 test_plotext_pycui.py
```

**SE FUNCIONAR:** Crie `runchart_adapter.py` usando plotext
**SE NÃO FUNCIONAR:** Implemente ASCII chart manual (código abaixo)

### Fallback: ASCII Chart Manual
```python
def draw_simple_line_chart(values, width=50, height=10):
    """
    Draw simple ASCII line chart without plotext.

    Returns multi-line string.
    """
    if not values:
        return "No data"

    # Normalize values to 0-height range
    min_val = min(values)
    max_val = max(values)

    if max_val == min_val:
        normalized = [height // 2] * len(values)
    else:
        normalized = [
            int((v - min_val) / (max_val - min_val) * (height - 1))
            for v in values
        ]

    # Build chart line by line (top to bottom)
    lines = []
    for row in range(height - 1, -1, -1):
        line = []
        for val in normalized[-width:]:  # Only last 'width' values
            if val == row:
                line.append('●')
            elif val > row:
                line.append('│')
            else:
                line.append(' ')
        lines.append(''.join(line))

    # Add axis
    lines.append('─' * width)

    return '\n'.join(lines)
```

---

## Sprint 5: PacketTable - Usar tabulate

### Instalar tabulate:
```bash
pip install tabulate --break-system-packages
```

### Código: `src/adapters/packet_table_adapter.py`
```python
from typing import Any
import py_cui
from tabulate import tabulate

from src.adapters.component_adapter import ComponentAdapter


class PacketTableAdapter(ComponentAdapter):
    """Adapter for PacketTable → py_cui TextBlock with tabulate."""

    def create_widget(self, pycui_root, row, col, row_span, col_span):
        widget = pycui_root.add_text_block(
            self.component.config.title,
            row, col,
            row_span=row_span,
            column_span=col_span
        )
        widget.set_text("Loading packets...")
        self.widget = widget
        return widget

    def update_widget(self, plugin_data: dict):
        if not self.widget:
            return

        # Get packet data from plugin
        plugin_name = self.component.config.plugin
        if plugin_name not in plugin_data:
            return

        packets = plugin_data[plugin_name].get('recent_packets', [])

        if not packets:
            self.widget.set_text("No packets captured")
            return

        # Build table
        headers = ['Time', 'Source', 'Dest', 'Protocol', 'Info']
        rows = []

        for pkt in packets[:10]:  # Max 10 packets
            rows.append([
                pkt.get('timestamp', 'N/A'),
                pkt.get('src', 'N/A'),
                pkt.get('dst', 'N/A'),
                pkt.get('protocol', 'N/A'),
                pkt.get('info', 'N/A')[:30]  # Truncate
            ])

        # Format as ASCII table
        table_str = tabulate(rows, headers=headers, tablefmt='grid')

        # Update widget
        self.widget.set_text(table_str)
```

---

## Validação Final

### Dashboard completo funcionando:
```bash
python3 main_v2.py --config config/dashboard_grid_complex.yml --pycui-mode --mock
```

### Checklist pixel-perfect:
- [ ] TODOS 7 componentes aparecem
- [ ] Borders Unicode (╭╮╰╯) perfeitos
- [ ] Sparklines: ▁▂▃▄▅▆▇█ corretos
- [ ] Charts renderizam
- [ ] Tabelas formatadas
- [ ] Atualização em tempo real
- [ ] Posições EXATAS conforme config
- [ ] Nenhum overlap ou gap
- [ ] 0 crashes em 5 minutos rodando

---

**Boa sorte na próxima sessão!**
**NÃO comemorar até 100% funcionar.**

Soli Deo Gloria ✝️
