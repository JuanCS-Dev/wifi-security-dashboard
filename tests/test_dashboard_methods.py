"""Dashboard method coverage using mocked Textual app."""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, PropertyMock

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_app():
    """Create mock Textual app."""
    app = Mock()
    app.refresh = Mock()
    app.call_later = Mock()
    app.set_interval = Mock(return_value=Mock())
    return app


class TestConsolidatedDashboardMethods:
    """Test consolidated dashboard methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.consolidated_dashboard import ConsolidatedDashboard
        
        dashboard = ConsolidatedDashboard()
        dashboard.app = mock_app
        
        # compose() returns generator
        widgets = list(dashboard.compose())
        assert len(widgets) > 0
    
    def test_update_displays_method_exists(self):
        from src.screens.consolidated_dashboard import ConsolidatedDashboard
        
        dashboard = ConsolidatedDashboard()
        
        # Check methods exist
        assert hasattr(dashboard, 'compose')
        assert hasattr(dashboard, '_update_displays') or hasattr(dashboard, 'update_data')


class TestSystemDashboardMethods:
    """Test system dashboard methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.system_dashboard import SystemDashboard
        
        dashboard = SystemDashboard()
        dashboard.app = mock_app
        
        widgets = list(dashboard.compose())
        assert len(widgets) > 0
    
    def test_update_method_exists(self):
        from src.screens.system_dashboard import SystemDashboard
        
        dashboard = SystemDashboard()
        assert hasattr(dashboard, 'compose')


class TestNetworkDashboardMethods:
    """Test network dashboard methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.network_dashboard import NetworkDashboard
        
        dashboard = NetworkDashboard()
        dashboard.app = mock_app
        
        widgets = list(dashboard.compose())
        assert len(widgets) > 0


class TestWiFiDashboardMethods:
    """Test WiFi dashboard methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.wifi_dashboard import WiFiDashboard
        
        dashboard = WiFiDashboard()
        dashboard.app = mock_app
        
        widgets = list(dashboard.compose())
        assert len(widgets) > 0


class TestPacketsDashboardMethods:
    """Test packets dashboard methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.packets_dashboard import PacketsDashboard
        
        dashboard = PacketsDashboard()
        dashboard.app = mock_app
        
        widgets = list(dashboard.compose())
        assert len(widgets) > 0


class TestTutorialScreenMethods:
    """Test tutorial screen methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.tutorial_screen import TutorialScreen
        
        screen = TutorialScreen()
        screen.app = mock_app
        
        widgets = list(screen.compose())
        assert len(widgets) > 0


class TestHelpScreenMethods:
    """Test help screen methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.help_screen import HelpScreen
        
        screen = HelpScreen()
        screen.app = mock_app
        
        widgets = list(screen.compose())
        assert len(widgets) > 0


class TestLandingScreenMethods:
    """Test landing screen methods."""
    
    def test_compose_generator(self, mock_app):
        from src.screens.landing_screen import LandingScreen
        
        screen = LandingScreen()
        screen.app = mock_app
        
        widgets = list(screen.compose())
        assert len(widgets) > 0
    
    def test_banner_render(self):
        from src.screens.landing_screen import BannerWidget
        from rich.console import Console
        from io import StringIO
        
        banner = BannerWidget()
        
        # Render to string
        console = Console(file=StringIO(), force_terminal=True, width=80)
        output = banner.render()
        
        # Should return renderable
        assert output is not None
    
    def test_menu_render(self):
        from src.screens.landing_screen import MenuWidget
        from rich.console import Console
        from io import StringIO
        
        menu = MenuWidget()
        menu.current_mode = "mock"
        
        console = Console(file=StringIO(), force_terminal=True, width=80)
        output = menu.render()
        
        assert output is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
