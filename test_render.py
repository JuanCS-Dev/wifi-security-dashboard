#!/usr/bin/env python3
from main import EducationalDashboard

# Cria dashboard
dash = EducationalDashboard(interface=None, mock_mode=True)

# Coleta dados uma vez
dash._collect_data()

# Testa renderização
print("=== TESTANDO RENDERIZAÇÃO ===\n")

print("1. Header:")
header = dash._render_header()
print(f"   Tipo: {type(header)}")
print(f"   Conteúdo: {header}\n")

print("2. WiFi Panel:")
wifi = dash._render_wifi_panel()
print(f"   Tipo: {type(wifi)}")
print(f"   Conteúdo: {wifi}\n")

print("3. System Panel:")
system = dash._render_system_panel()
print(f"   Tipo: {type(system)}")
print(f"   Conteúdo: {system}\n")

print("4. Devices Panel:")
devices = dash._render_devices_panel()
print(f"   Tipo: {type(devices)}")
print(f"   Conteúdo: {devices}\n")

print("5. Apps Panel:")
apps = dash._render_apps_panel()
print(f"   Tipo: {type(apps)}")
print(f"   Conteúdo: {apps}\n")

print("=== FIM DOS TESTES ===")
