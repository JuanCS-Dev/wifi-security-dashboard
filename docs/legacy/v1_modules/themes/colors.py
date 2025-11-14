#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Sistema de Cores para Dashboard Educacional
Paleta vibrante e amigável para crianças de 7-8 anos
"""

from rich.style import Style
from rich.color import Color

class DashboardColors:
    """Paleta de cores otimizada para educação e visualização"""
    
    # === CORES PRINCIPAIS ===
    PRIMARY = "#00D9FF"      # Cyan brilhante (WiFi, rede)
    SECONDARY = "#FF6B35"    # Laranja vibrante (alertas moderados)
    SUCCESS = "#00FF88"      # Verde neon (tudo OK)
    DANGER = "#FF3366"       # Rosa forte (perigo!)
    WARNING = "#FFD93D"      # Amarelo ouro (atenção)
    INFO = "#A78BFA"         # Roxo suave (informação)
    
    # === CORES EDUCACIONAIS ===
    WIFI_SIGNAL = "#00D9FF"      # Sinal WiFi
    WIFI_SECURITY = "#00FF88"    # Segurança OK
    WIFI_DANGER = "#FF3366"      # Rede insegura
    
    DEVICE_PHONE = "#FF6B35"     # Smartphone/tablet
    DEVICE_COMPUTER = "#00D9FF"  # Computador/laptop
    DEVICE_IOT = "#A78BFA"       # Dispositivos IoT
    DEVICE_UNKNOWN = "#94A3B8"   # Desconhecido
    
    APP_YOUTUBE = "#FF0000"      # YouTube vermelho
    APP_NETFLIX = "#E50914"      # Netflix vermelho escuro
    APP_WHATSAPP = "#25D366"     # WhatsApp verde
    APP_CHROME = "#4285F4"       # Chrome azul
    APP_FIREFOX = "#FF7139"      # Firefox laranja
    APP_GENERIC = "#94A3B8"      # App genérico
    
    # === CORES DE SISTEMA ===
    CPU_LOW = "#00FF88"          # CPU baixo (<30%)
    CPU_MEDIUM = "#FFD93D"       # CPU médio (30-70%)
    CPU_HIGH = "#FF6B35"         # CPU alto (70-90%)
    CPU_CRITICAL = "#FF3366"     # CPU crítico (>90%)
    
    RAM_LOW = "#00FF88"
    RAM_MEDIUM = "#FFD93D"
    RAM_HIGH = "#FF6B35"
    RAM_CRITICAL = "#FF3366"
    
    TEMP_COLD = "#00D9FF"        # Temperatura baixa (<50°C)
    TEMP_WARM = "#FFD93D"        # Morno (50-70°C)
    TEMP_HOT = "#FF6B35"         # Quente (70-85°C)
    TEMP_CRITICAL = "#FF3366"    # Crítico (>85°C)
    
    # === CORES DE GRÁFICOS ===
    CHART_LINE_1 = "#00D9FF"     # Linha 1 (download)
    CHART_LINE_2 = "#FF6B35"     # Linha 2 (upload)
    CHART_LINE_3 = "#A78BFA"     # Linha 3 (total)
    CHART_LINE_4 = "#00FF88"     # Linha 4 (apps)
    CHART_LINE_5 = "#FFD93D"     # Linha 5 (extra)
    
    CHART_BAR_1 = "#00FF88"      # Barra 1
    CHART_BAR_2 = "#00D9FF"      # Barra 2
    CHART_BAR_3 = "#FF6B35"      # Barra 3
    CHART_BAR_4 = "#A78BFA"      # Barra 4
    
    # === CORES DE BACKGROUND ===
    BG_DARK = "#0F1419"          # Fundo escuro principal
    BG_PANEL = "#1A1F28"         # Fundo de painéis
    BG_HIGHLIGHT = "#252B36"     # Destaque sutil
    
    # === CORES DE TEXTO ===
    TEXT_PRIMARY = "#FFFFFF"     # Texto principal
    TEXT_SECONDARY = "#94A3B8"   # Texto secundário
    TEXT_MUTED = "#64748B"       # Texto discreto
    TEXT_BRIGHT = "#F8FAFC"      # Texto brilhante
    
    # === EMOJIS EDUCACIONAIS ===
    EMOJI_WIFI = "📶"
    EMOJI_SECURITY = "🔒"
    EMOJI_DANGER = "⚠️"
    EMOJI_OK = "✅"
    EMOJI_DEVICE = "📱"
    EMOJI_COMPUTER = "💻"
    EMOJI_IOT = "🏠"
    EMOJI_APP = "📦"
    EMOJI_DOWNLOAD = "⬇️"
    EMOJI_UPLOAD = "⬆️"
    EMOJI_CPU = "🧠"
    EMOJI_RAM = "💾"
    EMOJI_DISK = "💿"
    EMOJI_TEMP = "🌡️"
    EMOJI_TIME = "🕐"
    EMOJI_PLAY = "▶️"
    EMOJI_PAUSE = "⏸️"
    EMOJI_STOP = "⏹️"
    
    @staticmethod
    def get_cpu_color(percent: float) -> str:
        """Retorna cor baseada no uso de CPU"""
        if percent < 30:
            return DashboardColors.CPU_LOW
        elif percent < 70:
            return DashboardColors.CPU_MEDIUM
        elif percent < 90:
            return DashboardColors.CPU_HIGH
        else:
            return DashboardColors.CPU_CRITICAL
    
    @staticmethod
    def get_ram_color(percent: float) -> str:
        """Retorna cor baseada no uso de RAM"""
        if percent < 30:
            return DashboardColors.RAM_LOW
        elif percent < 70:
            return DashboardColors.RAM_MEDIUM
        elif percent < 90:
            return DashboardColors.RAM_HIGH
        else:
            return DashboardColors.RAM_CRITICAL
    
    @staticmethod
    def get_temp_color(celsius: float) -> str:
        """Retorna cor baseada na temperatura"""
        if celsius < 50:
            return DashboardColors.TEMP_COLD
        elif celsius < 70:
            return DashboardColors.TEMP_WARM
        elif celsius < 85:
            return DashboardColors.TEMP_HOT
        else:
            return DashboardColors.TEMP_CRITICAL
    
    @staticmethod
    def get_signal_color(strength: int) -> str:
        """Retorna cor baseada na força do sinal WiFi (0-100)"""
        if strength >= 80:
            return DashboardColors.SUCCESS
        elif strength >= 60:
            return DashboardColors.WARNING
        elif strength >= 40:
            return DashboardColors.SECONDARY
        else:
            return DashboardColors.DANGER
    
    @staticmethod
    def get_device_color(device_type: str) -> str:
        """Retorna cor baseada no tipo de dispositivo"""
        device_type = device_type.lower()
        if 'phone' in device_type or 'mobile' in device_type:
            return DashboardColors.DEVICE_PHONE
        elif 'computer' in device_type or 'laptop' in device_type:
            return DashboardColors.DEVICE_COMPUTER
        elif 'iot' in device_type or 'smart' in device_type:
            return DashboardColors.DEVICE_IOT
        else:
            return DashboardColors.DEVICE_UNKNOWN
    
    @staticmethod
    def get_app_color(app_name: str) -> str:
        """Retorna cor baseada no aplicativo"""
        app_lower = app_name.lower()
        if 'youtube' in app_lower:
            return DashboardColors.APP_YOUTUBE
        elif 'netflix' in app_lower:
            return DashboardColors.APP_NETFLIX
        elif 'whatsapp' in app_lower or 'telegram' in app_lower:
            return DashboardColors.APP_WHATSAPP
        elif 'chrome' in app_lower:
            return DashboardColors.APP_CHROME
        elif 'firefox' in app_lower:
            return DashboardColors.APP_FIREFOX
        else:
            return DashboardColors.APP_GENERIC


class StyleManager:
    """Gerenciador de estilos Rich para o dashboard"""
    
    @staticmethod
    def get_style(color: str, bold: bool = False, italic: bool = False) -> Style:
        """Cria um estilo Rich personalizado"""
        return Style(color=color, bold=bold, italic=italic)
    
    @staticmethod
    def header_style() -> Style:
        """Estilo para cabeçalhos"""
        return Style(color=DashboardColors.PRIMARY, bold=True)
    
    @staticmethod
    def title_style() -> Style:
        """Estilo para títulos"""
        return Style(color=DashboardColors.TEXT_BRIGHT, bold=True)
    
    @staticmethod
    def subtitle_style() -> Style:
        """Estilo para subtítulos"""
        return Style(color=DashboardColors.TEXT_SECONDARY, italic=True)
    
    @staticmethod
    def value_style(color: str = None) -> Style:
        """Estilo para valores numéricos"""
        return Style(color=color or DashboardColors.INFO, bold=True)
    
    @staticmethod
    def alert_style() -> Style:
        """Estilo para alertas"""
        return Style(color=DashboardColors.DANGER, bold=True)
    
    @staticmethod
    def success_style() -> Style:
        """Estilo para sucesso"""
        return Style(color=DashboardColors.SUCCESS, bold=True)
    
    @staticmethod
    def muted_style() -> Style:
        """Estilo para texto discreto"""
        return Style(color=DashboardColors.TEXT_MUTED)
