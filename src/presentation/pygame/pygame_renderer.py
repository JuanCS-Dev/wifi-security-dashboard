"""
Pygame-specific renderer implementation.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
import pygame
from typing import Dict
from ..base_renderer import Renderer, SpriteData, TextData, ShapeData, Position, Color, Size


class PygameRenderer(Renderer):
    """Pygame-specific renderer implementation."""

    def __init__(self, screen: pygame.Surface):
        """
        Initialize with Pygame screen.

        Args:
            screen: pygame.Surface (from pygame.display.set_mode())
        """
        self.screen = screen
        self.sprites: Dict[str, pygame.Surface] = {}  # sprite_id -> pygame.Surface
        self.fonts: Dict[int, pygame.font.Font] = {}  # font_size -> pygame.font.Font

    def clear(self, color: Color) -> None:
        """Clear screen."""
        self.screen.fill(color)

    def draw_sprite(self, sprite_data: SpriteData) -> None:
        """Draw sprite using Pygame."""
        if sprite_data.sprite_id not in self.sprites:
            print(f"⚠️  Sprite not loaded: {sprite_data.sprite_id}")
            return

        sprite = self.sprites[sprite_data.sprite_id]

        # Apply transformations
        if sprite_data.rotation != 0:
            sprite = pygame.transform.rotate(sprite, sprite_data.rotation)
        if sprite_data.flip_x or sprite_data.flip_y:
            sprite = pygame.transform.flip(sprite, sprite_data.flip_x, sprite_data.flip_y)
        if sprite_data.alpha < 255:
            sprite = sprite.copy()
            sprite.set_alpha(sprite_data.alpha)

        self.screen.blit(sprite, sprite_data.position)

    def draw_text(self, text_data: TextData) -> None:
        """Draw text using Pygame."""
        # Get or create font
        if text_data.font_size not in self.fonts:
            self.fonts[text_data.font_size] = pygame.font.Font(None, text_data.font_size)

        font = self.fonts[text_data.font_size]
        text_surface = font.render(text_data.text, True, text_data.color)

        # Apply alignment
        rect = text_surface.get_rect()
        if text_data.align == "center":
            rect.center = (int(text_data.position[0]), int(text_data.position[1]))
        elif text_data.align == "right":
            rect.right = int(text_data.position[0])
            rect.top = int(text_data.position[1])
        else:  # left
            rect.topleft = (int(text_data.position[0]), int(text_data.position[1]))

        self.screen.blit(text_surface, rect)

    def draw_shape(self, shape_data: ShapeData) -> None:
        """Draw shape using Pygame."""
        if shape_data.shape_type == "rect":
            rect = pygame.Rect(
                int(shape_data.position[0]),
                int(shape_data.position[1]),
                int(shape_data.size[0]),
                int(shape_data.size[1])
            )
            if shape_data.filled:
                pygame.draw.rect(self.screen, shape_data.color, rect)
            else:
                pygame.draw.rect(
                    self.screen,
                    shape_data.color,
                    rect,
                    shape_data.border_width
                )

        elif shape_data.shape_type == "circle":
            radius = int(shape_data.size[0] / 2)
            center = (
                int(shape_data.position[0] + radius),
                int(shape_data.position[1] + radius)
            )
            if shape_data.filled:
                pygame.draw.circle(self.screen, shape_data.color, center, radius)
            else:
                pygame.draw.circle(
                    self.screen,
                    shape_data.color,
                    center,
                    radius,
                    shape_data.border_width
                )

        elif shape_data.shape_type == "line":
            pygame.draw.line(
                self.screen,
                shape_data.color,
                (int(shape_data.position[0]), int(shape_data.position[1])),
                (int(shape_data.size[0]), int(shape_data.size[1])),
                shape_data.border_width if shape_data.border_width > 0 else 1
            )

    def present(self) -> None:
        """Update display."""
        pygame.display.flip()

    def load_sprite(self, sprite_id: str, file_path: str) -> None:
        """Load sprite from file."""
        try:
            surface = pygame.image.load(file_path).convert_alpha()
            self.sprites[sprite_id] = surface
            print(f"✅ Loaded sprite: {sprite_id} from {file_path}")
        except Exception as e:
            print(f"❌ Failed to load sprite {sprite_id}: {e}")

    def get_screen_size(self) -> Size:
        """Get screen size."""
        return self.screen.get_size()
