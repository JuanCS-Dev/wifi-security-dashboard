#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 Table Renderer - Renderiza tabelas bonitas com Rich
Tabelas de dispositivos, aplicativos, métricas
"""

from rich.table import Table
from rich import box
from typing import List, Dict, Any
from themes.colors import DashboardColors


class TableRenderer:
    """Renderizador de tabelas para o dashboard"""
    
    @staticmethod
    def create_devices_table(devices: List[Any], max_rows: int = 10) -> Table:
        """
        Cria tabela de dispositivos conectados - TAMANHO FIXO
        
        Args:
            devices: Lista de DeviceInfo
            max_rows: Número máximo de linhas
        
        Returns:
            Tabela Rich
        """
        table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold cyan",
            border_style="dim",
            padding=(0, 1),
            collapse_padding=True,
            width=54,  # FIXO: largura total da tabela
            show_edge=False
        )
        
        table.add_column("IP", style="cyan", width=11, no_wrap=True)
        table.add_column("Nome", style="bright_white", width=11, no_wrap=True)
        table.add_column("Tipo", style="magenta", width=6, no_wrap=True)
        table.add_column("↓ Down", style="green", width=7, justify="right", no_wrap=True)
        table.add_column("↑ Up", style="yellow", width=5, justify="right", no_wrap=True)
        table.add_column("Status", style="white", width=5, no_wrap=True)
        
        # Sort por tráfego
        devices_sorted = sorted(devices, key=lambda d: d.total_traffic, reverse=True)
        
        for idx, device in enumerate(devices_sorted[:max_rows], 1):
            # Status emoji
            status = "🟢" if device.is_active else "🔴"
            if device.is_new:
                status += " 🆕"
            
            # Formata bytes
            down = TableRenderer._format_bytes(device.bytes_received)
            up = TableRenderer._format_bytes(device.bytes_sent)
            
            # Emoji por tipo
            type_emoji = device.get_emoji()
            
            table.add_row(
                device.ip_address[:12],
                device.hostname[:12],
                f"{type_emoji} {device.device_type[:4]}",
                down,
                up,
                status
            )
        
        return table
    
    @staticmethod
    def create_apps_table(apps: List[Any], max_rows: int = 10) -> Table:
        """
        Cria tabela de aplicativos detectados
        
        Args:
            apps: Lista de AppInfo
            max_rows: Número máximo de linhas
        
        Returns:
            Tabela Rich
        """
        table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold magenta",
            border_style="dim",
            padding=(0, 1),
            collapse_padding=True,
            width=54,  # FIXO: largura total da tabela
            show_edge=False
        )
        
        table.add_column("Aplicativo", style="bright_white", width=17, no_wrap=True)
        table.add_column("Categoria", style="cyan", width=9, no_wrap=True)
        table.add_column("Tráfego", style="green", width=9, justify="right", no_wrap=True)
        table.add_column("Conex", style="yellow", width=6, justify="right", no_wrap=True)
        table.add_column("Proto", style="blue", width=4, no_wrap=True)
        
        # Sort por tráfego
        apps_sorted = sorted(apps, key=lambda a: a.total_traffic, reverse=True)
        
        for idx, app in enumerate(apps_sorted[:max_rows], 1):
            emoji = app.get_emoji()
            traffic = TableRenderer._format_bytes(app.total_traffic)
            
            # Cor por categoria
            category_colors = {
                'streaming': 'red',
                'messaging': 'green',
                'browsing': 'blue',
                'gaming': 'magenta',
                'unknown': 'dim'
            }
            cat_color = category_colors.get(app.category, 'white')
            
            table.add_row(
                f"{emoji} {app.name[:12]}",
                f"[{cat_color}]{app.category[:8]}[/{cat_color}]",
                traffic,
                str(app.connections),
                app.protocol[:3]
            )
        
        return table
    
    @staticmethod
    def create_wifi_info_table(wifi: Any) -> Table:
        """
        Cria tabela de informações WiFi
        
        Args:
            wifi: WiFiInfo
        
        Returns:
            Tabela Rich
        """
        table = Table(
            title=f"{DashboardColors.EMOJI_WIFI} Informações da Rede WiFi",
            box=box.DOUBLE_EDGE,
            show_header=False,
            border_style="cyan",
            padding=(0, 1)
        )
        
        table.add_column("Campo", style="cyan bold", width=20)
        table.add_column("Valor", style="bright_white", width=40)
        
        # Cor do sinal
        signal_color = DashboardColors.get_signal_color(wifi.signal_strength)
        
        table.add_row("📡 SSID", f"[bold]{wifi.ssid}[/bold]")
        table.add_row("🔐 Segurança", wifi.get_security_level())
        table.add_row("📶 Sinal", f"[{signal_color}]{'█' * (wifi.signal_strength // 10)} {wifi.signal_strength}%[/{signal_color}]")
        table.add_row("📻 Frequência", wifi.get_frequency_explanation())
        table.add_row("📺 Canal", str(wifi.channel))
        table.add_row("🌐 IP", wifi.ip_address)
        table.add_row("💻 Interface", wifi.interface)
        
        return table
    
    @staticmethod
    def create_system_metrics_table(system: Any) -> Table:
        """
        Cria tabela de métricas do sistema
        
        Args:
            system: SystemMetrics
        
        Returns:
            Tabela Rich
        """
        table = Table(
            title=f"{DashboardColors.EMOJI_CPU} Métricas do Sistema",
            box=box.ROUNDED,
            show_header=False,
            border_style="green",
            padding=(0, 1)
        )
        
        table.add_column("Métrica", style="green bold", width=18)
        table.add_column("Valor", style="bright_white", width=30)
        table.add_column("Status", style="white", width=20)
        
        # CPU
        cpu_color = DashboardColors.get_cpu_color(system.cpu_percent)
        cpu_bar = TableRenderer._create_bar(system.cpu_percent, 20, cpu_color)
        table.add_row(
            f"{DashboardColors.EMOJI_CPU} CPU",
            f"{system.cpu_percent:.1f}%",
            cpu_bar
        )
        
        # RAM
        ram_color = DashboardColors.get_ram_color(system.ram_percent)
        ram_bar = TableRenderer._create_bar(system.ram_percent, 20, ram_color)
        table.add_row(
            f"{DashboardColors.EMOJI_RAM} RAM",
            f"{system.ram_percent:.1f}% ({system.ram_used_gb:.1f}/{system.ram_total_gb:.1f} GB)",
            ram_bar
        )
        
        # Disco
        disk_bar = TableRenderer._create_bar(system.disk_percent, 20, "yellow")
        table.add_row(
            f"{DashboardColors.EMOJI_DISK} Disco",
            f"{system.disk_percent:.1f}% ({system.disk_used_gb:.0f}/{system.disk_total_gb:.0f} GB)",
            disk_bar
        )
        
        # Temperatura
        if system.temp_available and system.temp_celsius:
            temp_color = DashboardColors.get_temp_color(system.temp_celsius)
            table.add_row(
                f"{DashboardColors.EMOJI_TEMP} Temp",
                f"[{temp_color}]{system.temp_celsius:.1f}°C[/{temp_color}]",
                system.get_temp_status()
            )
        
        return table
    
    @staticmethod
    def create_summary_table(snapshot: Any) -> Table:
        """
        Cria tabela de resumo geral
        
        Args:
            snapshot: NetworkSnapshot
        
        Returns:
            Tabela Rich
        """
        table = Table(
            title="📊 Resumo Geral",
            box=box.HEAVY,
            show_header=False,
            border_style="bright_cyan",
            padding=(0, 2)
        )
        
        table.add_column("Item", style="cyan bold", width=25)
        table.add_column("Valor", style="bright_white bold", width=25, justify="right")
        
        summary = snapshot.get_educational_summary()
        
        table.add_row("🌐 Status WiFi", summary['wifi_status'])
        table.add_row("📱 Dispositivos Ativos", f"{snapshot.active_devices} de {snapshot.total_devices}")
        table.add_row("📦 Apps Detectados", str(snapshot.total_apps))
        table.add_row("💾 Pacotes Totais", f"{snapshot.total_packets:,}")
        table.add_row("📥 Download Total", TableRenderer._format_bytes(snapshot.total_bytes_recv))
        table.add_row("📤 Upload Total", TableRenderer._format_bytes(snapshot.total_bytes_sent))
        
        return table
    
    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """Formata bytes em unidade legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    @staticmethod
    def _create_bar(percent: float, width: int = 20, color: str = "cyan") -> str:
        """Cria barra de progresso colorida"""
        filled = int((percent / 100) * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{color}]{bar}[/{color}]"
