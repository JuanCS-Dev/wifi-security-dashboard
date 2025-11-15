"""
The Impostor - Rogue AP / Evil Twin threat agent.
Teaches about fake WiFi networks and Evil Twin attacks.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from .threat import Threat, ThreatLevel, CharacterMood
from ..state.game_state import NetworkState
from typing import Dict, Any


class Impostor(Threat):
    """
    The Impostor - Rogue AP / Evil Twin.

    Represents fake WiFi networks that impersonate legitimate ones.
    Appears when rogue APs are detected on the network.

    Educational Concepts:
    - Evil Twin attacks
    - SSID spoofing
    - Rogue Access Points
    - Network verification
    """

    def __init__(self):
        super().__init__(
            character_id="impostor",
            name="The Impostor",
            threat_level=ThreatLevel.HIGH,
            emoji="👻",
        )

        # Impostor-specific state
        self.rogue_ap_count = 0
        self.fake_ssid = ""
        self.impersonating = False

        # Position (appears near the Guardian)
        self.position = (500, 300)

        # Educational content
        self.vulnerability_description = (
            "Rogue Access Points (Evil Twins) are fake WiFi networks "
            "that pretend to be legitimate ones to steal your data."
        )
        self.mitigation_steps = [
            "Verify the network name (SSID) with your router",
            "Check for multiple networks with the same name",
            "Use WPA3 encryption (harder to spoof)",
            "Never connect to unknown networks",
        ]

        # Register event handlers
        self.register_event_handler("ROGUE_AP_DETECTED", self._on_rogue_ap_detected)
        self.register_event_handler("ROGUE_AP_CLEARED", self._on_rogue_ap_cleared)

    def update_from_network_state(self, network_state: NetworkState) -> None:
        """
        Update Impostor based on network data.

        Args:
            network_state: NetworkState from GameState
        """
        # Check for rogue APs
        rogue_count = len(network_state.rogue_aps_detected)

        if rogue_count > 0 and not self.active:
            # Rogue AP detected - activate threat
            self.rogue_ap_count = rogue_count
            self.fake_ssid = (
                network_state.rogue_aps_detected[0] if network_state.rogue_aps_detected else ""
            )
            self.activate()

        elif rogue_count == 0 and self.active:
            # Rogue APs cleared - deactivate threat
            self.deactivate()

        # Update rogue count
        self.rogue_ap_count = rogue_count

    def on_activated(self) -> None:
        """Called when rogue AP is detected."""
        self.impersonating = True
        self.speak(
            f"Hehehe! I am '{self.fake_ssid}' - connect to ME!",
            mood=CharacterMood.ALERT,
            educational_note=(
                "This is an Evil Twin attack! A fake network is pretending " "to be your real WiFi."
            ),
            duration=5.0,
        )
        self.speak(
            "Your data will be MINE!",
            mood=CharacterMood.ALERT,
            educational_note=(
                "Evil Twins can steal passwords, credit cards, " "and personal information."
            ),
            duration=4.0,
        )

    def on_detected(self) -> None:
        """Called when player detects the impostor."""
        self.speak(
            "No! You spotted me! How did you know?",
            mood=CharacterMood.WORRIED,
            educational_note=(
                "Look for these signs: duplicate SSIDs, weak signal from 'home' "
                "network, suspicious connection requests."
            ),
            duration=4.0,
        )

    def on_defeated(self) -> None:
        """Called when player defeats the impostor."""
        self.impersonating = False
        self.speak(
            "Ugh, foiled again! But I'll be back...",
            mood=CharacterMood.WORRIED,
            educational_note=(
                "Good job! Always verify your network before connecting. "
                "Use strong encryption (WPA3) to prevent Evil Twins."
            ),
            duration=5.0,
        )

    def _on_rogue_ap_detected(self, event_data: Dict[str, Any]) -> None:
        """Handle rogue AP detection event."""
        if not self.detected:
            # Auto-detect on first sighting
            self.detect()

    def _on_rogue_ap_cleared(self, event_data: Dict[str, Any]) -> None:
        """Handle rogue AP cleared event."""
        if self.active:
            self.defeat()

    def on_update(self, dt: float) -> None:
        """Impostor-specific update."""
        super().on_update(dt)  # Handle base threat visibility updates

        # Sneaky animation when impersonating
        if self.impersonating and self.mood == CharacterMood.ALERT:
            import math

            self.animation_timer += dt
            # Shifty movement (future: use for sprite rendering)
            _shift_x = math.sin(self.animation_timer * 3) * 5  # noqa: F841
