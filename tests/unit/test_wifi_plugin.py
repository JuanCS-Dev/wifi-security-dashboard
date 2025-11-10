"""
Unit tests for WiFiPlugin.

Tests WiFi metrics collection with mocked subprocess and filesystem.
Target: 90%+ coverage of wifi_plugin.py

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import subprocess

from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.base import PluginConfig, PluginStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def plugin_config():
    """Create plugin configuration"""
    return PluginConfig(
        name="wifi",
        enabled=True,
        rate_ms=1000,
        config={"interface": "wlan0"}
    )


@pytest.fixture
def plugin_config_no_interface():
    """Create plugin config without interface (for auto-detect)"""
    return PluginConfig(
        name="wifi",
        enabled=True,
        rate_ms=1000,
        config={}
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestWiFiPluginInitialization:
    """Test WiFiPlugin initialization"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_initialize_uses_configured_interface(self, mock_run, plugin_config):
        """Test initialize uses interface from config"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        assert plugin._interface == "wlan0"
        assert plugin.status == PluginStatus.READY

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_initialize_auto_detects_interface_nmcli(self, mock_run, plugin_config_no_interface):
        """Test initialize auto-detects interface via nmcli"""
        # Mock nmcli device list
        mock_run.side_effect = [
            Mock(returncode=0, stdout="wlan0:wifi\neth0:ethernet\n", stderr=""),
            Mock(returncode=0, stdout="", stderr="")  # --version check
        ]

        plugin = WiFiPlugin(plugin_config_no_interface)
        plugin.initialize()

        assert plugin._interface == "wlan0"

    @patch('src.plugins.wifi_plugin.Path')
    def test_initialize_auto_detects_interface_sysfs(self, mock_path_class, plugin_config_no_interface):
        """Test initialize auto-detects interface via /sys/class/net"""
        # Mock /sys/class/net detection
        net_path = MagicMock()
        wlan0_path = MagicMock()
        wlan0_path.name = "wlan0"
        wireless_path = MagicMock()
        wireless_path.exists.return_value = True
        wlan0_path.__truediv__ = Mock(return_value=wireless_path)

        net_path.exists.return_value = True
        net_path.iterdir.return_value = [wlan0_path]

        mock_path_class.return_value = net_path

        with patch('src.plugins.wifi_plugin.subprocess.run', side_effect=FileNotFoundError):
            plugin = WiFiPlugin(plugin_config_no_interface)

            # Mock method detection
            with patch.object(plugin, '_has_nmcli', return_value=False):
                with patch.object(plugin, '_has_iwconfig', return_value=True):
                    plugin.initialize()

                    assert plugin._interface == "wlan0"

    def test_initialize_raises_if_no_interface_found(self, plugin_config_no_interface):
        """Test initialize raises RuntimeError if no interface detected"""
        plugin = WiFiPlugin(plugin_config_no_interface)

        with patch('src.plugins.wifi_plugin.subprocess.run', side_effect=FileNotFoundError):
            with patch('src.plugins.wifi_plugin.Path') as mock_path:
                mock_path.return_value.exists.return_value = False

                with pytest.raises(RuntimeError, match="No WiFi interface detected"):
                    plugin.initialize()

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_initialize_detects_nmcli_method(self, mock_run, plugin_config):
        """Test initialize detects nmcli as preferred method"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        assert plugin._method == 'nmcli'

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_initialize_falls_back_to_iwconfig(self, mock_run, plugin_config):
        """Test initialize falls back to iwconfig if nmcli unavailable"""
        # nmcli unavailable, iwconfig available
        mock_run.side_effect = [
            FileNotFoundError(),  # nmcli --version
            Mock(returncode=0, stdout="", stderr="")  # iwconfig
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        assert plugin._method == 'iwconfig'

    @patch('src.plugins.wifi_plugin.subprocess.run')
    @patch('src.plugins.wifi_plugin.Path')
    def test_initialize_falls_back_to_proc(self, mock_path_class, mock_run, plugin_config):
        """Test initialize falls back to /proc/net/wireless"""
        # nmcli and iwconfig unavailable
        mock_run.side_effect = FileNotFoundError()

        # /proc/net/wireless available
        proc_path = MagicMock()
        proc_path.exists.return_value = True
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        assert plugin._method == 'proc'

    @patch('src.plugins.wifi_plugin.subprocess.run')
    @patch('src.plugins.wifi_plugin.Path')
    def test_initialize_raises_if_no_method_available(self, mock_path_class, mock_run, plugin_config):
        """Test initialize raises RuntimeError if no method available"""
        mock_run.side_effect = FileNotFoundError()

        # No /proc/net/wireless
        proc_path = MagicMock()
        proc_path.exists.return_value = False
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(plugin_config)

        with pytest.raises(RuntimeError, match="No WiFi monitoring method available"):
            plugin.initialize()


# ============================================================================
# DATA COLLECTION TESTS - NMCLI METHOD
# ============================================================================

class TestWiFiPluginNmcliCollection:
    """Test WiFiPlugin nmcli data collection"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_nmcli_returns_connected_data(self, mock_run, plugin_config):
        """Test _collect_nmcli returns data when connected"""
        # Mock nmcli output for connected WiFi
        # Note: Using BSSID format without colons to avoid split() issues
        nmcli_output = "yes:MyNetwork:AABBCCDDEEFF:6:2437:75:WPA2\n"

        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # _has_nmcli check (initialization)
            Mock(returncode=0, stdout=nmcli_output, stderr=""),  # nmcli device wifi list (collection)
            Mock(returncode=0, stdout="Bit Rate=54 Mb/s", stderr="")  # _get_bitrate_iwconfig
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "MyNetwork"
        assert data["bssid"] == "AABBCCDDEEFF"
        assert data["channel"] == 6
        assert data["frequency_mhz"] == 2437
        assert data["signal_strength_percent"] == 75
        assert data["security"] == "WPA2"
        assert data["bitrate_mbps"] == 54.0
        assert data["interface"] == "wlan0"

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_nmcli_returns_disconnected_data(self, mock_run, plugin_config):
        """Test _collect_nmcli returns disconnected data when not connected"""
        # No active connection in nmcli output
        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # initialization
            Mock(returncode=0, stdout="no:MyNetwork:AA:BB:CC:DD:EE:FF:6:2437:75:WPA2\n", stderr="")
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "Not Connected"
        assert data["signal_strength_dbm"] == -100
        assert data["signal_strength_percent"] == 0

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_nmcli_handles_timeout(self, mock_run, plugin_config):
        """Test _collect_nmcli handles subprocess timeout"""
        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # _has_nmcli check
            subprocess.TimeoutExpired(cmd="nmcli", timeout=2)  # collection timeout
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "Not Connected"

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_nmcli_converts_signal_percentage(self, mock_run, plugin_config):
        """Test _collect_nmcli converts signal percentage to dBm"""
        nmcli_output = "yes:MyNetwork:AABBCCDDEEFF:6:2437:80:WPA2\n"

        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # _has_nmcli check
            Mock(returncode=0, stdout=nmcli_output, stderr=""),  # nmcli device wifi list
            Mock(returncode=0, stdout="", stderr="")  # _get_bitrate_iwconfig
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        # 80% -> -60 dBm (via _percent_to_dbm)
        assert data["signal_strength_percent"] == 80
        assert data["signal_strength_dbm"] == -60


# ============================================================================
# DATA COLLECTION TESTS - IWCONFIG METHOD
# ============================================================================

class TestWiFiPluginIwconfigCollection:
    """Test WiFiPlugin iwconfig data collection"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_iwconfig_returns_connected_data(self, mock_run, plugin_config):
        """Test _collect_iwconfig parses iwconfig output correctly"""
        iwconfig_output = '''wlan0     IEEE 802.11  ESSID:"TestNetwork"
                  Mode:Managed  Frequency:2.437 GHz  Access Point: AA:BB:CC:DD:EE:FF
                  Bit Rate=54 Mb/s   Tx-Power=20 dBm
                  Link Quality=50/70  Signal level=-45 dBm
                  Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0'''

        mock_run.side_effect = [
            FileNotFoundError(),  # nmcli unavailable
            Mock(returncode=0, stdout="", stderr=""),  # iwconfig available
            Mock(returncode=0, stdout=iwconfig_output, stderr="")  # collection
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "TestNetwork"
        assert data["bssid"] == "AA:BB:CC:DD:EE:FF"
        assert data["frequency_mhz"] == 2437
        assert data["channel"] == 6  # 2437 MHz = channel 6
        assert data["bitrate_mbps"] == 54.0
        assert data["signal_strength_dbm"] == -45
        assert data["link_quality"] == 71  # (50/70) * 100

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_iwconfig_handles_missing_fields(self, mock_run, plugin_config):
        """Test _collect_iwconfig handles missing regex matches"""
        # Empty ESSID - regex will match but extract empty string
        iwconfig_output = 'wlan0     IEEE 802.11  ESSID:off/any'

        mock_run.side_effect = [
            FileNotFoundError(),  # _has_nmcli
            Mock(returncode=0, stdout="", stderr=""),  # _has_iwconfig
            Mock(returncode=0, stdout=iwconfig_output, stderr="")  # iwconfig collection
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "Unknown"
        assert data["bssid"] == "00:00:00:00:00:00"
        assert data["frequency_mhz"] == 0
        assert data["bitrate_mbps"] == 0.0
        assert data["signal_strength_dbm"] == -100

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_collect_iwconfig_handles_timeout(self, mock_run, plugin_config):
        """Test _collect_iwconfig handles subprocess timeout"""
        import subprocess as subprocess_module

        mock_run.side_effect = [
            FileNotFoundError(),  # nmcli
            Mock(returncode=0, stdout="", stderr=""),  # iwconfig available
            subprocess_module.TimeoutExpired(cmd="iwconfig", timeout=2)
        ]

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        data = plugin.collect_data()

        assert data["ssid"] == "Not Connected"


# ============================================================================
# DATA COLLECTION TESTS - PROC METHOD
# ============================================================================

class TestWiFiPluginProcCollection:
    """Test WiFiPlugin /proc/net/wireless collection"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    @patch('src.plugins.wifi_plugin.Path')
    def test_collect_proc_reads_wireless_file(self, mock_path_class, mock_run, plugin_config):
        """Test _collect_proc reads /proc/net/wireless"""
        proc_content = '''Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
 face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
wlan0: 0000   50.  -45.    0.       0      0      0      0      0        0
'''

        # Mock initialization: nmcli and iwconfig unavailable
        mock_run.side_effect = FileNotFoundError()

        # /proc/net/wireless available
        proc_path = MagicMock()
        proc_path.exists.return_value = True
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        # Mock file read
        with patch('builtins.open', mock_open(read_data=proc_content)):
            data = plugin.collect_data()

        assert data["signal_strength_dbm"] == -45
        assert data["link_quality"] == 50
        assert data["interface"] == "wlan0"

    @patch('src.plugins.wifi_plugin.subprocess.run')
    @patch('src.plugins.wifi_plugin.Path')
    def test_collect_proc_handles_quality_format(self, mock_path_class, mock_run, plugin_config):
        """Test _collect_proc converts quality (0-70) to dBm"""
        # Quality format (positive numbers)
        proc_content = '''Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
 face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
wlan0: 0000   50.   60.    0.       0      0      0      0      0        0
'''

        mock_run.side_effect = FileNotFoundError()
        proc_path = MagicMock()
        proc_path.exists.return_value = True
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        with patch('builtins.open', mock_open(read_data=proc_content)):
            data = plugin.collect_data()

        # level=60 (positive) -> convert: -100 + 50 = -50 dBm
        assert data["signal_strength_dbm"] == -50

    @patch('src.plugins.wifi_plugin.subprocess.run')
    @patch('src.plugins.wifi_plugin.Path')
    def test_collect_proc_handles_file_not_found(self, mock_path_class, mock_run, plugin_config):
        """Test _collect_proc handles missing /proc/net/wireless"""
        mock_run.side_effect = FileNotFoundError()
        proc_path = MagicMock()
        proc_path.exists.return_value = True
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()

        with patch('builtins.open', side_effect=FileNotFoundError):
            data = plugin.collect_data()

        assert data["ssid"] == "Not Connected"


# ============================================================================
# CONVERSION TESTS
# ============================================================================

class TestWiFiPluginConversions:
    """Test WiFiPlugin conversion functions"""

    def test_dbm_to_percent_boundary_cases(self):
        """Test _dbm_to_percent boundary values"""
        assert WiFiPlugin._dbm_to_percent(-50) == 100
        assert WiFiPlugin._dbm_to_percent(-40) == 100  # Better than -50
        assert WiFiPlugin._dbm_to_percent(-100) == 0
        assert WiFiPlugin._dbm_to_percent(-110) == 0  # Worse than -100

    def test_dbm_to_percent_midrange(self):
        """Test _dbm_to_percent midrange values"""
        # -75 dBm -> 2 * (-75 + 100) = 2 * 25 = 50%
        assert WiFiPlugin._dbm_to_percent(-75) == 50

        # -60 dBm -> 2 * (-60 + 100) = 2 * 40 = 80%
        assert WiFiPlugin._dbm_to_percent(-60) == 80

    def test_percent_to_dbm_boundary_cases(self):
        """Test _percent_to_dbm boundary values"""
        assert WiFiPlugin._percent_to_dbm(100) == -50
        assert WiFiPlugin._percent_to_dbm(110) == -50  # Clamped
        assert WiFiPlugin._percent_to_dbm(0) == -100
        assert WiFiPlugin._percent_to_dbm(-10) == -100  # Clamped

    def test_percent_to_dbm_midrange(self):
        """Test _percent_to_dbm midrange values"""
        # 50% -> (50 / 2) - 100 = 25 - 100 = -75 dBm
        assert WiFiPlugin._percent_to_dbm(50) == -75

        # 80% -> (80 / 2) - 100 = 40 - 100 = -60 dBm
        assert WiFiPlugin._percent_to_dbm(80) == -60

    def test_dbm_percent_roundtrip(self):
        """Test dbm <-> percent conversion is reversible"""
        for dbm in [-50, -60, -75, -90, -100]:
            percent = WiFiPlugin._dbm_to_percent(dbm)
            roundtrip_dbm = WiFiPlugin._percent_to_dbm(percent)
            assert roundtrip_dbm == dbm

    def test_freq_to_channel_2_4ghz(self):
        """Test _freq_to_channel for 2.4 GHz band"""
        assert WiFiPlugin._freq_to_channel(2412) == 1   # Channel 1
        assert WiFiPlugin._freq_to_channel(2437) == 6   # Channel 6
        assert WiFiPlugin._freq_to_channel(2462) == 11  # Channel 11
        assert WiFiPlugin._freq_to_channel(2484) == 14  # Channel 14 (Japan)

    def test_freq_to_channel_5ghz(self):
        """Test _freq_to_channel for 5 GHz band"""
        assert WiFiPlugin._freq_to_channel(5180) == 36   # Channel 36
        assert WiFiPlugin._freq_to_channel(5200) == 40   # Channel 40
        assert WiFiPlugin._freq_to_channel(5745) == 149  # Channel 149
        assert WiFiPlugin._freq_to_channel(5825) == 165  # Channel 165

    def test_freq_to_channel_unknown(self):
        """Test _freq_to_channel for unknown frequencies"""
        assert WiFiPlugin._freq_to_channel(1000) == 0   # Too low
        assert WiFiPlugin._freq_to_channel(10000) == 0  # Too high
        assert WiFiPlugin._freq_to_channel(3000) == 0   # Between bands


# ============================================================================
# HELPER METHOD TESTS
# ============================================================================

class TestWiFiPluginHelpers:
    """Test WiFiPlugin helper methods"""

    def test_detect_wifi_interface_nmcli(self):
        """Test _detect_wifi_interface via nmcli"""
        mock_run = Mock(returncode=0, stdout="wlan0:wifi\neth0:ethernet\n", stderr="")

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={}))

        with patch('src.plugins.wifi_plugin.subprocess.run', return_value=mock_run):
            interface = plugin._detect_wifi_interface()

        assert interface == "wlan0"

    def test_detect_wifi_interface_nmcli_timeout(self):
        """Test _detect_wifi_interface handles nmcli timeout"""
        plugin = WiFiPlugin(PluginConfig(name="wifi", config={}))

        with patch('src.plugins.wifi_plugin.subprocess.run',
                   side_effect=subprocess.TimeoutExpired(cmd="nmcli", timeout=2)):
            with patch('src.plugins.wifi_plugin.Path') as mock_path:
                mock_path.return_value.exists.return_value = False
                interface = plugin._detect_wifi_interface()

        assert interface is None

    @patch('src.plugins.wifi_plugin.Path')
    def test_detect_wifi_interface_sysfs(self, mock_path_class):
        """Test _detect_wifi_interface via /sys/class/net"""
        net_path = MagicMock()
        wlan0_path = MagicMock()
        wlan0_path.name = "wlan0"
        wireless_path = MagicMock()
        wireless_path.exists.return_value = True
        wlan0_path.__truediv__ = Mock(return_value=wireless_path)

        net_path.exists.return_value = True
        net_path.iterdir.return_value = [wlan0_path]
        mock_path_class.return_value = net_path

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={}))

        with patch('src.plugins.wifi_plugin.subprocess.run', side_effect=FileNotFoundError):
            interface = plugin._detect_wifi_interface()

        assert interface == "wlan0"

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_has_nmcli_true(self, mock_run):
        """Test _has_nmcli returns True when nmcli available"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_nmcli() is True

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_has_nmcli_false(self, mock_run):
        """Test _has_nmcli returns False when nmcli unavailable"""
        mock_run.side_effect = FileNotFoundError()

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_nmcli() is False

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_has_iwconfig_true(self, mock_run):
        """Test _has_iwconfig returns True when iwconfig available"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_iwconfig() is True

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_has_iwconfig_false(self, mock_run):
        """Test _has_iwconfig returns False when iwconfig unavailable"""
        mock_run.side_effect = FileNotFoundError()

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_iwconfig() is False

    @patch('src.plugins.wifi_plugin.Path')
    def test_has_proc_wireless_true(self, mock_path_class):
        """Test _has_proc_wireless returns True when file exists"""
        proc_path = MagicMock()
        proc_path.exists.return_value = True
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_proc_wireless() is True

    @patch('src.plugins.wifi_plugin.Path')
    def test_has_proc_wireless_false(self, mock_path_class):
        """Test _has_proc_wireless returns False when file doesn't exist"""
        proc_path = MagicMock()
        proc_path.exists.return_value = False
        mock_path_class.return_value = proc_path

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))

        assert plugin._has_proc_wireless() is False

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_get_bitrate_iwconfig_success(self, mock_run):
        """Test _get_bitrate_iwconfig extracts bitrate"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Bit Rate=72.2 Mb/s   Tx-Power=20 dBm",
            stderr=""
        )

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))
        plugin._interface = "wlan0"

        bitrate = plugin._get_bitrate_iwconfig()

        assert bitrate == 72.2

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_get_bitrate_iwconfig_failure(self, mock_run):
        """Test _get_bitrate_iwconfig returns 0.0 on error"""
        mock_run.side_effect = Exception("Command failed")

        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))
        plugin._interface = "wlan0"

        bitrate = plugin._get_bitrate_iwconfig()

        assert bitrate == 0.0

    def test_disconnected_data(self):
        """Test _disconnected_data returns correct structure"""
        plugin = WiFiPlugin(PluginConfig(name="wifi", config={"interface": "wlan0"}))
        plugin._interface = "wlan0"

        data = plugin._disconnected_data()

        assert data["ssid"] == "Not Connected"
        assert data["signal_strength_dbm"] == -100
        assert data["signal_strength_percent"] == 0
        assert data["bssid"] == "00:00:00:00:00:00"
        assert data["channel"] == 0
        assert data["frequency_mhz"] == 0
        assert data["link_quality"] == 0
        assert data["bitrate_mbps"] == 0.0
        assert data["security"] == "None"
        assert data["interface"] == "wlan0"


# ============================================================================
# CLEANUP TESTS
# ============================================================================

class TestWiFiPluginCleanup:
    """Test WiFiPlugin cleanup"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_cleanup_sets_stopped_status(self, mock_run, plugin_config):
        """Test cleanup sets status to STOPPED"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        plugin = WiFiPlugin(plugin_config)
        plugin.initialize()
        plugin.cleanup()

        assert plugin.status == PluginStatus.STOPPED


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestWiFiPluginIntegration:
    """Test WiFiPlugin full lifecycle"""

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_full_lifecycle_nmcli(self, mock_run, plugin_config):
        """Test complete plugin lifecycle with nmcli"""
        nmcli_output = "yes:TestNet:AABBCCDDEEFF:11:2462:90:WPA3\n"

        mock_run.side_effect = [
            Mock(returncode=0, stdout="", stderr=""),  # _has_nmcli (initialization)
            Mock(returncode=0, stdout=nmcli_output, stderr=""),  # nmcli device wifi list
            Mock(returncode=0, stdout="Bit Rate=65 Mb/s", stderr="")  # _get_bitrate_iwconfig
        ]

        plugin = WiFiPlugin(plugin_config)

        # Initialize
        assert plugin.status == PluginStatus.UNINITIALIZED
        plugin.initialize()
        assert plugin.status == PluginStatus.READY
        assert plugin._method == 'nmcli'

        # Collect data
        data = plugin.collect_data()
        assert data["ssid"] == "TestNet"
        assert data["channel"] == 11
        assert data["signal_strength_percent"] == 90

        # Cleanup
        plugin.cleanup()
        assert plugin.status == PluginStatus.STOPPED

    @patch('src.plugins.wifi_plugin.subprocess.run')
    def test_full_lifecycle_iwconfig(self, mock_run, plugin_config):
        """Test complete plugin lifecycle with iwconfig"""
        iwconfig_output = '''wlan0     IEEE 802.11  ESSID:"MyWiFi"
                  Frequency:5.18 GHz  Access Point: 11:22:33:44:55:66
                  Bit Rate=300 Mb/s   Signal level=-50 dBm'''

        mock_run.side_effect = [
            FileNotFoundError(),  # nmcli unavailable
            Mock(returncode=0, stdout="", stderr=""),  # iwconfig available
            Mock(returncode=0, stdout=iwconfig_output, stderr="")  # collect
        ]

        plugin = WiFiPlugin(plugin_config)

        # Initialize
        plugin.initialize()
        assert plugin._method == 'iwconfig'

        # Collect data
        data = plugin.collect_data()
        assert data["ssid"] == "MyWiFi"
        assert data["bssid"] == "11:22:33:44:55:66"
        assert data["frequency_mhz"] == 5180
        assert data["channel"] == 36  # 5180 MHz = channel 36
        assert data["bitrate_mbps"] == 300.0
        assert data["signal_strength_dbm"] == -50

        # Cleanup
        plugin.cleanup()
        assert plugin.status == PluginStatus.STOPPED
