"""
WiFi Security Dashboard v3.0 - Pygame Game Engine
Main game loop and application entry point.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
import sys
import pygame
from typing import Optional
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import game components
from src.gamification.state.game_state import GameState
from src.presentation.pygame.ui.health_bar import HealthBar
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.system_plugin import SystemPlugin
from src.plugins.base import PluginConfig

# Import characters
from src.gamification.characters.guardian import Guardian
from src.gamification.characters.professor_packet import ProfessorPacket


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

        # Game state
        self.game_state = GameState()
        self.game_state.mock_mode = True  # Educational mode

        # Health bar widget
        self.health_bar = HealthBar(position=(50, 200), size=(300, 30))

        # Initialize plugins (mock mode for Phase 0)
        wifi_config = PluginConfig(
            name="wifi",
            rate_ms=100,
            config={'mock_mode': True}
        )
        system_config = PluginConfig(
            name="system",
            rate_ms=100,
            config={'mock_mode': True}
        )

        self.wifi_plugin = WiFiPlugin(wifi_config)
        self.system_plugin = SystemPlugin(system_config)

        self.wifi_plugin.initialize()
        self.system_plugin.initialize()

        # Data update throttling (10 Hz to avoid overload)
        self.data_update_timer = 0.0
        self.data_update_interval = 0.1  # 100ms = 10 Hz

        # Initialize characters
        self.guardian = Guardian()
        self.professor = ProfessorPacket()

        # Welcome player
        self.professor.give_welcome_message()

        print("✅ WiFi Security Game initialized")
        print(f"   Resolution: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        print(f"   Target FPS: {self.FPS_TARGET}")
        print(f"   Mode: {'MOCK (Educational)' if self.game_state.mock_mode else 'REAL'}")
        print(f"   Characters: Guardian, Professor Packet")

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

        # Collect data from plugins (throttled to 10 Hz to avoid overhead)
        self.data_update_timer += dt
        if self.data_update_timer >= self.data_update_interval:
            # Collect plugin data
            wifi_data = self.wifi_plugin.collect_data()
            system_data = self.system_plugin.collect_data()

            # Update game state
            plugin_data = {
                'wifi': wifi_data,
                'system': system_data
            }
            self.game_state.update_from_plugins(plugin_data)

            # Update health bar from signal strength
            signal_percent = self.game_state.network.signal_percent
            self.health_bar.set_health(signal_percent)

            # Update Guardian from network state
            self.guardian.update_from_network_state(self.game_state.network)

            # Reset timer
            self.data_update_timer = 0.0

        # Update UI animations (60 FPS smooth)
        self.health_bar.update(dt)

        # Update characters (state machines, dialogs, behaviors)
        self.guardian.update(dt)
        self.professor.update(dt)

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
            center=(self.WINDOW_WIDTH // 2, 60)
        )
        self.screen.blit(title_text, title_rect)

        # Render subtitle
        subtitle_text = self.font_medium.render(
            "Project Lighthouse - Phase 0",
            True,
            self.COLOR_SUCCESS
        )
        subtitle_rect = subtitle_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, 120)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

        # Render "Guardian Health" label
        label_text = self.font_medium.render(
            "Guardian Health (WiFi Signal)",
            True,
            self.COLOR_TEXT
        )
        self.screen.blit(label_text, (50, 170))

        # Render health bar (data flow: WiFi Plugin → GameState → HealthBar)
        self.health_bar.render(self.screen)

        # Render network information
        info_y = 250
        network_info = [
            f"SSID: {self.game_state.network.ssid}",
            f"Signal: {self.game_state.network.signal_dbm} dBm ({self.game_state.network.signal_percent}%)",
            f"Encryption: {self.game_state.network.encryption}",
            f"Channel: {self.game_state.network.channel}",
            f"Category: {self.game_state.network.signal_strength_category.upper()}",
        ]

        for info in network_info:
            info_text = self.font_small.render(info, True, self.COLOR_TEXT)
            self.screen.blit(info_text, (50, info_y))
            info_y += 25

        # System information
        system_y = 400
        system_info = [
            "System Resources:",
            f"  CPU: {self.game_state.network.cpu_percent:.1f}%",
            f"  RAM: {self.game_state.network.ram_percent:.1f}%",
            f"  Disk: {self.game_state.network.disk_percent:.1f}%",
        ]

        for info in system_info:
            info_text = self.font_small.render(info, True, self.COLOR_TEXT)
            self.screen.blit(info_text, (50, system_y))
            system_y += 25

        # Render character dialogs (speech bubbles)
        self._render_character_dialog(self.guardian, (450, 350))
        self._render_character_dialog(self.professor, (150, 550))

        # Render FPS counter
        fps = self.clock.get_fps()
        fps_text = self.font_small.render(
            f"FPS: {fps:.1f}",
            True,
            self.COLOR_TEXT
        )
        self.screen.blit(fps_text, (10, 10))

        # Render mode indicator
        mode_text = self.font_small.render(
            f"Mode: {'MOCK' if self.game_state.mock_mode else 'REAL'}",
            True,
            (255, 193, 7)  # Amber
        )
        self.screen.blit(mode_text, (self.WINDOW_WIDTH - 150, 10))

        # Render character status
        status_y = 35
        guardian_status = f"Guardian: {self.guardian.mood.name} | Armor: {self.guardian.armor_type}"
        status_text = self.font_small.render(guardian_status, True, self.COLOR_TEXT)
        self.screen.blit(status_text, (10, status_y))

        professor_status = f"Professor: {self.professor.mood.name}"
        prof_text = self.font_small.render(professor_status, True, self.COLOR_TEXT)
        self.screen.blit(prof_text, (10, status_y + 25))

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

    def _render_character_dialog(self, character, position):
        """
        Render character dialog bubble.

        Args:
            character: Character instance
            position: (x, y) position for dialog bubble
        """
        if not character.current_dialog:
            return

        dialog = character.current_dialog
        x, y = position

        # Dialog bubble dimensions
        max_width = 500
        padding = 15

        # Wrap text to fit bubble width
        words = dialog.text.split()
        lines = []
        current_line = []
        test_line = ""

        for word in words:
            test_line = " ".join(current_line + [word])
            test_surface = self.font_small.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width - (padding * 2):
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        # Calculate bubble size
        line_height = 25
        bubble_height = len(lines) * line_height + (padding * 2)
        bubble_width = max_width

        # Draw bubble background
        bubble_rect = pygame.Rect(x, y, bubble_width, bubble_height)
        pygame.draw.rect(self.screen, (255, 255, 220), bubble_rect)  # Light yellow
        pygame.draw.rect(self.screen, (100, 100, 100), bubble_rect, 2)  # Border

        # Draw character name
        name_text = self.font_small.render(
            f"{character.name}:",
            True,
            (50, 50, 150)
        )
        self.screen.blit(name_text, (x + padding, y + padding))

        # Draw dialog text
        text_y = y + padding + 25
        for line in lines:
            line_surface = self.font_small.render(line, True, (0, 0, 0))
            self.screen.blit(line_surface, (x + padding, text_y))
            text_y += line_height

        # Draw educational note if present
        if dialog.educational_note:
            note_y = text_y + 5
            note_text = self.font_small.render(
                f"💡 {dialog.educational_note}",
                True,
                (0, 100, 0)
            )
            # May extend beyond bubble - that's OK for educational content
            self.screen.blit(note_text, (x + padding, note_y))

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
