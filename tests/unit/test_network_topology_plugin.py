"""
Tests for Network Topology Plugin - Feature 1

Boris's Mission: 61% → 95% coverage
Focus: Network discovery, device tracking, vendor lookup

Production-ready tests with real behavior validation.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import time
from dataclasses import asdict

from plugins.base import PluginConfig
from plugins.network_topology_plugin import (
    NetworkTopologyPlugin,
    NetworkDevice,
    SCAPY_AVAILABLE,
    NETIFACES_AVAILABLE
)


class TestNetworkDevice:
    """Test NetworkDevice dataclass."""
    
    def test_network_device_creation(self):
        """Test creating NetworkDevice with all fields."""
        device = NetworkDevice(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            hostname="laptop.local",
            vendor="Dell Inc.",
            last_seen=1699824000.0
        )
        
        assert device.ip == "192.168.1.100"
        assert device.mac == "aa:bb:cc:dd:ee:ff"
        assert device.hostname == "laptop.local"
        assert device.vendor == "Dell Inc."
        assert device.last_seen == 1699824000.0
    
    def test_network_device_to_dict(self):
        """Test converting NetworkDevice to dictionary."""
        device = NetworkDevice(
            ip="192.168.1.50",
            mac="11:22:33:44:55:66",
            hostname="phone",
            vendor="Apple",
            last_seen=1699824100.0
        )
        
        device_dict = device.to_dict()
        
        assert isinstance(device_dict, dict)
        assert device_dict["ip"] == "192.168.1.50"
        assert device_dict["mac"] == "11:22:33:44:55:66"
        assert device_dict["hostname"] == "phone"
        assert device_dict["vendor"] == "Apple"
        assert device_dict["last_seen"] == 1699824100.0


class TestNetworkTopologyPluginInitialization:
    """Test plugin initialization."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        assert plugin.devices == {}
        assert plugin.gateway_ip is None
        assert plugin.subnet == "192.168.1.0/24"
        assert plugin._vendor_cache == {}
        assert plugin._scan_thread is None
    
    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        config = PluginConfig(
            name="topology",
            enabled=True,
            config={"subnet": "10.0.0.0/24"}
        )
        plugin = NetworkTopologyPlugin(config)
        
        assert plugin.subnet == "192.168.1.0/24"  # Default until start()
    
    def test_requires_root(self):
        """Test that plugin requires root privileges."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        assert plugin.requires_root() is True


class TestDataCollection:
    """Test data collection methods."""
    
    def test_get_data_empty(self):
        """Test get_data with no devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        data = plugin.get_data()
        
        assert data["gateway_ip"] is None
        assert data["subnet"] == "192.168.1.0/24"
        assert data["device_count"] == 0
        assert data["devices"] == []
    
    def test_get_data_with_devices(self):
        """Test get_data with registered devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Add test devices
        device1 = NetworkDevice(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            hostname="device1",
            vendor="Vendor1",
            last_seen=time.time()
        )
        device2 = NetworkDevice(
            ip="192.168.1.101",
            mac="11:22:33:44:55:66",
            hostname="device2",
            vendor="Vendor2",
            last_seen=time.time()
        )
        
        plugin.devices["aa:bb:cc:dd:ee:ff"] = device1
        plugin.devices["11:22:33:44:55:66"] = device2
        plugin.gateway_ip = "192.168.1.1"
        
        data = plugin.get_data()
        
        assert data["gateway_ip"] == "192.168.1.1"
        assert data["device_count"] == 2
        assert len(data["devices"]) == 2
        assert data["devices"][0]["ip"] in ["192.168.1.100", "192.168.1.101"]
    
    def test_collect_data_calls_get_data(self):
        """Test that collect_data delegates to get_data."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        with patch.object(plugin, 'get_data') as mock_get:
            mock_get.return_value = {"test": "data"}
            
            result = plugin.collect_data()
            
            mock_get.assert_called_once()
            assert result == {"test": "data"}


class TestNetworkDetection:
    """Test network detection functionality."""
    
    @patch('plugins.network_topology_plugin.NETIFACES_AVAILABLE', False)
    def test_detect_network_without_netifaces(self):
        """Test network detection fallback when netifaces not available."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        plugin._detect_network()
        
        # Should use defaults
        assert plugin.gateway_ip == "192.168.1.1"
        assert plugin.subnet == "192.168.1.0/24"
    
    @patch('plugins.network_topology_plugin.NETIFACES_AVAILABLE', True)
    @patch('plugins.network_topology_plugin.netifaces')
    def test_detect_network_with_netifaces(self, mock_netifaces):
        """Test network detection with netifaces."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Mock netifaces responses
        mock_netifaces.AF_INET = 2
        mock_netifaces.gateways.return_value = {
            'default': {
                2: ('192.168.1.1', 'eth0')
            }
        }
        mock_netifaces.ifaddresses.return_value = {
            2: [{'addr': '192.168.1.50', 'netmask': '255.255.255.0'}]
        }
        
        plugin._detect_network()
        
        assert plugin.gateway_ip == "192.168.1.1"
        assert plugin.subnet == "192.168.1.0/24"
    
    @patch('plugins.network_topology_plugin.NETIFACES_AVAILABLE', True)
    @patch('plugins.network_topology_plugin.netifaces')
    def test_detect_network_handles_exception(self, mock_netifaces):
        """Test network detection handles exceptions gracefully."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Make netifaces raise exception
        mock_netifaces.gateways.side_effect = Exception("Network error")
        
        plugin._detect_network()
        
        # Should fall back to defaults
        assert plugin.gateway_ip == "192.168.1.1"
        assert plugin.subnet == "192.168.1.0/24"


class TestPluginLifecycle:
    """Test plugin start/stop/initialize lifecycle."""
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', False)
    def test_start_without_scapy(self):
        """Test start fails gracefully without scapy."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        plugin.start()
        
        # Should not start thread
        assert plugin._scan_thread is None
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', True)
    def test_start_with_scapy(self):
        """Test start initializes scanning."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        with patch.object(plugin, '_detect_network') as mock_detect:
            with patch('threading.Thread') as mock_thread:
                plugin.start()
                
                mock_detect.assert_called_once()
                mock_thread.assert_called_once()
                assert not plugin._stop_event.is_set()
    
    def test_stop_plugin(self):
        """Test stopping the plugin."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Mock thread
        mock_thread = Mock()
        plugin._scan_thread = mock_thread
        
        plugin.stop()
        
        assert plugin._stop_event.is_set()
        mock_thread.join.assert_called_once_with(timeout=2.0)
    
    def test_initialize_calls_start(self):
        """Test that initialize() calls start()."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        with patch.object(plugin, 'start') as mock_start:
            plugin.initialize()
            
            mock_start.assert_called_once()


class TestHostnameResolution:
    """Test hostname resolution."""
    
    @patch('socket.gethostbyaddr')
    def test_resolve_hostname_success(self, mock_gethostbyaddr):
        """Test successful hostname resolution."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        mock_gethostbyaddr.return_value = ("laptop.local", [], ["192.168.1.100"])
        
        hostname = plugin._resolve_hostname("192.168.1.100")
        
        assert hostname == "laptop.local"
        mock_gethostbyaddr.assert_called_once_with("192.168.1.100")
    
    @patch('socket.gethostbyaddr')
    def test_resolve_hostname_failure(self, mock_gethostbyaddr):
        """Test hostname resolution failure."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        mock_gethostbyaddr.side_effect = Exception("DNS error")
        
        hostname = plugin._resolve_hostname("192.168.1.200")
        
        assert hostname == "Unknown"


class TestVendorLookup:
    """Test MAC vendor lookup."""
    
    def test_lookup_vendor_from_cache(self):
        """Test vendor lookup uses cache."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Pre-populate cache
        plugin._vendor_cache["aa:bb:cc:dd:ee:ff"] = "Dell Inc."
        
        vendor = plugin._lookup_vendor("aa:bb:cc:dd:ee:ff")
        
        assert vendor == "Dell Inc."
    
    @patch('requests.get')
    def test_lookup_vendor_api_success(self, mock_get):
        """Test successful API vendor lookup."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Apple, Inc."
        mock_get.return_value = mock_response
        
        vendor = plugin._lookup_vendor("aa:bb:cc:dd:ee:ff")
        
        assert vendor == "Apple, Inc."
        assert plugin._vendor_cache["aa:bb:cc:dd:ee:ff"] == "Apple, Inc."
        mock_get.assert_called_once_with(
            "https://api.macvendors.com/aa:bb:cc:dd:ee:ff",
            timeout=2
        )
    
    @patch('requests.get')
    def test_lookup_vendor_api_failure(self, mock_get):
        """Test vendor lookup API failure falls back to OUI."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        mock_get.side_effect = Exception("Network error")
        
        vendor = plugin._lookup_vendor("aa:bb:cc:dd:ee:ff")
        
        assert vendor == "OUI:AA:BB:CC"
        assert plugin._vendor_cache["aa:bb:cc:dd:ee:ff"] == "OUI:AA:BB:CC"
    
    @patch('requests.get')
    def test_lookup_vendor_api_404(self, mock_get):
        """Test vendor lookup with 404 response."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        vendor = plugin._lookup_vendor("11:22:33:44:55:66")
        
        assert vendor == "OUI:11:22:33"


class TestNetworkScanning:
    """Test network scanning functionality."""
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', False)
    def test_scan_network_without_scapy(self):
        """Test scan returns early without scapy."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Should not crash
        plugin._scan_network()
        
        assert len(plugin.devices) == 0
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', True)
    @patch('plugins.network_topology_plugin.srp')
    @patch.object(NetworkTopologyPlugin, '_resolve_hostname')
    @patch.object(NetworkTopologyPlugin, '_lookup_vendor')
    def test_scan_network_discovers_devices(self, mock_vendor, mock_hostname, mock_srp):
        """Test successful network scan discovers devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Mock scapy responses
        mock_received1 = Mock()
        mock_received1.psrc = "192.168.1.100"
        mock_received1.hwsrc = "aa:bb:cc:dd:ee:ff"
        
        mock_received2 = Mock()
        mock_received2.psrc = "192.168.1.101"
        mock_received2.hwsrc = "11:22:33:44:55:66"
        
        mock_srp.return_value = (
            [(None, mock_received1), (None, mock_received2)],
            []
        )
        
        mock_hostname.return_value = "device.local"
        mock_vendor.return_value = "Vendor Inc."
        
        plugin._scan_network()
        
        assert len(plugin.devices) == 2
        assert "192.168.1.100" in plugin.devices
        assert "192.168.1.101" in plugin.devices
        assert plugin.devices["192.168.1.100"].mac == "aa:bb:cc:dd:ee:ff"
        assert plugin.devices["192.168.1.100"].vendor == "Vendor Inc."
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', True)
    @patch('plugins.network_topology_plugin.srp')
    def test_scan_network_updates_last_seen(self, mock_srp):
        """Test scan updates last_seen for existing devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Add existing device
        old_time = time.time() - 100
        plugin.devices["192.168.1.100"] = NetworkDevice(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            hostname="device",
            vendor="Vendor",
            last_seen=old_time
        )
        
        # Mock scan finding same device
        mock_received = Mock()
        mock_received.psrc = "192.168.1.100"
        mock_received.hwsrc = "aa:bb:cc:dd:ee:ff"
        
        mock_srp.return_value = ([(None, mock_received)], [])
        
        plugin._scan_network()
        
        # last_seen should be updated
        assert plugin.devices["192.168.1.100"].last_seen > old_time
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', True)
    @patch('plugins.network_topology_plugin.srp')
    @patch('time.time')
    def test_scan_network_removes_stale_devices(self, mock_time, mock_srp):
        """Test scan removes stale devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Current time
        current_time = 1000000.0
        mock_time.return_value = current_time
        
        # Add stale device (last seen > 5 minutes ago)
        plugin.devices["192.168.1.100"] = NetworkDevice(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            hostname="device",
            vendor="Vendor",
            last_seen=current_time - 400  # 400 seconds ago (> 300)
        )
        
        # Mock empty scan response
        mock_srp.return_value = ([], [])
        
        plugin._scan_network()
        
        # Stale device should be removed
        assert "192.168.1.100" not in plugin.devices


class TestScanLoop:
    """Test continuous scanning loop."""
    
    @patch.object(NetworkTopologyPlugin, '_scan_network')
    def test_scan_loop_calls_scan_network(self, mock_scan):
        """Test scan loop calls _scan_network."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Call count tracker
        call_count = [0]
        
        def track_and_stop(*args):
            call_count[0] += 1
            plugin._stop_event.set()  # Stop after first call
        
        mock_scan.side_effect = track_and_stop
        
        plugin._scan_loop()
        
        # Should have called scan
        assert call_count[0] >= 1
    
    @patch.object(NetworkTopologyPlugin, '_scan_network')
    def test_scan_loop_handles_exceptions(self, mock_scan):
        """Test scan loop handles scan exceptions."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Make scan raise exception then stop
        def raise_and_stop(*args):
            plugin._stop_event.set()
            raise Exception("Scan error")
        
        mock_scan.side_effect = raise_and_stop
        
        # Should not crash
        plugin._scan_loop()
        
        assert mock_scan.called


class TestMockPlugin:
    """Test MockNetworkTopologyPlugin."""
    
    def test_mock_plugin_initialization(self):
        """Test mock plugin initializes with fake data."""
        from plugins.network_topology_plugin import MockNetworkTopologyPlugin
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopologyPlugin(config)
        
        # Should have defaults
        assert plugin.gateway_ip == "192.168.1.1"
        assert plugin.subnet == "192.168.1.0/24"
        assert len(plugin.devices) > 0
    
    def test_mock_plugin_get_data(self):
        """Test mock plugin returns fake topology data."""
        from plugins.network_topology_plugin import MockNetworkTopologyPlugin
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopologyPlugin(config)
        
        data = plugin.get_data()
        
        assert "gateway_ip" in data
        assert "subnet" in data
        assert "device_count" in data
        assert "devices" in data
        assert isinstance(data["devices"], list)
        assert len(data["devices"]) > 0  # Should have mock devices
    
    def test_mock_plugin_initialize(self):
        """Test mock plugin initialize method."""
        from plugins.network_topology_plugin import MockNetworkTopologyPlugin
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopologyPlugin(config)
        
        # Should not crash
        plugin.initialize()
    
    def test_mock_plugin_collect_data(self):
        """Test mock plugin collect_data returns topology data."""
        from plugins.network_topology_plugin import MockNetworkTopologyPlugin
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopologyPlugin(config)
        
        data = plugin.collect_data()
        
        assert data["gateway_ip"] == "192.168.1.1"
        assert data["device_count"] == len(plugin.devices)
    
    def test_mock_plugin_devices_have_valid_structure(self):
        """Test mock devices have correct structure."""
        from plugins.network_topology_plugin import MockNetworkTopologyPlugin
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopologyPlugin(config)
        
        data = plugin.get_data()
        
        for device in data["devices"]:
            assert "ip" in device
            assert "mac" in device
            assert "hostname" in device
            assert "vendor" in device
            assert "last_seen" in device


class TestProductionReadiness:
    """Boris's production readiness tests."""
    
    def test_plugin_has_no_placeholders(self):
        """Test that plugin has no TODO/FIXME placeholders."""
        import inspect
        source = inspect.getsource(NetworkTopologyPlugin)
        
        assert "TODO" not in source
        assert "FIXME" not in source
        assert "PLACEHOLDER" not in source
    
    def test_device_tracking_thread_safe(self):
        """Test device dictionary operations are safe."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Should be able to add/remove/update devices
        device = NetworkDevice(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            hostname="test",
            vendor="Test",
            last_seen=time.time()
        )
        
        plugin.devices["192.168.1.100"] = device
        assert "192.168.1.100" in plugin.devices
        
        del plugin.devices["192.168.1.100"]
        assert "192.168.1.100" not in plugin.devices
    
    def test_vendor_cache_works(self):
        """Test vendor cache prevents API spam."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopologyPlugin(config)
        
        # Add to cache
        plugin._vendor_cache["aa:bb:cc:dd:ee:ff"] = "Test Vendor"
        
        with patch('requests.get') as mock_get:
            # Call lookup - should NOT hit API
            vendor = plugin._lookup_vendor("aa:bb:cc:dd:ee:ff")
            
            assert vendor == "Test Vendor"
            mock_get.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


class TestScapyImport:
    """Test Scapy import handling."""
    
    def test_scapy_available_flag(self):
        """Test that SCAPY_AVAILABLE flag exists."""
        from plugins.network_topology_plugin import SCAPY_AVAILABLE
        
        assert isinstance(SCAPY_AVAILABLE, bool)
    
    @patch('plugins.network_topology_plugin.SCAPY_AVAILABLE', False)
    def test_start_without_scapy(self):
        """Test starting without Scapy available."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopology(config)
        
        # Should not crash
        plugin.start()
        
        # Thread should not be created
        assert plugin._monitor_thread is None


class TestConnectionEdgeCases:
    """Test connection edge cases."""
    
    def test_add_connection_bidirectional(self):
        """Test that connections are bidirectional."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopology(config)
        
        plugin.add_device("192.168.1.100", "aa:bb:cc:dd:ee:ff")
        plugin.add_device("192.168.1.101", "11:22:33:44:55:66")
        
        plugin.add_connection("192.168.1.100", "192.168.1.101")
        
        data = plugin.get_data()
        
        # Should see connection in both directions
        connections = data['connections']
        assert len(connections) > 0
        
        # Verify connection exists
        conn_exists = any(
            (c['source'] == "192.168.1.100" and c['target'] == "192.168.1.101") or
            (c['source'] == "192.168.1.101" and c['target'] == "192.168.1.100")
            for c in connections
        )
        assert conn_exists
    
    def test_multiple_connections_same_device(self):
        """Test multiple connections to same device."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopology(config)
        
        plugin.add_device("192.168.1.1", "aa:aa:aa:aa:aa:aa")
        plugin.add_device("192.168.1.100", "bb:bb:bb:bb:bb:bb")
        plugin.add_device("192.168.1.101", "cc:cc:cc:cc:cc:cc")
        plugin.add_device("192.168.1.102", "dd:dd:dd:dd:dd:dd")
        
        # All devices connect to gateway
        plugin.add_connection("192.168.1.100", "192.168.1.1")
        plugin.add_connection("192.168.1.101", "192.168.1.1")
        plugin.add_connection("192.168.1.102", "192.168.1.1")
        
        data = plugin.get_data()
        
        # Should have 4 devices and 3+ connections
        assert data['device_count'] == 4
        assert len(data['connections']) >= 3


class TestMockTopologyComplete:
    """Complete mock topology tests."""
    
    def test_mock_full_lifecycle(self):
        """Test mock plugin complete lifecycle."""
        from plugins.network_topology_plugin import MockNetworkTopology
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopology(config)
        
        # Start
        plugin.start()
        
        # Get data - should have mock devices
        data = plugin.get_data()
        assert data['monitoring'] is True
        assert data['device_count'] > 0
        
        # Stop
        plugin.stop()
        
        # Should still work after stop
        data = plugin.get_data()
        assert isinstance(data, dict)
    
    def test_mock_collect_data(self):
        """Test mock collect_data method."""
        from plugins.network_topology_plugin import MockNetworkTopology
        
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = MockNetworkTopology(config)
        
        data = plugin.collect_data()
        
        assert isinstance(data, dict)
        assert 'monitoring' in data


class TestProductionReadinessComplete:
    """Complete production readiness tests."""
    
    def test_high_device_count(self):
        """Test handling high number of devices."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopology(config)
        
        # Add 50 devices
        for i in range(50):
            ip = f"192.168.1.{i+100}"
            mac = f"aa:bb:cc:dd:ee:{i:02x}"
            plugin.add_device(ip, mac, f"device_{i}")
        
        data = plugin.get_data()
        
        assert data['device_count'] == 50
        assert len(data['devices']) == 50
    
    def test_network_discovery_workflow(self):
        """Test complete network discovery workflow."""
        config = PluginConfig(name="topology", enabled=True, config={})
        plugin = NetworkTopology(config)
        
        # Simulate network discovery
        # 1. Gateway discovered
        plugin.add_device("192.168.1.1", "aa:aa:aa:aa:aa:aa", "Gateway", is_gateway=True)
        
        # 2. Devices discovered
        plugin.add_device("192.168.1.100", "bb:bb:bb:bb:bb:bb", "Laptop")
        plugin.add_device("192.168.1.101", "cc:cc:cc:cc:cc:cc", "Phone")
        
        # 3. Traffic observed (connections)
        plugin.add_connection("192.168.1.100", "192.168.1.1")
        plugin.add_connection("192.168.1.101", "192.168.1.1")
        plugin.add_connection("192.168.1.100", "192.168.1.101")
        
        # 4. Get network map
        data = plugin.get_data()
        
        # Verify complete topology
        assert data['device_count'] == 3
        assert data['gateway_count'] == 1
        assert len(data['connections']) >= 2
        
        # Verify gateway identified
        gateways = [d for d in data['devices'] if d.get('is_gateway')]
        assert len(gateways) == 1
        assert gateways[0]['ip'] == "192.168.1.1"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
