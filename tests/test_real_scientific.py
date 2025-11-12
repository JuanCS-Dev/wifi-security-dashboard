"""
SCIENTIFIC TEST SUITE - NO BULLSHIT, ONLY TRUTH
Tests real behavior, not fantasy scenarios.

Author: Professor JuanCS-Dev (Boris Mode Activated) ✝️
Date: 2025-11-12
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.plugins.base import PluginConfig
from src.plugins.system_plugin import SystemPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
from src.plugins.network_topology_plugin import NetworkTopologyPlugin


class TestRealModePlugins:
    """Test plugins in REAL mode - scientific verification"""
    
    def test_system_plugin_requires_psutil(self):
        """System plugin MUST have psutil in real mode"""
        config = PluginConfig(name='system', rate_ms=1000, config={'mock_mode': False})
        plugin = SystemPlugin(config)
        
        try:
            plugin.initialize()
            # If successful, psutil must be available
            assert hasattr(plugin, 'psutil'), "Real mode must have psutil"
            assert plugin._mock_mode is False, "Should NOT be in mock mode"
        except RuntimeError as e:
            # Expected if psutil not installed
            assert "psutil" in str(e).lower(), f"Wrong error: {e}"
            pytest.skip("psutil not installed (expected in real environment)")
    
    def test_system_plugin_collects_real_data(self):
        """System plugin must return REAL system data"""
        config = PluginConfig(name='system', rate_ms=1000, config={'mock_mode': False})
        plugin = SystemPlugin(config)
        
        try:
            plugin.initialize()
        except RuntimeError:
            pytest.skip("psutil not available")
        
        data = plugin.collect_data()
        
        # Verify data is REAL (not mock constants)
        assert isinstance(data['cpu_percent'], (int, float)), "CPU must be numeric"
        assert 0 <= data['cpu_percent'] <= 100, "CPU must be 0-100%"
        assert isinstance(data['memory_used_mb'], (int, float)), "Memory must be numeric"
        assert data['memory_used_mb'] > 0, "Memory usage must be > 0"
        assert data['memory_total_mb'] > 0, "Total memory must be > 0"
        
        # Verify data changes over time (real data fluctuates)
        data2 = plugin.collect_data()
        # At least ONE metric should differ (system is never static)
        assert data != data2 or data['cpu_percent'] == 0, "Real system data should vary"
    
    def test_network_plugin_requires_psutil(self):
        """Network plugin MUST have psutil in real mode"""
        config = PluginConfig(name='network', rate_ms=1000, config={'mock_mode': False})
        plugin = NetworkPlugin(config)
        
        try:
            plugin.initialize()
            assert hasattr(plugin, 'psutil'), "Real mode must have psutil"
            assert plugin._mock_mode is False
        except RuntimeError as e:
            assert "psutil" in str(e).lower()
            pytest.skip("psutil not installed")
    
    def test_wifi_plugin_graceful_degradation(self):
        """WiFi plugin must handle no hardware gracefully"""
        config = PluginConfig(name='wifi', rate_ms=1000, config={'mock_mode': False})
        plugin = WiFiPlugin(config)
        
        plugin.initialize()
        data = plugin.collect_data()
        
        # Either has WiFi or reports unavailable
        if 'available' in data and not data['available']:
            assert 'status' in data
            assert data['status'] in ['unavailable', 'error']
        else:
            # Has WiFi - validate data
            assert 'signal_strength_dbm' in data or 'signal_strength_percent' in data
    
    def test_packet_analyzer_fails_without_backend(self):
        """Packet analyzer must FAIL HARD without Scapy/PyShark (no silent mock)"""
        config = PluginConfig(name='packet', rate_ms=1000, config={'mock_mode': False})
        plugin = PacketAnalyzerPlugin(config)
        
        plugin.initialize()
        
        # Check backend status
        if plugin._backend == 'unavailable':
            # GOOD - honest failure
            assert hasattr(plugin, '_unavailable_reason')
            assert plugin._unavailable_reason == 'no_backend'
            
            # Verify it returns unavailable status (not fake data)
            data = plugin.collect_data()
            assert 'available' in data
            assert data['available'] is False
        else:
            # Has real backend - verify it's actually real
            assert plugin._backend in ['scapy', 'pyshark']
            assert plugin._mock_mode is False, "Should NOT silently fall back to mock!"
    
    def test_network_topology_requires_scapy(self):
        """Network topology requires Scapy for real scanning"""
        config = PluginConfig(name='topology', rate_ms=1000, config={'mock_mode': False})
        plugin = NetworkTopologyPlugin(config)
        
        plugin.initialize()
        
        # Should either have Scapy or do nothing
        # (No silent mock fallback allowed!)
        data = plugin.get_data()
        
        # Verify structure
        assert 'device_count' in data
        assert 'devices' in data
        assert isinstance(data['devices'], list)


class TestMockModePlugins:
    """Test plugins in MOCK mode - educational data"""
    
    def test_all_plugins_work_in_mock_mode(self):
        """All plugins MUST work in mock mode (no dependencies)"""
        mock_config = {'mock_mode': True}
        
        plugins = [
            SystemPlugin(PluginConfig(name='system', rate_ms=1000, config=mock_config)),
            NetworkPlugin(PluginConfig(name='network', rate_ms=1000, config=mock_config)),
            WiFiPlugin(PluginConfig(name='wifi', rate_ms=1000, config=mock_config)),
            PacketAnalyzerPlugin(PluginConfig(name='packet', rate_ms=1000, config=mock_config)),
        ]
        
        for plugin in plugins:
            plugin.initialize()
            assert plugin._mock_mode is True, f"{plugin.__class__.__name__} not in mock mode"
            
            data = plugin.collect_data()
            assert data is not None
            assert len(data) > 0
    
    def test_mock_data_is_educational(self):
        """Mock data should be realistic and educational"""
        config = PluginConfig(name='packet', rate_ms=1000, config={'mock_mode': True})
        plugin = PacketAnalyzerPlugin(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        
        # Educational packet data
        assert 'top_protocols' in data
        assert 'HTTPS' in data['top_protocols'], "Educational: HTTPS should be present"
        assert 'HTTP' in data['top_protocols'], "Educational: HTTP for teaching unsafe traffic"


class TestTruth:
    """Verify we're not lying to the user"""
    
    def test_real_mode_doesnt_silently_mock(self):
        """CRITICAL: Real mode must NEVER silently fall back to mock"""
        config = PluginConfig(name='packet', rate_ms=1000, config={'mock_mode': False})
        plugin = PacketAnalyzerPlugin(config)
        plugin.initialize()
        
        # If backend is mock, mock_mode must be True
        if plugin._backend == 'mock':
            assert plugin._mock_mode is True, "LYING: Real mode silently using mock!"
        
        # If mock_mode is True, user must have requested it
        if plugin._mock_mode:
            assert config.config.get('mock_mode') is True, "LYING: Mock mode activated without request!"
    
    def test_unavailable_means_unavailable(self):
        """If plugin says unavailable, it must NOT return fake data"""
        config = PluginConfig(name='wifi', rate_ms=1000, config={'mock_mode': False})
        plugin = WiFiPlugin(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        
        if 'available' in data and data['available'] is False:
            # Should NOT have full WiFi data
            assert 'signal_strength_dbm' not in data or data.get('signal_strength_dbm') is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
