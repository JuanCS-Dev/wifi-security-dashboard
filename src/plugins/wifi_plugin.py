"""
WiFi metrics plugin for educational purposes.

Collects WiFi signal strength, SSID, channel, and security information.
Uses multiple methods for cross-platform compatibility:
1. nmcli (NetworkManager) - preferred on modern Linux
2. iwconfig - fallback for older systems
3. /proc/net/wireless - last resort for basic metrics

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from typing import Dict, Any, Optional
import subprocess
import re
from pathlib import Path

from .base import Plugin, PluginConfig, PluginStatus


class WiFiPlugin(Plugin):
    """
    WiFi metrics collection plugin.

    Provides real-time WiFi metrics for educational purposes:
    - Signal strength (dBm and percentage)
    - SSID and BSSID
    - Channel and frequency
    - Link quality
    - Bitrate
    - Security type (for educational demonstrations)

    Data Fields:
        signal_strength_dbm: Signal strength in dBm (-100 to 0)
        signal_strength_percent: Signal quality percentage (0-100)
        ssid: Network SSID (name)
        bssid: Access Point MAC address
        channel: WiFi channel (1-13 for 2.4GHz, 36+ for 5GHz)
        frequency_mhz: Frequency in MHz
        link_quality: Link quality (0-70 or 0-100 depending on driver)
        bitrate_mbps: Current bitrate in Mbps
        security: Security type (WPA2, WPA3, etc.)
        interface: WiFi interface name

    Example:
        >>> config = PluginConfig(name="wifi", rate_ms=500)
        >>> plugin = WiFiPlugin(config)
        >>> plugin.initialize()
        >>> data = plugin.collect_data()
        >>> print(f"Signal: {data['signal_strength_dbm']} dBm")
        Signal: -45 dBm
    """

    def initialize(self) -> None:
        """
        Initialize WiFi plugin.

        Detects available WiFi tools and interface.
        Priority: nmcli > iwconfig > /proc/net/wireless

        In mock mode, skips tool detection and uses MockDataGenerator.
        """
        # Check if running in mock mode
        self._mock_mode = self.config.config.get('mock_mode', False)

        if self._mock_mode:
            # Mock mode: use MockDataGenerator
            from src.utils.mock_data_generator import get_mock_generator
            self._mock_generator = get_mock_generator()
            self._status = PluginStatus.READY
            return

        # Real mode: Get WiFi interface from config or auto-detect
        interface = self.config.config.get('interface', None)

        if interface:
            self._interface = interface
        else:
            # Auto-detect WiFi interface
            self._interface = self._detect_wifi_interface()
            if not self._interface:
                raise RuntimeError(
                    "No WiFi interface detected. Please specify 'interface' in config."
                )

        # Detect available method
        if self._has_nmcli():
            self._method = 'nmcli'
        elif self._has_iwconfig():
            self._method = 'iwconfig'
        elif self._has_proc_wireless():
            self._method = 'proc'
        else:
            raise RuntimeError(
                "No WiFi monitoring method available. WiFiPlugin requires one of:\n"
                "  1. nmcli (NetworkManager) - Recommended\n"
                "     Ubuntu/Debian: sudo apt-get install network-manager\n"
                "     Fedora/RHEL: sudo dnf install NetworkManager\n"
                "  2. iwconfig (wireless-tools) - Legacy fallback\n"
                "     Ubuntu/Debian: sudo apt-get install wireless-tools\n"
                "  3. /proc/net/wireless - Minimal Linux kernel interface\n"
                "\n"
                f"Detected interface: {self._interface}\n"
                "None of the above methods were found on this system."
            )

        self._status = PluginStatus.READY

    def collect_data(self) -> Dict[str, Any]:
        """
        Collect WiFi metrics.

        In mock mode, returns simulated data from MockDataGenerator.

        Returns:
            Dictionary with WiFi metrics

        Note:
            Returns partial data if some metrics unavailable.
        """
        # Mock mode: return simulated data
        if self._mock_mode:
            return self._mock_generator.get_wifi_info()

        # Real mode: collect from system
        if self._method == 'nmcli':
            return self._collect_nmcli()
        elif self._method == 'iwconfig':
            return self._collect_iwconfig()
        else:
            return self._collect_proc()

    def _detect_wifi_interface(self) -> Optional[str]:
        """
        Auto-detect WiFi interface.

        Returns:
            WiFi interface name (e.g., 'wlan0', 'wlp2s0') or None
        """
        try:
            # Try nmcli
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'DEVICE,TYPE', 'device'],
                capture_output=True,
                text=True,
                timeout=2
            )
            for line in result.stdout.splitlines():
                device, dev_type = line.split(':', 1)
                if dev_type == 'wifi':
                    return device
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Try /sys/class/net
        net_path = Path('/sys/class/net')
        if net_path.exists():
            for iface in net_path.iterdir():
                wireless_path = iface / 'wireless'
                if wireless_path.exists():
                    return iface.name

        return None

    def _has_nmcli(self) -> bool:
        """Check if nmcli is available"""
        try:
            subprocess.run(['nmcli', '--version'], capture_output=True, timeout=1)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _has_iwconfig(self) -> bool:
        """Check if iwconfig is available"""
        try:
            subprocess.run(['iwconfig'], capture_output=True, timeout=1)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _has_proc_wireless(self) -> bool:
        """Check if /proc/net/wireless is available"""
        return Path('/proc/net/wireless').exists()

    def _collect_nmcli(self) -> Dict[str, Any]:
        """
        Collect WiFi data using nmcli.

        NetworkManager provides comprehensive WiFi information.
        Strategy: Parse BSSID by rejoining split colon-separated hex parts.
        The asterisk (*) in IN-USE column marks the currently connected network.
        
        Research: nmcli doesn't support --escape in all versions, so we rejoin BSSID parts.
        """
        try:
            # Get WiFi list with IN-USE marker for active connection
            # Note: Increase timeout to 5s as wifi scanning can be slow
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'IN-USE,SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY,RATE',
                 'device', 'wifi', 'list', 'ifname', self._interface],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse output and find line starting with '*' (active connection)
            # Format: "IN-USE:SSID:BSSID_P1:\:BSSID_P2:\:...:CHAN:FREQ:SIGNAL:SECURITY:RATE"
            # BSSID has colons that split() breaks into 6 parts
            # Example: "*:Maximus:38\:16\:5A\:69\:0C\:F9:44:5220 MHz:71:WPA2 WPA3:270 Mbit/s"
            # After split: ['*', 'Maximus', '38\\', '16\\', '5A\\', '69\\', '0C\\', 'F9', '44', '5220 MHz', '71', 'WPA2 WPA3', '270 Mbit/s']
            for line in result.stdout.splitlines():
                if not line or not line.strip():
                    continue
                
                # Check if this line has '*' at start (active connection)
                if line.startswith('*'):
                    parts = line.split(':')
                    
                    # BSSID is split into 6 parts (5 colons), so total should be at least 13
                    # IN-USE(1) + SSID(1) + BSSID(6) + CHAN(1) + FREQ(1) + SIGNAL(1) + SECURITY(1) + RATE(1) = 13
                    if len(parts) >= 13:
                        in_use = parts[0]                    # '*'
                        ssid = parts[1]                      # SSID
                        bssid = ':'.join(parts[2:8])         # Rejoin BSSID from 6 hex parts
                        channel = parts[8]                   # Channel
                        freq = parts[9]                      # Frequency (with ' MHz')
                        signal = parts[10]                   # Signal percentage
                        security = parts[11]                 # Security type
                        rate = parts[12] if len(parts) > 12 else ''  # Bitrate
                        
                        # Parse signal strength (as percentage)
                        try:
                            signal_percent = int(signal)
                        except ValueError:
                            signal_percent = 0
                        
                        # Convert signal from percentage to dBm (approximate)
                        # Formula: dBm ≈ (percentage / 2) - 100
                        signal_dbm = self._percent_to_dbm(signal_percent)
                        
                        # Parse bitrate (e.g., "270 Mbit/s" -> 270.0)
                        try:
                            bitrate_mbps = float(rate.split()[0]) if rate and rate.split() else 0.0
                        except (ValueError, IndexError):
                            bitrate_mbps = 0.0
                        
                        # Parse channel
                        try:
                            channel_int = int(channel)
                        except ValueError:
                            channel_int = 0
                        
                        # Parse frequency (remove ' MHz' suffix)
                        try:
                            freq_str = freq.replace(' MHz', '').strip()
                            freq_int = int(freq_str) if freq_str else 0
                        except ValueError:
                            freq_int = 0

                        return {
                            "signal_strength_dbm": signal_dbm,
                            "signal_strength_percent": signal_percent,
                            "ssid": ssid if ssid else "Unknown",
                            "bssid": bssid if bssid else "00:00:00:00:00:00",
                            "channel": channel_int,
                            "frequency_mhz": freq_int,
                            "link_quality": signal_percent,
                            "bitrate_mbps": bitrate_mbps,
                            "security": security if security else "Open",
                            "interface": self._interface,
                        }

            # No active connection found (no line starting with '*')
            return self._disconnected_data()

        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            return self._disconnected_data()

    def _collect_iwconfig(self) -> Dict[str, Any]:
        """
        Collect WiFi data using iwconfig.

        Legacy tool, but widely available.
        """
        try:
            result = subprocess.run(
                ['iwconfig', self._interface],
                capture_output=True,
                text=True,
                timeout=2
            )

            output = result.stdout

            # Parse output with regex
            ssid_match = re.search(r'ESSID:"([^"]*)"', output)
            bssid_match = re.search(r'Access Point: ([0-9A-Fa-f:]+)', output)
            freq_match = re.search(r'Frequency:([0-9.]+) GHz', output)
            bitrate_match = re.search(r'Bit Rate=([0-9.]+) Mb/s', output)
            signal_match = re.search(r'Signal level=(-?[0-9]+) dBm', output)
            quality_match = re.search(r'Link Quality=([0-9]+)/([0-9]+)', output)

            ssid = ssid_match.group(1) if ssid_match else "Unknown"
            bssid = bssid_match.group(1) if bssid_match else "00:00:00:00:00:00"

            # Frequency to channel approximation
            if freq_match:
                freq_ghz = float(freq_match.group(1))
                frequency_mhz = int(freq_ghz * 1000)
                channel = self._freq_to_channel(frequency_mhz)
            else:
                frequency_mhz = 0
                channel = 0

            bitrate_mbps = float(bitrate_match.group(1)) if bitrate_match else 0.0

            if signal_match:
                signal_dbm = int(signal_match.group(1))
                signal_percent = self._dbm_to_percent(signal_dbm)
            else:
                signal_dbm = -100
                signal_percent = 0

            if quality_match:
                quality_num = int(quality_match.group(1))
                quality_max = int(quality_match.group(2))
                link_quality = int((quality_num / quality_max) * 100)
            else:
                link_quality = signal_percent

            return {
                "signal_strength_dbm": signal_dbm,
                "signal_strength_percent": signal_percent,
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "frequency_mhz": frequency_mhz,
                "link_quality": link_quality,
                "bitrate_mbps": bitrate_mbps,
                "security": "Unknown",  # iwconfig doesn't show security type
                "interface": self._interface,
            }

        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            return self._disconnected_data()

    def _collect_proc(self) -> Dict[str, Any]:
        """
        Collect WiFi data from /proc/net/wireless.

        Minimal data, but always available on Linux.
        """
        try:
            with open('/proc/net/wireless', 'r') as f:
                lines = f.readlines()

            # Find line for our interface
            for line in lines[2:]:  # Skip header lines
                if line.strip().startswith(self._interface):
                    parts = line.split()
                    # Format: iface status quality level noise
                    quality = int(parts[2].rstrip('.'))
                    level = int(parts[3].rstrip('.'))

                    # /proc/net/wireless shows quality as 0-70 or signal in dBm
                    if level < 0:
                        # Already in dBm
                        signal_dbm = level
                    else:
                        # Convert from quality (0-70) to dBm
                        signal_dbm = -100 + quality

                    signal_percent = self._dbm_to_percent(signal_dbm)

                    return {
                        "signal_strength_dbm": signal_dbm,
                        "signal_strength_percent": signal_percent,
                        "ssid": "Unknown",
                        "bssid": "00:00:00:00:00:00",
                        "channel": 0,
                        "frequency_mhz": 0,
                        "link_quality": quality,
                        "bitrate_mbps": 0.0,
                        "security": "Unknown",
                        "interface": self._interface,
                    }

            return self._disconnected_data()

        except (FileNotFoundError, ValueError, IndexError):
            return self._disconnected_data()

    def _get_bitrate_iwconfig(self) -> float:
        """Get bitrate from iwconfig (helper for nmcli method)"""
        try:
            result = subprocess.run(
                ['iwconfig', self._interface],
                capture_output=True,
                text=True,
                timeout=1
            )
            match = re.search(r'Bit Rate=([0-9.]+) Mb/s', result.stdout)
            return float(match.group(1)) if match else 0.0
        except:
            return 0.0

    def _disconnected_data(self) -> Dict[str, Any]:
        """Return data for disconnected state"""
        return {
            "signal_strength_dbm": -100,
            "signal_strength_percent": 0,
            "ssid": "Not Connected",
            "bssid": "00:00:00:00:00:00",
            "channel": 0,
            "frequency_mhz": 0,
            "link_quality": 0,
            "bitrate_mbps": 0.0,
            "security": "None",
            "interface": self._interface,
        }

    @staticmethod
    def _dbm_to_percent(dbm: int) -> int:
        """
        Convert dBm to percentage (0-100).

        Formula: approximate mapping where:
        - -100 dBm or worse = 0%
        - -50 dBm or better = 100%
        """
        if dbm >= -50:
            return 100
        elif dbm <= -100:
            return 0
        else:
            return int(2 * (dbm + 100))

    @staticmethod
    def _percent_to_dbm(percent: int) -> int:
        """
        Convert percentage (0-100) to dBm.

        Inverse of _dbm_to_percent.
        """
        if percent >= 100:
            return -50
        elif percent <= 0:
            return -100
        else:
            return int((percent / 2) - 100)

    @staticmethod
    def _freq_to_channel(freq_mhz: int) -> int:
        """
        Convert frequency (MHz) to WiFi channel.

        Supports 2.4GHz (channels 1-14) and 5GHz (channels 36-165).
        """
        if 2412 <= freq_mhz <= 2484:
            # 2.4 GHz band
            if freq_mhz == 2484:
                return 14
            else:
                return (freq_mhz - 2407) // 5
        elif 5160 <= freq_mhz <= 5885:
            # 5 GHz band
            return (freq_mhz - 5000) // 5
        else:
            return 0  # Unknown

    def cleanup(self) -> None:
        """
        Cleanup WiFi plugin.

        No persistent resources to clean up.
        """
        self._status = PluginStatus.STOPPED
