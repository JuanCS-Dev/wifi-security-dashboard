#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 WiFi Security Education Dashboard - ÉPICO!
Dashboard educacional para ensinar crianças sobre redes e segurança

Juan-Dev - Soli Deo Gloria ✝️
Para meus filhos de 7 e 8 anos aprenderem enquanto se impressionam!
"""

import os
import sys
import time
import signal
from datetime import datetime
from collections import deque

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import box

# Imports dos nossos módulos
from models.network_snapshot import NetworkSnapshot, WiFiInfo, DeviceInfo, AppInfo, SystemMetrics
from data_collectors.system_collector import SystemCollector
from data_collectors.wifi_collector import WiFiCollector
from data_collectors.network_sniffer import NetworkSniffer
from renderers.chart_renderer import ChartRenderer
from renderers.table_renderer import TableRenderer
from renderers.progress_renderer import ProgressRenderer
from themes.colors import DashboardColors

# Console global com tamanho FIXO (120x46 - página estática)
console = Console(width=120, height=46, legacy_windows=False)


class EducationalDashboard:
    """Dashboard Educacional Principal"""
    
    def __init__(self, mock_mode: bool = False, interface: str = None):
        """
        Inicializa o dashboard
        
        Args:
            mock_mode: Modo simulado (sem privilégios root)
            interface: Interface de rede para monitorar
        """
        self.mock_mode = mock_mode
        self.interface = interface
        self.running = False
        
        # Collectors
        self.system_collector = SystemCollector(mock_mode=mock_mode)
        self.wifi_collector = WiFiCollector(interface=interface, mock_mode=mock_mode)
        self.network_sniffer = NetworkSniffer(
            interface=interface,
            mock_mode=mock_mode,
            callback=self._on_network_data
        )
        
        # State
        self.snapshot = NetworkSnapshot()
        self.last_update = datetime.now()
        self.refresh_rate = 0.25  # 250ms = 4 FPS
        self.paused = False
        
        # Histórico para gráficos (60 segundos)
        self.download_history = deque(maxlen=60)
        self.upload_history = deque(maxlen=60)
        self.cpu_history = deque(maxlen=60)
        self.ram_history = deque(maxlen=60)
        
        # Stats
        self.frames_rendered = 0
        self.start_time = time.time()
    
    def _on_network_data(self):
        """
        Callback quando novos dados de rede chegam.
        Atualiza snapshot parcialmente para eventos críticos.
        """
        if not self.running or self.paused:
            return
        
        # Atualiza apenas dados de rede (mais eficiente que full update)
        self.snapshot.devices = self.network_sniffer.get_devices()
        self.snapshot.apps = self.network_sniffer.get_apps()
        self.snapshot.total_devices = len(self.snapshot.devices)
        self.snapshot.active_devices = len([d for d in self.snapshot.devices if d.is_active])
    
    def _print_banner(self):
        """Imprime banner JUAN colorido (verde → amarelo → azul)"""
        banner_lines = [
            "     ██╗██╗   ██╗ █████╗ ███╗   ██╗",
            "     ██║██║   ██║██╔══██╗████╗  ██║",
            "     ██║██║   ██║███████║██╔██╗ ██║",
            "██   ██║██║   ██║██╔══██║██║╚██╗██║",
            "╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║",
            " ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝",
        ]
        
        # Gradient verde → amarelo → azul
        colors = ['bright_green', 'green', 'yellow', 'bright_yellow', 'cyan', 'bright_cyan']
        
        from rich.text import Text
        from rich.align import Align
        
        console.print()
        
        # Imprime cada linha com sua cor
        for i, line in enumerate(banner_lines):
            console.print(Align.center(Text(line, style=colors[i % len(colors)])))
        
        console.print()
        console.print(Align.center(Text("🎓 WiFi Security Education Dashboard 🎓", style="bold bright_yellow")))
        console.print(Align.center(Text("Soli Deo Gloria ✝️", style="bold bright_white")))
        console.print()
    
    def start(self):
        """Inicia o dashboard"""
        self.running = True
        
        # Banner JUAN
        self._print_banner()
        
        # Inicia collectors
        console.print("[cyan]🚀 Iniciando Dashboard Educacional WiFi...[/cyan]\n")
        
        console.print("[green]✓[/green] Sistema collector: OK")
        console.print("[green]✓[/green] WiFi collector: OK")
        
        console.print("[yellow]⚡[/yellow] Iniciando network sniffer...")
        self.network_sniffer.start()
        console.print("[green]✓[/green] Network sniffer: Ativo\n")
        
        if self.mock_mode:
            console.print("[yellow]⚠️  Modo SIMULADO ativo (sem root)[/yellow]")
            console.print("[yellow]   Para dados REAIS, execute: sudo python3 main.py[/yellow]\n")
        else:
            console.print("[green]✅ Modo REAL ativo - capturando dados reais![/green]\n")
        
        time.sleep(2)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Inicia rendering loop
        self._render_loop()
    
    def stop(self):
        """Para o dashboard"""
        self.running = False
        self.network_sniffer.stop()
        console.print("\n[cyan]Dashboard encerrado. Obrigado![/cyan]\n")
    
    def _signal_handler(self, signum, frame):
        """Handler para Ctrl+C"""
        self.stop()
        sys.exit(0)
    
    def _collect_data(self):
        """Coleta dados de todos os collectors"""
        # Sistema
        self.snapshot.system = self.system_collector.collect()
        
        # WiFi
        self.snapshot.wifi = self.wifi_collector.collect()
        
        # Rede (devices e apps)
        self.snapshot.devices = self.network_sniffer.get_devices()
        self.snapshot.total_devices = len(self.snapshot.devices)
        self.snapshot.active_devices = len([d for d in self.snapshot.devices if d.is_active])
        self.snapshot.new_devices = len([d for d in self.snapshot.devices if d.is_new])
        
        self.snapshot.apps = self.network_sniffer.get_apps()
        self.snapshot.total_apps = len(self.snapshot.apps)
        
        # Stats de rede
        net_stats = self.network_sniffer.get_stats()
        self.snapshot.total_packets = net_stats['total_packets']
        self.snapshot.total_bytes_sent = net_stats['bytes_sent']
        self.snapshot.total_bytes_recv = net_stats['bytes_recv']
        
        # Atualiza históricos
        self.cpu_history.append(self.snapshot.system.cpu_percent)
        self.ram_history.append(self.snapshot.system.ram_percent)
        
        # Calcula bandwidth atual (simplificado)
        download_speed = sum([d.bytes_received for d in self.snapshot.devices]) / (time.time() - self.start_time + 1)
        upload_speed = sum([d.bytes_sent for d in self.snapshot.devices]) / (time.time() - self.start_time + 1)
        
        self.download_history.append(download_speed / 1024)  # KB/s
        self.upload_history.append(upload_speed / 1024)
        
        self.snapshot.timestamp = datetime.now()
    
    def _create_layout(self) -> Layout:
        """Cria o layout principal do dashboard"""
        layout = Layout()
        
        # Estrutura principal
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Main split em duas colunas
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # Coluna esquerda (um pouco maior)
        layout["left"].split_column(
            Layout(name="wifi", size=10),
            Layout(name="system", size=13),
            Layout(name="traffic_chart", ratio=1)
        )
        
        # Coluna direita
        layout["right"].split_column(
            Layout(name="devices", ratio=1),
            Layout(name="apps", ratio=1)
        )
        
        return layout
    
    def _render_header(self) -> Panel:
        """Renderiza o cabeçalho"""
        title = Text()
        title.append("🛡️ ", style="cyan bold")
        title.append("DASHBOARD EDUCACIONAL WiFi", style="bright_white bold")
        title.append(" 🎓", style="cyan bold")
        
        subtitle = Text()
        subtitle.append("💝 Feito com amor para ", style="cyan")
        subtitle.append("Maximus", style="bright_green bold")
        subtitle.append(" e ", style="cyan")
        subtitle.append("Penelope", style="bright_magenta bold")
        subtitle.append(" 💝", style="cyan")
        
        # Status
        status = Text()
        if self.paused:
            status.append("⏸️  PAUSADO ", style="yellow bold")
        else:
            status.append(f"{ProgressRenderer.create_pulse_indicator(True)} AO VIVO ", style="green bold")
        
        status.append(f"| ⚡ {self.frames_rendered} frames | ", style="dim")
        status.append(f"⏱️ {self._format_uptime()}", style="cyan")
        
        content = Text()
        content.append(title)
        content.append("\n")
        content.append(subtitle)
        content.append("\n")
        content.append(status)
        
        return Panel(
            content,
            box=box.DOUBLE,
            border_style="bright_cyan",
            padding=(0, 2)
        )
    
    def _render_footer(self) -> Panel:
        """Renderiza o rodapé com controles"""
        controls = Text()
        controls.append("⌨️  Controles: ", style="cyan bold")
        controls.append("[Q]", style="red bold")
        controls.append(" Sair  ", style="white")
        controls.append("[P]", style="yellow bold")
        controls.append(" Pausar/Continuar  ", style="white")
        controls.append("[R]", style="green bold")
        controls.append(" Reset  ", style="white")
        controls.append("[H]", style="blue bold")
        controls.append(" Ajuda", style="white")
        
        time_str = datetime.now().strftime("%H:%M:%S")
        controls.append(f"  |  🕐 {time_str}", style="bright_white")
        
        return Panel(controls, box=box.ROUNDED, border_style="cyan")
    
    def _render_wifi_panel(self) -> Panel:
        """Renderiza painel WiFi"""
        wifi = self.snapshot.wifi

        content = Text()
        content.append(f"📡 SSID: ", style="cyan bold")
        content.append(f"{wifi.ssid}\n", style="bright_white bold")

        content.append(f"🔐 Segurança: ", style="cyan bold")
        content.append(f"{wifi.get_security_level()}\n", style="green" if "SEGURO" in wifi.get_security_level() else "red")

        content.append(f"📶 Sinal: ", style="cyan bold")
        signal_bars = ProgressRenderer.create_signal_strength_bars(wifi.signal_strength)
        # Processa markup Rich corretamente
        signal_text = Text.from_markup(signal_bars)
        content.append(signal_text)
        content.append(f" {wifi.signal_strength}%\n", style="bright_white")

        content.append(f"📻 Frequência: ", style="cyan bold")
        content.append(f"{wifi.frequency}\n", style="bright_white")

        content.append(f"🌐 IP: ", style="cyan bold")
        content.append(f"{wifi.ip_address}", style="bright_white")

        return Panel(
            content,
            title="🛜 Rede WiFi",
            title_align="left",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def _render_system_panel(self) -> Panel:
        """Renderiza painel de sistema"""
        sys = self.snapshot.system

        content = Text()

        # CPU
        cpu_color = DashboardColors.get_cpu_color(sys.cpu_percent)
        cpu_bar = ProgressRenderer.create_progress_bar(sys.cpu_percent, 100, 25, color=cpu_color)
        content.append(f"🧠 CPU: ", style="cyan bold")
        content.append(f"{sys.cpu_percent:.1f}%\n", style=cpu_color)
        # Processa markup Rich corretamente
        content.append("   ")
        cpu_bar_text = Text.from_markup(cpu_bar)
        content.append(cpu_bar_text)
        content.append("\n")
        content.append(f"   {sys.get_cpu_status()}\n\n", style="dim")

        # RAM
        ram_color = DashboardColors.get_ram_color(sys.ram_percent)
        ram_bar = ProgressRenderer.create_progress_bar(sys.ram_percent, 100, 25, color=ram_color)
        content.append(f"💾 RAM: ", style="cyan bold")
        content.append(f"{sys.ram_percent:.1f}% ", style=ram_color)
        content.append(f"({sys.ram_used_gb:.1f}/{sys.ram_total_gb:.1f} GB)\n", style="dim")
        # Processa markup Rich corretamente
        content.append("   ")
        ram_bar_text = Text.from_markup(ram_bar)
        content.append(ram_bar_text)
        content.append("\n")
        content.append(f"   {sys.get_ram_status()}\n\n", style="dim")

        # Temperatura
        if sys.temp_available and sys.temp_celsius:
            temp_color = DashboardColors.get_temp_color(sys.temp_celsius)
            content.append(f"🌡️ Temp: ", style="cyan bold")
            content.append(f"{sys.temp_celsius:.1f}°C", style=temp_color)

        return Panel(
            content,
            title="💻 Sistema",
            title_align="left",
            border_style="green",
            box=box.ROUNDED
        )
    
    def _render_traffic_chart(self) -> Panel:
        """Renderiza gráfico de tráfego"""
        # Prepara dados
        down_data = list(self.download_history) if len(self.download_history) > 0 else [0]
        up_data = list(self.upload_history) if len(self.upload_history) > 0 else [0]

        # Renderiza gráfico multi-linha
        datasets = [
            (down_data, "Download", "green"),
            (up_data, "Upload", "yellow")
        ]

        # TAMANHO FIXO do gráfico para caber perfeitamente no painel
        chart_str = ChartRenderer.render_multi_line_chart(
            datasets,
            title="",
            width=50,   # FIXO: largura exata para não vazar (50 chars)
            height=13,  # FIXO: altura exata (13 linhas)
            ylabel="KB/s",
            xlabel="60s"
        )

        # Converte códigos ANSI do plotext para Rich Text
        chart = Text.from_ansi(chart_str)

        return Panel(
            chart,
            title="📈 Tráfego em Tempo Real",
            title_align="left",
            border_style="magenta",
            box=box.ROUNDED,
            padding=(0, 1)
        )
    
    def _render_devices_panel(self) -> Panel:
        """Renderiza painel de dispositivos"""
        table = TableRenderer.create_devices_table(self.snapshot.devices, max_rows=5)
        
        summary = Text()
        summary.append(f"\n📊 {self.snapshot.total_devices} dispositivos | ", style="cyan")
        summary.append(f"🟢 {self.snapshot.active_devices} ativos | ", style="green")
        summary.append(f"🆕 {self.snapshot.new_devices} novos", style="yellow")
        
        from rich.console import Group
        
        content = Group(table, summary)
        
        return Panel(
            content,
            title="📱 Dispositivos Conectados",
            title_align="left",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(0, 1)
        )
    
    def _render_apps_panel(self) -> Panel:
        """Renderiza painel de aplicativos"""
        table = TableRenderer.create_apps_table(self.snapshot.apps, max_rows=5)
        
        # Dica educacional
        tip = self._get_educational_tip()
        tip_text = Text()
        tip_text.append("\n💡 ", style="yellow bold")
        tip_text.append(tip[:60] + "..." if len(tip) > 60 else tip, style="bright_white")
        
        from rich.console import Group
        
        content = Group(table, tip_text)
        
        return Panel(
            content,
            title="📦 Aplicativos Detectados",
            title_align="left",
            border_style="magenta",
            box=box.ROUNDED,
            padding=(0, 1)
        )
    
    def _get_educational_tip(self) -> str:
        """Retorna dica educacional aleatória"""
        import random
        
        tips = [
            "HTTPS (cadeado 🔒) significa que seus dados estão criptografados!",
            "WiFi 5GHz é mais rápido mas alcança menos longe que 2.4GHz",
            "WPA3 é a segurança mais forte para WiFi atualmente",
            "1 Mbps = 1024 Kbps (como 1 GB = 1024 MB)",
            "DNS traduz nomes (youtube.com) em números IP (142.250.x.x)",
            "Pacotes são pedaços pequenos de dados que viajam pela internet",
            "Seu roteador é como um carteiro que entrega pacotes aos dispositivos",
            "Upload = você enviando dados | Download = você recebendo dados",
            "Latência (ping) baixa é melhor para jogos online",
            "Firewall protege sua rede bloqueando conexões suspeitas"
        ]
        
        return random.choice(tips)
    
    def _format_uptime(self) -> str:
        """Formata tempo de execução"""
        uptime = int(time.time() - self.start_time)
        minutes = uptime // 60
        seconds = uptime % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def _render_loop(self):
        """Loop principal de rendering"""
        layout = self._create_layout()
        
        with Live(
            layout,
            console=console,
            screen=True,
            refresh_per_second=4,  # 4 FPS
            redirect_stderr=False
        ) as live:
            
            while self.running:
                try:
                    if not self.paused:
                        # Coleta dados
                        self._collect_data()
                        
                        # Atualiza layout
                        layout["header"].update(self._render_header())
                        layout["wifi"].update(self._render_wifi_panel())
                        layout["system"].update(self._render_system_panel())
                        layout["traffic_chart"].update(self._render_traffic_chart())
                        layout["devices"].update(self._render_devices_panel())
                        layout["apps"].update(self._render_apps_panel())
                        layout["footer"].update(self._render_footer())
                        
                        self.frames_rendered += 1
                    
                    # Sleep para manter refresh rate
                    time.sleep(self.refresh_rate)
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Erro: {e}[/red]")
                    time.sleep(1)


def show_banner():
    """Mostra banner inicial"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🛡️  DASHBOARD EDUCACIONAL WiFi SECURITY  🎓              ║
    ║                                                              ║
    ║   Aprenda sobre Redes e Segurança                           ║
    ║   enquanto monitora sua internet!                           ║
    ║                                                              ║
    ║   Feito com ❤️  para meus filhos de 7 e 8 anos             ║
    ║   Juan-Dev - Soli Deo Gloria ✝️                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bright_cyan")


def main():
    """Entry point principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dashboard Educacional WiFi")
    parser.add_argument('-i', '--interface', help="Interface de rede (auto-detect se omitido)")
    parser.add_argument('-m', '--mock', action='store_true', help="Modo simulado (sem root)")
    args = parser.parse_args()
    
    # Mostra banner
    show_banner()
    
    # Detecta se tem privilégios
    is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
    
    if not is_root and not args.mock:
        console.print("\n[yellow]⚠️  Executando sem privilégios root[/yellow]")
        console.print("[yellow]   Modo SIMULADO será usado[/yellow]")
        console.print("[yellow]   Para dados REAIS: sudo python3 main.py[/yellow]\n")
        args.mock = True
    
    # Cria e inicia dashboard
    dashboard = EducationalDashboard(
        mock_mode=args.mock,
        interface=args.interface
    )
    
    try:
        dashboard.start()
    except KeyboardInterrupt:
        dashboard.stop()
    except Exception as e:
        console.print(f"\n[red bold]Erro fatal: {e}[/red bold]\n")
        dashboard.stop()
        raise


if __name__ == "__main__":
    main()
