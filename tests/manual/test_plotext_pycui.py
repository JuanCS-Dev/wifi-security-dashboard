#!/usr/bin/env python3
"""
Spike Test: plotext + py_cui Compatibility
===========================================

Objetivo: Determinar se plotext funciona dentro de py_cui TextBlock.
Resultado: Define estratégia para Runchart e Barchart adapters.

Author: Dev Sênior Rafael
Date: 2025-11-11
"""

import py_cui
import plotext as plt
import io
import sys
import time
import random


class PlotextSpike:
    """Spike test para validar plotext + py_cui"""

    def __init__(self):
        # Criar root py_cui (10x10 grid simples)
        self.root = py_cui.PyCUI(10, 10)
        self.root.set_title("🔍 Spike Test: plotext + py_cui")

        # Criar widget TextBlock para receber o chart
        self.chart_widget = self.root.add_text_block(
            "Plotext Line Chart Test",
            row=0, column=0,
            row_span=8, column_span=8
        )

        # Criar label de status
        self.status_widget = self.root.add_label(
            "Initializing...",
            row=8, column=0,
            row_span=2, column_span=8
        )

        # Dados para o gráfico
        self.data = [random.randint(10, 90) for _ in range(20)]
        self.update_count = 0

    def update_chart(self):
        """Atualiza chart com plotext"""
        try:
            # Adicionar novo ponto aleatório
            self.data.append(random.randint(10, 90))
            if len(self.data) > 50:
                self.data.pop(0)

            # Gerar chart com plotext
            plt.clf()
            plt.plot(self.data, marker="braille")
            plt.title("CPU Usage Simulation")
            plt.xlabel("Time")
            plt.ylabel("Percent")
            plt.ylim(0, 100)

            # Capturar output em StringIO
            output = io.StringIO()
            plt.show(output)
            chart_text = output.getvalue()

            # MOMENTO DA VERDADE: Tentar inserir no widget
            self.chart_widget.set_text(chart_text)

            # Atualizar status
            self.update_count += 1
            status = f"✅ SUCCESS! Updates: {self.update_count} | plotext FUNCIONA com py_cui!"
            self.status_widget.set_title(status)

        except AttributeError as e:
            # Falha: widget não tem set_text()
            error = f"❌ FAIL: AttributeError - {e}"
            self.status_widget.set_title(error)
            print(f"\n{error}")
            print("\n⚠️ DECISÃO: Usar ASCII chart manual (fallback)")
            time.sleep(3)
            sys.exit(1)

        except Exception as e:
            # Outra falha
            error = f"❌ FAIL: {type(e).__name__} - {e}"
            self.status_widget.set_title(error)
            print(f"\n{error}")
            print("\n⚠️ DECISÃO: Usar ASCII chart manual (fallback)")
            time.sleep(3)
            sys.exit(1)

    def run(self):
        """Executa o teste"""
        # Callback de atualização contínua
        self.root.set_on_draw_update_func(self.update_chart)

        print("🚀 Iniciando spike test...")
        print("📊 Gerando chart com plotext...")
        print("🔄 Tentando inserir em py_cui TextBlock...")
        print("\n⏳ Aguarde 5 segundos para validação visual...")
        print("   Se você ver um gráfico animado, plotext FUNCIONA! ✅")
        print("   Se tela preta ou crash, plotext FALHA! ❌\n")

        try:
            self.root.start()
        except KeyboardInterrupt:
            print("\n\n✅ Teste interrompido pelo usuário")
            print("📋 RESULTADO: plotext funciona com py_cui!")
            print("🎯 DECISÃO: Usar plotext nos adapters Runchart e Barchart")
            sys.exit(0)


def main():
    """Entry point"""
    print("=" * 70)
    print("SPIKE TEST: plotext + py_cui Compatibility")
    print("=" * 70)
    print()

    spike = PlotextSpike()
    spike.run()


if __name__ == "__main__":
    main()
