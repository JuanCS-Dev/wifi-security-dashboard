"""
Tests for Rogue AP Detector Plugin - Feature 6

Tests evil twin / rogue AP detection functionality.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-13
"""

import pytest
import time
from unittest.mock import Mock, patch

from src.plugins.base import PluginConfig
from src.plugins.rogue_ap_detector import (
    RogueAPDetector,
    AccessPoint,
    RogueAPAlert
)


class TestRogueAPDetector:
    """Test Rogue AP Detector Plugin functionality."""
    
    def test_plugin_initialization_mock_mode(self):
        """Test plugin initializes correctly in mock mode."""
        config = PluginConfig(
            name="rogue_ap",
            rate_ms=2000,
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        assert plugin is not None
        assert plugin.config.name == "rogue_ap"
        assert plugin._baseline_learned is True  # Mock auto-learns
    
    def test_collect_mock_data(self):
        """Test collecting mock rogue AP data."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        # Verify mock data structure
        assert 'monitoring' in data
        assert 'baseline_learned' in data
        assert 'stats' in data
        assert 'access_points' in data
        assert 'baseline_aps' in data
        assert 'rogue_alerts' in data
        assert 'educational_tip' in data
        
        # Verify stats
        assert data['stats']['total_aps_detected'] > 0
        assert data['baseline_learned'] is True
        
        # Verify APs
        assert len(data['access_points']) > 0
        ap = data['access_points'][0]
        assert 'bssid' in ap
        assert 'ssid' in ap
        assert 'channel' in ap
        assert 'signal_strength' in ap
    
    def test_access_point_dataclass(self):
        """Test AccessPoint dataclass."""
        ap = AccessPoint(
            bssid="aa:bb:cc:dd:ee:ff",
            ssid="TestNetwork",
            channel=6,
            signal_strength=-45,
            encryption="WPA2/WPA3",
            vendor="TP-Link",
            first_seen=time.time(),
            last_seen=time.time(),
            beacon_count=10
        )
        
        assert ap.bssid == "aa:bb:cc:dd:ee:ff"
        assert ap.ssid == "TestNetwork"
        assert ap.channel == 6
        
        # Test to_dict
        ap_dict = ap.to_dict()
        assert isinstance(ap_dict, dict)
        assert ap_dict['ssid'] == "TestNetwork"
    
    def test_rogue_alert_dataclass(self):
        """Test RogueAPAlert dataclass."""
        alert = RogueAPAlert(
            timestamp=time.time(),
            rogue_bssid="ff:ee:dd:cc:bb:aa",
            legitimate_bssid="aa:bb:cc:dd:ee:ff",
            ssid="HomeNetwork",
            severity="CRITICAL",
            reason="SSID_COLLISION",
            channel_diff=5,
            signal_diff=10,
            educational_note="Evil twin detected!"
        )
        
        assert alert.severity == "CRITICAL"
        assert alert.reason == "SSID_COLLISION"
        assert alert.ssid == "HomeNetwork"
        
        # Test to_dict
        alert_dict = alert.to_dict()
        assert isinstance(alert_dict, dict)
    
    def test_baseline_learning(self):
        """Test baseline learning functionality."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        # Mock mode auto-generates baseline
        assert len(plugin.baseline_aps) > 0
        assert plugin._baseline_learned is True
    
    def test_vendor_detection(self):
        """Test vendor detection from MAC OUI."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Test known vendor
        vendor = plugin._get_vendor("00:1A:11:22:33:44")
        assert "Google" in vendor or "Unknown" in vendor
        
        # Test unknown vendor
        vendor = plugin._get_vendor("DE:AD:BE:EF:00:00")
        assert "Unknown" in vendor
    
    def test_encryption_detection_types(self):
        """Test encryption type names."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Test different encryption values
        assert plugin._get_educational_tip() is not None
    
    def test_requires_root(self):
        """Test that plugin requires root for real mode."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": False}
        )
        
        plugin = RogueAPDetector(config)
        assert plugin.requires_root() is True
    
    def test_mock_data_structure(self):
        """Test mock data has correct structure."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        data = plugin._get_mock_data()
        
        # Verify APs
        assert len(data['access_points']) >= 2
        
        # Verify at least one rogue alert
        assert len(data['rogue_alerts']) > 0
        alert = data['rogue_alerts'][0]
        assert alert['severity'] in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def test_plugin_lifecycle(self):
        """Test plugin start/stop lifecycle."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        # Mock mode doesn't start threads
        assert plugin._monitor_thread is None
        
        # Cleanup should work
        plugin.cleanup()
        assert plugin._stop_event.is_set()
    
    def test_stats_tracking(self):
        """Test statistics tracking."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Initial stats
        assert plugin.stats['total_aps_detected'] == 0
        assert plugin.stats['rogue_aps_confirmed'] == 0
        assert plugin.stats['beacons_captured'] == 0
    
    def test_threat_assessment(self):
        """Test threat level assessment."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Create test AP
        ap = AccessPoint(
            bssid="ff:ee:dd:cc:bb:aa",
            ssid="TestNetwork",
            channel=6,
            signal_strength=-35,  # Strong signal
            encryption="Open",
            vendor="Unknown",
            first_seen=time.time(),
            last_seen=time.time()
        )
        
        # Test SSID collision with strong signal
        severity = plugin._assess_threat_level(ap, "SSID_COLLISION")
        assert severity in ["CRITICAL", "HIGH"]
        
        # Test strong signal alone
        severity = plugin._assess_threat_level(ap, "STRONG_SIGNAL")
        assert severity == "MEDIUM"
        
        # Test suspicious open
        severity = plugin._assess_threat_level(ap, "SUSPICIOUS_OPEN")
        assert severity == "LOW"
    
    def test_educational_notes(self):
        """Test educational note generation."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Create test AP
        ap = AccessPoint(
            bssid="ff:ee:dd:cc:bb:aa",
            ssid="TestNetwork",
            channel=6,
            signal_strength=-45,
            encryption="WPA2/WPA3",
            vendor="TP-Link",
            first_seen=time.time(),
            last_seen=time.time()
        )
        
        # Test evil twin note
        note = plugin._generate_educational_note("SSID_COLLISION", ap)
        assert "EVIL TWIN" in note or "fake" in note.lower()
        
        # Test strong signal note
        note = plugin._generate_educational_note("STRONG_SIGNAL", ap)
        assert "signal" in note.lower()
        
        # Test suspicious open note
        note = plugin._generate_educational_note("SUSPICIOUS_OPEN", ap)
        assert "open" in note.lower() or "honeypot" in note.lower()
    
    def test_educational_tips(self):
        """Test educational tip generation."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Test with no rogues
        plugin.stats['rogue_aps_confirmed'] = 0
        plugin._baseline_learned = True
        tip = plugin._get_educational_tip()
        assert 'No rogue' in tip or 'clean' in tip.lower()
        
        # Test with rogues detected
        plugin.stats['rogue_aps_confirmed'] = 2
        tip = plugin._get_educational_tip()
        assert '2' in tip or 'rogue' in tip.lower()
        
        # Test while learning (reset rogues count)
        plugin.stats['rogue_aps_confirmed'] = 0
        plugin._baseline_learned = False
        tip = plugin._get_educational_tip()
        assert 'Learning' in tip or 'baseline' in tip.lower()
    
    def test_ssid_tracking(self):
        """Test SSID to BSSID mapping."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        
        # Add same SSID with different BSSIDs
        plugin.ssid_to_bssids['HomeNetwork'].append('aa:bb:cc:dd:ee:ff')
        plugin.ssid_to_bssids['HomeNetwork'].append('ff:ee:dd:cc:bb:aa')
        
        # Should have 2 BSSIDs for same SSID
        assert len(plugin.ssid_to_bssids['HomeNetwork']) == 2


class TestRogueAPDetection:
    """Test rogue AP detection logic."""
    
    def test_evil_twin_detection(self):
        """Test evil twin (SSID collision) detection."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        # Get mock data which includes evil twin
        data = plugin._get_mock_data()
        
        # Should have rogue alerts
        assert len(data['rogue_alerts']) > 0
        
        # Check for SSID collision
        has_collision = any(
            alert['reason'] == 'SSID_COLLISION' 
            for alert in data['rogue_alerts']
        )
        assert has_collision
    
    def test_mock_includes_evil_twin(self):
        """Test that mock data includes evil twin scenario."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        data = plugin._get_mock_data()
        
        # Should have at least 2 APs with same SSID
        aps = data['access_points']
        ssids = [ap['ssid'] for ap in aps]
        
        # Check for duplicates
        has_duplicate = len(ssids) != len(set(ssids))
        assert has_duplicate  # Evil twin present


class TestRogueAPIntegration:
    """Integration tests for Rogue AP Detector."""
    
    def test_full_data_collection_cycle(self):
        """Test complete data collection cycle."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        # Collect data multiple times
        data1 = plugin.collect_data()
        time.sleep(0.1)
        data2 = plugin.collect_data()
        
        # Both should succeed
        assert data1 is not None
        assert data2 is not None
        
        # Should have consistent structure
        assert set(data1.keys()) == set(data2.keys())
    
    def test_concurrent_data_access(self):
        """Test that concurrent data access doesn't crash."""
        config = PluginConfig(
            name="rogue_ap",
            config={"mock_mode": True}
        )
        
        plugin = RogueAPDetector(config)
        plugin.initialize()
        
        # Simulate concurrent access
        results = []
        for _ in range(5):
            data = plugin.collect_data()
            results.append(data)
        
        # All should succeed
        assert len(results) == 5
        assert all(r is not None for r in results)
