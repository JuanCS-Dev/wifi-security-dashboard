"""
Renderer abstraction for multi-platform support.
Allows swapping Pygame → Web Canvas → VR without changing game logic.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional


# Type aliases
Position = Tuple[float, float]
Color = Tuple[int, int, int]
Size = Tuple[int, int]


@dataclass
class SpriteData:
    """Data needed to render a sprite."""
    sprite_id: str
    position: Position
    size: Size
    rotation: float = 0.0
    alpha: int = 255
    flip_x: bool = False
    flip_y: bool = False


@dataclass
class TextData:
    """Data needed to render text."""
    text: str
    position: Position
    font_size: int = 24
    color: Color = (255, 255, 255)
    align: str = "left"  # left, center, right


@dataclass
class ShapeData:
    """Data for rendering shapes (bars, circles, etc)."""
    shape_type: str  # "rect", "circle", "line"
    position: Position
    size: Size
    color: Color
    filled: bool = True
    border_width: int = 0


class Renderer(ABC):
    """
    Abstract renderer interface.

    Implementations:
    - PygameRenderer (desktop, Phase 1)
    - WebCanvasRenderer (web, Phase 4)
    - VRRenderer (future, Phase 5+)
    """

    @abstractmethod
    def clear(self, color: Color) -> None:
        """Clear screen with color."""
        pass

    @abstractmethod
    def draw_sprite(self, sprite_data: SpriteData) -> None:
        """Draw a sprite."""
        pass

    @abstractmethod
    def draw_text(self, text_data: TextData) -> None:
        """Draw text."""
        pass

    @abstractmethod
    def draw_shape(self, shape_data: ShapeData) -> None:
        """Draw geometric shape."""
        pass

    @abstractmethod
    def present(self) -> None:
        """Present rendered frame to screen."""
        pass

    @abstractmethod
    def load_sprite(self, sprite_id: str, file_path: str) -> None:
        """Load sprite from file."""
        pass

    @abstractmethod
    def get_screen_size(self) -> Size:
        """Get screen dimensions."""
        pass
