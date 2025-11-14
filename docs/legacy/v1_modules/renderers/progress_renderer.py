#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏳ Progress Renderer - Barras de progresso e indicadores animados
"""

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from typing import Optional


class ProgressRenderer:
    """Renderizador de barras de progresso e indicadores"""
    
    @staticmethod
    def create_progress_bar(
        value: float,
        total: float = 100.0,
        width: int = 30,
        filled_char: str = "█",
        empty_char: str = "░",
        color: str = "cyan",
        show_percentage: bool = True
    ) -> str:
        """
        Cria barra de progresso simples
        
        Args:
            value: Valor atual
            total: Valor total
            width: Largura da barra
            filled_char: Caractere preenchido
            empty_char: Caractere vazio
            color: Cor
            show_percentage: Mostrar porcentagem
        
        Returns:
            String da barra
        """
        percentage = min(100, (value / total) * 100)
        filled = int((percentage / 100) * width)
        empty = width - filled
        
        bar = filled_char * filled + empty_char * empty
        
        if show_percentage:
            return f"[{color}]{bar}[/{color}] {percentage:.1f}%"
        return f"[{color}]{bar}[/{color}]"
    
    @staticmethod
    def create_bandwidth_indicator(
        download_bps: float,
        upload_bps: float,
        width: int = 40
    ) -> Panel:
        """
        Cria indicador visual de bandwidth
        
        Args:
            download_bps: Download em bytes/segundo
            upload_bps: Upload em bytes/segundo
            width: Largura
        
        Returns:
            Panel Rich com indicadores
        """
        # Formata valores
        down_str = ProgressRenderer._format_bandwidth(download_bps)
        up_str = ProgressRenderer._format_bandwidth(upload_bps)
        
        # Cria barras proporcionais
        max_speed = 100 * 1024 * 1024  # 100 MB/s como máximo
        down_percent = min(100, (download_bps / max_speed) * 100)
        up_percent = min(100, (upload_bps / max_speed) * 100)
        
        down_bar = ProgressRenderer.create_progress_bar(
            down_percent, 100, width, color="green", show_percentage=False
        )
        up_bar = ProgressRenderer.create_progress_bar(
            up_percent, 100, width, color="yellow", show_percentage=False
        )
        
        content = Text()
        content.append("📥 Download: ", style="bold green")
        content.append(f"{down_str:>12s}\n", style="bright_white")
        content.append(f"{down_bar}\n\n")
        content.append("📤 Upload:   ", style="bold yellow")
        content.append(f"{up_str:>12s}\n", style="bright_white")
        content.append(f"{up_bar}")
        
        return Panel(content, title="🌐 Tráfego de Rede", border_style="cyan")
    
    @staticmethod
    def create_loading_spinner(message: str = "Carregando...") -> str:
        """
        Cria spinner de loading
        
        Args:
            message: Mensagem
        
        Returns:
            String do spinner
        """
        import time
        spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = int(time.time() * 10) % len(spinners)
        return f"{spinners[idx]} {message}"
    
    @staticmethod
    def create_time_progress(
        current_second: int,
        label: str = "Tempo",
        max_seconds: int = 60
    ) -> str:
        """
        Cria barra de progresso de tempo
        
        Args:
            current_second: Segundo atual
            label: Label
            max_seconds: Segundos totais
        
        Returns:
            String da barra
        """
        percent = (current_second / max_seconds) * 100
        bar = ProgressRenderer.create_progress_bar(percent, 100, width=40, color="cyan")
        return f"{label}: {current_second:02d}s / {max_seconds:02d}s | {bar}"
    
    @staticmethod
    def create_animated_dots(count: int = 3) -> str:
        """
        Cria animação de pontos (...)
        
        Args:
            count: Número de pontos
        
        Returns:
            String animada
        """
        import time
        dots = int(time.time() * 2) % (count + 1)
        return "." * dots + " " * (count - dots)
    
    @staticmethod
    def create_pulse_indicator(active: bool = True) -> str:
        """
        Cria indicador pulsante
        
        Args:
            active: Se está ativo
        
        Returns:
            String do indicador
        """
        import time
        if not active:
            return "⚪"
        
        # Pulsa entre ● e ○
        pulse = int(time.time() * 4) % 2
        return "🟢" if pulse == 0 else "🟡"
    
    @staticmethod
    def create_signal_strength_bars(strength: int) -> str:
        """
        Cria barras de força de sinal (como WiFi)
        
        Args:
            strength: Força 0-100
        
        Returns:
            String das barras
        """
        if strength >= 80:
            return "📶 [green]▂▄▆█[/green]"
        elif strength >= 60:
            return "📶 [yellow]▂▄▆[/yellow]░"
        elif strength >= 40:
            return "📶 [yellow]▂▄[/yellow]░░"
        elif strength >= 20:
            return "📶 [red]▂[/red]░░░"
        else:
            return "📶 [red]░░░░[/red]"
    
    @staticmethod
    def _format_bandwidth(bytes_per_sec: float) -> str:
        """Formata bandwidth"""
        for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
            if bytes_per_sec < 1024.0:
                return f"{bytes_per_sec:.1f} {unit}"
            bytes_per_sec /= 1024.0
        return f"{bytes_per_sec:.1f} TB/s"
    
    @staticmethod
    def create_heatmap_char(value: float, max_value: float) -> str:
        """
        Cria caractere de heatmap
        
        Args:
            value: Valor atual
            max_value: Valor máximo
        
        Returns:
            Caractere com cor
        """
        if max_value == 0:
            return "░"
        
        percent = (value / max_value) * 100
        
        if percent >= 90:
            return "[red]█[/red]"
        elif percent >= 70:
            return "[yellow]▓[/yellow]"
        elif percent >= 50:
            return "[green]▒[/green]"
        elif percent >= 30:
            return "[cyan]░[/cyan]"
        else:
            return "░"
