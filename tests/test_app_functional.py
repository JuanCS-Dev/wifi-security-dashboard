#!/usr/bin/env python3
"""
Functional tests for WiFi Security Education Dashboard.
Tests the application in realistic scenarios, both mock and real modes.

These are REAL tests - no lies, no ego-massaging. We test what matters.
"""

import pytest
import sys
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_textual import WiFiSecurityDashboardApp
from src.plugins.base import PluginConfig
from src.plugins.system_plugin import SystemPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin


class TestMockModeOperation:
    """Test the application running in mock mode - this should ALWAYS work."""
    
    def test_app_runs_in_mock_mode(self):
        """Test that app can start and initialize in mock mode."""
        app = WiFiSecurityDashboardApp(mock_mode=True)
        assert app is not None
        assert app.mock_mode is True
        
    def test_mock_plugins_collect_valid_data(self):
        """Test that all mock plugins return valid, realistic data."""
        # System plugin
        sys_config = PluginConfig(name="system", rate_ms=1000, enabled=True, config={"mock_mode": True})
        sys_plugin = SystemPlugin(sys_config)
        sys_plugin.initialize()
        sys_data = sys_plugin.collect_data()
        
        # Validate system data
        assert 0 <= sys_data["cpu_percent"] <= 100
        assert 0 <= sys_data["memory_percent"] <= 100
        assert 0 <= sys_data["disk_percent"] <= 100
        assert sys_data["cpu_count"] > 0
        assert sys_data["memory_total_mb"] > 0
        
        # WiFi plugin
        wifi_config = PluginConfig(name="wifi", rate_ms=1000, enabled=True, config={"mock_mode": True})
        wifi_plugin = WiFiPlugin(wifi_config)
        wifi_plugin.initialize()
        wifi_data = wifi_plugin.collect_data()
        
        # Validate WiFi data
        assert "ssid" in wifi_data
        assert -100 <= wifi_data["signal_strength"] <= 0
        assert wifi_data["frequency"] in [2.4, 5.0]
        assert wifi_data["security"] in ["WPA2", "WPA3", "Open", "WPA2-PSK"]
        
        # Network plugin
        net_config = PluginConfig(name="network", rate_ms=1000, enabled=True, config={"mock_mode": True})
        net_plugin = NetworkPlugin(net_config)
        net_plugin.initialize()
        net_data = net_plugin.collect_data()
        
        # Validate network data
        assert net_data["bytes_sent"] >= 0
        assert net_data["bytes_recv"] >= 0
        assert net_data["packets_sent"] >= 0
        assert net_data["packets_recv"] >= 0
        
        # Packet analyzer plugin
        pkt_config = PluginConfig(name="packets", rate_ms=1000, enabled=True, config={"mock_mode": True})
        pkt_plugin = PacketAnalyzerPlugin(pkt_config)
        pkt_plugin.initialize()
        pkt_data = pkt_plugin.collect_data()
        
        # Validate packet data
        assert isinstance(pkt_data["recent_packets"], list)
        assert len(pkt_data["recent_packets"]) > 0
        assert isinstance(pkt_data["top_protocols"], dict)
        assert pkt_data["total_packets"] > 0
        assert pkt_data["packet_rate"] >= 0
        
    def test_mock_data_consistency_over_time(self):
        """Test that mock data evolves consistently over multiple collections."""
        config = PluginConfig(name="system", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = SystemPlugin(config)
        plugin.initialize()
        
        # Collect data 3 times
        data1 = plugin.collect_data()
        data2 = plugin.collect_data()
        data3 = plugin.collect_data()
        
        # Data should be different (simulating change over time)
        assert data1["cpu_percent"] != data2["cpu_percent"] or data2["cpu_percent"] != data3["cpu_percent"]
        
        # But structure should remain consistent
        assert set(data1.keys()) == set(data2.keys()) == set(data3.keys())


class TestPluginIntegration:
    """Test plugin lifecycle and integration."""
    
    def test_plugin_lifecycle_mock(self):
        """Test complete plugin lifecycle in mock mode."""
        config = PluginConfig(name="test", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = SystemPlugin(config)
        
        # Before initialize - plugin should be uninitialized
        # (we don't check status directly as it's not part of public API)
        
        # Initialize
        plugin.initialize()
        
        # Collect data - should work
        data = plugin.collect_data()
        assert data is not None
        assert isinstance(data, dict)
        
    def test_plugin_disabled_state(self):
        """Test that disabled plugins can be created but not used."""
        config = PluginConfig(name="disabled", rate_ms=1000, enabled=False, config={"mock_mode": True})
        plugin = SystemPlugin(config)
        
        assert plugin.config.enabled is False
        # Plugin should still be instantiable even if disabled


class TestDataRealism:
    """Test that generated data looks realistic - the TRUTH matters."""
    
    def test_cpu_data_realistic(self):
        """Test CPU data looks like real system metrics."""
        config = PluginConfig(name="system", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = SystemPlugin(config)
        plugin.initialize()
        
        # Collect multiple samples
        samples = [plugin.collect_data() for _ in range(10)]
        
        # All samples should have valid CPU percentages
        for sample in samples:
            assert 0 <= sample["cpu_percent"] <= 100
            assert sample["cpu_count"] in [2, 4, 6, 8, 10, 12, 16]  # Common CPU counts
            
        # CPU should vary (not static)
        cpu_values = [s["cpu_percent"] for s in samples]
        assert len(set(cpu_values)) > 1  # Should have variety
        
    def test_wifi_signal_realistic(self):
        """Test WiFi signal strength looks realistic."""
        config = PluginConfig(name="wifi", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = WiFiPlugin(config)
        plugin.initialize()
        
        # Collect multiple samples
        samples = [plugin.collect_data() for _ in range(10)]
        
        # All samples should have realistic signal strength
        for sample in samples:
            # WiFi signal is negative dBm, typically -30 to -90
            assert -100 <= sample["signal_strength"] <= 0
            
        # Signal should vary (simulating fluctuation)
        signal_values = [s["signal_strength"] for s in samples]
        assert len(set(signal_values)) > 1
        
    def test_network_bandwidth_realistic(self):
        """Test network bandwidth changes look realistic."""
        config = PluginConfig(name="network", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = NetworkPlugin(config)
        plugin.initialize()
        
        # Collect samples
        samples = [plugin.collect_data() for _ in range(5)]
        
        # Bytes should be monotonically increasing (counters)
        for i in range(1, len(samples)):
            assert samples[i]["bytes_sent"] >= samples[i-1]["bytes_sent"]
            assert samples[i]["bytes_recv"] >= samples[i-1]["bytes_recv"]
            
    def test_packet_data_educational_value(self):
        """Test packet data is educationally valuable - shows security concepts."""
        config = PluginConfig(name="packets", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = PacketAnalyzerPlugin(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        
        # Should show mix of protocols
        protocols = data["top_protocols"]
        assert "HTTPS" in protocols  # Secure
        assert "HTTP" in protocols   # Insecure - educational!
        
        # Should have recent packets with educational info
        packets = data["recent_packets"]
        assert len(packets) > 0
        
        # At least one packet should be marked safe, one unsafe
        safe_flags = [p.get("safe", True) for p in packets]
        assert True in safe_flags   # Some safe traffic
        assert False in safe_flags  # Some unsafe traffic (educational!)


class TestErrorHandling:
    """Test that errors are handled gracefully."""
    
    def test_invalid_plugin_config(self):
        """Test that invalid configuration is rejected."""
        with pytest.raises(ValueError):
            # Empty name should raise error
            config = PluginConfig(name="", rate_ms=1000)
            
    def test_negative_rate(self):
        """Test that negative update rate is rejected."""
        with pytest.raises(ValueError):
            config = PluginConfig(name="test", rate_ms=-100)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
