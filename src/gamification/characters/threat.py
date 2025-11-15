"""
Base Threat class - antagonist characters that teach security concepts.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from .base_character import Character, CharacterMood
from typing import Dict, Any, List


class ThreatLevel:
    """Threat severity levels."""

    LOW = "low"  # Informational
    MEDIUM = "medium"  # Warning
    HIGH = "high"  # Danger
    CRITICAL = "critical"  # Severe


class Threat(Character):
    """
    Base class for all threat agents (antagonists).

    Threats are educational antagonists that:
    - Represent real security vulnerabilities
    - React to network conditions
    - Teach security concepts through interaction
    - Can be "defeated" by player actions
    """

    def __init__(
        self, character_id: str, name: str, threat_level: str = ThreatLevel.MEDIUM, emoji: str = "👤"
    ):
        """
        Initialize threat.

        Args:
            character_id: Unique identifier (e.g., "impostor", "eavesdropper")
            name: Display name (e.g., "The Impostor")
            threat_level: Severity level
            emoji: Visual emoji representation
        """
        super().__init__(character_id=character_id, name=name, emoji=emoji)

        # Threat-specific state
        self.threat_level = threat_level
        self.active = False  # Is threat currently present?
        self.detected = False  # Has player detected this threat?
        self.defeated = False  # Has player defeated/mitigated this threat?

        # Educational content
        self.vulnerability_description = ""
        self.mitigation_steps: List[str] = []

        # Visual state
        self.visibility = 0.0  # 0.0 = invisible, 1.0 = fully visible

    def activate(self) -> None:
        """
        Activate this threat (appears in the game).
        Called when network conditions match threat pattern.
        """
        self.active = True
        self.transition_to(CharacterMood.ALERT)
        self.on_activated()

    def detect(self) -> None:
        """
        Player detected this threat.
        Makes threat visible and triggers educational dialog.
        """
        if not self.detected:
            self.detected = True
            self.visibility = 1.0
            self.on_detected()

    def defeat(self) -> None:
        """
        Player defeated/mitigated this threat.
        Removes threat and awards XP.
        """
        if not self.defeated:
            self.defeated = True
            self.active = False
            self.transition_to(CharacterMood.WORRIED)
            self.on_defeated()

    def deactivate(self) -> None:
        """
        Deactivate this threat (network conditions no longer match).
        Threat disappears without player action.
        """
        self.active = False
        self.detected = False
        self.visibility = 0.0
        self.transition_to(CharacterMood.IDLE)

    # Hooks for subclasses

    def on_activated(self) -> None:
        """Called when threat is activated."""
        pass

    def on_detected(self) -> None:
        """Called when player detects threat."""
        pass

    def on_defeated(self) -> None:
        """Called when player defeats threat."""
        pass

    def on_update(self, dt: float) -> None:
        """Threat-specific update logic."""
        # Update visibility (fade in/out)
        if self.active and self.detected:
            # Fade in
            self.visibility = min(1.0, self.visibility + dt * 2.0)
        elif not self.active:
            # Fade out
            self.visibility = max(0.0, self.visibility - dt * 2.0)

    def get_threat_info(self) -> Dict[str, Any]:
        """
        Get threat information for UI display.

        Returns:
            Dict with threat details
        """
        return {
            "name": self.name,
            "level": self.threat_level,
            "active": self.active,
            "detected": self.detected,
            "defeated": self.defeated,
            "visibility": self.visibility,
            "vulnerability": self.vulnerability_description,
            "mitigation": self.mitigation_steps,
        }
