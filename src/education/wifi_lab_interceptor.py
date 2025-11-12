"""
WiFi Lab Interceptor - Educational Network Security Lab
========================================================

Laboratório educacional para demonstrar perigos de redes WiFi abertas.
Ambiente controlado para ensinar crianças sobre segurança na internet.

IMPORTANTE: Use apenas em sua rede doméstica com dispositivos próprios!

Author: Professor JuanCS-Dev ✝️
Date: 2025-11-12
License: Educational Use Only
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import time
import os
from scapy.all import (
    sniff, ARP, BOOTP, DHCP, DNS, DNSQR, DNSRR,
    TCP, UDP, IP, Raw, Ether, Dot11, RadioTap,
    wrpcap, rdpcap
)


@dataclass
class InterceptedData:
    """Estrutura para dados interceptados"""
    timestamp: str
    device_name: str
    device_mac: str
    device_ip: str
    protocol: str
    danger_level: str  # "SAFE", "WARNING", "DANGER"
    description: str
    raw_data: Optional[str] = None
    educational_note: str = ""


class WiFiLabInterceptor:
    """
    Interceptador educacional para laboratório WiFi doméstico.
    
    Captura e analisa tráfego em rede controlada para demonstrar:
    - Dados visíveis em redes abertas
    - Diferença entre HTTP e HTTPS
    - Informações vazadas por apps
    - Perigos de redes públicas
    
    Modes:
        - passive: Apenas observa (modo monitor)
        - active: Análise ativa (requer rede própria)
    """
    
    def __init__(self, interface: str = "wlan0", lab_mode: bool = True):
        """
        Inicializa o interceptador educacional.
        
        Args:
            interface: Interface de rede (wlan0, wlp2s0, etc)
            lab_mode: Modo laboratório (adiciona avisos educacionais)
        """
        self.interface = interface
        self.lab_mode = lab_mode
        self.captured_data: List[InterceptedData] = []
        self.device_registry: Dict[str, str] = {}  # MAC -> Name
        self.stats = {
            'total_packets': 0,
            'http_packets': 0,
            'https_packets': 0,
            'dns_queries': 0,
            'leaked_data': 0,
            'safe_data': 0
        }
        
    def register_lab_device(self, mac: str, name: str, device_type: str):
        """
        Registra dispositivo do laboratório para identificação.
        
        Args:
            mac: MAC address do dispositivo
            name: Nome amigável (ex: "Arduino-1", "Phone-Filho1")
            device_type: Tipo (arduino, phone, tablet, laptop)
        """
        self.device_registry[mac.lower()] = {
            'name': name,
            'type': device_type,
            'first_seen': datetime.now().isoformat()
        }
        print(f"[LAB] Dispositivo registrado: {name} ({mac})")
    
    def start_capture(self, duration: int = 60, packet_count: int = 1000):
        """
        Inicia captura de pacotes no modo educacional.
        
        Args:
            duration: Duração em segundos
            packet_count: Número máximo de pacotes
        """
        if self.lab_mode:
            print("\n" + "="*70)
            print("🎓 LABORATÓRIO DE SEGURANÇA WiFi - MODO EDUCACIONAL")
            print("="*70)
            print("⚠️  Use apenas em sua rede doméstica!")
            print("📚 Objetivo: Ensinar sobre segurança em redes abertas")
            print(f"🔍 Interface: {self.interface}")
            print(f"⏱️  Duração: {duration} segundos")
            print("="*70 + "\n")
        
        print("🎯 Iniciando captura... (Ctrl+C para parar)\n")
        
        try:
            packets = sniff(
                iface=self.interface,
                prn=self._process_packet,
                timeout=duration,
                count=packet_count,
                store=True
            )
            
            print(f"\n✅ Captura finalizada: {len(packets)} pacotes analisados")
            self._show_summary()
            
        except PermissionError:
            print("❌ ERRO: Necessário executar com sudo/root")
            print("💡 Comando: sudo python3 <script>")
        except KeyboardInterrupt:
            print("\n⏹️  Captura interrompida pelo usuário")
            self._show_summary()
        except Exception as e:
            print(f"❌ ERRO: {e}")
    
    def _process_packet(self, packet):
        """Processa cada pacote capturado"""
        self.stats['total_packets'] += 1
        
        # Análise de DNS (descobrir o que dispositivos estão acessando)
        if packet.haslayer(DNSQR):
            self._analyze_dns(packet)
        
        # Análise de HTTP (dados não criptografados - PERIGO!)
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            self._analyze_http(packet)
        
        # Análise de HTTPS (seguro, mas ainda vemos IPs)
        if packet.haslayer(TCP):
            self._analyze_https(packet)
        
        # Análise de ARP (descobrir dispositivos na rede)
        if packet.haslayer(ARP):
            self._analyze_arp(packet)
    
    def _analyze_dns(self, packet):
        """Analisa queries DNS - mostra o que dispositivos estão acessando"""
        self.stats['dns_queries'] += 1
        
        if packet.haslayer(DNSQR):
            query = packet[DNSQR].qname.decode('utf-8', errors='ignore')
            src_ip = packet[IP].src if packet.haslayer(IP) else "Unknown"
            
            # Identifica dispositivo
            device_name = self._identify_device(src_ip, packet)
            
            # Categoriza o acesso
            danger_level, educational_note = self._categorize_dns_query(query)
            
            intercepted = InterceptedData(
                timestamp=datetime.now().isoformat(),
                device_name=device_name,
                device_mac=packet[Ether].src if packet.haslayer(Ether) else "Unknown",
                device_ip=src_ip,
                protocol="DNS",
                danger_level=danger_level,
                description=f"Acessando: {query}",
                educational_note=educational_note
            )
            
            self.captured_data.append(intercepted)
            
            if self.lab_mode:
                self._print_interception(intercepted)
    
    def _analyze_http(self, packet):
        """Analisa tráfego HTTP - DADOS NÃO CRIPTOGRAFADOS!"""
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            # Verifica se é HTTP
            if 'HTTP' in payload[:20] or 'GET' in payload[:10] or 'POST' in payload[:10]:
                self.stats['http_packets'] += 1
                self.stats['leaked_data'] += 1
                
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                device_name = self._identify_device(src_ip, packet)
                
                # Extrai informações sensíveis
                sensitive_info = self._extract_sensitive_data(payload)
                
                intercepted = InterceptedData(
                    timestamp=datetime.now().isoformat(),
                    device_name=device_name,
                    device_mac=packet[Ether].src if packet.haslayer(Ether) else "Unknown",
                    device_ip=src_ip,
                    protocol="HTTP",
                    danger_level="DANGER",
                    description=f"⚠️ DADOS NÃO CRIPTOGRAFADOS para {dst_ip}",
                    raw_data=payload[:200],
                    educational_note=(
                        "🚨 HTTP NÃO É SEGURO! Qualquer pessoa na rede pode ler isso!\n"
                        f"   Dados visíveis: {sensitive_info}"
                    )
                )
                
                self.captured_data.append(intercepted)
                
                if self.lab_mode:
                    self._print_interception(intercepted)
        
        except:
            pass
    
    def _analyze_https(self, packet):
        """Analisa tráfego HTTPS - criptografado mas vemos metadados"""
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            
            # Porta 443 = HTTPS
            if tcp_layer.dport == 443 or tcp_layer.sport == 443:
                self.stats['https_packets'] += 1
                self.stats['safe_data'] += 1
                
                src_ip = packet[IP].src if packet.haslayer(IP) else "Unknown"
                dst_ip = packet[IP].dst if packet.haslayer(IP) else "Unknown"
                device_name = self._identify_device(src_ip, packet)
                
                # Mesmo com HTTPS, vemos IP de destino
                intercepted = InterceptedData(
                    timestamp=datetime.now().isoformat(),
                    device_name=device_name,
                    device_mac=packet[Ether].src if packet.haslayer(Ether) else "Unknown",
                    device_ip=src_ip,
                    protocol="HTTPS",
                    danger_level="SAFE",
                    description=f"✅ Conexão segura com {dst_ip}",
                    educational_note=(
                        "🔒 HTTPS é SEGURO! Dados criptografados.\n"
                        "   Mas ainda vemos: IP origem, IP destino, horário"
                    )
                )
                
                # Só mostra alguns exemplos HTTPS para não poluir
                if self.stats['https_packets'] % 100 == 0 and self.lab_mode:
                    self._print_interception(intercepted)
    
    def _analyze_arp(self, packet):
        """Analisa ARP - descobre dispositivos na rede"""
        if packet.haslayer(ARP):
            arp_layer = packet[ARP]
            
            if arp_layer.op == 2:  # ARP Reply
                mac = arp_layer.hwsrc
                ip = arp_layer.psrc
                
                if mac.lower() not in [k.lower() for k in self.device_registry.keys()]:
                    device_info = {
                        'name': f"Device-{mac[-5:].replace(':', '')}",
                        'type': 'unknown',
                        'first_seen': datetime.now().isoformat()
                    }
                    self.device_registry[mac.lower()] = device_info
                    
                    if self.lab_mode:
                        print(f"📱 Novo dispositivo detectado: {device_info['name']} ({ip})")
    
    def _identify_device(self, ip: str, packet) -> str:
        """Identifica dispositivo pelo MAC ou IP"""
        if packet.haslayer(Ether):
            mac = packet[Ether].src.lower()
            if mac in self.device_registry:
                return self.device_registry[mac]['name']
        
        return f"Device-{ip.split('.')[-1]}"
    
    def _categorize_dns_query(self, query: str) -> tuple:
        """Categoriza query DNS e retorna (danger_level, educational_note)"""
        query_lower = query.lower()
        
        # Sites educacionais
        if any(edu in query_lower for edu in ['edu', 'escola', 'wikipedia']):
            return "SAFE", "🎓 Site educacional - Seguro"
        
        # Redes sociais
        if any(social in query_lower for social in ['facebook', 'instagram', 'tiktok', 'twitter']):
            return "WARNING", "📱 Rede social - Cuidado com informações pessoais"
        
        # Streaming
        if any(stream in query_lower for stream in ['youtube', 'netflix', 'spotify']):
            return "SAFE", "🎬 Streaming - Geralmente seguro"
        
        # Games
        if any(game in query_lower for game in ['minecraft', 'roblox', 'steam', 'game']):
            return "WARNING", "🎮 Gaming - Cuidado com chat de desconhecidos"
        
        # Bancos/Pagamentos
        if any(bank in query_lower for bank in ['bank', 'banco', 'pay', 'payment']):
            return "DANGER", "🏦 Financeiro - NUNCA use em rede pública!"
        
        return "SAFE", "ℹ️  Site comum"
    
    def _extract_sensitive_data(self, payload: str) -> str:
        """Extrai dados sensíveis de payload HTTP"""
        sensitive_items = []
        
        if 'password' in payload.lower():
            sensitive_items.append("SENHA")
        if 'user' in payload.lower() or 'email' in payload.lower():
            sensitive_items.append("USUÁRIO/EMAIL")
        if 'cookie' in payload.lower():
            sensitive_items.append("COOKIES")
        if 'token' in payload.lower():
            sensitive_items.append("TOKEN")
        
        return ", ".join(sensitive_items) if sensitive_items else "Headers, URLs"
    
    def _print_interception(self, data: InterceptedData):
        """Imprime interceptação no modo educacional"""
        colors = {
            'SAFE': '\033[92m',      # Verde
            'WARNING': '\033[93m',   # Amarelo
            'DANGER': '\033[91m'     # Vermelho
        }
        reset = '\033[0m'
        
        color = colors.get(data.danger_level, '')
        icon = {'SAFE': '✅', 'WARNING': '⚠️', 'DANGER': '🚨'}.get(data.danger_level, 'ℹ️')
        
        print(f"{color}{icon} [{data.protocol}] {data.device_name}{reset}")
        print(f"   {data.description}")
        if data.educational_note:
            print(f"   💡 {data.educational_note}")
        print()
    
    def _show_summary(self):
        """Mostra resumo educacional da captura"""
        print("\n" + "="*70)
        print("📊 RESUMO DO LABORATÓRIO")
        print("="*70)
        print(f"Total de pacotes analisados: {self.stats['total_packets']}")
        print(f"🔍 DNS queries (sites acessados): {self.stats['dns_queries']}")
        print(f"✅ HTTPS (seguro): {self.stats['https_packets']}")
        print(f"⚠️  HTTP (INSEGURO): {self.stats['http_packets']}")
        print(f"🚨 Dados vazados: {self.stats['leaked_data']}")
        print(f"🔒 Dados protegidos: {self.stats['safe_data']}")
        print("="*70)
        
        if self.lab_mode:
            print("\n🎓 LIÇÃO APRENDIDA:")
            if self.stats['http_packets'] > 0:
                print("   🚨 Detectamos tráfego HTTP (não criptografado)!")
                print("   ⚠️  Em rede pública, qualquer pessoa veria esses dados!")
                print("   ✅ SEMPRE use HTTPS (cadeado no navegador)")
            else:
                print("   ✅ Parabéns! Todo tráfego estava criptografado (HTTPS)")
            
            print("\n💡 REGRA DE OURO:")
            print("   NUNCA se conecte em redes WiFi públicas abertas!")
            print("   Se precisar, use VPN ou dados móveis.")
            print("="*70 + "\n")
    
    def export_results(self, filename: str = None):
        """Exporta resultados para análise posterior"""
        if not filename:
            filename = f"lab_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("LABORATÓRIO DE SEGURANÇA WiFi - RESULTADOS\n")
            f.write("="*70 + "\n\n")
            
            f.write("ESTATÍSTICAS:\n")
            for key, value in self.stats.items():
                f.write(f"  {key}: {value}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("INTERCEPTAÇÕES DETALHADAS:\n")
            f.write("="*70 + "\n\n")
            
            for data in self.captured_data:
                f.write(f"[{data.timestamp}] {data.danger_level}\n")
                f.write(f"Dispositivo: {data.device_name} ({data.device_ip})\n")
                f.write(f"Protocolo: {data.protocol}\n")
                f.write(f"Descrição: {data.description}\n")
                if data.educational_note:
                    f.write(f"Nota: {data.educational_note}\n")
                f.write("\n" + "-"*70 + "\n\n")
        
        print(f"📄 Resultados exportados para: {filename}")


def create_lab_scenario():
    """
    Cria cenário de laboratório com dispositivos registrados.
    Exemplo de uso para aula educacional.
    """
    print("🎓 Configurando Laboratório Educacional WiFi")
    print("="*70)
    
    # Cria interceptador
    interceptor = WiFiLabInterceptor(interface="wlan0", lab_mode=True)
    
    # Registra dispositivos do laboratório (substitua pelos seus MACs)
    print("\n📱 Registrando dispositivos do laboratório...")
    print("💡 Dica: Use 'ip link show' para ver MAC addresses\n")
    
    # Exemplos (substitua pelos seus dispositivos reais)
    # interceptor.register_lab_device("aa:bb:cc:dd:ee:01", "Arduino-ESP32", "arduino")
    # interceptor.register_lab_device("aa:bb:cc:dd:ee:02", "Phone-Filho1", "phone")
    # interceptor.register_lab_device("aa:bb:cc:dd:ee:03", "Laptop-Lab", "laptop")
    
    print("✅ Laboratório configurado!")
    print("\n⚠️  IMPORTANTE:")
    print("   1. Use apenas em sua rede doméstica")
    print("   2. Informe todos os participantes sobre a captura")
    print("   3. Objetivo: EDUCAÇÃO sobre segurança\n")
    
    return interceptor


if __name__ == "__main__":
    """Exemplo de uso do laboratório"""
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          🎓 LABORATÓRIO DE SEGURANÇA WiFi EDUCACIONAL 🎓             ║
║                                                                      ║
║  Demonstra perigos de redes abertas em ambiente controlado          ║
║  Use apenas com sua família em sua rede doméstica!                  ║
║                                                                      ║
║  Author: Professor JuanCS-Dev ✝️                                     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Verifica se está rodando como root
    if os.geteuid() != 0:
        print("❌ Este script precisa ser executado com sudo/root")
        print("💡 Comando: sudo python3 wifi_lab_interceptor.py")
        sys.exit(1)
    
    # Cria laboratório
    interceptor = create_lab_scenario()
    
    # Pergunta interface
    print(f"\n🔍 Interface padrão: {interceptor.interface}")
    interface = input("   Pressione ENTER para continuar ou digite outra interface: ").strip()
    if interface:
        interceptor.interface = interface
    
    # Pergunta duração
    print(f"\n⏱️  Duração da captura")
    duration = input("   Quantos segundos? (padrão: 60): ").strip()
    duration = int(duration) if duration.isdigit() else 60
    
    print("\n🚀 Iniciando captura educacional...\n")
    
    # Inicia captura
    interceptor.start_capture(duration=duration)
    
    # Exporta resultados
    export = input("\n💾 Exportar resultados? (s/N): ").strip().lower()
    if export == 's':
        interceptor.export_results()
    
    print("\n🎓 Aula concluída! Discuta os resultados com seus filhos.")
    print("💡 Reforce: NUNCA use redes WiFi públicas sem proteção!\n")
