"""
The Eavesdropper - Packet Sniffer threat agent.
Teaches about packet sniffing, HTTP vs HTTPS, and encryption importance.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

from .threat import Threat, ThreatLevel, CharacterMood
from ..state.game_state import NetworkState
from typing import Dict, Any


class Eavesdropper(Threat):
    """
    The Eavesdropper - Packet Sniffer.

    Represents attackers who intercept unencrypted network traffic.
    Appears when insecure HTTP traffic is detected or encryption is weak.

    Educational Concepts:
    - Packet sniffing
    - HTTP vs HTTPS
    - Unencrypted traffic dangers
    - Man-in-the-Middle attacks
    - Importance of encryption
    """

    def __init__(self):
        super().__init__(
            character_id="eavesdropper",
            name="The Eavesdropper",
            threat_level=ThreatLevel.MEDIUM,
            emoji="👁️",
        )

        # Eavesdropper-specific state
        self.http_connections_count = 0
        self.sniffing = False
        self.data_intercepted = []

        # Position (lurks in shadows)
        self.position = (700, 250)

        # Educational content
        self.vulnerability_description = (
            "Packet sniffers can read unencrypted data flying through the air. "
            "HTTP traffic is like sending postcards - anyone can read them!"
        )
        self.mitigation_steps = [
            "Always use HTTPS (look for the lock icon in browser)",
            "Use strong WiFi encryption (WPA2 or WPA3)",
            "Avoid public/open WiFi for sensitive tasks",
            "Use a VPN on untrusted networks",
        ]

        # Starts invisible
        self.visibility = 0.0
        self.detected = False

        # Register event handlers
        self.register_event_handler("HTTP_DETECTED", self._on_http_detected)
        self.register_event_handler("WEAK_ENCRYPTION", self._on_weak_encryption)

    def update_from_network_state(self, network_state: NetworkState) -> None:
        """
        Update Eavesdropper based on network data.

        Args:
            network_state: NetworkState from GameState
        """
        # Check for weak encryption (opportunities to sniff)
        weak_encryption = network_state.encryption in ["None", "WEP"]

        # Check for HTTP traffic (mock: simulate based on time)
        # In real implementation, would check actual protocol data
        import time

        current_time = time.time()
        # Simulate HTTP traffic every 10 seconds in mock mode
        http_present = (int(current_time) % 10) < 3 if network_state.mock_mode else False

        # Activate if conditions are right for sniffing
        should_activate = weak_encryption or http_present

        if should_activate and not self.active:
            self.activate()
        elif not should_activate and self.active:
            self.deactivate()

    def on_activated(self) -> None:
        """Called when eavesdropping conditions detected."""
        self.sniffing = True
        # Eavesdropper starts invisible - player must detect
        self.visibility = 0.3  # Slight shimmer
        self.speak(
            "Shh... I'm watching everything you do online...",
            mood=CharacterMood.ALERT,
            educational_note=(
                "Packet sniffers are invisible attackers that read " "unencrypted network traffic."
            ),
            duration=5.0,
        )

    def on_detected(self) -> None:
        """Called when player detects the eavesdropper."""
        self.speak(
            "What?! You can SEE me? Impossible!",
            mood=CharacterMood.WORRIED,
            educational_note=(
                "Packet sniffers can be detected using network monitoring tools. "
                "Look for suspicious devices on your network."
            ),
            duration=4.0,
        )
        self.speak(
            "Fine, you caught me. But I already saw your HTTP passwords...",
            mood=CharacterMood.ALERT,
            educational_note=(
                "HTTP sends data in plain text. Passwords, credit cards, messages - "
                "all visible to sniffers!"
            ),
            duration=5.0,
        )

    def on_defeated(self) -> None:
        """Called when player defeats the eavesdropper."""
        self.sniffing = False
        self.data_intercepted.clear()
        self.speak(
            "Ugh, HTTPS everywhere! I can't read anything!",
            mood=CharacterMood.WORRIED,
            educational_note=(
                "HTTPS encrypts your data. Even if intercepted, "
                "it looks like gibberish to attackers."
            ),
            duration=5.0,
        )
        self.speak(
            "I'll retreat... for now. But I'm always watching...",
            mood=CharacterMood.WORRIED,
            educational_note=(
                "Stay vigilant! Always verify the lock icon (HTTPS) "
                "before entering sensitive information."
            ),
            duration=4.0,
        )

    def _on_http_detected(self, event_data: Dict[str, Any]) -> None:
        """Handle HTTP traffic detection."""
        self.http_connections_count += 1
        if not self.active:
            self.activate()

    def _on_weak_encryption(self, event_data: Dict[str, Any]) -> None:
        """Handle weak encryption detection."""
        if not self.active:
            self.activate()

    def intercept_data(self, data_type: str) -> None:
        """
        Simulate intercepting data (for educational demonstration).

        Args:
            data_type: Type of data intercepted (e.g., "password", "email")
        """
        self.data_intercepted.append(data_type)
        self.speak(
            f"Hehe! I just intercepted your {data_type}!",
            mood=CharacterMood.ALERT,
            educational_note=(
                f"Without HTTPS, {data_type}s are sent in plain text. "
                "Always check for the lock icon!"
            ),
            duration=4.0,
        )

    def on_update(self, dt: float) -> None:
        """Eavesdropper-specific update."""
        super().on_update(dt)  # Handle base threat visibility updates

        # Lurking animation when sniffing
        if self.sniffing:
            import math

            self.animation_timer += dt
            # Pulsing visibility (shimmer effect)
            if not self.detected:
                # Invisible but shimmering
                pulse = math.sin(self.animation_timer * 2) * 0.15
                self.visibility = 0.3 + pulse  # 15-45% visible
            # _pulse variable for future use  # noqa: F841
