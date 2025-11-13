"""
Tests for ARP Spoofing Detector Dashboard

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import pytest
from src.screens.arp_detector_dashboard import ARPDetectorDashboard
from src.plugins.arp_spoofing_detector import MockARPSpoofingDetector
from src.plugins.base import PluginConfig


class TestARPDetectorDashboard:
    """Test suite for ARP Detector Dashboard."""
    
    def test_dashboard_instantiation(self):
        """Test that dashboard can be instantiated."""
        dashboard = ARPDetectorDashboard()
        assert dashboard is not None
        assert hasattr(dashboard, 'monitoring')
        assert hasattr(dashboard, 'alert_count')
        assert hasattr(dashboard, 'arp_cache_size')
    
    def test_dashboard_bindings(self):
        """Test that dashboard has correct key bindings."""
        dashboard = ARPDetectorDashboard()
        bindings = [b[0] for b in dashboard.BINDINGS]
        
        assert "r" in bindings  # Refresh
        assert "c" in bindings  # Clear alerts
        assert "0" in bindings  # Switch to consolidated
        assert "h" in bindings  # Help
        assert "q" in bindings  # Quit


class TestARPDetectorPlugin:
    """Test suite for ARP Detector Plugin (mock mode)."""
    
    def test_mock_plugin_instantiation(self):
        """Test that mock plugin can be instantiated."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        assert plugin is not None
    
    def test_mock_plugin_initialize(self):
        """Test that mock plugin initializes without errors."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        plugin.initialize()
        # Should not raise exception
    
    def test_mock_plugin_collect_data(self):
        """Test that mock plugin returns valid data structure."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        
        # Validate data structure
        assert isinstance(data, dict)
        assert 'monitoring' in data
        assert 'arp_cache_size' in data
        assert 'alert_count' in data
        assert 'recent_alerts' in data
        assert 'stats' in data
        assert 'trusted_devices' in data
        
        # Validate data types
        assert isinstance(data['monitoring'], bool)
        assert isinstance(data['arp_cache_size'], int)
        assert isinstance(data['alert_count'], int)
        assert isinstance(data['recent_alerts'], list)
        assert isinstance(data['stats'], dict)
        assert isinstance(data['trusted_devices'], list)
    
    def test_mock_plugin_alert_structure(self):
        """Test that mock alerts have correct structure."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        alerts = data['recent_alerts']
        
        assert len(alerts) > 0, "Mock plugin should have at least one alert"
        
        # Validate first alert structure
        alert = alerts[0]
        assert 'ip' in alert
        assert 'old_mac' in alert
        assert 'new_mac' in alert
        assert 'timestamp' in alert
        assert 'severity' in alert
        assert 'description' in alert
        assert 'educational_note' in alert
        
        # Validate severity levels
        assert alert['severity'] in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    
    def test_mock_plugin_stats_structure(self):
        """Test that mock stats have correct structure."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        stats = data['stats']
        
        # Validate stats structure
        assert 'arp_packets' in stats
        assert 'mac_changes' in stats
        assert 'alerts_raised' in stats
        assert 'critical_alerts' in stats
        
        # Validate stats are non-negative
        assert stats['arp_packets'] >= 0
        assert stats['mac_changes'] >= 0
        assert stats['alerts_raised'] >= 0
        assert stats['critical_alerts'] >= 0
    
    def test_mock_plugin_no_root_required(self):
        """Test that mock plugin doesn't require root."""
        config = PluginConfig(
            name="arp_detector",
            rate_ms=1000,
            config={"mock_mode": True}
        )
        plugin = MockARPSpoofingDetector(config)
        
        assert plugin.requires_root() is False
