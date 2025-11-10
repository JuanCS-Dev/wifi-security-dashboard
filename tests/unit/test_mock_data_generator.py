"""
Scientific tests for MockDataGenerator.

Tests realistic, cohesive educational data generation with focus on:
- Data ranges and validity
- Natural variations (not chaotic)
- Temporal consistency
- Device-app-traffic correlation
- Educational clarity

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import pytest
import time
from src.utils.mock_data_generator import (
    MockDataGenerator,
    MockDevice,
    get_mock_generator
)


class TestMockDevice:
    """Test MockDevice dataclass"""

    def test_mock_device_creation(self):
        """Test creating a mock device with realistic data"""
        device = MockDevice(
            mac="AA:BB:CC:DD:EE:01",
            ip="192.168.1.101",
            hostname="Dad-Phone",
            type="smartphone",
            owner="Pai",
            baseline_download=0.5,
            baseline_upload=0.1,
            current_app="WhatsApp"
        )

        assert device.mac == "AA:BB:CC:DD:EE:01"
        assert device.ip == "192.168.1.101"
        assert device.hostname == "Dad-Phone"
        assert device.type == "smartphone"
        assert device.owner == "Pai"
        assert device.is_active is True
        assert device.baseline_download == 0.5
        assert device.baseline_upload == 0.1
        assert device.current_app == "WhatsApp"


class TestMockDataGeneratorInitialization:
    """Test MockDataGenerator initialization"""

    def test_generator_initialization(self):
        """Test generator creates family scenario"""
        gen = MockDataGenerator()

        assert gen.devices is not None
        assert len(gen.devices) == 6  # Family of 4 + 2 shared devices
        assert gen.wifi_info is not None
        assert gen._start_time > 0
        assert gen._cycle_time == 0.0

    def test_family_devices_created(self):
        """Test all family devices are present"""
        gen = MockDataGenerator()

        # Check we have expected device types
        types = [d.type for d in gen.devices]
        assert "smartphone" in types
        assert "laptop" in types
        assert "tablet" in types
        assert "smart_tv" in types

        # Check we have identifiable devices
        hostnames = [d.hostname for d in gen.devices]
        assert any("Dad" in h for h in hostnames)
        assert any("Mom" in h for h in hostnames)
        assert any("Filho" in h or "Filha" in h for h in hostnames)

    def test_wifi_info_created(self):
        """Test WiFi info has realistic values"""
        gen = MockDataGenerator()

        assert gen.wifi_info["ssid"] == "Casa-Familia"
        assert gen.wifi_info["security"] == "WPA2"
        assert gen.wifi_info["frequency"] == 5.0
        assert gen.wifi_info["channel"] == 36
        assert gen.wifi_info["signal_strength"] == -45
        assert gen.wifi_info["link_speed"] == 300


class TestSystemMetrics:
    """Test system metrics generation (scientific validation)"""

    def test_system_metrics_structure(self):
        """Test system metrics has required fields"""
        gen = MockDataGenerator()
        metrics = gen.get_system_metrics()

        required_fields = [
            "cpu_percent", "cpu_count", "ram_percent",
            "ram_total_gb", "ram_used_gb", "disk_percent",
            "disk_total_gb", "disk_used_gb", "temperature_celsius",
            "uptime_seconds"
        ]

        for field in required_fields:
            assert field in metrics, f"Missing field: {field}"

    def test_system_metrics_ranges(self):
        """Test system metrics are within realistic ranges"""
        gen = MockDataGenerator()
        metrics = gen.get_system_metrics()

        # CPU should be reasonable load (not 100%)
        assert 0 <= metrics["cpu_percent"] <= 100
        assert 15 <= metrics["cpu_percent"] <= 50  # Light load

        # RAM should be typical usage
        assert 0 <= metrics["ram_percent"] <= 100
        assert 40 <= metrics["ram_percent"] <= 80  # Normal usage

        # Disk should be stable
        assert 0 <= metrics["disk_percent"] <= 100
        assert metrics["disk_percent"] > 50  # Used disk

        # Temperature should be normal
        assert 30 <= metrics["temperature_celsius"] <= 80

        # CPU count realistic
        assert metrics["cpu_count"] == 8

        # RAM realistic
        assert metrics["ram_total_gb"] == 16.0
        assert 0 < metrics["ram_used_gb"] < metrics["ram_total_gb"]

    def test_system_metrics_natural_variation(self):
        """Test metrics vary naturally (not randomly)"""
        gen = MockDataGenerator()

        samples = []
        for _ in range(10):
            metrics = gen.get_system_metrics()
            samples.append(metrics["cpu_percent"])
            time.sleep(0.05)  # Small delay for cycle update

        # Check variation exists but is bounded
        min_cpu = min(samples)
        max_cpu = max(samples)
        variation = max_cpu - min_cpu

        # Should vary (not fixed)
        assert variation > 0

        # But not wildly (±15% max)
        assert variation < 15, "CPU variation too chaotic"

    def test_system_metrics_uptime_increases(self):
        """Test uptime increases over time"""
        gen = MockDataGenerator()

        uptime1 = gen.get_system_metrics()["uptime_seconds"]
        time.sleep(1.1)  # Sleep more than 1 second to see int change
        uptime2 = gen.get_system_metrics()["uptime_seconds"]

        assert uptime2 > uptime1, "Uptime should increase"
        assert uptime2 - uptime1 >= 1, "Uptime delta realistic"


class TestWiFiInfo:
    """Test WiFi information generation"""

    def test_wifi_info_structure(self):
        """Test WiFi info has required fields"""
        gen = MockDataGenerator()
        info = gen.get_wifi_info()

        required_fields = [
            "ssid", "security", "frequency", "channel",
            "signal_strength", "link_speed"
        ]

        for field in required_fields:
            assert field in info, f"Missing field: {field}"

    def test_wifi_info_values(self):
        """Test WiFi info has realistic values"""
        gen = MockDataGenerator()
        info = gen.get_wifi_info()

        assert info["ssid"] == "Casa-Familia"
        assert info["security"] == "WPA2"
        assert info["frequency"] == 5.0
        assert info["channel"] == 36
        assert info["link_speed"] == 300

    def test_wifi_signal_variation(self):
        """Test WiFi signal varies naturally"""
        gen = MockDataGenerator()

        signals = []
        for _ in range(10):
            info = gen.get_wifi_info()
            signals.append(info["signal_strength"])
            time.sleep(0.05)

        # Signal should be strong (good WiFi)
        # -45 with ±6% variation = -47.7 to -42.3 (rounded to int)
        for sig in signals:
            assert -48 <= sig <= -42, f"Signal should be strong, got {sig}"

        # Should vary slightly (walls, movement)
        min_sig = min(signals)
        max_sig = max(signals)
        variation = max_sig - min_sig

        # Small natural variation
        assert 0 <= variation <= 10, "Signal variation should be small"


class TestNetworkStats:
    """Test network statistics generation"""

    def test_network_stats_structure(self):
        """Test network stats has required fields"""
        gen = MockDataGenerator()
        stats = gen.get_network_stats()

        required_fields = [
            "bandwidth_rx", "bandwidth_tx", "bytes_sent",
            "bytes_recv", "packets_sent", "packets_recv"
        ]

        for field in required_fields:
            assert field in stats, f"Missing field: {field}"

    def test_network_stats_ranges(self):
        """Test network stats are realistic"""
        gen = MockDataGenerator()
        stats = gen.get_network_stats()

        # Bandwidth should be reasonable (home network)
        assert 0 <= stats["bandwidth_rx"] <= 20  # Max ~20 Mbps
        assert 0 <= stats["bandwidth_tx"] <= 5   # Upload lower

        # Download > Upload (typical)
        assert stats["bandwidth_rx"] >= stats["bandwidth_tx"]

        # Bytes and packets should be non-negative
        assert stats["bytes_sent"] >= 0
        assert stats["bytes_recv"] >= 0
        assert stats["packets_sent"] >= 0
        assert stats["packets_recv"] >= 0

    def test_network_stats_consistency(self):
        """Test network traffic is consistent over time"""
        gen = MockDataGenerator()

        # Collect samples
        samples_rx = []
        for _ in range(5):
            stats = gen.get_network_stats()
            samples_rx.append(stats["bandwidth_rx"])
            time.sleep(0.1)

        # Should stay in reasonable range (cohesive, not random)
        avg = sum(samples_rx) / len(samples_rx)
        for sample in samples_rx:
            deviation = abs(sample - avg) / avg if avg > 0 else 0
            assert deviation < 0.3, "Traffic should be stable (±30%)"


class TestDevices:
    """Test device list generation"""

    def test_devices_list_structure(self):
        """Test get_devices returns list of device dicts"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        assert isinstance(devices, list)
        assert len(devices) == 6  # Family devices

    def test_device_fields(self):
        """Test each device has required fields"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        required_fields = [
            "mac", "ip", "hostname", "type", "owner",
            "is_active", "traffic_down_mbps", "traffic_up_mbps",
            "current_app"
        ]

        for device in devices:
            for field in required_fields:
                assert field in device, f"Missing field: {field}"

    def test_device_macs_unique(self):
        """Test all devices have unique MAC addresses"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        macs = [d["mac"] for d in devices]
        assert len(macs) == len(set(macs)), "MACs should be unique"

    def test_device_ips_unique(self):
        """Test all devices have unique IP addresses"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        ips = [d["ip"] for d in devices]
        assert len(ips) == len(set(ips)), "IPs should be unique"

    def test_device_traffic_realistic(self):
        """Test device traffic is realistic"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        for device in devices:
            # Download >= Upload (typical)
            assert device["traffic_down_mbps"] >= device["traffic_up_mbps"]

            # Reasonable ranges
            assert 0 <= device["traffic_down_mbps"] <= 10
            assert 0 <= device["traffic_up_mbps"] <= 2


class TestTopApps:
    """Test top applications generation"""

    def test_top_apps_structure(self):
        """Test get_top_apps returns dict"""
        gen = MockDataGenerator()
        apps = gen.get_top_apps()

        assert isinstance(apps, dict)

    def test_top_apps_realistic(self):
        """Test apps are from known educational apps"""
        gen = MockDataGenerator()
        apps = gen.get_top_apps()

        # Should have common apps
        known_apps = ["Netflix", "YouTube", "WhatsApp", "Instagram", "Gmail"]
        app_names = list(apps.keys())

        # At least some apps should be from known list
        assert any(app in known_apps for app in app_names)

    def test_top_apps_bandwidth(self):
        """Test app bandwidth values are realistic"""
        gen = MockDataGenerator()
        apps = gen.get_top_apps()

        for app, bandwidth in apps.items():
            # Bandwidth should be positive
            assert bandwidth > 0, f"{app} has non-positive bandwidth"

            # Should be reasonable
            assert bandwidth < 15, f"{app} bandwidth too high"

    def test_top_apps_correlation(self):
        """Test app traffic correlates with device traffic"""
        gen = MockDataGenerator()

        # Get device traffic
        devices = gen.get_devices()
        total_device_traffic = sum(d["traffic_down_mbps"] for d in devices if d["is_active"])

        # Get app traffic
        apps = gen.get_top_apps()
        total_app_traffic = sum(apps.values())

        # Should be similar (apps are running on devices)
        ratio = total_app_traffic / total_device_traffic if total_device_traffic > 0 else 0
        assert 0.5 <= ratio <= 1.5, "App traffic should correlate with device traffic"


class TestSingletonPattern:
    """Test singleton pattern for consistency"""

    def test_get_mock_generator_returns_same_instance(self):
        """Test get_mock_generator returns singleton"""
        gen1 = get_mock_generator()
        gen2 = get_mock_generator()

        assert gen1 is gen2, "Should return same instance (singleton)"

    def test_singleton_maintains_state(self):
        """Test singleton maintains state across calls"""
        gen1 = get_mock_generator()
        start_time1 = gen1._start_time

        time.sleep(0.1)

        gen2 = get_mock_generator()
        start_time2 = gen2._start_time

        assert start_time1 == start_time2, "Start time should be preserved"


class TestNaturalVariation:
    """Test _natural_variation method"""

    def test_natural_variation_bounds(self):
        """Test variation stays within amplitude bounds"""
        gen = MockDataGenerator()

        base = 50.0
        amplitude = 0.1  # ±10%

        # Collect samples
        samples = []
        for _ in range(100):
            value = gen._natural_variation(base, amplitude)
            samples.append(value)
            gen._update_cycle()  # Advance cycle

        # All values should be within bounds (roughly)
        min_val = min(samples)
        max_val = max(samples)

        # Should be within ±amplitude (with some tolerance for noise)
        assert min_val >= base * (1 - amplitude - 0.05)
        assert max_val <= base * (1 + amplitude + 0.05)

    def test_natural_variation_not_constant(self):
        """Test variation produces different values"""
        gen = MockDataGenerator()

        samples = []
        for _ in range(20):
            value = gen._natural_variation(50.0)
            samples.append(value)
            time.sleep(0.01)
            gen._update_cycle()

        # Should have some variation
        assert len(set(samples)) > 1, "Values should vary"


class TestTemporalCycle:
    """Test _update_cycle temporal consistency"""

    def test_cycle_advances_with_time(self):
        """Test cycle time advances"""
        gen = MockDataGenerator()

        gen._update_cycle()
        cycle1 = gen._cycle_time

        time.sleep(0.5)
        gen._update_cycle()
        cycle2 = gen._cycle_time

        assert cycle2 > cycle1, "Cycle should advance with time"

    def test_cycle_wraps_around(self):
        """Test cycle wraps from 1.0 back to 0.0"""
        gen = MockDataGenerator()

        # Cycle is 30 seconds, so check it's in [0, 1)
        gen._update_cycle()
        assert 0 <= gen._cycle_time < 1.0


class TestEducationalClarity:
    """Test data is clear for educational purposes"""

    def test_device_owners_identifiable(self):
        """Test device owners are clear (Pai, Mãe, Filho, Filha)"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        owners = [d["owner"] for d in devices]

        # Should have clear family members
        assert any("Pai" in owner for owner in owners)
        assert any("Mãe" in owner for owner in owners)
        assert any("Filho" in owner or "Filha" in owner for owner in owners)

    def test_device_types_educational(self):
        """Test device types are educational (smartphone, tablet, etc)"""
        gen = MockDataGenerator()
        devices = gen.get_devices()

        types = [d["type"] for d in devices]
        educational_types = ["smartphone", "laptop", "tablet", "smart_tv"]

        for device_type in types:
            assert device_type in educational_types, f"Unknown type: {device_type}"

    def test_apps_recognizable(self):
        """Test apps are recognizable for children"""
        gen = MockDataGenerator()
        apps = gen.get_top_apps()

        recognizable_apps = [
            "YouTube", "Netflix", "WhatsApp", "Instagram",
            "Gmail", "Chrome", "YouTube Kids", "Netflix Kids"
        ]

        for app in apps.keys():
            assert any(known in app for known in recognizable_apps), f"Unknown app: {app}"

    def test_app_aggregation_over_time(self):
        """Test app traffic is aggregated correctly over multiple calls"""
        gen = MockDataGenerator()

        # Simulate same app on multiple devices by modifying scenario
        gen.devices[0].current_app = "Netflix"
        gen.devices[1].current_app = "Netflix"
        gen.devices[2].current_app = "WhatsApp"

        apps = gen.get_top_apps()

        # Netflix should aggregate traffic from multiple devices
        assert "Netflix" in apps
        assert "WhatsApp" in apps

        # Multiple calls should work consistently
        apps2 = gen.get_top_apps()
        assert "Netflix" in apps2
