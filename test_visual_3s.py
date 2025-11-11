#!/usr/bin/env python3
"""
Test visual da dashboard por 3 segundos.
RODE ESTE COMANDO NO SEU TERMINAL para ver a dashboard com seus olhos!

python3 test_visual_3s.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.dashboard import Dashboard

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                 TESTE VISUAL DASHBOARD - 3 SEGUNDOS                     ║
║                                                                          ║
║  A dashboard vai aparecer por 3 segundos.                               ║
║  Observe ATENTAMENTE se cada pixel está no lugar!                       ║
║                                                                          ║
║  Pressione ENTER para começar...                                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

input()

print("\n\n🚀 Iniciando dashboard em 3... 2... 1...\n")
time.sleep(1)

# Criar dashboard
dashboard = Dashboard('config/dashboard_grid_complex.yml', mock_mode=True, grid_mode=True)

# Rodar por 3 segundos
import threading

def stop_after_3s():
    time.sleep(3)
    dashboard.stop()

stopper = threading.Thread(target=stop_after_3s)
stopper.start()

try:
    dashboard.run()
except KeyboardInterrupt:
    pass

stopper.join()

print("\n\n")
print("="*80)
print("TESTE CONCLUÍDO!")
print("="*80)
print()
print("Perguntas para você responder:")
print()
print("1. As bordas dos painéis estavam COMPLETAS? (sim/não)")
print("2. Os componentes estavam nas posições corretas? (sim/não)")
print("3. Havia algum pixel fora do lugar? (sim/não)")
print("4. Os espaçamentos estavam perfeitos? (sim/não)")
print()
print("="*80)
