#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💻 System Collector - Coleta métricas do sistema
CPU, RAM, Disco, Temperatura, Network stats
"""

import os
import time
import random
from datetime import datetime
from typing import Optional
from models.network_snapshot import SystemMetrics


class SystemCollector:
    """Coleta métricas de sistema em tempo real"""
    
    def __init__(self, mock_mode: bool = False):
        """
        Inicializa o collector
        
        Args:
            mock_mode: Se True, simula dados quando psutil não está disponível
        """
        self.mock_mode = mock_mode
        self.has_psutil = False
        self.start_time = time.time()
        
        # Tenta importar psutil
        try:
            import psutil
            self.psutil = psutil
            self.has_psutil = True
            self.mock_mode = False
        except ImportError:
            self.psutil = None
            self.mock_mode = True
    
    def collect(self) -> SystemMetrics:
        """Coleta métricas atuais do sistema"""
        if self.has_psutil and not self.mock_mode:
            return self._collect_real()
        else:
            return self._collect_mock()
    
    def _collect_real(self) -> SystemMetrics:
        """Coleta dados REAIS usando psutil"""
        metrics = SystemMetrics()
        
        try:
            # CPU
            metrics.cpu_percent = self.psutil.cpu_percent(interval=0.1)
            cpu_freq = self.psutil.cpu_freq()
            if cpu_freq:
                metrics.cpu_freq_current = cpu_freq.current
                metrics.cpu_freq_max = cpu_freq.max
            metrics.cpu_count = self.psutil.cpu_count()
            
            # RAM
            mem = self.psutil.virtual_memory()
            metrics.ram_percent = mem.percent
            metrics.ram_used_gb = mem.used / (1024**3)
            metrics.ram_total_gb = mem.total / (1024**3)
            metrics.ram_available_gb = mem.available / (1024**3)
            
            # Disco
            disk = self.psutil.disk_usage('/')
            metrics.disk_percent = disk.percent
            metrics.disk_used_gb = disk.used / (1024**3)
            metrics.disk_total_gb = disk.total / (1024**3)
            metrics.disk_free_gb = disk.free / (1024**3)
            
            # Temperatura (nem sempre disponível)
            try:
                temps = self.psutil.sensors_temperatures()
                if temps:
                    # Procura por temperatura da CPU
                    for name, entries in temps.items():
                        if entries and len(entries) > 0:
                            metrics.temp_celsius = entries[0].current
                            metrics.temp_available = True
                            break
            except:
                pass
            
            # Network
            net_io = self.psutil.net_io_counters()
            metrics.bytes_sent = net_io.bytes_sent
            metrics.bytes_recv = net_io.bytes_recv
            metrics.packets_sent = net_io.packets_sent
            metrics.packets_recv = net_io.packets_recv
            
            # Uptime
            metrics.uptime_seconds = int(time.time() - self.psutil.boot_time())
            
        except Exception as e:
            print(f"Erro coletando métricas: {e}")
        
        metrics.timestamp = datetime.now()
        return metrics
    
    def _collect_mock(self) -> SystemMetrics:
        """Gera dados SIMULADOS realistas para demonstração"""
        metrics = SystemMetrics()
        
        # CPU (simula variação realista)
        base_cpu = 35 + random.gauss(0, 15)
        metrics.cpu_percent = max(5, min(95, base_cpu))
        metrics.cpu_freq_current = 2400 + random.randint(-200, 400)
        metrics.cpu_freq_max = 3500
        metrics.cpu_count = 4
        
        # RAM (simula uso típico)
        base_ram = 55 + random.gauss(0, 10)
        metrics.ram_percent = max(20, min(85, base_ram))
        metrics.ram_total_gb = 16.0
        metrics.ram_used_gb = metrics.ram_total_gb * (metrics.ram_percent / 100)
        metrics.ram_available_gb = metrics.ram_total_gb - metrics.ram_used_gb
        
        # Disco
        metrics.disk_percent = 62.5
        metrics.disk_total_gb = 500.0
        metrics.disk_used_gb = 312.5
        metrics.disk_free_gb = 187.5
        
        # Temperatura (simula variação térmica)
        current_hour = datetime.now().hour
        base_temp = 45 if current_hour < 12 else 55
        metrics.temp_celsius = base_temp + random.gauss(0, 8)
        metrics.temp_celsius = max(35, min(85, metrics.temp_celsius))
        metrics.temp_available = True
        
        # Network (simula tráfego acumulado)
        uptime = int(time.time() - self.start_time)
        metrics.bytes_sent = uptime * 1024 * random.randint(10, 100)
        metrics.bytes_recv = uptime * 1024 * random.randint(50, 500)
        metrics.packets_sent = uptime * random.randint(10, 50)
        metrics.packets_recv = uptime * random.randint(50, 200)
        
        # Uptime
        metrics.uptime_seconds = uptime
        
        metrics.timestamp = datetime.now()
        return metrics
    
    def get_cpu_info(self) -> dict:
        """Retorna informações detalhadas sobre CPU"""
        if self.has_psutil:
            return {
                'physical_cores': self.psutil.cpu_count(logical=False),
                'logical_cores': self.psutil.cpu_count(logical=True),
                'frequency': self.psutil.cpu_freq(),
                'per_cpu_percent': self.psutil.cpu_percent(percpu=True),
            }
        return {
            'physical_cores': 4,
            'logical_cores': 8,
            'frequency': None,
            'per_cpu_percent': [random.randint(10, 60) for _ in range(8)],
        }
    
    def get_memory_info(self) -> dict:
        """Retorna informações detalhadas sobre memória"""
        if self.has_psutil:
            mem = self.psutil.virtual_memory()
            swap = self.psutil.swap_memory()
            return {
                'virtual': {
                    'total': mem.total,
                    'available': mem.available,
                    'used': mem.used,
                    'free': mem.free,
                    'percent': mem.percent,
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent,
                }
            }
        return {
            'virtual': {
                'total': 16 * 1024**3,
                'available': 8 * 1024**3,
                'used': 8 * 1024**3,
                'free': 8 * 1024**3,
                'percent': 50.0,
            },
            'swap': {
                'total': 4 * 1024**3,
                'used': 0,
                'free': 4 * 1024**3,
                'percent': 0.0,
            }
        }
    
    def format_bytes(self, bytes_value: int) -> str:
        """Formata bytes em unidade legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def format_uptime(self, seconds: int) -> str:
        """Formata uptime em formato legível"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        else:
            return f"{minutes}m {secs}s"
