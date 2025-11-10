#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📶 WiFi Collector - Coleta informações sobre rede WiFi
SSID, sinal, segurança, frequência, dispositivos conectados
"""

import subprocess
import re
import random
from typing import Optional, List
from models.network_snapshot import WiFiInfo


class WiFiCollector:
    """Coleta informações sobre a rede WiFi"""
    
    def __init__(self, interface: Optional[str] = None, mock_mode: bool = False):
        """
        Inicializa o collector
        
        Args:
            interface: Interface WiFi (auto-detecta se None)
            mock_mode: Se True, simula dados
        """
        self.interface = interface
        self.mock_mode = mock_mode
        
        if not interface and not mock_mode:
            self.interface = self._detect_wifi_interface()
    
    def _detect_wifi_interface(self) -> Optional[str]:
        """Detecta interface WiFi ativa"""
        try:
            result = subprocess.run(
                ['ip', '-o', 'link', 'show'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'wlan' in line or 'wlp' in line:
                        match = re.search(r'^\d+:\s+(\S+):', line)
                        if match:
                            iface = match.group(1).split('@')[0]
                            # Verifica se está UP
                            if 'UP' in line:
                                return iface
        except:
            pass
        
        return None
    
    def collect(self) -> WiFiInfo:
        """Coleta informações atuais do WiFi"""
        if self.mock_mode or not self.interface:
            return self._collect_mock()
        else:
            return self._collect_real()
    
    def _collect_real(self) -> WiFiInfo:
        """Coleta dados REAIS do WiFi"""
        wifi = WiFiInfo()
        wifi.interface = self.interface
        
        try:
            # Usa iwconfig para pegar informações básicas
            result = subprocess.run(
                ['iwconfig', self.interface],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout
                
                # SSID
                ssid_match = re.search(r'ESSID:"([^"]+)"', output)
                if ssid_match:
                    wifi.ssid = ssid_match.group(1)
                    wifi.connected = True
                
                # Frequência
                freq_match = re.search(r'Frequency:([\d.]+)\s*GHz', output)
                if freq_match:
                    freq = float(freq_match.group(1))
                    if freq < 3:
                        wifi.frequency = "2.4GHz"
                    elif freq < 6:
                        wifi.frequency = "5GHz"
                    else:
                        wifi.frequency = "6GHz"
                
                # Qualidade do sinal
                quality_match = re.search(r'Link Quality=(\d+)/(\d+)', output)
                if quality_match:
                    current = int(quality_match.group(1))
                    maximum = int(quality_match.group(2))
                    wifi.signal_strength = int((current / maximum) * 100)
                else:
                    # Tenta pegar por dBm
                    signal_match = re.search(r'Signal level=(-?\d+)\s*dBm', output)
                    if signal_match:
                        dbm = int(signal_match.group(1))
                        # Converte dBm para porcentagem (aproximado)
                        wifi.signal_strength = min(100, max(0, (dbm + 100) * 2))
            
            # Usa iw para informações mais detalhadas
            try:
                result = subprocess.run(
                    ['iw', 'dev', self.interface, 'link'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    output = result.stdout
                    
                    # Canal
                    channel_match = re.search(r'freq:\s*(\d+)', output)
                    if channel_match:
                        freq_mhz = int(channel_match.group(1))
                        # Conversão aproximada de MHz para canal
                        if freq_mhz < 3000:
                            wifi.channel = (freq_mhz - 2412) // 5 + 1
                        else:
                            wifi.channel = (freq_mhz - 5180) // 5 + 36
            except:
                pass
            
            # IP address
            try:
                result = subprocess.run(
                    ['ip', 'addr', 'show', self.interface],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    ip_match = re.search(r'inet\s+([\d.]+)', result.stdout)
                    if ip_match:
                        wifi.ip_address = ip_match.group(1)
            except:
                pass
            
            # Segurança (requer wpa_cli ou iw, pode falhar sem root)
            wifi.security = self._detect_security()
            
        except Exception as e:
            print(f"Erro coletando WiFi: {e}")
        
        return wifi
    
    def _detect_security(self) -> str:
        """Tenta detectar tipo de segurança"""
        try:
            # Tenta usando iw scan (requer privilégios)
            result = subprocess.run(
                ['sudo', 'iw', self.interface, 'scan'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout
                if 'WPA3' in output:
                    return 'WPA3'
                elif 'RSN' in output or 'WPA2' in output:
                    return 'WPA2'
                elif 'WPA' in output:
                    return 'WPA'
                elif 'Open' in output or 'privacy: off' in output:
                    return 'Open'
        except:
            pass
        
        # Fallback: assume WPA2 se conectado
        return 'WPA2 (assumed)'
    
    def _collect_mock(self) -> WiFiInfo:
        """Gera dados SIMULADOS realistas"""
        wifi = WiFiInfo()
        
        # Simula rede doméstica típica
        mock_networks = [
            ("Casa_WiFi", "WPA2", "5GHz", 85),
            ("NET_2G", "WPA2", "2.4GHz", 72),
            ("VIVO_FIBRA", "WPA3", "5GHz", 92),
        ]
        
        network = random.choice(mock_networks)
        
        wifi.ssid = network[0]
        wifi.security = network[1]
        wifi.frequency = network[2]
        wifi.signal_strength = network[3] + random.randint(-5, 5)
        wifi.signal_strength = max(0, min(100, wifi.signal_strength))
        
        wifi.connected = True
        wifi.interface = "wlan0"
        wifi.ip_address = f"192.168.1.{random.randint(100, 250)}"
        wifi.channel = random.choice([1, 6, 11, 36, 40, 44, 48])
        wifi.encryption = "CCMP" if "WPA" in wifi.security else "None"
        wifi.mac_address = self._generate_random_mac()
        
        return wifi
    
    def _generate_random_mac(self) -> str:
        """Gera endereço MAC aleatório"""
        return ':'.join([f"{random.randint(0, 255):02X}" for _ in range(6)])
    
    def scan_networks(self) -> List[dict]:
        """Escaneia redes WiFi disponíveis (requer privilégios)"""
        if self.mock_mode or not self.interface:
            return self._scan_mock()
        
        networks = []
        
        try:
            result = subprocess.run(
                ['sudo', 'iwlist', self.interface, 'scan'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                output = result.stdout
                
                # Parse output (formato iwlist)
                cells = output.split('Cell ')
                for cell in cells[1:]:  # Pula primeira entrada vazia
                    network = {}
                    
                    # SSID
                    ssid_match = re.search(r'ESSID:"([^"]+)"', cell)
                    if ssid_match:
                        network['ssid'] = ssid_match.group(1)
                    
                    # Sinal
                    signal_match = re.search(r'Quality=(\d+)/(\d+)', cell)
                    if signal_match:
                        quality = int(signal_match.group(1))
                        maximum = int(signal_match.group(2))
                        network['signal'] = int((quality / maximum) * 100)
                    
                    # Frequência
                    freq_match = re.search(r'Frequency:([\d.]+)', cell)
                    if freq_match:
                        freq = float(freq_match.group(1))
                        network['frequency'] = f"{freq:.1f}GHz"
                    
                    # Segurança
                    if 'WPA3' in cell:
                        network['security'] = 'WPA3'
                    elif 'WPA2' in cell or 'RSN' in cell:
                        network['security'] = 'WPA2'
                    elif 'WPA' in cell:
                        network['security'] = 'WPA'
                    else:
                        network['security'] = 'Open'
                    
                    if network.get('ssid'):
                        networks.append(network)
        
        except Exception as e:
            print(f"Erro escaneando redes: {e}")
        
        return networks if networks else self._scan_mock()
    
    def _scan_mock(self) -> List[dict]:
        """Gera lista de redes simuladas"""
        mock_networks = [
            {"ssid": "Casa_WiFi", "signal": 92, "frequency": "5GHz", "security": "WPA3"},
            {"ssid": "NET_2G", "signal": 78, "frequency": "2.4GHz", "security": "WPA2"},
            {"ssid": "VIVO_FIBRA", "signal": 65, "frequency": "5GHz", "security": "WPA2"},
            {"ssid": "Vizinho_Net", "signal": 45, "frequency": "2.4GHz", "security": "WPA2"},
            {"ssid": "FREE_WIFI", "signal": 32, "frequency": "2.4GHz", "security": "Open"},
            {"ssid": "CLARO_5G", "signal": 88, "frequency": "5GHz", "security": "WPA3"},
        ]
        
        return random.sample(mock_networks, random.randint(3, 6))
