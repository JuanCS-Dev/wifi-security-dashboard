"""
Health bar widget for Guardian character.
Shows WiFi signal strength as visual health.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import pygame
import math
from typing import Tuple

Color = Tuple[int, int, int]


class HealthBar:
    """Visual health bar widget."""

    # Colors
    COLOR_BACKGROUND = (40, 40, 50)
    COLOR_BORDER = (100, 100, 120)
    COLOR_EXCELLENT = (76, 175, 80)  # Green
    COLOR_GOOD = (156, 204, 101)  # Light green
    COLOR_FAIR = (255, 193, 7)  # Amber
    COLOR_WEAK = (244, 67, 54)  # Red

    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        """
        Initialize health bar.

        Args:
            position: (x, y) top-left corner
            size: (width, height) of bar
        """
        self.position = position
        self.size = size
        self.current_health = 100.0
        self.target_health = 100.0
        self.transition_speed = 2.0  # Smoothing

    def set_health(self, health: float) -> None:
        """
        Set target health (will animate to this value).

        Args:
            health: 0-100
        """
        self.target_health = max(0, min(100, health))

    def update(self, dt: float) -> None:
        """
        Update animation (smooth transition).

        Args:
            dt: Delta time in seconds
        """
        # Exponential smoothing
        alpha = 1.0 - math.exp(-self.transition_speed * dt)
        self.current_health += (self.target_health - self.current_health) * alpha

    def _get_color(self) -> Color:
        """Get bar color based on health."""
        if self.current_health >= 75:
            return self.COLOR_EXCELLENT
        elif self.current_health >= 50:
            return self.COLOR_GOOD
        elif self.current_health >= 25:
            return self.COLOR_FAIR
        else:
            return self.COLOR_WEAK

    def render(self, screen: pygame.Surface) -> None:
        """
        Render health bar to screen.

        Args:
            screen: Pygame surface to draw on
        """
        x, y = self.position
        width, height = self.size

        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.COLOR_BACKGROUND, bg_rect)

        # Border
        pygame.draw.rect(screen, self.COLOR_BORDER, bg_rect, 2)

        # Health fill
        fill_width = int((width - 4) * (self.current_health / 100))
        if fill_width > 0:
            fill_rect = pygame.Rect(x + 2, y + 2, fill_width, height - 4)
            pygame.draw.rect(screen, self._get_color(), fill_rect)

        # Text label
        font = pygame.font.Font(None, 20)
        text = font.render(f"{int(self.current_health)}%", True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text, text_rect)
