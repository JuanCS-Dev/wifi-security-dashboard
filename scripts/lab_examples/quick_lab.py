#!/usr/bin/env python3
"""
Quick Lab Session - Sessão Rápida de Laboratório WiFi

Script simplificado para demonstrações rápidas com seus filhos.

Usage:
    sudo python3 quick_lab.py [duração_segundos]

Example:
    sudo python3 quick_lab.py 60

Author: Professor JuanCS-Dev ✝️
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.education import create_lab_scenario


def main():
    """Executa sessão rápida de laboratório"""
    
    # Verifica root
    if os.geteuid() != 0:
        print("❌ Este script precisa ser executado com sudo")
        print("💡 Comando: sudo python3 quick_lab.py")
        sys.exit(1)
    
    # Duração (padrão 60s)
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                  🎓 LABORATÓRIO WiFi RÁPIDO 🎓                       ║
║                                                                      ║
║  Demonstração educacional de segurança em redes WiFi                ║
║  Ambiente controlado - Use apenas em casa!                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"⏱️  Duração: {duration} segundos")
    print("\n🎯 Objetivo da aula:")
    print("   Mostrar o que pode ser visto em redes WiFi abertas\n")
    
    input("📚 Pressione ENTER quando estiver pronto para começar...")
    
    # Cria e executa laboratório
    lab = create_lab_scenario()
    lab.start_capture(duration=duration)
    
    # Pergunta se quer exportar
    export = input("\n💾 Salvar resultados? (s/N): ").strip().lower()
    if export == 's':
        filename = f"lab_session_{duration}s.txt"
        lab.export_results(filename)
        print(f"\n✅ Resultados salvos em: {filename}")
    
    print("\n" + "="*70)
    print("🎓 PERGUNTAS PARA DISCUSSÃO:")
    print("="*70)
    print("1. O que vocês viram que pode ser interceptado?")
    print("2. Qual a diferença entre HTTP e HTTPS?")
    print("3. Por que não devemos usar WiFi público?")
    print("4. Como podemos nos proteger online?")
    print("="*70 + "\n")
    
    print("✅ Laboratório concluído! Parabéns! 🎉\n")


if __name__ == "__main__":
    main()
