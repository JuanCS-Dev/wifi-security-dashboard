"""
Final Comprehensive Coverage - 80%+ Target
Disciplined testing with correct APIs.

Author: Juan-Dev - Soli Deo Gloria ✝️
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAllPluginsCoverage:
    """Test all plugins comprehensively."""
    
    def test_all_plugins_mock_mode(self):
        """Test all plugins in safe mock mode."""
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.network_plugin import NetworkPlugin
        from src.plugins.wifi_plugin import WiFiPlugin
        from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
        from src.plugins.base import PluginConfig
        
        plugins = [
            SystemPlugin,
            NetworkPlugin,
            WiFiPlugin,
            PacketAnalyzerPlugin
        ]
        
        for PluginClass in plugins:
            config = PluginConfig(name=PluginClass.__name__, rate_ms=1000, config={'mock_mode': True})
            plugin = PluginClass(config)
            plugin.initialize()
            data = plugin.collect_data()
            
            # All should return data dictionary
            assert isinstance(data, dict)
            assert len(data) > 0
    
    def test_network_plugin_coverage(self):
        """Test network plugin specific paths."""
        from src.plugins.network_plugin import NetworkPlugin
        from src.plugins.base import PluginConfig
        
        # Test mock mode
        config_mock = PluginConfig(name="net", rate_ms=1000, config={'mock_mode': True})
        plugin_mock = NetworkPlugin(config_mock)
        plugin_mock.initialize()
        data_mock = plugin_mock.collect_data()
        assert 'bytes_recv' in data_mock
        
        # Test real mode
        config_real = PluginConfig(name="net", rate_ms=1000, config={'mock_mode': False})
        plugin_real = NetworkPlugin(config_real)
        plugin_real.initialize()
        data_real = plugin_real.collect_data()
        assert 'bytes_recv' in data_real


class TestAllDashboardsCoverage:
    """Test all dashboard screens."""
    
    def test_all_dashboards_creation(self):
        """Test all dashboards can be instantiated."""
        from src.screens import (
            ConsolidatedDashboard,
            SystemDashboard,
            NetworkDashboard,
            WiFiDashboard,
            PacketsDashboard,
            HelpScreen,
            LandingScreen
        )
        
        dashboards = [
            ConsolidatedDashboard,
            SystemDashboard,
            NetworkDashboard,
            WiFiDashboard,
            PacketsDashboard,
            HelpScreen,
            LandingScreen
        ]
        
        for DashboardClass in dashboards:
            dashboard = DashboardClass()
            assert dashboard is not None
            assert hasattr(dashboard, 'compose')


class TestWidgetsCoverage:
    """Test widget implementations."""
    
    def test_network_chart_proper_api(self):
        """Test NetworkChart with correct API."""
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        
        # Correct API: update_data(plugin_data: Dict)
        plugin_data = {
            'bytes_recv': 1024 * 1024,
            'bytes_sent': 512 * 1024,
            'bandwidth_rx_mbps': 10.5,
            'bandwidth_tx_mbps': 5.2
        }
        
        chart.update_data(plugin_data)
        
        # Chart should update reactively
        assert chart is not None
    
    def test_packet_table_proper_usage(self):
        """Test PacketTable correctly."""
        from src.widgets.packet_table import PacketTable
        
        table = PacketTable()
        
        # PacketTable is a DataTable, check it exists
        assert table is not None
        assert hasattr(table, 'add_rows')
    
    def test_tooltip_proper_api(self):
        """Test Tooltip and EducationalTip with correct API."""
        from src.widgets.tooltip_widget import Tooltip, EducationalTip, get_tip
        
        # Tooltip with content
        tooltip = Tooltip(content="Test content")
        assert tooltip is not None
        
        # EducationalTip with content (not tip_key)
        https_tip_content = get_tip('https')
        if https_tip_content:
            edu_tip = EducationalTip(content=https_tip_content, tip_type='security')
            assert edu_tip is not None


class TestMockDataGeneratorFull:
    """Complete mock data generator coverage."""
    
    def test_mock_generator_all_methods(self):
        """Test all mock generator methods."""
        from src.utils.mock_data_generator import get_mock_generator, get_mock_packet_generator
        
        gen = get_mock_generator()
        packet_gen = get_mock_packet_generator()
        
        # Test all data methods
        system = gen.get_system_metrics()
        wifi = gen.get_wifi_info()
        network = gen.get_network_stats()
        packets = packet_gen.get_packet_analysis()
        
        # Validate system
        assert 'cpu_percent' in system
        assert 0 <= system['cpu_percent'] <= 100
        
        # Validate WiFi (correct keys)
        assert 'ssid' in wifi
        assert 'signal_strength' in wifi
        
        # Validate network
        assert 'bytes_recv' in network
        assert network['bytes_recv'] >= 0
        
        # Validate packets
        assert 'backend' in packets
        assert packets['backend'] == 'mock'


class TestScreenLifecycles:
    """Test screen lifecycle methods."""
    
    def test_tutorial_screen_workflow(self):
        """Test tutorial screen workflow."""
        from src.screens.tutorial_screen import TutorialScreen
        from pathlib import Path
        
        # Test should_show_tutorial
        flag = Path.home() / ".wifi_security_dashboard" / "tutorial_completed"
        if flag.exists():
            flag.unlink()
        
        assert TutorialScreen.should_show_tutorial() == True
        
        # Create flag
        flag.parent.mkdir(parents=True, exist_ok=True)
        flag.touch()
        
        assert TutorialScreen.should_show_tutorial() == False
        
        flag.unlink()
    
    def test_landing_screen_widgets(self):
        """Test landing screen widgets."""
        from src.screens.landing_screen import BannerWidget, MenuWidget
        
        banner = BannerWidget()
        menu = MenuWidget()
        
        assert banner is not None
        assert menu is not None
        
        # Test menu mode toggle
        menu.current_mode = "mock"
        assert menu.current_mode == "mock"
        menu.current_mode = "real"
        assert menu.current_mode == "real"


class TestPluginErrorHandling:
    """Test plugin error handling."""
    
    def test_wifi_no_hardware_handling(self):
        """Test WiFi handles missing hardware."""
        from src.plugins.wifi_plugin import WiFiPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="wifi", rate_ms=1000, config={'mock_mode': False})
        plugin = WiFiPlugin(config)
        plugin.initialize()  # Should not crash
        
        data = plugin.collect_data()
        
        # Either has data or shows unavailable
        assert 'ssid' in data or 'message' in data
    
    def test_packet_analyzer_no_backend(self):
        """Test packet analyzer without Scapy."""
        from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="packets", rate_ms=1000, config={'mock_mode': False})
        plugin = PacketAnalyzerPlugin(config)
        plugin.initialize()  # Should not crash
        
        data = plugin.collect_data()
        
        # Either has backend or shows unavailable
        assert 'backend' in data


class TestSystemPluginComplete:
    """Complete system plugin testing."""
    
    def test_system_plugin_all_metrics(self):
        """Test all system metrics collected."""
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        import time
        
        config = PluginConfig(name="system", rate_ms=1000, config={'mock_mode': False})
        plugin = SystemPlugin(config)
        plugin.initialize()
        time.sleep(0.1)
        
        data = plugin.collect_data()
        
        # Required metrics
        assert 'cpu_percent' in data
        assert 'memory_percent' in data
        assert 'disk_percent' in data
        assert 'cpu_percent_per_core' in data
        assert 'cpu_count' in data
        assert 'memory_used_mb' in data
        assert 'memory_total_mb' in data
        assert 'disk_used_gb' in data
        assert 'disk_total_gb' in data
        
        # Validate ranges
        assert data['cpu_percent'] >= 0
        assert 0 <= data['memory_percent'] <= 100
        assert 0 <= data['disk_percent'] <= 100


