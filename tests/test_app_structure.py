#!/usr/bin/env python3
"""
Test suite for WiFi Security Education Dashboard - Structural Tests
Tests the application structure, imports, and basic instantiation.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_textual import WiFiSecurityDashboardApp
from src.plugins.base import Plugin, PluginConfig
from src.plugins.system_plugin import SystemPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
from src.plugins.network_topology_plugin import NetworkTopologyPlugin, MockNetworkTopologyPlugin


class TestPluginInstantiation:
    """Test that all plugins can be instantiated."""
    
    def test_system_plugin_real(self):
        """Test SystemPlugin instantiation."""
        config = PluginConfig(
            name="system",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": False}
        )
        plugin = SystemPlugin(config)
        assert plugin is not None
        assert plugin.config.name == "system"
    
    def test_system_plugin_mock(self):
        """Test SystemPlugin in mock mode."""
        config = PluginConfig(
            name="system",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": True}
        )
        plugin = SystemPlugin(config)
        assert plugin is not None
        plugin.initialize()
        data = plugin.collect_data()
        assert "cpu_percent" in data
        assert "memory_percent" in data
    
    def test_wifi_plugin_real(self):
        """Test WiFiPlugin instantiation."""
        config = PluginConfig(
            name="wifi",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": False}
        )
        plugin = WiFiPlugin(config)
        assert plugin is not None
    
    def test_wifi_plugin_mock(self):
        """Test WiFiPlugin in mock mode."""
        config = PluginConfig(
            name="wifi",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": True}
        )
        plugin = WiFiPlugin(config)
        assert plugin is not None
        plugin.initialize()
        data = plugin.collect_data()
        assert "ssid" in data
        assert "signal_strength" in data
    
    def test_network_plugin_real(self):
        """Test NetworkPlugin instantiation."""
        config = PluginConfig(
            name="network",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": False}
        )
        plugin = NetworkPlugin(config)
        assert plugin is not None
    
    def test_network_plugin_mock(self):
        """Test NetworkPlugin in mock mode."""
        config = PluginConfig(
            name="network",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": True}
        )
        plugin = NetworkPlugin(config)
        assert plugin is not None
        plugin.initialize()
        data = plugin.collect_data()
        assert "bytes_sent" in data
        assert "bytes_recv" in data
    
    def test_packet_analyzer_plugin_real(self):
        """Test PacketAnalyzerPlugin instantiation."""
        config = PluginConfig(
            name="packet_analyzer",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": False}
        )
        plugin = PacketAnalyzerPlugin(config)
        assert plugin is not None
    
    def test_packet_analyzer_plugin_mock(self):
        """Test PacketAnalyzerPlugin in mock mode."""
        config = PluginConfig(
            name="packet_analyzer",
            rate_ms=1000,
            enabled=True,
            config={"mock_mode": True}
        )
        plugin = PacketAnalyzerPlugin(config)
        assert plugin is not None
        plugin.initialize()
        data = plugin.collect_data()
        assert "recent_packets" in data
        assert "top_protocols" in data
    
    def test_topology_plugin_mock(self):
        """Test MockNetworkTopologyPlugin instantiation."""
        config = PluginConfig(
            name="topology",
            rate_ms=5000,
            enabled=True,
            config={"mock_mode": True}
        )
        plugin = MockNetworkTopologyPlugin(config)
        assert plugin is not None
        plugin.initialize()
        data = plugin.collect_data()
        assert "devices" in data
        assert len(data["devices"]) > 0


class TestApplicationInstantiation:
    """Test that the main application can be instantiated."""
    
    def test_app_instantiation_mock(self):
        """Test app instantiation in mock mode."""
        app = WiFiSecurityDashboardApp(mock_mode=True)
        assert app is not None
        assert app.mock_mode is True
    
    def test_app_instantiation_real(self):
        """Test app instantiation in real mode."""
        app = WiFiSecurityDashboardApp(mock_mode=False)
        assert app is not None
        assert app.mock_mode is False


class TestPluginDataCollection:
    """Test that plugins can collect data."""
    
    def test_mock_system_data_structure(self):
        """Test mock system plugin data structure."""
        config = PluginConfig(name="system", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = SystemPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert "cpu_percent" in data
        assert "memory_percent" in data
        assert "disk_percent" in data
        assert isinstance(data["cpu_percent"], (int, float))
        assert 0 <= data["cpu_percent"] <= 100
        assert 0 <= data["memory_percent"] <= 100
    
    def test_mock_wifi_data_structure(self):
        """Test mock wifi plugin data structure."""
        config = PluginConfig(name="wifi", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = WiFiPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert "ssid" in data
        assert "signal_strength" in data
        assert "frequency" in data
        assert isinstance(data["signal_strength"], (int, float))
        assert -100 <= data["signal_strength"] <= 0
    
    def test_mock_network_data_structure(self):
        """Test mock network plugin data structure."""
        config = PluginConfig(name="network", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = NetworkPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert "bytes_sent" in data
        assert "bytes_recv" in data
        assert "packets_sent" in data
        assert "packets_recv" in data
        assert isinstance(data["bytes_sent"], int)
        assert data["bytes_sent"] >= 0
    
    def test_mock_packet_data_structure(self):
        """Test mock packet analyzer plugin data structure."""
        config = PluginConfig(name="packet_analyzer", rate_ms=1000, enabled=True, config={"mock_mode": True})
        plugin = PacketAnalyzerPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert "recent_packets" in data
        assert "top_protocols" in data
        assert isinstance(data["recent_packets"], list)
        assert isinstance(data["top_protocols"], dict)
    
    def test_mock_topology_data_structure(self):
        """Test mock topology plugin data structure."""
        config = PluginConfig(name="topology", rate_ms=5000, enabled=True, config={"mock_mode": True})
        plugin = MockNetworkTopologyPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert "devices" in data
        assert isinstance(data["devices"], list)
        assert len(data["devices"]) > 0
        
        # Check device structure
        device = data["devices"][0]
        assert "ip" in device
        assert "mac" in device
        assert "hostname" in device
        assert "vendor" in device


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
