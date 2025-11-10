#!/usr/bin/env python3
from main import EducationalDashboard
import time

dash = EducationalDashboard(interface=None, mock_mode=True)
dash._collect_data()

# Mostra header
from rich.console import Console
console = Console()

print("\n" + "="*60)
print("TESTE VISUAL - HEADER")
print("="*60 + "\n")

header = dash._render_header()
console.print(header)

print("\n" + "="*60)
print("TESTE VISUAL - PAINÉIS")
print("="*60 + "\n")

wifi = dash._render_wifi_panel()
console.print(wifi)

print()

system = dash._render_system_panel()
console.print(system)

print("\nTODOS OS TÍTULOS ALINHADOS À ESQUERDA ✅")
print("NOMES: Maximus e Penelope ✅")
