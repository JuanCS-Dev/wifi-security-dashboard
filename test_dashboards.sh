#!/bin/bash
# Quick test of all dashboards with mock data

echo "🧪 TESTE VISUAL DAS DASHBOARDS"
echo "================================"
echo ""
echo "Iniciando app em modo mock..."
echo "Navegue pelas dashboards usando teclas 0-9, a, b"
echo ""
echo "Dashboards para testar:"
echo "  0 - Consolidated (Overview)"
echo "  1 - System"
echo "  2 - Network"
echo "  3 - WiFi"
echo "  4 - Packets"
echo "  5 - Topology"
echo "  6 - ARP Detector"
echo "  8 - DNS Monitor"
echo "  9 - HTTP Sniffer"
echo "  a - Rogue AP"
echo "  b - Handshake"
echo ""
echo "Pressione Ctrl+C para sair"
echo ""

python3 app_textual.py --mock
