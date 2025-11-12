#!/usr/bin/env python3
"""
Device Tracker - Rastreador de Dispositivos Educacional

Mostra quais dispositivos estão na rede e o que estão fazendo.
Ensina sobre privacidade e metadados.

Usage:
    sudo python3 device_tracker.py

Author: Professor JuanCS-Dev ✝️
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.education import WiFiLabInterceptor


class DeviceActivityTracker:
    """Rastreia atividades de dispositivos na rede"""
    
    def __init__(self):
        self.devices = defaultdict(lambda: {
            'dns_queries': [],
            'protocols': defaultdict(int),
            'first_seen': None,
            'last_seen': None,
            'danger_score': 0
        })
    
    def analyze_interception(self, interceptor):
        """Analisa dados interceptados e gera relatório"""
        
        for data in interceptor.captured_data:
            device = data.device_name
            
            # Atualiza timestamps
            if not self.devices[device]['first_seen']:
                self.devices[device]['first_seen'] = data.timestamp
            self.devices[device]['last_seen'] = data.timestamp
            
            # Registra protocolo
            self.devices[device]['protocols'][data.protocol] += 1
            
            # Registra DNS queries
            if data.protocol == 'DNS' and 'Acessando:' in data.description:
                site = data.description.replace('Acessando: ', '')
                self.devices[device]['dns_queries'].append(site)
            
            # Calcula score de perigo
            if data.danger_level == 'DANGER':
                self.devices[device]['danger_score'] += 10
            elif data.danger_level == 'WARNING':
                self.devices[device]['danger_score'] += 3
    
    def generate_report(self):
        """Gera relatório educacional"""
        
        print("\n" + "="*70)
        print("📱 RELATÓRIO DE DISPOSITIVOS NA REDE")
        print("="*70)
        
        for device, info in sorted(self.devices.items()):
            print(f"\n🔹 {device}")
            print("   " + "-"*66)
            
            # Protocolos usados
            print("   📊 Protocolos:")
            for proto, count in sorted(info['protocols'].items(), key=lambda x: x[1], reverse=True)[:5]:
                icon = "🔒" if proto == "HTTPS" else "⚠️" if proto == "HTTP" else "📦"
                print(f"      {icon} {proto}: {count} pacotes")
            
            # Sites acessados
            if info['dns_queries']:
                print("\n   🌐 Sites acessados:")
                unique_sites = list(set(info['dns_queries']))[:10]
                for site in unique_sites:
                    print(f"      • {site}")
            
            # Score de perigo
            danger = info['danger_score']
            if danger > 20:
                level = "🚨 ALTO RISCO"
                color = '\033[91m'
            elif danger > 5:
                level = "⚠️  MÉDIO RISCO"
                color = '\033[93m'
            else:
                level = "✅ BAIXO RISCO"
                color = '\033[92m'
            
            reset = '\033[0m'
            print(f"\n   🎯 Nível de exposição: {color}{level}{reset} (score: {danger})")
        
        print("\n" + "="*70)


def print_intro():
    """Introdução educacional"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║            📱 RASTREADOR DE DISPOSITIVOS EDUCACIONAL 📱              ║
║                                                                      ║
║  Mostra o que pode ser rastreado em redes WiFi abertas              ║
╚══════════════════════════════════════════════════════════════════════╝

🎓 OBJETIVO DA AULA:
   Demonstrar que em redes públicas, todos os seus dispositivos
   podem ser rastreados e suas atividades monitoradas.

⚠️  O QUE SERÁ MOSTRADO:
   ✅ Quais dispositivos você tem
   ✅ Quando você os usa
   ✅ Quais apps/sites você acessa
   ✅ Seus horários e padrões de uso

💡 LIÇÃO:
   Mesmo sem ver CONTEÚDO, alguém pode saber MUITO sobre você
   apenas observando METADADOS (dados sobre dados).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


def scenario_explanation():
    """Explica o cenário"""
    print("""
📖 CENÁRIO SIMULADO:

Imagine que você está em um SHOPPING com WiFi grátis:

┌────────────────────────────────────────────────────┐
│  🏬 Shopping Center Mall                           │
│  📶 WiFi Grátis: "ShoppingWiFi-Free"               │
│  🔓 Sem senha                                      │
└────────────────────────────────────────────────────┘

Você conecta seu celular e começa a usar...

🤔 O que o DONO do WiFi pode ver sobre VOCÊ?
   Vamos descobrir!
    """)
    input("\n📚 Pressione ENTER para começar o rastreamento...")


def main():
    """Executa demonstração de rastreamento"""
    
    # Verifica root
    if os.geteuid() != 0:
        print("❌ Este script precisa ser executado com sudo")
        print("💡 Comando: sudo python3 device_tracker.py")
        sys.exit(1)
    
    print_intro()
    input("📚 Pressione ENTER para começar a aula...")
    
    scenario_explanation()
    
    print("\n🎯 RASTREAMENTO INICIADO!")
    print("   Agora USE seus dispositivos normalmente...\n")
    
    # Cria interceptador
    interceptor = WiFiLabInterceptor(interface="wlan0", lab_mode=False)
    
    # Captura por 60 segundos
    print("⏱️  Rastreando por 60 segundos...")
    interceptor.start_capture(duration=60, packet_count=1000)
    
    # Analisa resultados
    print("\n🔍 Analisando dispositivos...")
    tracker = DeviceActivityTracker()
    tracker.analyze_interception(interceptor)
    tracker.generate_report()
    
    # Conclusões educacionais
    print("\n" + "="*70)
    print("🎓 CONCLUSÕES EDUCACIONAIS")
    print("="*70)
    print("""
📊 O QUE APRENDEMOS:

1. 👁️  PRIVACIDADE NÃO EXISTE em WiFi público
   → Todos os seus dispositivos são visíveis
   → Horários de uso são rastreados
   → Padrões de comportamento são identificados

2. 🔍 METADADOS REVELAM MUITO
   → Mesmo sem ver mensagens, sabem o que você faz
   → Apps usados, sites visitados, horários
   → É possível criar um PERFIL seu completo

3. 🎯 MARKETING DIRECIONADO
   → Empresas fazem isso LEGALMENTE
   → Shopping sabe: quantas vezes você visitou
                    quanto tempo ficou
                    quais lojas passou perto
                    quando costuma vir

4. 🚨 CRIMINOSOS PODEM:
   → Identificar pessoas com iPhones/Samsung caros
   → Saber seus horários e rotinas
   → Fazer ataques direcionados
   → Roubar contas com dados vazados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️  COMO SE PROTEGER:

✅ NÃO use WiFi público (dados móveis são mais seguros)
✅ Se precisar, use VPN confiável
✅ Desative WiFi quando não usar
✅ Configure para "Esquecer rede" após uso
✅ Use HTTPS sempre
✅ Ative "Endereço MAC Aleatório" no celular

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    print("="*70)
    
    # Quiz final
    print("\n❓ PERGUNTA PARA REFLEXÃO:")
    print("   O que você acha de empresas rastrearem seus dados?")
    print("   Isso deveria ser permitido? Por quê?")
    print("\n💬 Discuta com sua família!\n")
    
    print("🎉 Laboratório concluído!")
    print("📖 Continue aprendendo sobre privacidade digital!\n")


if __name__ == "__main__":
    main()
