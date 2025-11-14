#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Chart Renderer - Renderiza gráficos impressionantes em terminal
Line charts, bar charts, histogramas usando plotext
"""

import plotext as plt
from typing import List, Tuple, Optional
from collections import deque


class ChartRenderer:
    """Renderizador de gráficos para terminal"""
    
    @staticmethod
    def render_line_chart(
        data: List[float],
        title: str = "Chart",
        width: int = 80,
        height: int = 20,
        color: str = "cyan",
        ylabel: str = "",
        xlabel: str = "Time (s)"
    ) -> str:
        """
        Renderiza gráfico de linha
        
        Args:
            data: Dados para plotar
            title: Título do gráfico
            width: Largura em caracteres
            height: Altura em linhas
            color: Cor da linha
            ylabel: Label do eixo Y
            xlabel: Label do eixo X
        
        Returns:
            String do gráfico renderizado
        """
        plt.clf()  # Clear figure
        plt.plotsize(width, height)
        
        if len(data) > 0:
            x = list(range(len(data)))
            plt.plot(x, data, color=color, marker="braille")
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def render_multi_line_chart(
        datasets: List[Tuple[List[float], str, str]],  # (data, label, color)
        title: str = "Multi-Line Chart",
        width: int = 80,
        height: int = 20,
        ylabel: str = "",
        xlabel: str = "Time (s)"
    ) -> str:
        """
        Renderiza gráfico com múltiplas linhas
        
        Args:
            datasets: Lista de (dados, label, cor)
            title: Título do gráfico
            width: Largura
            height: Altura
            ylabel: Label Y
            xlabel: Label X
        
        Returns:
            String do gráfico
        """
        plt.clf()
        plt.plotsize(width, height)
        
        for data, label, color in datasets:
            if len(data) > 0:
                x = list(range(len(data)))
                plt.plot(x, data, label=label, color=color, marker="braille")
        
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def render_bar_chart_horizontal(
        labels: List[str],
        values: List[float],
        title: str = "Bar Chart",
        width: int = 60,
        height: int = 20,
        color: str = "cyan"
    ) -> str:
        """
        Renderiza gráfico de barras horizontal
        
        Args:
            labels: Labels das barras
            values: Valores
            title: Título
            width: Largura
            height: Altura
            color: Cor das barras
        
        Returns:
            String do gráfico
        """
        plt.clf()
        plt.plotsize(width, height)
        
        if len(labels) > 0 and len(values) > 0:
            plt.bar(labels, values, orientation='horizontal', color=color)
            plt.title(title)
            plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def render_bar_chart_vertical(
        labels: List[str],
        values: List[float],
        title: str = "Bar Chart",
        width: int = 60,
        height: int = 20,
        color: str = "cyan"
    ) -> str:
        """
        Renderiza gráfico de barras vertical
        
        Args:
            labels: Labels das barras
            values: Valores
            title: Título
            width: Largura
            height: Altura
            color: Cor das barras
        
        Returns:
            String do gráfico
        """
        plt.clf()
        plt.plotsize(width, height)
        
        if len(labels) > 0 and len(values) > 0:
            plt.bar(labels, values, orientation='vertical', color=color)
            plt.title(title)
            plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def render_stacked_bar(
        labels: List[str],
        datasets: List[Tuple[List[float], str, str]],  # (values, label, color)
        title: str = "Stacked Bar",
        width: int = 60,
        height: int = 20
    ) -> str:
        """
        Renderiza gráfico de barras empilhadas
        
        Args:
            labels: Labels do eixo X
            datasets: Lista de (valores, label, cor)
            title: Título
            width: Largura
            height: Altura
        
        Returns:
            String do gráfico
        """
        plt.clf()
        plt.plotsize(width, height)
        
        if len(labels) > 0:
            for values, label, color in datasets:
                if len(values) > 0:
                    plt.bar(labels, values, label=label, color=color)
            
            plt.title(title)
            plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def render_histogram(
        data: List[float],
        bins: int = 20,
        title: str = "Histogram",
        width: int = 60,
        height: int = 20,
        color: str = "cyan"
    ) -> str:
        """
        Renderiza histograma
        
        Args:
            data: Dados
            bins: Número de bins
            title: Título
            width: Largura
            height: Altura
            color: Cor
        
        Returns:
            String do gráfico
        """
        plt.clf()
        plt.plotsize(width, height)
        
        if len(data) > 0:
            plt.hist(data, bins=bins, color=color)
            plt.title(title)
            plt.theme("dark")
        
        return plt.build()
    
    @staticmethod
    def create_mini_sparkline(data: List[float], width: int = 20) -> str:
        """
        Cria uma sparkline (gráfico minúsculo inline)
        
        Args:
            data: Dados
            width: Largura
        
        Returns:
            String da sparkline
        """
        if not data or len(data) == 0:
            return "─" * width
        
        # Normaliza dados para a altura (8 níveis de bloco)
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            return "▄" * width
        
        # Caracteres de bloco unicode para diferentes alturas
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        
        # Resampling se necessário
        if len(data) > width:
            # Amostragem simples
            step = len(data) / width
            data = [data[int(i * step)] for i in range(width)]
        elif len(data) < width:
            # Preenche com zeros
            data = data + [data[-1]] * (width - len(data))
        
        # Normaliza e converte
        sparkline = ""
        for value in data:
            normalized = (value - min_val) / (max_val - min_val)
            block_index = min(7, int(normalized * 8))
            sparkline += blocks[block_index]
        
        return sparkline
    
    @staticmethod
    def format_bandwidth(bytes_per_sec: float) -> str:
        """
        Formata bandwidth em unidade legível
        
        Args:
            bytes_per_sec: Bytes por segundo
        
        Returns:
            String formatada (ex: "5.2 MB/s")
        """
        for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
            if bytes_per_sec < 1024.0:
                return f"{bytes_per_sec:.1f} {unit}"
            bytes_per_sec /= 1024.0
        return f"{bytes_per_sec:.1f} TB/s"
    
    @staticmethod
    def create_gauge(
        value: float,
        max_value: float = 100.0,
        width: int = 30,
        filled_char: str = "█",
        empty_char: str = "░",
        show_percentage: bool = True
    ) -> str:
        """
        Cria uma barra de gauge (medidor)
        
        Args:
            value: Valor atual
            max_value: Valor máximo
            width: Largura da barra
            filled_char: Caractere preenchido
            empty_char: Caractere vazio
            show_percentage: Mostrar porcentagem
        
        Returns:
            String do gauge
        """
        percentage = min(100, (value / max_value) * 100)
        filled = int((percentage / 100) * width)
        empty = width - filled
        
        bar = filled_char * filled + empty_char * empty
        
        if show_percentage:
            return f"{bar} {percentage:.1f}%"
        return bar
    
    @staticmethod
    def create_trend_arrow(current: float, previous: float) -> str:
        """
        Cria seta de tendência
        
        Args:
            current: Valor atual
            previous: Valor anterior
        
        Returns:
            String com seta (↑ ↓ →)
        """
        if current > previous * 1.05:  # 5% de margem
            return "↑"
        elif current < previous * 0.95:
            return "↓"
        else:
            return "→"
