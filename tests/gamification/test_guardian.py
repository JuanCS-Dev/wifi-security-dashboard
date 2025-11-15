"""
Unit tests for Guardian character.

Tests the Guardian character implementation, armor system, and network event handling.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import pytest
from src.gamification.characters.guardian import Guardian
from src.gamification.characters.base_character import CharacterMood
from src.gamification.state.game_state import NetworkState


class TestGuardianInitialization:
    """Tests for Guardian initialization."""

    def test_guardian_init(self):
        """Test Guardian initializes correctly."""
        guardian = Guardian()

        assert guardian.character_id == "guardian"
        assert guardian.name == "The Guardian"
        assert guardian.emoji == "🛡️"
        assert guardian.armor_type == Guardian.ARMOR_NONE
        assert guardian.shield_active is False
        assert guardian.last_signal_dbm == -100

    def test_guardian_position(self):
        """Test Guardian has correct initial position."""
        guardian = Guardian()
        assert guardian.position == (400, 300)

    def test_guardian_event_handlers_registered(self):
        """Test Guardian registers all event handlers."""
        guardian = Guardian()

        assert "SIGNAL_WEAK" in guardian.event_handlers
        assert "SIGNAL_STRONG" in guardian.event_handlers
        assert "ENCRYPTION_CHANGED" in guardian.event_handlers
        assert "ROGUE_AP_DETECTED" in guardian.event_handlers
        assert "THREAT_CLEARED" in guardian.event_handlers


class TestGuardianArmorSystem:
    """Tests for Guardian armor/encryption mapping."""

    def test_armor_from_none_encryption(self):
        """Test armor mapping for no encryption."""
        guardian = Guardian()
        armor = guardian._get_armor_from_encryption("None")
        assert armor == Guardian.ARMOR_NONE

    def test_armor_from_wep(self):
        """Test armor mapping for WEP."""
        guardian = Guardian()
        armor = guardian._get_armor_from_encryption("WEP")
        assert armor == Guardian.ARMOR_WEAK

    def test_armor_from_wpa2(self):
        """Test armor mapping for WPA2."""
        guardian = Guardian()

        assert guardian._get_armor_from_encryption("WPA2") == Guardian.ARMOR_STRONG
        assert guardian._get_armor_from_encryption("WPA2-PSK") == Guardian.ARMOR_STRONG

    def test_armor_from_wpa3(self):
        """Test armor mapping for WPA3."""
        guardian = Guardian()

        assert guardian._get_armor_from_encryption("WPA3") == Guardian.ARMOR_MAXIMUM
        assert guardian._get_armor_from_encryption("WPA3-SAE") == Guardian.ARMOR_MAXIMUM

    def test_armor_from_unknown(self):
        """Test armor mapping for unknown encryption defaults to weak."""
        guardian = Guardian()
        armor = guardian._get_armor_from_encryption("UNKNOWN")
        assert armor == Guardian.ARMOR_WEAK


class TestGuardianNetworkStateUpdates:
    """Tests for Guardian reacting to network state changes."""

    def test_update_health_from_signal(self):
        """Test Guardian health updates from signal strength."""
        guardian = Guardian()
        network = NetworkState(
            ssid="TestNet",
            signal_dbm=-50,
            signal_percent=90,
            encryption="WPA2",
        )

        guardian.update_from_network_state(network)
        assert guardian.health == 90.0

    def test_update_armor_from_encryption(self):
        """Test Guardian armor updates from encryption type."""
        guardian = Guardian()

        # Start with no encryption
        network = NetworkState(ssid="Test", encryption="None")
        guardian.update_from_network_state(network)
        assert guardian.armor_type == Guardian.ARMOR_NONE

        # Upgrade to WPA3
        network.encryption = "WPA3"
        guardian.update_from_network_state(network)
        assert guardian.armor_type == Guardian.ARMOR_MAXIMUM


class TestGuardianSignalEvents:
    """Tests for Guardian signal strength event handling."""

    def test_weak_signal_triggers_event(self):
        """Test weak signal triggers SIGNAL_WEAK event."""
        guardian = Guardian()
        guardian.last_signal_dbm = -50  # Start strong

        # Signal drops to weak
        network = NetworkState(signal_dbm=-75, signal_percent=30)
        guardian.update_from_network_state(network)

        # Should have queued dialog about weak signal
        assert len(guardian.dialog_queue) > 0
        assert guardian.mood == CharacterMood.WORRIED

    def test_strong_signal_triggers_event(self):
        """Test strong signal triggers SIGNAL_STRONG event."""
        guardian = Guardian()
        guardian.last_signal_dbm = -75  # Start weak

        # Signal improves to strong
        network = NetworkState(signal_dbm=-45, signal_percent=95)
        guardian.update_from_network_state(network)

        # Should have queued dialog about strong signal
        assert len(guardian.dialog_queue) > 0
        assert guardian.mood == CharacterMood.HAPPY

    def test_signal_threshold_boundaries(self):
        """Test signal event triggers at correct thresholds."""
        guardian = Guardian()

        # -70 dBm is the weak threshold
        network_weak = NetworkState(signal_dbm=-71, signal_percent=40)
        network_ok = NetworkState(signal_dbm=-69, signal_percent=50)

        # Should not trigger when staying in same category
        guardian.last_signal_dbm = -72
        guardian.update_from_network_state(network_weak)
        dialog_count_1 = len(guardian.dialog_queue)

        guardian.last_signal_dbm = -68
        guardian.update_from_network_state(network_ok)
        dialog_count_2 = len(guardian.dialog_queue)

        # Dialog count should be same (no new events)
        assert dialog_count_1 == dialog_count_2


class TestGuardianEncryptionEvents:
    """Tests for Guardian encryption change event handling."""

    def test_no_encryption_event(self):
        """Test Guardian reacts to no encryption."""
        guardian = Guardian()

        # Start with some encryption, then remove it
        network = NetworkState(encryption="WPA2")
        guardian.update_from_network_state(network)

        # Now remove encryption
        network.encryption = "None"
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.WORRIED
        assert len(guardian.dialog_queue) > 0
        # Check for warning in dialog
        assert any("No encryption" in line.text or "no armor" in line.text.lower()
                   for line in guardian.dialog_queue)

    def test_weak_encryption_event(self):
        """Test Guardian reacts to weak encryption (WEP)."""
        guardian = Guardian()

        network = NetworkState(encryption="WEP")
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.WORRIED
        assert len(guardian.dialog_queue) > 0

    def test_strong_encryption_event(self):
        """Test Guardian reacts positively to strong encryption (WPA2)."""
        guardian = Guardian()
        guardian.armor_type = Guardian.ARMOR_NONE  # Start unencrypted

        network = NetworkState(encryption="WPA2")
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.HAPPY
        assert len(guardian.dialog_queue) > 0

    def test_maximum_encryption_event(self):
        """Test Guardian celebrates maximum encryption (WPA3)."""
        guardian = Guardian()
        guardian.armor_type = Guardian.ARMOR_WEAK  # Start with weak

        network = NetworkState(encryption="WPA3")
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.CELEBRATING
        assert len(guardian.dialog_queue) > 0


class TestGuardianRogueAPEvents:
    """Tests for Guardian rogue AP detection events."""

    def test_rogue_ap_detection(self):
        """Test Guardian reacts to rogue AP detection."""
        guardian = Guardian()

        network = NetworkState(rogue_aps_detected=["FakeWiFi"])
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.ALERT
        assert len(guardian.dialog_queue) > 0
        # Check for alert message
        assert any("ALERT" in line.text or "impostor" in line.text.lower()
                   for line in guardian.dialog_queue)

    def test_multiple_rogue_aps(self):
        """Test Guardian reacts to multiple rogue APs."""
        guardian = Guardian()

        network = NetworkState(rogue_aps_detected=["Fake1", "Fake2", "Fake3"])
        guardian.update_from_network_state(network)

        assert guardian.mood == CharacterMood.ALERT
        # Should mention count in dialog
        assert any("3" in line.text for line in guardian.dialog_queue)

    def test_threat_cleared_event(self):
        """Test Guardian can receive threat cleared events."""
        guardian = Guardian()
        guardian.transition_to(CharacterMood.ALERT)

        guardian.process_event("THREAT_CLEARED", {})

        assert guardian.mood == CharacterMood.HAPPY
        assert len(guardian.dialog_queue) > 0


class TestGuardianDialogContent:
    """Tests for Guardian dialog content and educational notes."""

    def test_weak_signal_has_educational_note(self):
        """Test weak signal dialog includes educational content."""
        guardian = Guardian()
        guardian.last_signal_dbm = -50

        network = NetworkState(signal_dbm=-75, signal_percent=30)
        guardian.update_from_network_state(network)

        # Should have educational note
        assert guardian.dialog_queue[0].educational_note is not None
        assert "dBm" in guardian.dialog_queue[0].educational_note.lower() or \
               "router" in guardian.dialog_queue[0].educational_note.lower()

    def test_encryption_change_has_educational_note(self):
        """Test encryption change dialog includes educational content."""
        guardian = Guardian()

        # Start with encryption, then change it to trigger event
        network = NetworkState(encryption="WPA2")
        guardian.update_from_network_state(network)

        # Now change to no encryption
        network.encryption = "None"
        guardian.update_from_network_state(network)

        # Should have educational note
        assert len(guardian.dialog_queue) > 0
        assert guardian.dialog_queue[0].educational_note is not None
        assert len(guardian.dialog_queue[0].educational_note) > 0


class TestGuardianUpdate:
    """Tests for Guardian update loop."""

    def test_on_update_breathing_animation(self):
        """Test Guardian's breathing animation in idle mode."""
        guardian = Guardian()
        guardian.transition_to(CharacterMood.IDLE)

        # Animation timer should advance
        initial_timer = guardian.animation_timer
        guardian.update(0.016)

        assert guardian.animation_timer > initial_timer

    def test_update_processes_base_character_logic(self):
        """Test Guardian update calls base Character update."""
        guardian = Guardian()
        guardian.speak("Test")

        guardian.update(0.016)

        # Dialog should be active
        assert guardian.current_dialog is not None


class TestGuardianIntegration:
    """Integration tests for Guardian with full network state."""

    def test_full_network_state_update(self):
        """Test Guardian handles complete network state update."""
        guardian = Guardian()

        network = NetworkState(
            ssid="HomeNetwork",
            signal_dbm=-60,
            signal_percent=70,
            encryption="WPA2",
            channel=6,
            rogue_aps_detected=[],
        )

        # Should not raise errors
        guardian.update_from_network_state(network)

        assert guardian.health == 70.0
        assert guardian.armor_type == Guardian.ARMOR_STRONG

    def test_degrading_network_conditions(self):
        """Test Guardian reacts to degrading network conditions."""
        guardian = Guardian()

        # Start good
        network = NetworkState(
            signal_dbm=-50,
            signal_percent=90,
            encryption="WPA3",
        )
        guardian.update_from_network_state(network)
        assert guardian.mood == CharacterMood.CELEBRATING

        # Degrade signal
        guardian.last_signal_dbm = -50
        network.signal_dbm = -75
        network.signal_percent = 30
        guardian.update_from_network_state(network)
        assert guardian.mood == CharacterMood.WORRIED

        # Add rogue AP
        network.rogue_aps_detected = ["EvilTwin"]
        guardian.update_from_network_state(network)
        assert guardian.mood == CharacterMood.ALERT
