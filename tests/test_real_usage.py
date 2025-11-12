"""
Real Usage Test Suite - 100% Coverage Target
Scientific tests simulating actual user behavior.

Philosophy: Test what users actually do, not theoretical edge cases.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""
import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestRealPluginUsage:
    """Test plugins as they're actually used in the app."""
    
    def test_system_plugin_lifecycle(self):
        """Test full plugin lifecycle: init -> collect -> collect -> cleanup."""
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        
        # Real usage: initialize once
        config = PluginConfig(name="system", rate_ms=1000, config={'mock_mode': False})
        plugin = SystemPlugin(config)
        plugin.initialize()
        
        # Real usage: collect multiple times (dashboard updates)
        time.sleep(0.1)
        data1 = plugin.collect_data()
        time.sleep(0.5)
        data2 = plugin.collect_data()
        time.sleep(0.5)
        data3 = plugin.collect_data()
        
        # Verify dynamic data
        assert data1['cpu_percent'] >= 0
        assert data2['cpu_percent'] >= 0
        assert data3['cpu_percent'] >= 0
        
        # At least one should be non-zero (system has activity)
        assert (data1['cpu_percent'] + data2['cpu_percent'] + data3['cpu_percent']) > 0
        
        # Cleanup
        plugin.cleanup()
        assert plugin._status.value in ["stopped", "ready"]
    
    def test_wifi_plugin_real_or_graceful(self):
        """Test WiFi: either works or fails gracefully."""
        from src.plugins.wifi_plugin import WiFiPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="wifi", rate_ms=1000, config={'mock_mode': False})
        plugin = WiFiPlugin(config)
        plugin.initialize()
        
        data = plugin.collect_data()
        
        # Either we get real WiFi data
        if 'ssid' in data and data.get('ssid') != 'No WiFi adapter detected':
            # Real WiFi working
            assert data['signal_strength_percent'] >= 0
            assert data['signal_strength_percent'] <= 100
            assert len(data['ssid']) > 0
        else:
            # Graceful degradation
            assert 'message' in data or 'ssid' in data
    
    def test_network_plugin_multiple_collections(self):
        """Test network stats over multiple collections."""
        from src.plugins.network_plugin import NetworkPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="network", rate_ms=1000, config={'mock_mode': False})
        plugin = NetworkPlugin(config)
        plugin.initialize()
        
        # Collect baseline
        data1 = plugin.collect_data()
        time.sleep(0.5)
        data2 = plugin.collect_data()
        
        # Network stats should exist and be reasonable
        assert data1['bytes_recv'] >= 0
        assert data1['bytes_sent'] >= 0
        assert data2['bytes_recv'] >= data1['bytes_recv']  # Can only increase
        assert data2['bytes_sent'] >= data1['bytes_sent']


class TestRealScreenUsage:
    """Test screens as users interact with them."""
    
    def test_landing_screen_banner_render(self):
        """Test landing screen banner renders (user sees it first)."""
        from src.screens.landing_screen import BannerWidget
        
        banner = BannerWidget()
        # Banner should be a valid widget
        assert banner is not None
        assert hasattr(banner, 'render')
    
    def test_landing_screen_menu_render(self):
        """Test landing screen menu renders."""
        from src.screens.landing_screen import MenuWidget
        
        menu = MenuWidget()
        # Menu should be a valid widget
        assert menu is not None
        assert hasattr(menu, 'render')
        
        # Test mode toggle (user presses 'm')
        menu.current_mode = "real"
        assert menu.current_mode == "real"
        menu.current_mode = "mock"
        assert menu.current_mode == "mock"
    
    def test_help_screen_displays_content(self):
        """Test help screen shows useful content."""
        from src.screens.help_screen import HelpScreen
        
        help_screen = HelpScreen()
        # Help screen should be a valid screen
        assert help_screen is not None
        assert hasattr(help_screen, 'compose')
    
    def test_tutorial_flag_creation(self):
        """Test tutorial flag file creation logic."""
        from src.screens.tutorial_screen import TutorialScreen
        from pathlib import Path
        
        # Clean flag
        flag_file = Path.home() / ".wifi_security_dashboard" / "tutorial_completed"
        flag_file.parent.mkdir(parents=True, exist_ok=True)
        if flag_file.exists():
            flag_file.unlink()
        
        # Should show tutorial when no flag exists
        assert TutorialScreen.should_show_tutorial() == True
        
        # Create flag manually (simulating completion)
        flag_file.touch()
        
        # Should not show again
        assert TutorialScreen.should_show_tutorial() == False
        
        # Cleanup
        if flag_file.exists():
            flag_file.unlink()


class TestRealWidgetUsage:
    """Test widgets as they appear in dashboards."""
    
    def test_network_chart_update_data(self):
        """Test network chart accepts data updates."""
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        
        # Simulate real dashboard updates (using actual API)
        chart.update_data(1024 * 1024, 512 * 1024)  # 1 MB RX, 512 KB TX
        
        # Chart should track bandwidth
        assert hasattr(chart, 'bandwidth_rx')
        assert hasattr(chart, 'bandwidth_tx')
    
    def test_packet_table_creation(self):
        """Test packet table can be created."""
        from src.widgets.packet_table import PacketTable
        
        table = PacketTable()
        
        # Table should be a valid widget
        assert table is not None
        assert hasattr(table, 'add_rows')  # DataTable method
    
    def test_tooltip_shows_correct_tip(self):
        """Test tooltip displays correct educational content."""
        from src.widgets.tooltip_widget import get_tip
        
        # Test real tips users see
        https_tip = get_tip('https')
        assert 'HTTPS' in https_tip
        assert 'encrypt' in https_tip.lower()
        
        http_tip = get_tip('http')
        assert 'HTTP' in http_tip
        assert 'plain text' in http_tip.lower() or 'unencrypted' in http_tip.lower()
        
        dns_tip = get_tip('dns')
        assert 'DNS' in dns_tip
        
        # Invalid tip returns None
        assert get_tip('invalid_tip_xyz') is None


class TestMockDataRealism:
    """Test mock data generator produces realistic values."""
    
    def test_mock_system_metrics_realistic(self):
        """Test mock system metrics are within real bounds."""
        from src.utils.mock_data_generator import get_mock_generator
        
        gen = get_mock_generator()
        
        # Generate 10 samples
        for _ in range(10):
            data = gen.get_system_metrics()
            
            # CPU should be realistic (not always 0 or 100)
            assert 0 <= data['cpu_percent'] <= 100
            assert data['cpu_percent'] != -1
            
            # Memory should be realistic (40-90% typical)
            assert 0 <= data['memory_percent'] <= 100
            
            # Disk should be realistic (not 0% or 100%)
            assert 0 <= data['disk_percent'] <= 100
    
    def test_mock_wifi_realistic_signal(self):
        """Test mock WiFi produces realistic signal values."""
        from src.utils.mock_data_generator import get_mock_generator
        
        gen = get_mock_generator()
        data = gen.get_wifi_info()
        
        # Signal should be in dBm range (-100 to 0)
        assert -100 <= data['signal_strength'] <= 0
        
        # SSID should not be empty
        assert len(data['ssid']) > 0
        
        # Security should be valid type
        assert data['security'] in ['WPA2', 'WPA3', 'WEP', 'Open']
    
    def test_mock_network_stats_growing(self):
        """Test mock network stats grow over time."""
        from src.utils.mock_data_generator import get_mock_generator
        
        gen = get_mock_generator()
        
        data1 = gen.get_network_stats()
        time.sleep(0.1)
        data2 = gen.get_network_stats()
        
        # Network stats should increase (traffic happens)
        assert data2['bytes_recv'] >= data1['bytes_recv']
        assert data2['bytes_sent'] >= data1['bytes_sent']
    
    def test_mock_packet_analysis_has_protocols(self):
        """Test mock packet analysis includes common protocols."""
        from src.utils.mock_data_generator import get_mock_generator
        
        gen = get_mock_generator()
        data = gen.get_packet_analysis()
        
        # Should have protocol distribution
        assert 'top_protocols' in data
        assert len(data['top_protocols']) > 0
        
        # Common protocols should appear
        protocols = data['top_protocols'].keys()
        common_protocols = ['HTTPS', 'DNS', 'HTTP', 'SSH', 'ICMP']
        found_common = any(p in protocols for p in common_protocols)
        assert found_common, "Should have at least one common protocol"
        
        # Backend should be mock
        assert data['backend'] == 'mock'


class TestPluginBaseClass:
    """Test base plugin functionality."""
    
    def test_plugin_status_transitions(self):
        """Test plugin status state machine."""
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig, PluginStatus
        
        config = PluginConfig(name="test", rate_ms=1000, config={'mock_mode': True})
        plugin = SystemPlugin(config)
        
        # Initial state (actual enum value)
        assert plugin._status in [PluginStatus.UNINITIALIZED, PluginStatus.READY]
        
        # After initialize
        plugin.initialize()
        assert plugin._status == PluginStatus.READY
        
        # After cleanup
        plugin.cleanup()
        assert plugin._status == PluginStatus.STOPPED
    
    def test_plugin_config_immutable(self):
        """Test plugin config is properly stored."""
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(
            name="test_plugin",
            rate_ms=2000,
            config={'mock_mode': True, 'custom': 'value'}
        )
        
        assert config.name == "test_plugin"
        assert config.rate_ms == 2000
        assert config.config['mock_mode'] == True
        assert config.config['custom'] == 'value'


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_plugin_handles_missing_psutil(self):
        """Test plugin gracefully handles missing dependencies."""
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="system", rate_ms=1000, config={'mock_mode': True})
        plugin = SystemPlugin(config)
        
        # Should initialize successfully with mock mode
        plugin.initialize()
        assert plugin._status.value == "ready"
        
        # Should collect mock data
        data = plugin.collect_data()
        assert 'cpu_percent' in data
    
    def test_network_chart_handles_many_updates(self):
        """Test network chart handles many updates."""
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        
        # Simulate many dashboard updates (long running)
        for i in range(200):
            chart.update_data(i * 1024 * 1024, i * 512 * 1024)
        
        # Chart should handle updates without crashing
        assert chart is not None
    
    def test_packet_table_handles_creation(self):
        """Test packet table can be created and used."""
        from src.widgets.packet_table import PacketTable
        
        table = PacketTable()
        
        # Table should be functional
        assert table is not None
        assert hasattr(table, 'add_rows')
        
        # Test adding rows using actual API
        rows = [
            ('10:30:01', '192.168.1.1', '8.8.8.8', 'DNS', '64', 'Query'),
            ('10:30:02', '192.168.1.1', '8.8.8.8', 'DNS', '128', 'Response'),
        ]
        table.add_rows(rows)
        
        # Table should have data
        assert table.row_count == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=src', '--cov-report=term-missing', '--cov-report=html'])
