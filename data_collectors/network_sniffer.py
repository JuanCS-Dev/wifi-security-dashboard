#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Network Sniffer - Detecta dispositivos e aplicativos na rede
Usa Scapy para captura de pacotes e análise em tempo real
"""

import threading
import time
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Callable
from collections import defaultdict
from models.network_snapshot import DeviceInfo, AppInfo


class NetworkSniffer:
    """Sniffer de rede para detectar dispositivos e aplicativos"""
    
    def __init__(self, interface: Optional[str] = None, mock_mode: bool = False, callback: Optional[Callable] = None):
        """
        Inicializa o sniffer
        
        Args:
            interface: Interface de rede para monitorar
            mock_mode: Se True, gera dados simulados
            callback: Função chamada quando novos dados estão disponíveis
        """
        self.interface = interface
        self.mock_mode = mock_mode
        self.callback = callback
        self.running = False
        self.thread = None
        
        # Storage
        self.devices: Dict[str, DeviceInfo] = {}
        self.apps: Dict[str, AppInfo] = {}
        self.lock = threading.Lock()
        
        # Statistics
        self.total_packets = 0
        self.bytes_sent = 0
        self.bytes_recv = 0
        
        # Scapy availability
        self.has_scapy = False
        try:
            from scapy.all import sniff, IP, TCP, UDP, DNS, Raw
            self.scapy = True
            self.has_scapy = True
            self.IP = IP
            self.TCP = TCP
            self.UDP = UDP
            self.DNS = DNS
            self.Raw = Raw
        except ImportError:
            self.scapy = None
            self.mock_mode = True
    
    def start(self):
        """Inicia captura de pacotes em thread separada"""
        if self.running:
            return
        
        self.running = True
        
        if self.mock_mode:
            self.thread = threading.Thread(target=self._mock_loop, daemon=True)
        else:
            self.thread = threading.Thread(target=self._sniff_loop, daemon=True)
        
        self.thread.start()
    
    def stop(self):
        """Para a captura"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _sniff_loop(self):
        """Loop de captura REAL usando Scapy"""
        if not self.has_scapy:
            print("Scapy não disponível, usando modo mock")
            self._mock_loop()
            return
        
        try:
            from scapy.all import sniff
            
            print(f"Iniciando captura na interface {self.interface}...")
            
            sniff(
                iface=self.interface,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda x: not self.running
            )
        except PermissionError:
            print("⚠️  Permissão negada! Execute com sudo para captura real.")
            print("Mudando para modo simulado...")
            self.mock_mode = True
            self._mock_loop()
        except Exception as e:
            print(f"Erro na captura: {e}")
            self.mock_mode = True
            self._mock_loop()
    
    def _process_packet(self, packet):
        """Processa um pacote capturado"""
        try:
            self.total_packets += 1
            
            if not packet.haslayer(self.IP):
                return
            
            ip_layer = packet[self.IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            packet_len = len(packet)
            
            # Atualiza device info
            with self.lock:
                # Source device
                if src_ip not in self.devices:
                    self.devices[src_ip] = DeviceInfo(
                        ip_address=src_ip,
                        mac_address=packet.src if hasattr(packet, 'src') else "Unknown",
                        is_new=True
                    )
                
                device = self.devices[src_ip]
                device.last_seen = datetime.now()
                device.bytes_sent += packet_len
                device.packets_sent += 1
                
                # Detecta aplicativo
                if packet.haslayer(self.TCP) or packet.haslayer(self.UDP):
                    app_name = self._identify_app(packet)
                    if app_name and app_name not in device.active_apps:
                        device.active_apps.append(app_name)
                    
                    if app_name:
                        if app_name not in self.apps:
                            self.apps[app_name] = AppInfo(name=app_name)
                        
                        self.apps[app_name].bytes_sent += packet_len
                        self.apps[app_name].connections += 1
                        self.apps[app_name].last_seen = datetime.now()
                
                self.bytes_sent += packet_len
            
            # Callback
            if self.callback:
                self.callback()
        
        except Exception as e:
            pass  # Ignora erros individuais de pacotes
    
    def _identify_app(self, packet) -> Optional[str]:
        """Identifica aplicativo pelo pacote"""
        try:
            # DNS queries
            if packet.haslayer(self.DNS) and packet[self.DNS].qd:
                domain = packet[self.DNS].qd.qname.decode('utf-8').strip('.')
                return self._identify_by_domain(domain)
            
            # HTTP Host header
            if packet.haslayer(self.Raw):
                payload = packet[self.Raw].load
                if isinstance(payload, bytes):
                    payload_str = payload.decode('utf-8', errors='ignore')
                    if 'Host:' in payload_str:
                        match = re.search(r'Host:\s*([^\r\n]+)', payload_str)
                        if match:
                            host = match.group(1).strip()
                            return self._identify_by_domain(host)
            
            # Por porta
            if packet.haslayer(self.TCP):
                port = packet[self.TCP].dport
                return self._identify_by_port(port)
            elif packet.haslayer(self.UDP):
                port = packet[self.UDP].dport
                return self._identify_by_port(port)
        
        except:
            pass
        
        return None
    
    def _identify_by_domain(self, domain: str) -> Optional[str]:
        """Identifica app por domínio"""
        domain = domain.lower()
        
        if 'youtube' in domain or 'googlevideo' in domain:
            return 'YouTube'
        elif 'netflix' in domain:
            return 'Netflix'
        elif 'whatsapp' in domain:
            return 'WhatsApp'
        elif 'telegram' in domain:
            return 'Telegram'
        elif 'discord' in domain:
            return 'Discord'
        elif 'facebook' in domain or 'fbcdn' in domain:
            return 'Facebook'
        elif 'instagram' in domain or 'cdninstagram' in domain:
            return 'Instagram'
        elif 'twitter' in domain or 'twimg' in domain:
            return 'Twitter'
        elif 'spotify' in domain:
            return 'Spotify'
        elif 'twitch' in domain:
            return 'Twitch'
        elif 'steam' in domain:
            return 'Steam'
        elif 'amazon' in domain:
            return 'Amazon'
        elif 'google' in domain:
            return 'Google'
        
        return None
    
    def _identify_by_port(self, port: int) -> Optional[str]:
        """Identifica serviço por porta"""
        port_map = {
            80: 'HTTP',
            443: 'HTTPS',
            22: 'SSH',
            21: 'FTP',
            25: 'SMTP',
            53: 'DNS',
            3389: 'RDP',
            5222: 'XMPP',
            5228: 'Google Services',
        }
        
        return port_map.get(port)
    
    def _mock_loop(self):
        """Gera dados simulados realistas"""
        # Dispositivos simulados
        mock_devices = [
            ("192.168.1.100", "AA:BB:CC:DD:EE:01", "phone", "iPhone 12"),
            ("192.168.1.101", "AA:BB:CC:DD:EE:02", "computer", "Laptop"),
            ("192.168.1.102", "AA:BB:CC:DD:EE:03", "phone", "Galaxy S21"),
            ("192.168.1.103", "AA:BB:CC:DD:EE:04", "iot", "Smart TV"),
            ("192.168.1.104", "AA:BB:CC:DD:EE:05", "computer", "Desktop PC"),
        ]
        
        # Aplicativos populares
        mock_apps = ["YouTube", "Netflix", "WhatsApp", "Chrome", "Firefox", "Instagram", "Spotify"]
        
        # Inicializa dispositivos
        with self.lock:
            for ip, mac, dev_type, hostname in mock_devices:
                self.devices[ip] = DeviceInfo(
                    ip_address=ip,
                    mac_address=mac,
                    hostname=hostname,
                    device_type=dev_type,
                    is_new=random.random() < 0.3
                )
        
        # Simula tráfego contínuo
        while self.running:
            with self.lock:
                # Atualiza dispositivos
                for ip, device in self.devices.items():
                    # Simula atividade aleatória
                    if random.random() < 0.8:  # 80% chance de estar ativo
                        bytes_delta = random.randint(1000, 500000)  # 1KB - 500KB
                        device.bytes_sent += bytes_delta // 3
                        device.bytes_received += bytes_delta * 2 // 3
                        device.packets_sent += random.randint(10, 100)
                        device.packets_received += random.randint(20, 200)
                        device.last_seen = datetime.now()
                        
                        # Simula apps ativos
                        if random.random() < 0.3:
                            app = random.choice(mock_apps)
                            if app not in device.active_apps:
                                device.active_apps.append(app)
                            
                            # Atualiza stats do app
                            if app not in self.apps:
                                self.apps[app] = AppInfo(
                                    name=app,
                                    category=self._get_app_category(app)
                                )
                            
                            self.apps[app].bytes_sent += bytes_delta // 4
                            self.apps[app].bytes_received += bytes_delta * 3 // 4
                            self.apps[app].connections += 1
                            self.apps[app].last_seen = datetime.now()
                
                # Stats globais
                self.total_packets += random.randint(100, 500)
                self.bytes_sent += random.randint(50000, 200000)
                self.bytes_recv += random.randint(100000, 500000)
            
            # Callback
            if self.callback:
                self.callback()
            
            time.sleep(1)  # Atualiza a cada segundo
    
    def _get_app_category(self, app_name: str) -> str:
        """Retorna categoria do app"""
        categories = {
            'YouTube': 'streaming',
            'Netflix': 'streaming',
            'Spotify': 'streaming',
            'Twitch': 'streaming',
            'WhatsApp': 'messaging',
            'Telegram': 'messaging',
            'Discord': 'messaging',
            'Instagram': 'social',
            'Facebook': 'social',
            'Twitter': 'social',
            'Chrome': 'browsing',
            'Firefox': 'browsing',
            'Safari': 'browsing',
            'Steam': 'gaming',
        }
        return categories.get(app_name, 'unknown')
    
    def get_devices(self) -> List[DeviceInfo]:
        """Retorna lista de dispositivos detectados"""
        with self.lock:
            return list(self.devices.values())
    
    def get_apps(self) -> List[AppInfo]:
        """Retorna lista de aplicativos detectados"""
        with self.lock:
            return list(self.apps.values())
    
    def get_stats(self) -> dict:
        """Retorna estatísticas gerais"""
        with self.lock:
            return {
                'total_packets': self.total_packets,
                'bytes_sent': self.bytes_sent,
                'bytes_recv': self.bytes_recv,
                'total_devices': len(self.devices),
                'total_apps': len(self.apps),
            }
    
    def clear(self):
        """Limpa dados coletados"""
        with self.lock:
            self.devices.clear()
            self.apps.clear()
            self.total_packets = 0
            self.bytes_sent = 0
            self.bytes_recv = 0
