"""
WiFi Security Dashboard v3.0 - Pygame Game Engine
Main game loop and application entry point.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import sys
import pygame
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import game components  # noqa: E402
from src.gamification.state.game_state import GameState  # noqa: E402
from src.presentation.pygame.ui.health_bar import HealthBar  # noqa: E402
from src.plugins.wifi_plugin import WiFiPlugin  # noqa: E402
from src.plugins.system_plugin import SystemPlugin  # noqa: E402
from src.plugins.base import PluginConfig  # noqa: E402

# Import characters
from src.gamification.characters.guardian import Guardian  # noqa: E402
from src.gamification.characters.professor_packet import ProfessorPacket  # noqa: E402
from src.gamification.characters.impostor import Impostor  # noqa: E402
from src.gamification.characters.eavesdropper import Eavesdropper  # noqa: E402

# Import scenario system
from src.gamification.story.scenario_manager import ScenarioManager  # noqa: E402
from src.gamification.story.progression import PlayerProgress  # noqa: E402
from src.gamification.story.scenarios_library import ALL_SCENARIOS  # noqa: E402


class WiFiSecurityGame:
    """Main game application class."""

    # Window settings
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FPS_TARGET = 60

    # Colors
    COLOR_BACKGROUND = (20, 20, 40)  # Dark blue
    COLOR_TEXT = (255, 255, 255)  # White
    COLOR_SUCCESS = (76, 175, 80)  # Green

    def __init__(self):
        """Initialize Pygame and game components."""
        pygame.init()

        # Display setup
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
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
        wifi_config = PluginConfig(name="wifi", rate_ms=100, config={"mock_mode": True})
        system_config = PluginConfig(name="system", rate_ms=100, config={"mock_mode": True})

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

        # Initialize threat agents
        self.impostor = Impostor()
        self.eavesdropper = Eavesdropper()

        # Initialize progression and scenarios
        self.player_progress = PlayerProgress()
        self.scenario_manager = ScenarioManager(self.player_progress)

        # Start first scenario automatically
        self.scenario_manager.start_scenario("first_day_online")
        if self.scenario_manager.current_scenario:
            for line in self.scenario_manager.current_scenario.intro_dialog:
                self.professor.speak(line, duration=4.0)

        # Welcome player
        self.professor.give_welcome_message()

        print("✅ WiFi Security Game initialized")
        print(f"   Resolution: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        print(f"   Target FPS: {self.FPS_TARGET}")
        print(f"   Mode: {'MOCK (Educational)' if self.game_state.mock_mode else 'REAL'}")
        print("   Characters: Guardian, Professor Packet")
        print("   Threats: Impostor, Eavesdropper")
        print(f"   Scenarios: {len(ALL_SCENARIOS)} available")
        if self.scenario_manager.current_scenario:
            print(f"   Current Scenario: {self.scenario_manager.current_scenario.name}")

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
                elif event.key == pygame.K_c:
                    # Complete next objective (for testing)
                    next_obj = self.scenario_manager.get_next_objective()
                    if next_obj:
                        self.scenario_manager.update_objective(next_obj.objective_id)
                elif event.key == pygame.K_1:
                    # Load scenario 1
                    self.scenario_manager.start_scenario("first_day_online")
                    print("📖 Scenario 1 loaded")
                elif event.key == pygame.K_2:
                    # Load scenario 2
                    self.scenario_manager.start_scenario("the_impostor")
                    print("📖 Scenario 2 loaded")
                elif event.key == pygame.K_3:
                    # Load scenario 3
                    self.scenario_manager.start_scenario("invisible_listener")
                    print("📖 Scenario 3 loaded")
                elif event.key == pygame.K_i:
                    # Toggle Impostor (for testing)
                    if self.impostor.active:
                        self.impostor.deactivate()
                        print("🔵 Impostor deactivated")
                    else:
                        self.impostor.activate()
                        print("🚨 Impostor activated")
                elif event.key == pygame.K_e:
                    # Toggle Eavesdropper (for testing)
                    if self.eavesdropper.active:
                        self.eavesdropper.deactivate()
                        print("🔵 Eavesdropper deactivated")
                    else:
                        self.eavesdropper.activate()
                        print("🚨 Eavesdropper activated")
                elif event.key == pygame.K_d:
                    # Detect active threats (for testing)
                    if self.impostor.active and not self.impostor.detected:
                        self.impostor.detect()
                        print("✅ Impostor detected!")
                    if self.eavesdropper.active and not self.eavesdropper.detected:
                        self.eavesdropper.detect()
                        print("✅ Eavesdropper detected!")

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
            plugin_data = {"wifi": wifi_data, "system": system_data}
            self.game_state.update_from_plugins(plugin_data)

            # Update health bar from signal strength
            signal_percent = self.game_state.network.signal_percent
            self.health_bar.set_health(signal_percent)

            # Update Guardian from network state
            self.guardian.update_from_network_state(self.game_state.network)

            # Update threats from network state
            self.impostor.update_from_network_state(self.game_state.network)
            self.eavesdropper.update_from_network_state(self.game_state.network)

            # Reset timer
            self.data_update_timer = 0.0

        # Update UI animations (60 FPS smooth)
        self.health_bar.update(dt)

        # Update characters (state machines, dialogs, behaviors)
        self.guardian.update(dt)
        self.professor.update(dt)

        # Update threats (only if active)
        if self.impostor.active or self.impostor.visibility > 0:
            self.impostor.update(dt)
        if self.eavesdropper.active or self.eavesdropper.visibility > 0:
            self.eavesdropper.update(dt)

    def render(self) -> None:
        """Render current frame."""
        # Clear screen
        self.screen.fill(self.COLOR_BACKGROUND)

        # Render title
        title_text = self.font_large.render("WiFi Kingdom", True, self.COLOR_TEXT)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)

        # Render subtitle
        subtitle_text = self.font_medium.render(
            "Project Lighthouse - Phase 0", True, self.COLOR_SUCCESS
        )
        subtitle_rect = subtitle_text.get_rect(center=(self.WINDOW_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Render "Guardian Health" label with emoji
        guardian_emoji = self.font.render(self.guardian.emoji, True, self.COLOR_TEXT)
        label_text = self.font_medium.render("Guardian Health (WiFi Signal)", True, self.COLOR_TEXT)
        self.screen.blit(guardian_emoji, (10, 165))
        self.screen.blit(label_text, (50, 170))

        # Render health bar (data flow: WiFi Plugin → GameState → HealthBar)
        self.health_bar.render(self.screen)

        # Render network information
        info_y = 250
        signal_dbm = self.game_state.network.signal_dbm
        signal_pct = self.game_state.network.signal_percent
        network_info = [
            f"SSID: {self.game_state.network.ssid}",
            f"Signal: {signal_dbm} dBm ({signal_pct}%)",
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

        # Render threat dialogs (only if visible)
        if self.impostor.visibility > 0:
            self._render_character_dialog(self.impostor, (800, 200))
        if self.eavesdropper.visibility > 0:
            self._render_character_dialog(self.eavesdropper, (800, 450))

        # Render FPS counter
        fps = self.clock.get_fps()
        fps_text = self.font_small.render(f"FPS: {fps:.1f}", True, self.COLOR_TEXT)
        self.screen.blit(fps_text, (10, 10))

        # Render mode indicator
        mode_text = self.font_small.render(
            f"Mode: {'MOCK' if self.game_state.mock_mode else 'REAL'}", True, (255, 193, 7)  # Amber
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

        # Render threat status (warnings)
        threat_y = status_y + 60
        if self.impostor.active:
            threat_color = (255, 0, 0) if self.impostor.detected else (255, 165, 0)  # Red/Orange
            impostor_emoji = self.font.render(self.impostor.emoji, True, threat_color)
            impostor_status = (
                f"⚠️  THREAT: {self.impostor.name} [Level: {self.impostor.threat_level.upper()}]"
            )
            impostor_text = self.font_small.render(impostor_status, True, threat_color)
            self.screen.blit(impostor_emoji, (10, threat_y - 5))
            self.screen.blit(impostor_text, (45, threat_y))
            threat_y += 25

        if self.eavesdropper.active:
            threat_color = (255, 0, 0) if self.eavesdropper.detected else (255, 165, 0)
            eavesdropper_emoji = self.font.render(self.eavesdropper.emoji, True, threat_color)
            eavesdropper_status = (
                f"⚠️  THREAT: {self.eavesdropper.name} "
                f"[Level: {self.eavesdropper.threat_level.upper()}]"
            )
            eavesdropper_text = self.font_small.render(eavesdropper_status, True, threat_color)
            self.screen.blit(eavesdropper_emoji, (10, threat_y - 5))
            self.screen.blit(eavesdropper_text, (45, threat_y))
            threat_y += 25

        # Render player progress (right side)
        progress_x = self.WINDOW_WIDTH - 400
        progress_y = 35
        progress_info = [
            f"Level: {self.player_progress.level}",
            f"XP: {self.player_progress.total_xp}/{self.player_progress.xp_to_next_level}",
            f"Badges: {len(self.player_progress.badges_earned)}",
            f"Quests: {self.player_progress.quests_completed}",
        ]
        for info in progress_info:
            text = self.font_small.render(info, True, (76, 175, 80))  # Green
            self.screen.blit(text, (progress_x, progress_y))
            progress_y += 25

        # Render current scenario and quest (right side, below progress)
        if self.scenario_manager.current_scenario:
            scenario_x = self.WINDOW_WIDTH - 600
            scenario_y = self.WINDOW_HEIGHT - 200

            # Scenario title
            scenario_title = self.font_medium.render(
                f"📖 {self.scenario_manager.current_scenario.name}", True, (255, 193, 7)  # Amber
            )
            self.screen.blit(scenario_title, (scenario_x, scenario_y))
            scenario_y += 35

            # Current quest objectives
            for quest in self.scenario_manager.current_scenario.quests:
                quest_text = self.font_small.render(
                    f"Quest: {quest.name} ({quest.get_progress()[0]}/{quest.get_progress()[1]})",
                    True,
                    self.COLOR_TEXT,
                )
                self.screen.blit(quest_text, (scenario_x, scenario_y))
                scenario_y += 25

                # Show objectives
                for obj in quest.objectives:
                    status_icon = "✅" if obj.is_complete() else "⏳"
                    obj_text = self.font_small.render(
                        f"  {status_icon} {obj.description}",
                        True,
                        (100, 200, 100) if obj.is_complete() else (200, 200, 200),
                    )
                    self.screen.blit(obj_text, (scenario_x, scenario_y))
                    scenario_y += 22

        # Render instructions
        instructions = [
            "ESC: Exit | P: Pause | F11: Fullscreen",
            "C: Complete next objective | D: Detect threats",
            "1/2/3: Load Scenario 1/2/3",
            "I: Toggle Impostor | E: Toggle Eavesdropper",
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
        current_line: list[str] = []
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

        # Draw character emoji and name
        emoji_text = self.font.render(character.emoji, True, (0, 0, 0))
        name_text = self.font_small.render(f"{character.name}:", True, (50, 50, 150))
        self.screen.blit(emoji_text, (x + padding, y + padding - 5))
        self.screen.blit(name_text, (x + padding + 40, y + padding))

        # Draw dialog text
        text_y = y + padding + 25
        for line in lines:
            line_surface = self.font_small.render(line, True, (0, 0, 0))
            self.screen.blit(line_surface, (x + padding, text_y))
            text_y += line_height

        # Draw educational note if present
        if dialog.educational_note:
            note_y = text_y + 5
            note_text = self.font_small.render(f"💡 {dialog.educational_note}", True, (0, 100, 0))
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
        print("\n📊 Session Statistics:")
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
