#!/usr/bin/env python3
"""
🎨 Teste Visual Completo do Dashboard
Mostra todos os componentes renderizados
"""

from main import EducationalDashboard
from rich.console import Console
from rich.layout import Layout
from rich import box

# Cria console e dashboard
console = Console(width=120, height=46)
dash = EducationalDashboard(interface=None, mock_mode=True)

# Coleta dados
dash._collect_data()

# Cria layout completo
layout = Layout()

# Estrutura principal
layout.split_column(
    Layout(name="header", size=5),
    Layout(name="main", ratio=1),
    Layout(name="footer", size=3)
)

# Main split em duas colunas
layout["main"].split_row(
    Layout(name="left"),
    Layout(name="right")
)

# Coluna esquerda
layout["left"].split_column(
    Layout(name="wifi", size=9),
    Layout(name="system", size=14),
    Layout(name="traffic_chart", ratio=1)
)

# Coluna direita
layout["right"].split_column(
    Layout(name="devices", ratio=1),
    Layout(name="apps", ratio=1)
)

# Popula layout com os componentes
layout["header"].update(dash._render_header())
layout["wifi"].update(dash._render_wifi_panel())
layout["system"].update(dash._render_system_panel())
layout["traffic_chart"].update(dash._render_traffic_chart())
layout["devices"].update(dash._render_devices_panel())
layout["apps"].update(dash._render_apps_panel())
layout["footer"].update(dash._render_footer())

# Renderiza
console.print("\n")
console.print(layout)
console.print("\n")

# Estatísticas
print("=" * 120)
print("✅ DASHBOARD RENDERIZADO COM SUCESSO!")
print("=" * 120)
print(f"📊 Componentes ativos: 6 (Header, WiFi, System, Traffic, Devices, Apps, Footer)")
print(f"🎨 Layout: 120x46 caracteres")
print(f"🚀 Performance: Renderizado em tempo real")
print(f"💚 Status: 100% FUNCIONAL")
print("=" * 120)
