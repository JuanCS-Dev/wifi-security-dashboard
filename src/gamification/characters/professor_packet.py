"""
Professor Packet character - the wise mentor and educational guide.
Explains concepts, gives quests, and celebrates achievements.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from .base_character import Character, CharacterMood
from typing import Dict, Any, Optional


class ProfessorPacket(Character):
    """
    Professor Packet - The Educational Mentor.

    Functions:
    - Explains technical concepts in kid-friendly language
    - Gives quests and missions
    - Celebrates player achievements
    - Offers hints when player is stuck
    """

    def __init__(self):
        super().__init__(character_id="professor", name="Professor Packet", emoji="👨‍🏫")

        # Professor-specific state
        self.teaching_mode = False
        self.current_lesson: Optional[str] = None
        self.hints_given = 0

        # Position in kingdom (usually near the player)
        self.position = (100, 500)

        # Register event handlers
        self.register_event_handler("PLAYER_JOINED", self._on_player_joined)
        self.register_event_handler("QUEST_COMPLETED", self._on_quest_completed)
        self.register_event_handler("PLAYER_CONFUSED", self._on_player_confused)
        self.register_event_handler("LESSON_REQUESTED", self._on_lesson_requested)

    def give_welcome_message(self) -> None:
        """Give initial welcome message."""
        self.transition_to(CharacterMood.TEACHING)
        self.speak(
            "Welcome to the WiFi Kingdom! I'm Professor Packet, your guide.",
            educational_note="WiFi networks are like invisible kingdoms all around us!",
            duration=4.0,
        )
        self.speak(
            "Today, you'll learn how to protect your network from threats.",
            educational_note="Learning about WiFi security helps keep you safe online.",
            duration=4.0,
        )

    def explain_concept(self, concept: str) -> None:
        """
        Explain a technical concept in educational terms.

        Args:
            concept: Concept ID (e.g., "wifi_signal", "encryption", "rogue_ap")
        """
        self.transition_to(CharacterMood.TEACHING)
        self.teaching_mode = True
        self.current_lesson = concept

        explanations = {
            "wifi_signal": (
                "WiFi signal is like the Guardian's health. Stronger signal = healthier Guardian!",
                "Signal strength is measured in dBm. -50 dBm is excellent, -70 dBm is weak.",
            ),
            "encryption": (
                "Encryption is like armor for your data. "
                "It scrambles messages so only you can read them.",
                "WPA3 is the strongest armor. WPA2 is good. "
                "WEP is like cardboard - very weak!",
            ),
            "rogue_ap": (
                "Rogue APs are impostor networks pretending to be your WiFi. "
                "Very dangerous!",
                "Always check the network name carefully before connecting. "
                "Evil Twins try to trick you!",
            ),
            "packets": (
                "Packets are like letters carrying your data. "
                "HTTP letters are open, HTTPS are sealed.",
                "Always look for HTTPS (the padlock 🔒) when visiting websites!",
            ),
        }

        if concept in explanations:
            main_text, detail_text = explanations[concept]
            self.speak(main_text, educational_note=detail_text, duration=5.0)

    def give_hint(self, hint_type: str) -> None:
        """
        Provide a helpful hint.

        Args:
            hint_type: Type of hint needed
        """
        self.transition_to(CharacterMood.TEACHING)
        self.hints_given += 1

        hints = {
            "signal_weak": "Try moving closer to your router to improve signal strength!",
            "encryption_weak": "Check your router settings and upgrade to WPA2 or WPA3 encryption.",
            "general": "Observe the Guardian's health and mood - they tell you about your network!",
        }

        hint_text = hints.get(hint_type, hints["general"])
        self.speak(f"💡 Hint: {hint_text}", duration=4.0)

    # Event handlers

    def _on_player_joined(self, event_data: Dict[str, Any]) -> None:
        """Handle player joining the game."""
        self.give_welcome_message()

    def _on_quest_completed(self, event_data: Dict[str, Any]) -> None:
        """Handle quest completion."""
        self.transition_to(CharacterMood.CELEBRATING)
        quest_name = event_data.get("quest_name", "quest")
        xp_earned = event_data.get("xp", 0)

        self.speak(f"🎉 Excellent work! You completed '{quest_name}'!", duration=3.0)
        self.speak(
            f"You earned {xp_earned} XP! Keep learning and protecting your network.", duration=3.0
        )

    def _on_player_confused(self, event_data: Dict[str, Any]) -> None:
        """Handle player confusion (stuck, needs help)."""
        self.give_hint(event_data.get("hint_type", "general"))

    def _on_lesson_requested(self, event_data: Dict[str, Any]) -> None:
        """Handle explicit lesson request."""
        concept = event_data.get("concept", "wifi_signal")
        self.explain_concept(concept)

    def on_update(self, dt: float) -> None:
        """Professor-specific update."""
        # Gentle animation when teaching
        if self.teaching_mode and self.mood == CharacterMood.TEACHING:
            import math

            self.animation_timer += dt
            # Gentle head nod animation (future: use for sprite rendering)
            _nod_cycle = math.sin(self.animation_timer * 1.5) * 0.05  # noqa: F841

        # Return to idle after teaching finishes
        if self.teaching_mode and not self.current_dialog and not self.dialog_queue:
            self.teaching_mode = False
            self.current_lesson = None
            self.transition_to(CharacterMood.IDLE)

    def on_mood_changed(self, old_mood: CharacterMood, new_mood: CharacterMood) -> None:
        """React to mood changes."""
        if new_mood == CharacterMood.TEACHING:
            self.teaching_mode = True
