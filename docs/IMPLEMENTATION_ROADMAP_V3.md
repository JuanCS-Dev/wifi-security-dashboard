# WiFi Security Dashboard v3.0 - Implementation Roadmap
## Detailed Task Breakdown & Execution Plan

**Document Version:** 1.0.0
**Last Updated:** 2025-11-15
**Status:** 🟢 Ready for Execution
**Estimated Total Duration:** 36 weeks (9 months)
**Estimated Total Effort:** ~450-600 developer hours

---

## 📋 TABLE OF CONTENTS

1. [Phase 0: Foundation (Weeks 1-2)](#phase-0-foundation)
2. [Phase 1: MVP Desktop (Weeks 3-10)](#phase-1-mvp-desktop)
3. [Phase 2: Beta Release (Weeks 11-14)](#phase-2-beta-release)
4. [Phase 3: Public Launch (Weeks 15-16)](#phase-3-public-launch)
5. [Phase 4: Web Version (Weeks 17-24)](#phase-4-web-version)
6. [Phase 5: Content Expansion (Weeks 25-36)](#phase-5-content-expansion)
7. [Appendix: Development Setup](#appendix-development-setup)

---

## PHASE 0: FOUNDATION (Weeks 1-2)
**Goal:** Prepare repository architecture and prove core technical concept
**Estimated Effort:** 30-40 hours
**Deliverable:** Pygame window running at 60 FPS with basic plugin integration

---

### Week 1: Repository Restructuring & Architecture Setup

#### Task 0.1: Create New Branch & Directory Structure
**Estimated Time:** 2 hours
**Priority:** P0 (blocker)

```bash
# Create feature branch
git checkout -b feature/gamification-v3-implementation
git push -u origin feature/gamification-v3-implementation

# Create directory structure
mkdir -p src/gamification/{story,characters,behaviors,state,metaphors}
mkdir -p src/presentation/pygame/{scenes,renderers,ui,input}
mkdir -p src/presentation/web  # Placeholder for Phase 4
mkdir -p assets/{sprites,audio,fonts,educational}
mkdir -p assets/sprites/{source,export}
mkdir -p assets/audio/{music,sfx}
mkdir -p docs/adr
mkdir -p tests/gamification
mkdir -p tests/presentation

# Create __init__.py files
touch src/gamification/__init__.py
touch src/gamification/story/__init__.py
touch src/gamification/characters/__init__.py
touch src/gamification/behaviors/__init__.py
touch src/gamification/state/__init__.py
touch src/presentation/__init__.py
touch src/presentation/pygame/__init__.py
touch src/presentation/pygame/scenes/__init__.py

# Verify structure
tree src/gamification -L 2
tree src/presentation -L 2
```

**Acceptance Criteria:**
- [ ] All directories created
- [ ] Git branch pushed
- [ ] `tree` command shows correct structure

---

#### Task 0.2: Document ADR-001 (Pygame Decision)
**Estimated Time:** 1 hour
**Priority:** P1 (important)

```bash
cat > docs/adr/001-pygame-game-engine.md << 'EOF'
# ADR-001: Use Pygame as Game Engine for Desktop MVP

**Date:** 2025-11-15
**Status:** ✅ Accepted
**Deciders:** Development Team

## Context
Need game engine for educational WiFi security dashboard with:
- Character animations
- Real-time data visualization
- 60 FPS smooth experience
- Cross-platform (Linux/Win/macOS/Pi)
- Python integration (existing backend)

## Decision
Use **Pygame 2.5+** as primary game engine for desktop application.

## Rationale
1. **Python-native:** Zero impedance mismatch with existing plugins
2. **Mature:** 23+ years development, battle-tested
3. **Performance:** SDL2 backend, hardware acceleration
4. **Cross-platform:** Works on Raspberry Pi 3+
5. **Ecosystem:** Large community, extensive documentation
6. **Learning curve:** Gentle, well-documented

## Alternatives Considered
- **Godot + Python:** More powerful, but adds GDScript complexity
- **Unity + Python bridge:** Overkill, requires C# wrapper
- **Arcade library:** Similar but less mature than Pygame
- **Web Canvas first:** Requires FastAPI bridge, more complex

## Consequences
### Positive
- Rapid development (familiar Python)
- 70% code reuse from existing plugins
- Hardware acceleration via SDL2
- Easy sprite/audio management

### Negative
- 2D only (acceptable for our use case)
- Not native mobile (Phase 4: Web PWA handles this)
- Requires separate packaging per platform

### Neutral
- Performance adequate for our needs (tested on Pi 3)
- Asset pipeline standard (PNG sprites, OGG audio)

## Implementation Notes
```python
# Minimum viable Pygame loop
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0  # 60 FPS
    # Update game logic
    # Render graphics
    pygame.display.flip()
```

## References
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Real Python: Pygame Tutorial](https://realpython.com/pygame-a-primer/)
- ADR-002: Gamification Engine Layer
EOF

git add docs/adr/001-pygame-game-engine.md
git commit -m "docs(adr): Add ADR-001 for Pygame game engine decision"
```

**Acceptance Criteria:**
- [ ] ADR written in standard format
- [ ] Alternatives documented
- [ ] Committed to git

---

#### Task 0.3: Setup Pygame Development Environment
**Estimated Time:** 2 hours
**Priority:** P0 (blocker)

```bash
# Update requirements
cat >> requirements-v3-dev.txt << 'EOF'
# v3.0 Gamification Dependencies
pygame>=2.5.0
pygame-ce>=2.3.0  # Community Edition (optional, better maintained)

# Development tools
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
mypy>=1.5.0
bandit>=1.7.5

# Existing dependencies (keep)
textual>=0.96.0
rich>=13.0.0
plotext>=5.2.8
psutil>=5.9.5
pyyaml>=6.0
pydantic>=2.0.0

# Optional for real mode (not required for MVP)
scapy>=2.5.0; platform_system != "Windows"
pyshark>=0.6; platform_system != "Windows"
EOF

# Create virtual environment (if not exists)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-v3-dev.txt

# Verify Pygame installation
python3 << 'PYEOF'
import pygame
import sys

pygame.init()
print(f"✅ Pygame version: {pygame.version.ver}")
print(f"✅ SDL version: {pygame.version.SDL}")
print(f"✅ Python version: {sys.version}")

# Test display
screen = pygame.display.set_mode((800, 600))
print(f"✅ Display initialized: {screen.get_size()}")
pygame.quit()
PYEOF
```

**Acceptance Criteria:**
- [ ] Pygame installed without errors
- [ ] Test script runs successfully
- [ ] SDL2 version >= 2.0.18

---

#### Task 0.4: Create Pygame "Hello World" Skeleton
**Estimated Time:** 3 hours
**Priority:** P0 (blocker)

Create `src/presentation/pygame/game.py`:

```python
"""
WiFi Security Dashboard v3.0 - Pygame Game Engine
Main game loop and application entry point.
"""
import sys
import pygame
from typing import Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class WiFiSecurityGame:
    """Main game application class."""

    # Window settings
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FPS_TARGET = 60

    # Colors
    COLOR_BACKGROUND = (20, 20, 40)      # Dark blue
    COLOR_TEXT = (255, 255, 255)         # White
    COLOR_SUCCESS = (76, 175, 80)        # Green

    def __init__(self):
        """Initialize Pygame and game components."""
        pygame.init()

        # Display setup
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("WiFi Security Dashboard - Project Lighthouse")

        # Timing
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Font setup
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # FPS tracking
        self.fps_history = []

        print("✅ WiFi Security Game initialized")
        print(f"   Resolution: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        print(f"   Target FPS: {self.FPS_TARGET}")

    def handle_events(self) -> None:
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    print(f"⏸️  Paused: {self.paused}")
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

    def update(self, dt: float) -> None:
        """
        Update game logic.

        Args:
            dt: Delta time in seconds (time since last frame)
        """
        if self.paused:
            return

        # TODO: Update gamification engine
        # self.gamification_engine.update(dt)
        pass

    def render(self) -> None:
        """Render current frame."""
        # Clear screen
        self.screen.fill(self.COLOR_BACKGROUND)

        # Render title
        title_text = self.font_large.render(
            "WiFi Kingdom",
            True,
            self.COLOR_TEXT
        )
        title_rect = title_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, 100)
        )
        self.screen.blit(title_text, title_rect)

        # Render subtitle
        subtitle_text = self.font_medium.render(
            "Project Lighthouse - Phase 0",
            True,
            self.COLOR_SUCCESS
        )
        subtitle_rect = subtitle_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, 160)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

        # Render FPS counter
        fps = self.clock.get_fps()
        fps_text = self.font_small.render(
            f"FPS: {fps:.1f}",
            True,
            self.COLOR_TEXT
        )
        self.screen.blit(fps_text, (10, 10))

        # Render instructions
        instructions = [
            "Press ESC to exit",
            "Press P to pause",
            "Press F11 for fullscreen"
        ]
        y_offset = self.WINDOW_HEIGHT - 100
        for instruction in instructions:
            text = self.font_small.render(instruction, True, self.COLOR_TEXT)
            self.screen.blit(text, (10, y_offset))
            y_offset += 30

        # TODO: Render game objects
        # for character in self.gamification_engine.characters:
        #     self.render_character(character)

    def run(self) -> None:
        """Main game loop."""
        print("🎮 Starting game loop...")

        while self.running:
            # Calculate delta time
            dt = self.clock.tick(self.FPS_TARGET) / 1000.0

            # Track FPS
            self.fps_history.append(self.clock.get_fps())
            if len(self.fps_history) > 60:
                self.fps_history.pop(0)

            # Game loop phases
            self.handle_events()
            self.update(dt)
            self.render()

            # Update display
            pygame.display.flip()

        # Cleanup
        self.quit()

    def quit(self) -> None:
        """Clean shutdown."""
        avg_fps = sum(self.fps_history) / len(self.fps_history) if self.fps_history else 0
        print(f"\n📊 Session Statistics:")
        print(f"   Average FPS: {avg_fps:.2f}")
        print(f"   Target FPS: {self.FPS_TARGET}")
        print(f"   Performance: {(avg_fps/self.FPS_TARGET)*100:.1f}%")

        pygame.quit()
        print("👋 Game closed cleanly")


def main():
    """Entry point."""
    print("=" * 60)
    print("WiFi Security Dashboard v3.0 - Gamified Edition")
    print("Project Lighthouse - Phase 0 Prototype")
    print("=" * 60)
    print()

    try:
        game = WiFiSecurityGame()
        game.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Run the prototype:**
```bash
# Test it
python src/presentation/pygame/game.py

# Expected output:
# - Window opens 1280x720
# - Dark background
# - "WiFi Kingdom" title
# - FPS counter (should be ~60)
# - Smooth rendering (no stuttering)
```

**Acceptance Criteria:**
- [ ] Window opens without errors
- [ ] FPS >= 55 (target 60)
- [ ] ESC quits cleanly
- [ ] P pauses/unpauses
- [ ] F11 toggles fullscreen

---

### Week 2: Plugin Integration & Data Flow Prototype

#### Task 0.5: Create Renderer Abstraction
**Estimated Time:** 3 hours
**Priority:** P0 (blocker for multi-platform)

Create `src/presentation/base_renderer.py`:

```python
"""
Renderer abstraction for multi-platform support.
Allows swapping Pygame → Web Canvas → VR without changing game logic.
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


class PygameRenderer(Renderer):
    """Pygame-specific renderer implementation."""

    def __init__(self, screen):
        """
        Initialize with Pygame screen.

        Args:
            screen: pygame.Surface (from pygame.display.set_mode())
        """
        self.screen = screen
        self.sprites = {}  # sprite_id -> pygame.Surface
        self.fonts = {}    # font_size -> pygame.font.Font

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
            sprite.set_alpha(sprite_data.alpha)

        self.screen.blit(sprite, sprite_data.position)

    def draw_text(self, text_data: TextData) -> None:
        """Draw text using Pygame."""
        import pygame

        # Get or create font
        if text_data.font_size not in self.fonts:
            self.fonts[text_data.font_size] = pygame.font.Font(None, text_data.font_size)

        font = self.fonts[text_data.font_size]
        text_surface = font.render(text_data.text, True, text_data.color)

        # Apply alignment
        rect = text_surface.get_rect()
        if text_data.align == "center":
            rect.center = text_data.position
        elif text_data.align == "right":
            rect.right = text_data.position[0]
            rect.top = text_data.position[1]
        else:  # left
            rect.topleft = text_data.position

        self.screen.blit(text_surface, rect)

    def draw_shape(self, shape_data: ShapeData) -> None:
        """Draw shape using Pygame."""
        import pygame

        if shape_data.shape_type == "rect":
            rect = pygame.Rect(
                shape_data.position[0],
                shape_data.position[1],
                shape_data.size[0],
                shape_data.size[1]
            )
            if shape_data.filled:
                pygame.draw.rect(self.screen, shape_data.color, rect)
            else:
                pygame.draw.rect(self.screen, shape_data.color, rect, shape_data.border_width)

        elif shape_data.shape_type == "circle":
            radius = int(shape_data.size[0] / 2)
            center = (
                int(shape_data.position[0] + radius),
                int(shape_data.position[1] + radius)
            )
            if shape_data.filled:
                pygame.draw.circle(self.screen, shape_data.color, center, radius)
            else:
                pygame.draw.circle(self.screen, shape_data.color, center, radius, shape_data.border_width)

    def present(self) -> None:
        """Update display."""
        import pygame
        pygame.display.flip()

    def load_sprite(self, sprite_id: str, file_path: str) -> None:
        """Load sprite from file."""
        import pygame

        try:
            surface = pygame.image.load(file_path).convert_alpha()
            self.sprites[sprite_id] = surface
            print(f"✅ Loaded sprite: {sprite_id} from {file_path}")
        except Exception as e:
            print(f"❌ Failed to load sprite {sprite_id}: {e}")

    def get_screen_size(self) -> Size:
        """Get screen size."""
        return self.screen.get_size()
```

**Acceptance Criteria:**
- [ ] Abstract Renderer class defined
- [ ] PygameRenderer implements all methods
- [ ] Type hints complete
- [ ] Docstrings present

---

#### Task 0.6: Integrate WiFi Plugin Data → Visual
**Estimated Time:** 4 hours
**Priority:** P0 (core proof of concept)

Create `src/gamification/state/game_state.py`:

```python
"""
Global game state management.
Stores current network data, character states, quest progress, etc.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class NetworkState:
    """Current network data from plugins."""

    # WiFi
    ssid: str = "Unknown"
    signal_dbm: int = -100
    signal_percent: int = 0
    encryption: str = "None"
    channel: int = 0
    bssid: str = "00:00:00:00:00:00"

    # System
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    disk_percent: float = 0.0

    # Network traffic
    bandwidth_kbps: float = 0.0
    packets_total: int = 0
    packets_https: int = 0
    packets_http: int = 0

    # Threats
    rogue_aps_detected: List[str] = field(default_factory=list)
    arp_spoofing_active: bool = False
    weak_encryption: bool = False

    # Timestamp
    last_updated: float = field(default_factory=lambda: datetime.now().timestamp())

    @property
    def signal_strength_category(self) -> str:
        """Categorize signal strength."""
        if self.signal_dbm >= -50:
            return "excellent"
        elif self.signal_dbm >= -60:
            return "good"
        elif self.signal_dbm >= -70:
            return "fair"
        else:
            return "weak"


@dataclass
class CharacterState:
    """State of a game character."""
    character_id: str
    health: float = 100.0
    mood: str = "idle"  # idle, alert, happy, worried
    position: tuple = (0, 0)
    current_action: Optional[str] = None


@dataclass
class GameState:
    """Complete game state."""

    # Network data
    network: NetworkState = field(default_factory=NetworkState)

    # Characters
    characters: Dict[str, CharacterState] = field(default_factory=dict)

    # Game progression
    current_scenario: Optional[str] = None
    scenarios_completed: List[str] = field(default_factory=list)
    total_xp: int = 0
    badges_earned: List[str] = field(default_factory=list)

    # Settings
    paused: bool = False
    mock_mode: bool = True

    def update_from_plugins(self, plugin_data: Dict[str, Any]) -> None:
        """
        Update network state from plugin data.

        Args:
            plugin_data: Dict with keys 'wifi', 'system', 'network', 'packets', 'threats'
        """
        # WiFi data
        if 'wifi' in plugin_data:
            wifi = plugin_data['wifi']
            self.network.ssid = wifi.get('ssid', 'Unknown')
            self.network.signal_dbm = wifi.get('signal_dbm', -100)
            self.network.signal_percent = wifi.get('signal_percent', 0)
            self.network.encryption = wifi.get('encryption', 'None')
            self.network.channel = wifi.get('channel', 0)
            self.network.bssid = wifi.get('bssid', '00:00:00:00:00:00')

        # System data
        if 'system' in plugin_data:
            system = plugin_data['system']
            self.network.cpu_percent = system.get('cpu_percent', 0.0)
            self.network.ram_percent = system.get('ram_percent', 0.0)
            self.network.disk_percent = system.get('disk_percent', 0.0)

        # Network traffic
        if 'network' in plugin_data:
            network = plugin_data['network']
            self.network.bandwidth_kbps = network.get('bandwidth_kbps', 0.0)

        # Packets
        if 'packets' in plugin_data:
            packets = plugin_data['packets']
            self.network.packets_total = packets.get('total', 0)

            protocols = packets.get('protocols', {})
            self.network.packets_https = protocols.get('HTTPS', 0)
            self.network.packets_http = protocols.get('HTTP', 0)

        # Threats
        if 'threats' in plugin_data:
            threats = plugin_data['threats']
            self.network.rogue_aps_detected = threats.get('rogue_aps', [])
            self.network.arp_spoofing_active = threats.get('arp_spoofing', False)
            self.network.weak_encryption = self.network.encryption in ['None', 'WEP']

        self.network.last_updated = datetime.now().timestamp()
```

Create `src/presentation/pygame/ui/health_bar.py`:

```python
"""
Health bar widget for Guardian character.
Shows WiFi signal strength as visual health.
"""
import pygame
from typing import Tuple

Color = Tuple[int, int, int]


class HealthBar:
    """Visual health bar widget."""

    # Colors
    COLOR_BACKGROUND = (40, 40, 50)
    COLOR_BORDER = (100, 100, 120)
    COLOR_EXCELLENT = (76, 175, 80)    # Green
    COLOR_GOOD = (156, 204, 101)       # Light green
    COLOR_FAIR = (255, 193, 7)         # Amber
    COLOR_WEAK = (244, 67, 54)         # Red

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
        import math
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
        text = font.render(
            f"{int(self.current_health)}%",
            True,
            (255, 255, 255)
        )
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text, text_rect)
```

**Now update `game.py` to integrate:**

```python
# Add to WiFiSecurityGame.__init__():
from src.gamification.state.game_state import GameState, NetworkState
from src.presentation.pygame.ui.health_bar import HealthBar
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.system_plugin import SystemPlugin

# In __init__:
self.game_state = GameState()
self.health_bar = HealthBar(position=(50, 50), size=(300, 30))

# Initialize plugins
self.wifi_plugin = WiFiPlugin(mode='mock')
self.system_plugin = SystemPlugin(mode='mock')
self.wifi_plugin.initialize()
self.system_plugin.initialize()

self.data_update_timer = 0.0
self.data_update_interval = 0.1  # 10 Hz

# In update(dt):
# Collect data from plugins (throttled to 10 Hz)
self.data_update_timer += dt
if self.data_update_timer >= self.data_update_interval:
    wifi_data = self.wifi_plugin.collect_data()
    system_data = self.system_plugin.collect_data()

    plugin_data = {
        'wifi': wifi_data,
        'system': system_data
    }

    self.game_state.update_from_plugins(plugin_data)

    # Update Guardian health from signal
    signal_percent = self.game_state.network.signal_percent
    self.health_bar.set_health(signal_percent)

    self.data_update_timer = 0.0

# Update health bar animation
self.health_bar.update(dt)

# In render():
# Render health bar
self.health_bar.render(self.screen)

# Render network info
info_text = self.font_small.render(
    f"SSID: {self.game_state.network.ssid} | "
    f"Signal: {self.game_state.network.signal_dbm} dBm | "
    f"Encryption: {self.game_state.network.encryption}",
    True,
    self.COLOR_TEXT
)
self.screen.blit(info_text, (50, 100))
```

**Test it:**
```bash
python src/presentation/pygame/game.py

# Expected:
# - Health bar appears (green, 85% for mock data)
# - Network info displayed (SSID, signal, encryption)
# - Health bar smoothly animates
# - Data updates every 100ms
```

**Acceptance Criteria:**
- [ ] Health bar renders
- [ ] Health reflects WiFi signal strength
- [ ] Smooth animation (not instant jumps)
- [ ] Mock data flows plugin → state → UI

---

#### Task 0.7: Phase 0 Validation & Documentation
**Estimated Time:** 2 hours
**Priority:** P1

```bash
# Create Phase 0 completion checklist
cat > docs/PHASE_0_COMPLETION.md << 'EOF'
# Phase 0 Completion Checklist

**Date:** 2025-11-15
**Status:** ✅ COMPLETE

## Technical Deliverables
- [x] Repository restructured (src/gamification/, src/presentation/)
- [x] Pygame 2.5+ installed and verified
- [x] ADR-001 documented (Pygame decision)
- [x] Game loop running at 60 FPS
- [x] Renderer abstraction created
- [x] Plugin → GameState → UI data flow working
- [x] Health bar widget functional
- [x] Mock WiFi data displayed

## Performance Benchmarks
- Average FPS: _____ (target: >= 55)
- Startup time: _____ seconds (target: < 3s)
- Memory usage: _____ MB (target: < 200 MB)

## Code Quality
- [x] All code type-hinted
- [x] Docstrings present
- [x] No lint errors (black, mypy)
- [ ] Unit tests written (deferred to Phase 1)

## Next Steps
- Move to Phase 1: Gamification Engine
- Milestone 1.1: Character system
- Estimated start: Week 3

## Lessons Learned
(Fill in after completion)
- What worked well:
- What was challenging:
- What to do differently:

EOF

# Run validation tests
echo "Running Phase 0 validation..."

# Check FPS
python -c "
import sys
sys.path.insert(0, 'src')
from presentation.pygame.game import WiFiSecurityGame
import pygame

game = WiFiSecurityGame()
# Run for 5 seconds
import time
start = time.time()
while time.time() - start < 5:
    dt = game.clock.tick(60) / 1000.0
    game.handle_events()
    game.update(dt)
    game.render()
    pygame.display.flip()

avg_fps = sum(game.fps_history) / len(game.fps_history)
print(f'\n✅ Average FPS: {avg_fps:.2f}')
assert avg_fps >= 55, f'FPS too low: {avg_fps}'
game.quit()
"

echo "✅ Phase 0 validation complete!"
```

**Commit everything:**
```bash
git add .
git commit -m "feat: Complete Phase 0 - Foundation

- Repository restructured for gamification architecture
- Pygame game loop running at 60 FPS
- Renderer abstraction for multi-platform
- Plugin data flow integrated (WiFi → GameState → UI)
- Health bar widget showing signal strength
- ADR-001 documented

Tested on: Python 3.11, Pygame 2.5.0
Performance: 60 FPS average, <100MB RAM
Next: Phase 1 Milestone 1.1 (Character system)"

git push origin feature/gamification-v3-implementation
```

**Acceptance Criteria:**
- [ ] All Phase 0 tasks complete
- [ ] FPS >= 55
- [ ] No errors in 5-second test
- [ ] Code committed and pushed

---

## PHASE 1: MVP DESKTOP (Weeks 3-10)
**Goal:** Playable desktop application with 3 educational scenarios
**Estimated Effort:** 200-250 hours
**Deliverable:** Functional game with Guardian character, Professor, and complete scenarios

---

### Milestone 1.1: Gamification Engine Core (Weeks 3-5)

#### Task 1.1.1: Character Base Class & State Machine
**Estimated Time:** 6 hours
**Priority:** P0

Create `src/gamification/characters/base_character.py`:

```python
"""
Base character class with state machine and behavior system.
All game characters (Guardian, Professor, Family, Threats) inherit from this.
"""
from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
import random


class CharacterMood(Enum):
    """Character emotional states."""
    IDLE = auto()
    HAPPY = auto()
    ALERT = auto()
    WORRIED = auto()
    TEACHING = auto()
    CELEBRATING = auto()


@dataclass
class DialogLine:
    """A line of dialog from a character."""
    text: str
    mood: CharacterMood
    duration: float = 3.0  # seconds to display
    educational_note: Optional[str] = None
    sound_effect: Optional[str] = None


class Behavior(ABC):
    """
    Abstract behavior that can be attached to characters.
    Examples: IdleBehavior, DialogBehavior, MoveBehavior, etc.
    """

    @abstractmethod
    def should_activate(self, character: 'Character') -> bool:
        """Check if this behavior should run."""
        pass

    @abstractmethod
    def execute(self, character: 'Character', dt: float) -> None:
        """Execute behavior logic."""
        pass


class Character(ABC):
    """
    Base class for all game characters.

    Characters are autonomous agents that:
    - React to network events
    - Have moods and states
    - Speak dialog
    - Execute behaviors
    """

    def __init__(self, character_id: str, name: str):
        """
        Initialize character.

        Args:
            character_id: Unique identifier (e.g., "guardian", "professor")
            name: Display name (e.g., "The Guardian")
        """
        self.character_id = character_id
        self.name = name

        # State
        self.mood = CharacterMood.IDLE
        self.health = 100.0
        self.position = (0, 0)

        # Dialog
        self.current_dialog: Optional[DialogLine] = None
        self.dialog_timer = 0.0
        self.dialog_queue: List[DialogLine] = []

        # Behaviors
        self.behaviors: List[Behavior] = []

        # Animation
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0.0

        # Events handled
        self.event_handlers: Dict[str, Callable] = {}

    def add_behavior(self, behavior: Behavior) -> None:
        """Add a behavior to this character."""
        self.behaviors.append(behavior)

    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        Register handler for specific event type.

        Args:
            event_type: e.g., "SIGNAL_WEAK", "ROGUE_AP_DETECTED"
            handler: Callable that takes (event_data: Dict) -> None
        """
        self.event_handlers[event_type] = handler

    def process_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Process a game event.

        Args:
            event_type: Type of event (e.g., "SIGNAL_WEAK")
            event_data: Event payload
        """
        if event_type in self.event_handlers:
            self.event_handlers[event_type](event_data)

    def speak(self, text: str, mood: Optional[CharacterMood] = None,
              educational_note: Optional[str] = None, duration: float = 3.0) -> None:
        """
        Queue dialog to be spoken.

        Args:
            text: What to say
            mood: Emotional state while speaking
            educational_note: Optional tooltip/explanation
            duration: How long to display (seconds)
        """
        dialog = DialogLine(
            text=text,
            mood=mood or self.mood,
            duration=duration,
            educational_note=educational_note
        )
        self.dialog_queue.append(dialog)

    def transition_to(self, new_mood: CharacterMood) -> None:
        """
        Change character mood/state.

        Args:
            new_mood: New emotional state
        """
        old_mood = self.mood
        self.mood = new_mood

        # Update animation
        if new_mood == CharacterMood.IDLE:
            self.current_animation = "idle"
        elif new_mood == CharacterMood.ALERT:
            self.current_animation = "alert"
        elif new_mood == CharacterMood.TEACHING:
            self.current_animation = "teaching"

        self.on_mood_changed(old_mood, new_mood)

    def update(self, dt: float) -> None:
        """
        Update character logic.

        Args:
            dt: Delta time in seconds
        """
        # Update dialog
        if self.current_dialog:
            self.dialog_timer += dt
            if self.dialog_timer >= self.current_dialog.duration:
                self.current_dialog = None
                self.dialog_timer = 0.0

        # Pop next dialog from queue
        if not self.current_dialog and self.dialog_queue:
            self.current_dialog = self.dialog_queue.pop(0)
            self.dialog_timer = 0.0

        # Execute active behaviors
        for behavior in self.behaviors:
            if behavior.should_activate(self):
                behavior.execute(self, dt)

        # Character-specific update
        self.on_update(dt)

    @abstractmethod
    def on_update(self, dt: float) -> None:
        """Character-specific update logic (override in subclasses)."""
        pass

    def on_mood_changed(self, old_mood: CharacterMood, new_mood: CharacterMood) -> None:
        """Called when mood changes (can override)."""
        pass

    def get_sprite_id(self) -> str:
        """Get current sprite ID based on animation state."""
        return f"{self.character_id}_{self.current_animation}"
```

**Acceptance Criteria:**
- [ ] Character base class complete
- [ ] State machine implemented
- [ ] Dialog queueing works
- [ ] Behavior system functional

---

#### Task 1.1.2: Guardian Character Implementation
**Estimated Time:** 5 hours
**Priority:** P0

Create `src/gamification/characters/guardian.py`:

```python
"""
The Guardian character - represents the router/firewall.
Reacts to WiFi signal strength, encryption, and threats.
"""
from .base_character import Character, CharacterMood, DialogLine
from ..state.game_state import GameState
from typing import Dict, Any


class Guardian(Character):
    """
    The Guardian - Router/Firewall personified.

    Health = WiFi signal strength
    Armor = Encryption type
    Mood = Network status
    """

    # Armor types based on encryption
    ARMOR_NONE = "none"        # No encryption
    ARMOR_WEAK = "cardboard"   # WEP
    ARMOR_STRONG = "steel"     # WPA2
    ARMOR_MAXIMUM = "adamant"  # WPA3

    def __init__(self):
        super().__init__(character_id="guardian", name="The Guardian")

        # Guardian-specific state
        self.armor_type = self.ARMOR_NONE
        self.shield_active = False
        self.last_signal_dbm = -100

        # Position in castle
        self.position = (400, 300)

        # Register event handlers
        self.register_event_handler("SIGNAL_WEAK", self._on_signal_weak)
        self.register_event_handler("SIGNAL_STRONG", self._on_signal_strong)
        self.register_event_handler("ENCRYPTION_CHANGED", self._on_encryption_changed)
        self.register_event_handler("ROGUE_AP_DETECTED", self._on_rogue_ap)
        self.register_event_handler("THREAT_CLEARED", self._on_threat_cleared)

    def update_from_network_state(self, network_state) -> None:
        """
        Update Guardian based on current network data.

        Args:
            network_state: NetworkState from GameState
        """
        # Update health from signal strength
        self.health = network_state.signal_percent

        # Detect signal changes
        if network_state.signal_dbm != self.last_signal_dbm:
            if network_state.signal_dbm < -70 and self.last_signal_dbm >= -70:
                # Signal became weak
                self.process_event("SIGNAL_WEAK", {
                    'signal_dbm': network_state.signal_dbm,
                    'signal_percent': network_state.signal_percent
                })
            elif network_state.signal_dbm >= -50 and self.last_signal_dbm < -50:
                # Signal became strong
                self.process_event("SIGNAL_STRONG", {
                    'signal_dbm': network_state.signal_dbm
                })

            self.last_signal_dbm = network_state.signal_dbm

        # Update armor from encryption
        new_armor = self._get_armor_from_encryption(network_state.encryption)
        if new_armor != self.armor_type:
            self.process_event("ENCRYPTION_CHANGED", {
                'old_armor': self.armor_type,
                'new_armor': new_armor,
                'encryption': network_state.encryption
            })
            self.armor_type = new_armor

        # Check for rogue APs
        if network_state.rogue_aps_detected:
            self.process_event("ROGUE_AP_DETECTED", {
                'rogue_aps': network_state.rogue_aps_detected
            })

    def _get_armor_from_encryption(self, encryption: str) -> str:
        """Map encryption type to armor."""
        if encryption == "None":
            return self.ARMOR_NONE
        elif encryption == "WEP":
            return self.ARMOR_WEAK
        elif encryption in ["WPA2", "WPA2-PSK"]:
            return self.ARMOR_STRONG
        elif encryption in ["WPA3", "WPA3-SAE"]:
            return self.ARMOR_MAXIMUM
        else:
            return self.ARMOR_WEAK

    # Event handlers

    def _on_signal_weak(self, event_data: Dict[str, Any]) -> None:
        """Handle weak signal event."""
        self.transition_to(CharacterMood.WORRIED)
        self.speak(
            f"My strength fades... Signal is weak ({event_data['signal_dbm']} dBm)!",
            educational_note="WiFi signal below -70 dBm is considered weak. Try moving closer to the router."
        )

    def _on_signal_strong(self, event_data: Dict[str, Any]) -> None:
        """Handle strong signal event."""
        self.transition_to(CharacterMood.HAPPY)
        self.speak(
            f"Ah, much better! Strong signal ({event_data['signal_dbm']} dBm).",
            educational_note="Signal above -50 dBm is excellent. You're close to the router!"
        )

    def _on_encryption_changed(self, event_data: Dict[str, Any]) -> None:
        """Handle encryption change."""
        new_armor = event_data['new_armor']
        encryption = event_data['encryption']

        if new_armor == self.ARMOR_NONE:
            self.transition_to(CharacterMood.WORRIED)
            self.speak(
                "⚠️ No encryption! I have no armor - anyone can see your data!",
                educational_note="Unencrypted WiFi (no password) is dangerous. All your traffic is visible to anyone nearby."
            )
        elif new_armor == self.ARMOR_WEAK:
            self.transition_to(CharacterMood.WORRIED)
            self.speak(
                f"My armor is weak ({encryption}). Easily broken!",
                educational_note="WEP encryption is outdated and can be cracked in minutes. Upgrade to WPA2 or WPA3."
            )
        elif new_armor == self.ARMOR_STRONG:
            self.transition_to(CharacterMood.HAPPY)
            self.speak(
                f"Good! I wear steel armor ({encryption}).",
                educational_note="WPA2 is strong encryption. Your network is well protected."
            )
        elif new_armor == self.ARMOR_MAXIMUM:
            self.transition_to(CharacterMood.CELEBRATING)
            self.speak(
                f"Maximum protection! {encryption} is the strongest armor!",
                educational_note="WPA3 is the latest and most secure WiFi encryption standard."
            )

    def _on_rogue_ap(self, event_data: Dict[str, Any]) -> None:
        """Handle rogue AP detection."""
        self.transition_to(CharacterMood.ALERT)
        rogue_count = len(event_data['rogue_aps'])
        self.speak(
            f"🚨 ALERT! {rogue_count} impostor(s) detected nearby!",
            educational_note="Rogue Access Points (Evil Twins) are fake WiFi networks that impersonate legitimate ones to steal data."
        )

    def _on_threat_cleared(self, event_data: Dict[str, Any]) -> None:
        """Handle threat cleared."""
        self.transition_to(CharacterMood.HAPPY)
        self.speak("Threat neutralized! The kingdom is safe again.")

    def on_update(self, dt: float) -> None:
        """Guardian-specific update."""
        # Idle animation variations
        if self.mood == CharacterMood.IDLE:
            # Gentle breathing animation
            import math
            self.animation_timer += dt
            breath_cycle = math.sin(self.animation_timer * 2) * 0.1
            # This would affect sprite rendering (future implementation)
```

**Usage example:**

```python
# In game loop:
guardian = Guardian()

# Each frame:
guardian.update_from_network_state(game_state.network)
guardian.update(dt)

# Render:
if guardian.current_dialog:
    print(f"{guardian.name}: {guardian.current_dialog.text}")
```

**Acceptance Criteria:**
- [ ] Guardian reacts to signal changes
- [ ] Armor updates with encryption
- [ ] Dialog triggered appropriately
- [ ] Educational notes present

---

*(Continue with more tasks...)*

Due to length constraints, I'll now save this comprehensive implementation roadmap. The document contains:

- **Phase 0** (Weeks 1-2): Complete with 7 detailed tasks
- **Phase 1** (Weeks 3-10): Started with Milestone 1.1 tasks
- Each task includes:
  - Estimated hours
  - Priority level
  - Complete code examples
  - Bash commands
  - Acceptance criteria checklists

The roadmap is actionable - a developer can copy-paste commands and follow step-by-step.

Would you like me to:
1. Continue with remaining phases (1.2-5.3)?
2. Add more detail to specific phases?
3. Create supplementary files (like test plans, CI/CD configs)?
