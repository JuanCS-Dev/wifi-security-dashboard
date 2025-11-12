#!/bin/bash
# Quick Start - Laboratório Educacional WiFi
# Author: Professor JuanCS-Dev ✝️

clear

cat << 'BANNER'
╔══════════════════════════════════════════════════════════════════════╗
║          🎓 LABORATÓRIO EDUCACIONAL DE SEGURANÇA WiFi 🎓             ║
║                                                                      ║
║  Sistema completo para ensinar segurança em redes WiFi              ║
║  Ambiente controlado - Perfeito para ensinar crianças!              ║
║                                                                      ║
║  Author: Professor JuanCS-Dev ✝️                                     ║
║  Motto: "Soli Deo Gloria - Teaching with Purpose"                   ║
╚══════════════════════════════════════════════════════════════════════╝

BANNER

echo ""
echo "🎯 Escolha um laboratório:"
echo ""
echo "  1️⃣  Quick Lab (Introdutório - 5 min)"
echo "      → Primeira aula sobre interceptação"
echo ""
echo "  2️⃣  HTTP vs HTTPS Demo (Intermediário - 15 min)"
echo "      → Entenda criptografia na prática"
echo ""
echo "  3️⃣  Device Tracker (Avançado - 20 min)"
echo "      → Rastreamento e privacidade"
echo ""
echo "  4️⃣  Dashboard Completo (Modo visualização)"
echo "      → Interface gráfica do sistema"
echo ""
echo "  5️⃣  Ler Guia Completo"
echo "      → Documentação detalhada"
echo ""
echo "  0️⃣  Sair"
echo ""

read -p "Digite sua escolha (0-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Iniciando Quick Lab..."
        echo "⚠️  Necessário executar com sudo!"
        echo ""
        sudo python3 scripts/lab_examples/quick_lab.py
        ;;
    2)
        echo ""
        echo "🚀 Iniciando HTTP vs HTTPS Demo..."
        echo "⚠️  Necessário executar com sudo!"
        echo ""
        sudo python3 scripts/lab_examples/http_vs_https_demo.py
        ;;
    3)
        echo ""
        echo "🚀 Iniciando Device Tracker..."
        echo "⚠️  Necessário executar com sudo!"
        echo ""
        sudo python3 scripts/lab_examples/device_tracker.py
        ;;
    4)
        echo ""
        echo "🚀 Iniciando Dashboard (modo mock)..."
        echo ""
        python3 app_textual.py --mock
        ;;
    5)
        echo ""
        echo "📚 Abrindo guia educacional..."
        echo ""
        if command -v less &> /dev/null; then
            less EDUCATIONAL_LAB_README.md
        else
            cat EDUCATIONAL_LAB_README.md
        fi
        ;;
    0)
        echo ""
        echo "👋 Até logo! Continue ensinando segurança digital!"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opção inválida!"
        echo ""
        exit 1
        ;;
esac

echo ""
echo "✅ Laboratório concluído!"
echo ""
read -p "Pressione ENTER para voltar ao menu..."
exec "$0"
