#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Modelos de Dados para o Dashboard Educacional
Estruturas que representam o estado da rede em tempo real
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque


@dataclass
class WiFiInfo:
    """Informações sobre a rede WiFi conectada"""
    ssid: str = "Não conectado"
    signal_strength: int = 0  # 0-100
    frequency: str = "N/A"  # 2.4GHz, 5GHz, 6GHz
    channel: int = 0
    security: str = "Unknown"  # WPA2, WPA3, Open
    encryption: str = "Unknown"
    mac_address: str = "00:00:00:00:00:00"
    connected: bool = False
    interface: str = "wlan0"
    ip_address: str = "0.0.0.0"
    
    def get_security_level(self) -> str:
        """Retorna nível de segurança simplificado"""
        if "WPA3" in self.security.upper():
            return "🔒 MUITO SEGURO"
        elif "WPA2" in self.security.upper():
            return "🔐 SEGURO"
        elif "WPA" in self.security.upper():
            return "⚠️ SEGURANÇA FRACA"
        elif "OPEN" in self.security.upper() or "None" in self.security:
            return "🚨 INSEGURO!"
        return "❓ DESCONHECIDO"
    
    def get_frequency_explanation(self) -> str:
        """Explicação educacional sobre frequência"""
        if "2.4" in self.frequency:
            return "2.4GHz: Mais alcance, mais lento"
        elif "5" in self.frequency:
            return "5GHz: Menos alcance, mais rápido"
        elif "6" in self.frequency:
            return "6GHz: WiFi 6E - Super rápido!"
        return "Frequência desconhecida"


@dataclass
class DeviceInfo:
    """Informações sobre um dispositivo na rede"""
    ip_address: str
    mac_address: str
    hostname: str = "Unknown"
    device_type: str = "unknown"  # phone, computer, iot, router
    vendor: str = "Unknown"
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    active_apps: List[str] = field(default_factory=list)
    is_new: bool = False
    
    @property
    def total_traffic(self) -> int:
        """Total de tráfego em bytes"""
        return self.bytes_sent + self.bytes_received
    
    @property
    def is_active(self) -> bool:
        """Dispositivo ativo nos últimos 5 minutos"""
        return (datetime.now() - self.last_seen).seconds < 300
    
    def get_emoji(self) -> str:
        """Retorna emoji apropriado para o tipo"""
        type_map = {
            'phone': '📱',
            'mobile': '📱',
            'computer': '💻',
            'laptop': '💻',
            'router': '📡',
            'iot': '🏠',
            'smart': '🏠',
            'tv': '📺',
            'unknown': '❓'
        }
        for key, emoji in type_map.items():
            if key in self.device_type.lower():
                return emoji
        return '❓'


@dataclass
class AppInfo:
    """Informações sobre um aplicativo detectado"""
    name: str
    category: str = "unknown"  # streaming, messaging, browsing, gaming
    bytes_sent: int = 0
    bytes_received: int = 0
    connections: int = 0
    last_seen: datetime = field(default_factory=datetime.now)
    protocol: str = "Unknown"  # HTTP, HTTPS, DNS, etc
    domains: List[str] = field(default_factory=list)
    
    @property
    def total_traffic(self) -> int:
        """Total de tráfego em bytes"""
        return self.bytes_sent + self.bytes_received
    
    def get_emoji(self) -> str:
        """Retorna emoji apropriado para o app"""
        app_lower = self.name.lower()
        
        # Streaming
        if 'youtube' in app_lower:
            return '▶️'
        elif 'netflix' in app_lower:
            return '🎬'
        elif 'spotify' in app_lower:
            return '🎵'
        elif 'twitch' in app_lower:
            return '🎮'
        
        # Messaging
        elif 'whatsapp' in app_lower:
            return '💬'
        elif 'telegram' in app_lower:
            return '✈️'
        elif 'discord' in app_lower:
            return '💭'
        
        # Browsers
        elif 'chrome' in app_lower:
            return '🌐'
        elif 'firefox' in app_lower:
            return '🦊'
        elif 'safari' in app_lower:
            return '🧭'
        
        # Gaming
        elif 'steam' in app_lower:
            return '🎮'
        elif 'epic' in app_lower:
            return '🎯'
        
        # Category fallback
        elif self.category == 'streaming':
            return '📺'
        elif self.category == 'messaging':
            return '💬'
        elif self.category == 'browsing':
            return '🌐'
        elif self.category == 'gaming':
            return '🎮'
        
        return '📦'
    
    def get_educational_info(self) -> str:
        """Informação educacional sobre o app"""
        if 'youtube' in self.name.lower():
            return "YouTube usa muito dados para vídeos HD"
        elif 'netflix' in self.name.lower():
            return "Netflix: 1 hora HD = ~3GB de internet"
        elif 'whatsapp' in self.name.lower():
            return "WhatsApp: mensagens criptografadas 🔒"
        elif 'game' in self.name.lower() or 'steam' in self.name.lower():
            return "Jogos precisam de conexão rápida (baixa latência)"
        else:
            return f"App de {self.category}"


@dataclass
class SystemMetrics:
    """Métricas do sistema (CPU, RAM, etc)"""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # CPU
    cpu_percent: float = 0.0
    cpu_freq_current: float = 0.0
    cpu_freq_max: float = 0.0
    cpu_count: int = 0
    
    # RAM
    ram_percent: float = 0.0
    ram_used_gb: float = 0.0
    ram_total_gb: float = 0.0
    ram_available_gb: float = 0.0
    
    # Disco
    disk_percent: float = 0.0
    disk_used_gb: float = 0.0
    disk_total_gb: float = 0.0
    disk_free_gb: float = 0.0
    
    # Temperatura (se disponível)
    temp_celsius: Optional[float] = None
    temp_available: bool = False
    
    # Network
    bytes_sent: int = 0
    bytes_recv: int = 0
    packets_sent: int = 0
    packets_recv: int = 0
    
    # Sistema
    uptime_seconds: int = 0
    
    def get_cpu_status(self) -> str:
        """Status educacional do CPU"""
        if self.cpu_percent < 30:
            return "😴 CPU descansando"
        elif self.cpu_percent < 60:
            return "🏃 CPU trabalhando"
        elif self.cpu_percent < 90:
            return "🔥 CPU muito ocupado!"
        else:
            return "🚨 CPU SOBRECARREGADO!"
    
    def get_ram_status(self) -> str:
        """Status educacional da RAM"""
        if self.ram_percent < 50:
            return "😊 Memória OK"
        elif self.ram_percent < 80:
            return "⚠️ Memória ficando cheia"
        else:
            return "🚨 Pouca memória livre!"
    
    def get_temp_status(self) -> str:
        """Status educacional da temperatura"""
        if not self.temp_available or self.temp_celsius is None:
            return "🌡️ Temperatura não disponível"
        
        if self.temp_celsius < 50:
            return "❄️ Bem frio"
        elif self.temp_celsius < 70:
            return "🌤️ Temperatura normal"
        elif self.temp_celsius < 85:
            return "🔥 Ficando quente!"
        else:
            return "🚨 MUITO QUENTE!"


@dataclass
class NetworkSnapshot:
    """Snapshot completo do estado da rede e sistema"""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # WiFi
    wifi: WiFiInfo = field(default_factory=WiFiInfo)
    
    # Dispositivos
    devices: List[DeviceInfo] = field(default_factory=list)
    total_devices: int = 0
    active_devices: int = 0
    new_devices: int = 0
    
    # Aplicativos
    apps: List[AppInfo] = field(default_factory=list)
    total_apps: int = 0
    
    # Sistema
    system: SystemMetrics = field(default_factory=SystemMetrics)
    
    # Tráfego (histórico para gráficos)
    download_history: deque = field(default_factory=lambda: deque(maxlen=60))  # Últimos 60s
    upload_history: deque = field(default_factory=lambda: deque(maxlen=60))
    
    # Estatísticas gerais
    total_bytes_sent: int = 0
    total_bytes_recv: int = 0
    total_packets: int = 0
    
    # Alertas educacionais
    alerts: List[str] = field(default_factory=list)
    
    def add_download_sample(self, bytes_per_sec: float):
        """Adiciona amostra de download ao histórico"""
        self.download_history.append(bytes_per_sec)
    
    def add_upload_sample(self, bytes_per_sec: float):
        """Adiciona amostra de upload ao histórico"""
        self.upload_history.append(bytes_per_sec)
    
    def get_active_devices(self) -> List[DeviceInfo]:
        """Retorna apenas dispositivos ativos"""
        return [d for d in self.devices if d.is_active]
    
    def get_top_apps(self, limit: int = 10) -> List[AppInfo]:
        """Retorna top N apps por tráfego"""
        return sorted(self.apps, key=lambda a: a.total_traffic, reverse=True)[:limit]
    
    def get_educational_summary(self) -> Dict[str, str]:
        """Retorna resumo educacional para as crianças"""
        return {
            'wifi_status': f"WiFi: {self.wifi.ssid} - {self.wifi.get_security_level()}",
            'devices': f"{self.active_devices} dispositivos usando a internet agora",
            'apps': f"{self.total_apps} aplicativos detectados",
            'cpu': self.system.get_cpu_status(),
            'ram': self.system.get_ram_status(),
            'temp': self.system.get_temp_status(),
        }
