"""
The Guardian character - represents the router/firewall.
Reacts to WiFi signal strength, encryption, and threats.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""
from .base_character import Character, CharacterMood, DialogLine
from ..state.game_state import NetworkState
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

        # Position in kingdom
        self.position = (400, 300)

        # Register event handlers
        self.register_event_handler("SIGNAL_WEAK", self._on_signal_weak)
        self.register_event_handler("SIGNAL_STRONG", self._on_signal_strong)
        self.register_event_handler("ENCRYPTION_CHANGED", self._on_encryption_changed)
        self.register_event_handler("ROGUE_AP_DETECTED", self._on_rogue_ap)
        self.register_event_handler("THREAT_CLEARED", self._on_threat_cleared)

    def update_from_network_state(self, network_state: NetworkState) -> None:
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
            educational_note="WiFi signal below -70 dBm is considered weak. Try moving closer to the router.",
            duration=4.0
        )

    def _on_signal_strong(self, event_data: Dict[str, Any]) -> None:
        """Handle strong signal event."""
        self.transition_to(CharacterMood.HAPPY)
        self.speak(
            f"Ah, much better! Strong signal ({event_data['signal_dbm']} dBm).",
            educational_note="Signal above -50 dBm is excellent. You're close to the router!",
            duration=3.0
        )

    def _on_encryption_changed(self, event_data: Dict[str, Any]) -> None:
        """Handle encryption change."""
        new_armor = event_data['new_armor']
        encryption = event_data['encryption']

        if new_armor == self.ARMOR_NONE:
            self.transition_to(CharacterMood.WORRIED)
            self.speak(
                "⚠️ No encryption! I have no armor - anyone can see your data!",
                educational_note="Unencrypted WiFi (no password) is dangerous. All your traffic is visible to anyone nearby.",
                duration=5.0
            )
        elif new_armor == self.ARMOR_WEAK:
            self.transition_to(CharacterMood.WORRIED)
            self.speak(
                f"My armor is weak ({encryption}). Easily broken!",
                educational_note="WEP encryption is outdated and can be cracked in minutes. Upgrade to WPA2 or WPA3.",
                duration=4.0
            )
        elif new_armor == self.ARMOR_STRONG:
            self.transition_to(CharacterMood.HAPPY)
            self.speak(
                f"Good! I wear steel armor ({encryption}).",
                educational_note="WPA2 is strong encryption. Your network is well protected.",
                duration=3.0
            )
        elif new_armor == self.ARMOR_MAXIMUM:
            self.transition_to(CharacterMood.CELEBRATING)
            self.speak(
                f"Maximum protection! {encryption} is the strongest armor!",
                educational_note="WPA3 is the latest and most secure WiFi encryption standard.",
                duration=4.0
            )

    def _on_rogue_ap(self, event_data: Dict[str, Any]) -> None:
        """Handle rogue AP detection."""
        self.transition_to(CharacterMood.ALERT)
        rogue_count = len(event_data['rogue_aps'])
        self.speak(
            f"🚨 ALERT! {rogue_count} impostor(s) detected nearby!",
            educational_note="Rogue Access Points (Evil Twins) are fake WiFi networks that impersonate legitimate ones to steal data.",
            duration=5.0
        )

    def _on_threat_cleared(self, event_data: Dict[str, Any]) -> None:
        """Handle threat cleared."""
        self.transition_to(CharacterMood.HAPPY)
        self.speak(
            "Threat neutralized! The kingdom is safe again.",
            duration=3.0
        )

    def on_update(self, dt: float) -> None:
        """Guardian-specific update."""
        # Idle animation variations (breathing effect)
        if self.mood == CharacterMood.IDLE:
            import math
            self.animation_timer += dt
            breath_cycle = math.sin(self.animation_timer * 2) * 0.1
            # This would affect sprite rendering (future: y_offset = breath_cycle * 5)
