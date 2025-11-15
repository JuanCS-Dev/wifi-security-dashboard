"""
Unit tests for Threat system (Threat base, Impostor, Eavesdropper).

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import pytest
from src.gamification.characters.threat import Threat, ThreatLevel
from src.gamification.characters.impostor import Impostor
from src.gamification.characters.eavesdropper import Eavesdropper
from src.gamification.characters.base_character import CharacterMood
from src.gamification.state.game_state import NetworkState


# Mock Threat for testing base class
class MockThreat(Threat):
    """Mock threat for testing."""

    def __init__(self):
        super().__init__(
            character_id="mock_threat",
            name="Mock Threat",
            threat_level=ThreatLevel.MEDIUM,
            emoji="🧪"
        )
        self.activated_called = False
        self.detected_called = False
        self.defeated_called = False

    def on_activated(self):
        self.activated_called = True

    def on_detected(self):
        self.detected_called = True

    def on_defeated(self):
        self.defeated_called = True

    def on_update(self, dt: float):
        super().on_update(dt)  # Call base class fade logic


class TestThreatLevel:
    """Tests for ThreatLevel enum."""

    def test_threat_levels_exist(self):
        """Test all threat levels defined."""
        assert ThreatLevel.LOW == "low"
        assert ThreatLevel.MEDIUM == "medium"
        assert ThreatLevel.HIGH == "high"
        assert ThreatLevel.CRITICAL == "critical"


class TestThreatBase:
    """Tests for Threat base class."""

    def test_threat_initialization(self):
        """Test Threat initializes correctly."""
        threat = MockThreat()

        assert threat.character_id == "mock_threat"
        assert threat.name == "Mock Threat"
        assert threat.emoji == "🧪"
        assert threat.threat_level == ThreatLevel.MEDIUM
        assert threat.active is False
        assert threat.detected is False
        assert threat.defeated is False
        assert threat.visibility == 0.0

    def test_threat_activate(self):
        """Test threat activation."""
        threat = MockThreat()
        threat.activate()

        assert threat.active is True
        assert threat.mood == CharacterMood.ALERT
        assert threat.activated_called is True

    def test_threat_detect(self):
        """Test threat detection."""
        threat = MockThreat()
        threat.detect()

        assert threat.detected is True
        assert threat.visibility == 1.0
        assert threat.detected_called is True

    def test_threat_defeat(self):
        """Test threat defeat."""
        threat = MockThreat()
        threat.active = True
        threat.defeat()

        assert threat.defeated is True
        assert threat.active is False
        assert threat.mood == CharacterMood.WORRIED
        assert threat.defeated_called is True

    def test_threat_deactivate(self):
        """Test threat deactivation."""
        threat = MockThreat()
        threat.active = True
        threat.detected = True
        threat.visibility = 1.0

        threat.deactivate()

        assert threat.active is False
        assert threat.detected is False
        assert threat.visibility == 0.0
        assert threat.mood == CharacterMood.IDLE

    def test_threat_visibility_fade_in(self):
        """Test threat visibility fades in when detected."""
        threat = MockThreat()
        threat.active = True
        threat.detected = True
        threat.visibility = 0.0

        threat.update(0.5)  # Call update, not on_update

        assert threat.visibility > 0.0
        assert threat.visibility <= 1.0

    def test_threat_visibility_fade_out(self):
        """Test threat visibility fades out when inactive."""
        threat = MockThreat()
        threat.active = False
        threat.visibility = 1.0

        threat.update(0.5)  # Call update, not on_update

        assert threat.visibility < 1.0
        assert threat.visibility >= 0.0

    def test_get_threat_info(self):
        """Test get_threat_info returns correct data."""
        threat = MockThreat()
        threat.vulnerability_description = "Test vulnerability"
        threat.mitigation_steps = ["Step 1", "Step 2"]

        info = threat.get_threat_info()

        assert info["name"] == "Mock Threat"
        assert info["level"] == ThreatLevel.MEDIUM
        assert info["active"] is False
        assert info["detected"] is False
        assert info["defeated"] is False
        assert info["visibility"] == 0.0
        assert info["vulnerability"] == "Test vulnerability"
        assert info["mitigation"] == ["Step 1", "Step 2"]


class TestImpostor:
    """Tests for Impostor threat."""

    def test_impostor_initialization(self):
        """Test Impostor initializes correctly."""
        impostor = Impostor()

        assert impostor.character_id == "impostor"
        assert impostor.name == "The Impostor"
        assert impostor.emoji == "👻"
        assert impostor.threat_level == ThreatLevel.HIGH
        assert impostor.rogue_ap_count == 0
        assert impostor.fake_ssid == ""
        assert len(impostor.mitigation_steps) == 4

    def test_impostor_activates_on_rogue_ap(self):
        """Test Impostor activates when rogue AP detected."""
        impostor = Impostor()
        network = NetworkState(rogue_aps_detected=["FakeWiFi"])

        impostor.update_from_network_state(network)

        assert impostor.active is True
        assert impostor.rogue_ap_count == 1
        assert impostor.fake_ssid == "FakeWiFi"

    def test_impostor_deactivates_when_clear(self):
        """Test Impostor deactivates when rogue APs cleared."""
        impostor = Impostor()

        # Activate
        network = NetworkState(rogue_aps_detected=["Fake1"])
        impostor.update_from_network_state(network)
        assert impostor.active is True

        # Clear
        network.rogue_aps_detected = []
        impostor.update_from_network_state(network)
        assert impostor.active is False

    def test_impostor_multiple_rogue_aps(self):
        """Test Impostor handles multiple rogue APs."""
        impostor = Impostor()
        network = NetworkState(rogue_aps_detected=["Fake1", "Fake2", "Fake3"])

        impostor.update_from_network_state(network)

        assert impostor.rogue_ap_count == 3
        assert impostor.fake_ssid == "Fake1"  # First one

    def test_impostor_educational_content(self):
        """Test Impostor has educational content."""
        impostor = Impostor()

        assert "Rogue Access Point" in impostor.vulnerability_description or \
               "Evil Twin" in impostor.vulnerability_description
        assert len(impostor.mitigation_steps) == 4
        assert any("SSID" in step for step in impostor.mitigation_steps)


class TestEavesdropper:
    """Tests for Eavesdropper threat."""

    def test_eavesdropper_initialization(self):
        """Test Eavesdropper initializes correctly."""
        eavesdropper = Eavesdropper()

        assert eavesdropper.character_id == "eavesdropper"
        assert eavesdropper.name == "The Eavesdropper"
        assert eavesdropper.emoji == "👁️"
        assert eavesdropper.threat_level == ThreatLevel.MEDIUM
        assert eavesdropper.http_connections_count == 0
        assert eavesdropper.sniffing is False
        assert len(eavesdropper.mitigation_steps) == 4

    def test_eavesdropper_activates_on_weak_encryption(self):
        """Test Eavesdropper activates on weak encryption."""
        eavesdropper = Eavesdropper()

        # Test None encryption
        network = NetworkState(encryption="None")
        eavesdropper.update_from_network_state(network)
        assert eavesdropper.active is True

        # Reset
        eavesdropper.deactivate()

        # Test WEP encryption
        network.encryption = "WEP"
        eavesdropper.update_from_network_state(network)
        assert eavesdropper.active is True

    def test_eavesdropper_deactivates_on_strong_encryption(self):
        """Test Eavesdropper deactivates on strong encryption."""
        eavesdropper = Eavesdropper()

        # Activate with weak
        network = NetworkState(encryption="None")
        eavesdropper.update_from_network_state(network)
        assert eavesdropper.active is True

        # Upgrade to strong
        network.encryption = "WPA2"
        network.mock_mode = False  # No HTTP traffic
        eavesdropper.update_from_network_state(network)
        assert eavesdropper.active is False

    def test_eavesdropper_starts_invisible(self):
        """Test Eavesdropper starts with low visibility."""
        eavesdropper = Eavesdropper()
        network = NetworkState(encryption="None")

        eavesdropper.update_from_network_state(network)

        # Should activate but stay low visibility until detected
        assert eavesdropper.active is True
        assert eavesdropper.visibility < 1.0

    def test_eavesdropper_educational_content(self):
        """Test Eavesdropper has educational content."""
        eavesdropper = Eavesdropper()

        assert "packet" in eavesdropper.vulnerability_description.lower() or \
               "sniff" in eavesdropper.vulnerability_description.lower()
        assert len(eavesdropper.mitigation_steps) == 4
        assert any("HTTPS" in step for step in eavesdropper.mitigation_steps)


class TestThreatIntegration:
    """Integration tests for threat system."""

    def test_impostor_full_lifecycle(self):
        """Test Impostor full activation/detection/defeat cycle."""
        impostor = Impostor()

        # 1. Activate
        network = NetworkState(rogue_aps_detected=["EvilTwin"])
        impostor.update_from_network_state(network)
        assert impostor.active is True

        # 2. Detect
        impostor.detect()
        assert impostor.detected is True
        assert impostor.visibility == 1.0

        # 3. Defeat
        impostor.defeat()
        assert impostor.defeated is True
        assert impostor.active is False

    def test_eavesdropper_full_lifecycle(self):
        """Test Eavesdropper full activation/detection/defeat cycle."""
        eavesdropper = Eavesdropper()

        # 1. Activate
        network = NetworkState(encryption="None")
        eavesdropper.update_from_network_state(network)
        assert eavesdropper.active is True

        # 2. Detect (becomes visible)
        eavesdropper.detect()
        assert eavesdropper.detected is True
        assert eavesdropper.visibility == 1.0

        # 3. Defeat
        eavesdropper.defeat()
        assert eavesdropper.defeated is True
        assert eavesdropper.active is False

    def test_multiple_threats_simultaneously(self):
        """Test multiple threats can be active at once."""
        impostor = Impostor()
        eavesdropper = Eavesdropper()

        network = NetworkState(
            encryption="None",
            rogue_aps_detected=["Fake1"]
        )

        impostor.update_from_network_state(network)
        eavesdropper.update_from_network_state(network)

        assert impostor.active is True
        assert eavesdropper.active is True
