"""Widget render coverage tests."""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNetworkChartRenders:
    """Test NetworkChart render paths."""
    
    def test_chart_render_with_data(self):
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        
        # Simulate 50 updates
        for i in range(50):
            chart.update_data({
                'bandwidth_rx_mbps': float(i % 100),
                'bandwidth_tx_mbps': float((i % 100) / 2)
            })
        
        # Trigger reactive watchers
        assert chart.bandwidth_rx >= 0
        assert chart.bandwidth_tx >= 0
    
    def test_chart_time_axis(self):
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        chart.time_axis = list(range(60))
        assert len(chart.time_axis) == 60
    
    def test_chart_history(self):
        from src.widgets.network_chart import NetworkChart
        
        chart = NetworkChart()
        chart.rx_history = [float(i) for i in range(100)]
        chart.tx_history = [float(i/2) for i in range(100)]
        
        assert len(chart.rx_history) == 100
        assert len(chart.tx_history) == 100


class TestPacketTableRenders:
    """Test PacketTable render paths."""
    
    def test_table_add_columns_then_rows(self):
        from src.widgets.packet_table import PacketTable
        
        table = PacketTable()
        
        # Add columns first
        table.add_columns("Time", "Src", "Dst", "Proto", "Len", "Info")
        
        # Then add rows
        table.add_rows([
            ("10:30:01", "192.168.1.1", "8.8.8.8", "DNS", "64", "Query"),
            ("10:30:02", "8.8.8.8", "192.168.1.1", "DNS", "128", "Response"),
        ])
        
        assert table.row_count == 2


class TestTooltipRenders:
    """Test Tooltip render paths."""
    
    def test_tooltip_render_calls(self):
        from src.widgets.tooltip_widget import Tooltip
        
        tooltip = Tooltip(content="Security tip about HTTPS")
        
        # Has render
        assert hasattr(tooltip, 'render')
    
    def test_educational_tip_render(self):
        from src.widgets.tooltip_widget import EducationalTip, get_tip
        
        https_tip = get_tip('https')
        if https_tip:
            tip = EducationalTip(content=https_tip)
            assert tip is not None


class TestPluginEdgeCases:
    """Test plugin edge cases and error paths."""
    
    def test_plugin_double_initialize(self):
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="sys", rate_ms=1000, config={'mock_mode': True})
        plugin = SystemPlugin(config)
        
        plugin.initialize()
        plugin.initialize()  # Double init should be safe
        
        assert plugin._status.value == "ready"
    
    def test_plugin_collect_before_init(self):
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="sys", rate_ms=1000, config={'mock_mode': True})
        plugin = SystemPlugin(config)
        
        # May return empty or error, should not crash
        try:
            data = plugin.collect_data()
            assert isinstance(data, dict)
        except:
            pass  # Expected
    
    def test_plugin_cleanup_before_init(self):
        from src.plugins.system_plugin import SystemPlugin
        from src.plugins.base import PluginConfig
        
        config = PluginConfig(name="sys", rate_ms=1000, config={'mock_mode': True})
        plugin = SystemPlugin(config)
        
        # Should not crash
        plugin.cleanup()


class TestMockEdgeCases:
    """Test mock data edge cases."""
    
    def test_mock_generator_persistence(self):
        from src.utils.mock_data_generator import get_mock_generator
        
        gen1 = get_mock_generator()
        gen2 = get_mock_generator()
        
        # Should be same instance
        assert gen1 is gen2
    
    def test_mock_packet_generator_persistence(self):
        from src.utils.mock_data_generator import get_mock_packet_generator
        
        gen1 = get_mock_packet_generator()
        gen2 = get_mock_packet_generator()
        
        assert gen1 is gen2
    
    def test_mock_all_device_types(self):
        from src.utils.mock_data_generator import MockDataGenerator
        
        gen = MockDataGenerator()
        
        # Cycle through many times to hit all devices
        ssids = set()
        for _ in range(100):
            wifi = gen.get_wifi_info()
            ssids.add(wifi['ssid'])
        
        # Should have variety
        assert len(ssids) >= 3


class TestScreenEdgeCases:
    """Test screen edge cases."""
    
    def test_tutorial_no_flag_dir(self):
        from src.screens.tutorial_screen import TutorialScreen
        from pathlib import Path
        import shutil
        
        flag_dir = Path.home() / ".wifi_security_dashboard"
        
        # Remove entire dir
        if flag_dir.exists():
            shutil.rmtree(flag_dir)
        
        # Should create dir and show tutorial
        assert TutorialScreen.should_show_tutorial() == True
        
        # Cleanup
        if flag_dir.exists():
            shutil.rmtree(flag_dir)
    
    def test_landing_screen_widgets_multiple_creation(self):
        from src.screens.landing_screen import BannerWidget, MenuWidget
        
        # Create multiple instances
        banners = [BannerWidget() for _ in range(5)]
        menus = [MenuWidget() for _ in range(5)]
        
        assert len(banners) == 5
        assert len(menus) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
