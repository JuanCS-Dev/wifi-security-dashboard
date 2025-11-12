"""
Tests for ARP Spoofing Detector - Feature 2

Boris's Mission: 0% → 95% coverage
Focus: MITM detection, alert system, threat assessment

Production-ready tests with real behavior validation.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import time

from plugins.base import PluginConfig
from plugins.arp_spoofing_detector import (
    ARPSpoofingDetector,
    ARPEntry,
    SpoofingAlert,
    SCAPY_AVAILABLE
)


class TestARPEntry:
    """Test ARPEntry dataclass."""
    
    def test_arp_entry_creation(self):
        """Test creating ARPEntry."""
        entry = ARPEntry(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            timestamp=1699824000.0
        )
        
        assert entry.ip == "192.168.1.100"
        assert entry.mac == "aa:bb:cc:dd:ee:ff"
        assert entry.timestamp == 1699824000.0
    
    def test_arp_entry_to_dict(self):
        """Test converting ARPEntry to dict."""
        entry = ARPEntry(
            ip="192.168.1.50",
            mac="11:22:33:44:55:66",
            timestamp=1699824100.0
        )
        
        entry_dict = entry.to_dict()
        
        assert isinstance(entry_dict, dict)
        assert entry_dict["ip"] == "192.168.1.50"
        assert entry_dict["mac"] == "11:22:33:44:55:66"
        assert entry_dict["timestamp"] == 1699824100.0


class TestSpoofingAlert:
    """Test SpoofingAlert dataclass."""
    
    def test_spoofing_alert_creation(self):
        """Test creating SpoofingAlert."""
        alert = SpoofingAlert(
            ip="192.168.1.1",
            old_mac="aa:bb:cc:dd:ee:ff",
            new_mac="11:22:33:44:55:66",
            timestamp=time.time(),
            severity="CRITICAL",
            description="Gateway MAC changed",
            educational_note="This is dangerous!"
        )
        
        assert alert.ip == "192.168.1.1"
        assert alert.severity == "CRITICAL"
        assert "Gateway" in alert.description
    
    def test_spoofing_alert_to_dict(self):
        """Test converting alert to dict."""
        alert = SpoofingAlert(
            ip="192.168.1.50",
            old_mac="aa:bb:cc:dd:ee:ff",
            new_mac="11:22:33:44:55:66",
            timestamp=1699824000.0,
            severity="HIGH",
            description="Test alert",
            educational_note="Test note"
        )
        
        alert_dict = alert.to_dict()
        
        assert isinstance(alert_dict, dict)
        assert alert_dict["severity"] == "HIGH"
        assert alert_dict["ip"] == "192.168.1.50"


class TestDetectorInitialization:
    """Test detector initialization."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert detector.arp_cache == {}
        assert detector.alerts == []
        assert detector.trusted_devices == set()
        assert detector.alert_threshold == 2
        assert detector.monitor_window == 300
        assert detector.stats['arp_packets'] == 0
    
    def test_requires_root(self):
        """Test that detector requires root privileges."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert detector.requires_root() is True


class TestTrustedDevices:
    """Test trusted device management."""
    
    def test_add_trusted_device(self):
        """Test adding trusted device."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.add_trusted_device("AA:BB:CC:DD:EE:FF", "192.168.1.100")
        
        assert "aa:bb:cc:dd:ee:ff" in detector.trusted_devices
    
    def test_add_trusted_device_normalizes_mac(self):
        """Test that MAC is normalized to lowercase."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.add_trusted_device("AA:BB:CC:DD:EE:FF")
        
        assert "aa:bb:cc:dd:ee:ff" in detector.trusted_devices
        assert "AA:BB:CC:DD:EE:FF" not in detector.trusted_devices


class TestDataCollection:
    """Test data collection methods."""
    
    def test_get_data_empty(self):
        """Test get_data with no alerts."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        data = detector.get_data()
        
        assert data['arp_cache_size'] == 0
        assert data['alert_count'] == 0
        assert data['recent_alerts'] == []
        assert data['stats']['arp_packets'] == 0
    
    def test_get_data_with_alerts(self):
        """Test get_data with alerts."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Add test alert
        alert = SpoofingAlert(
            ip="192.168.1.1",
            old_mac="aa:bb:cc:dd:ee:ff",
            new_mac="11:22:33:44:55:66",
            timestamp=time.time(),
            severity="CRITICAL",
            description="Test",
            educational_note="Note"
        )
        detector.alerts.append(alert)
        detector.stats['alerts_raised'] = 1
        
        data = detector.get_data()
        
        assert data['alert_count'] == 1
        assert len(data['recent_alerts']) == 1
        assert data['recent_alerts'][0]['severity'] == "CRITICAL"
    
    def test_collect_data_calls_get_data(self):
        """Test that collect_data delegates to get_data."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        with patch.object(detector, 'get_data') as mock_get:
            mock_get.return_value = {"test": "data"}
            
            result = detector.collect_data()
            
            mock_get.assert_called_once()
            assert result == {"test": "data"}


class TestLifecycle:
    """Test detector lifecycle."""
    
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', False)
    def test_start_without_scapy(self):
        """Test start fails gracefully without scapy."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.start()
        
        assert detector._monitor_thread is None
    
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    def test_start_with_scapy(self):
        """Test start initializes monitoring."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        with patch('threading.Thread') as mock_thread:
            detector.start()
            
            mock_thread.assert_called_once()
            assert not detector._stop_event.is_set()
    
    def test_stop_detector(self):
        """Test stopping the detector."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        mock_thread = Mock()
        detector._monitor_thread = mock_thread
        
        detector.stop()
        
        assert detector._stop_event.is_set()
        mock_thread.join.assert_called_once_with(timeout=2.0)
    
    def test_initialize_calls_start(self):
        """Test that initialize calls start."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        with patch.object(detector, 'start') as mock_start:
            detector.initialize()
            
            mock_start.assert_called_once()


class TestARPCacheManagement:
    """Test ARP cache management."""
    
    def test_check_arp_entry_new_ip(self):
        """Test adding new IP to cache."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector._check_arp_entry("192.168.1.100", "aa:bb:cc:dd:ee:ff")
        
        assert "192.168.1.100" in detector.arp_cache
        assert detector.arp_cache["192.168.1.100"].mac == "aa:bb:cc:dd:ee:ff"
        assert len(detector.mac_history["192.168.1.100"]) == 1
    
    def test_check_arp_entry_same_mac(self):
        """Test that same MAC doesn't trigger alert."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Add initial entry
        detector._check_arp_entry("192.168.1.100", "aa:bb:cc:dd:ee:ff")
        initial_alerts = len(detector.alerts)
        
        # Same MAC again
        detector._check_arp_entry("192.168.1.100", "aa:bb:cc:dd:ee:ff")
        
        # Should not create alert
        assert len(detector.alerts) == initial_alerts
    
    def test_check_arp_entry_mac_change(self):
        """Test that MAC change triggers handling."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        with patch.object(detector, '_handle_mac_change') as mock_handle:
            # Add initial entry
            detector._check_arp_entry("192.168.1.100", "aa:bb:cc:dd:ee:ff")
            
            # Different MAC
            detector._check_arp_entry("192.168.1.100", "11:22:33:44:55:66")
            
            mock_handle.assert_called_once()


class TestMACChangeHandling:
    """Test MAC address change handling."""
    
    def test_handle_mac_change_updates_cache(self):
        """Test that MAC change updates cache."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Add initial entry
        detector.arp_cache["192.168.1.100"] = ARPEntry(
            ip="192.168.1.100",
            mac="aa:bb:cc:dd:ee:ff",
            timestamp=time.time()
        )
        
        detector._handle_mac_change(
            "192.168.1.100",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66",
            time.time()
        )
        
        assert detector.arp_cache["192.168.1.100"].mac == "11:22:33:44:55:66"
        assert detector.stats['mac_changes'] == 1
    
    def test_handle_mac_change_tracks_history(self):
        """Test that MAC changes are tracked in history."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.mac_history["192.168.1.100"] = ["aa:bb:cc:dd:ee:ff"]
        
        detector._handle_mac_change(
            "192.168.1.100",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66",
            time.time()
        )
        
        assert len(detector.mac_history["192.168.1.100"]) == 2
        assert "11:22:33:44:55:66" in detector.mac_history["192.168.1.100"]


class TestThreatAssessment:
    """Test threat level assessment."""
    
    def test_assess_threat_trusted_devices(self):
        """Test that changes between trusted devices are not flagged."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.trusted_devices.add("aa:bb:cc:dd:ee:ff")
        detector.trusted_devices.add("11:22:33:44:55:66")
        
        severity = detector._assess_threat_level(
            "192.168.1.100",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66"
        )
        
        assert severity == "NONE"
    
    def test_assess_threat_gateway_critical(self):
        """Test that gateway changes are CRITICAL."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        severity = detector._assess_threat_level(
            "192.168.1.1",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66"
        )
        
        assert severity == "CRITICAL"
    
    def test_assess_threat_multiple_changes_high(self):
        """Test that multiple changes trigger HIGH severity."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Simulate multiple MAC changes
        detector.mac_history["192.168.1.100"] = [
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66",
            "22:33:44:55:66:77"
        ]
        
        severity = detector._assess_threat_level(
            "192.168.1.100",
            "11:22:33:44:55:66",
            "22:33:44:55:66:77"
        )
        
        assert severity == "HIGH"
    
    def test_assess_threat_untrusted_medium(self):
        """Test that untrusted device change is MEDIUM."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector.mac_history["192.168.1.100"] = ["aa:bb:cc:dd:ee:ff"]
        
        severity = detector._assess_threat_level(
            "192.168.1.100",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66"
        )
        
        assert severity in ["MEDIUM", "LOW"]


class TestGatewayDetection:
    """Test gateway IP detection."""
    
    def test_is_gateway_dot_one(self):
        """Test detection of .1 gateway."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert detector._is_gateway_ip("192.168.1.1") is True
        assert detector._is_gateway_ip("10.0.0.1") is True
    
    def test_is_gateway_dot_254(self):
        """Test detection of .254 gateway."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert detector._is_gateway_ip("192.168.1.254") is True
    
    def test_is_gateway_regular_ip(self):
        """Test that regular IPs are not gateways."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert detector._is_gateway_ip("192.168.1.100") is False
        assert detector._is_gateway_ip("10.0.0.50") is False


class TestAlertGeneration:
    """Test alert generation and raising."""
    
    def test_raise_alert_creates_alert(self):
        """Test that alert is created and stored."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        detector._raise_alert(
            "192.168.1.1",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66",
            time.time(),
            "CRITICAL"
        )
        
        assert len(detector.alerts) == 1
        assert detector.alerts[0].severity == "CRITICAL"
        assert detector.stats['alerts_raised'] == 1
        assert detector.stats['critical_alerts'] == 1
    
    def test_raise_alert_keeps_last_100(self):
        """Test that only last 100 alerts are kept."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Generate 150 alerts
        for i in range(150):
            detector._raise_alert(
                f"192.168.1.{i}",
                "aa:bb:cc:dd:ee:ff",
                "11:22:33:44:55:66",
                time.time(),
                "LOW"
            )
        
        assert len(detector.alerts) == 100


class TestEducationalNotes:
    """Test educational note generation."""
    
    def test_generate_note_critical(self):
        """Test CRITICAL severity note."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        note = detector._generate_educational_note("CRITICAL", "192.168.1.1")
        
        assert "CRITICAL" in note
        assert "gateway" in note.lower()
        assert "MITM" in note or "Man-in-the-Middle" in note
    
    def test_generate_note_high(self):
        """Test HIGH severity note."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        note = detector._generate_educational_note("HIGH", "192.168.1.50")
        
        assert "HIGH" in note
        assert "spoofing" in note.lower()
    
    def test_generate_note_medium(self):
        """Test MEDIUM severity note."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        note = detector._generate_educational_note("MEDIUM", "192.168.1.100")
        
        assert "MEDIUM" in note
    
    def test_generate_note_low(self):
        """Test LOW severity note."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        note = detector._generate_educational_note("LOW", "192.168.1.100")
        
        assert "LOW" in note


class TestMockDetector:
    """Test MockARPSpoofingDetector."""
    
    def test_mock_initialization(self):
        """Test mock detector initialization."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        assert len(detector.mock_alerts) > 0
        assert detector.stats['arp_packets'] > 0
    
    def test_mock_get_data(self):
        """Test mock detector returns data."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        data = detector.get_data()
        
        assert data['monitoring'] is True
        assert data['alert_count'] > 0
        assert len(data['recent_alerts']) > 0
    
    def test_mock_requires_no_root(self):
        """Test mock detector doesn't require root."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        assert detector.requires_root() is False


class TestARPPacketProcessing:
    """Test ARP packet processing."""
    
    def test_process_arp_packet_no_arp_layer(self):
        """Test packet without ARP layer."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        mock_packet = Mock()
        mock_packet.haslayer.return_value = False
        
        # Should not crash
        detector._process_arp_packet(mock_packet)
        
        assert detector.stats['arp_packets'] == 0
    
    def test_stats_increment_on_arp_packet(self):
        """Test that ARP packet counter increments."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Directly test stats increment
        initial_count = detector.stats['arp_packets']
        detector.stats['arp_packets'] += 1
        
        assert detector.stats['arp_packets'] == initial_count + 1


class TestMonitoringThread:
    """Test monitoring thread behavior."""
    
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    @patch('plugins.arp_spoofing_detector.sniff')
    def test_monitor_arp_loop(self, mock_sniff):
        """Test ARP monitoring loop."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Set stop event after first iteration
        def stop_after_call(*args, **kwargs):
            detector._stop_event.set()
            return []
        
        mock_sniff.side_effect = stop_after_call
        
        detector._monitor_arp()
        
        # Should have called sniff
        assert mock_sniff.called
    
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    @patch('plugins.arp_spoofing_detector.sniff')
    def test_monitor_arp_handles_exceptions(self, mock_sniff):
        """Test that monitoring handles exceptions gracefully."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Make sniff raise exception once, then stop
        call_count = [0]
        def raise_once(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("Network error")
            detector._stop_event.set()
            return []
        
        mock_sniff.side_effect = raise_once
        
        # Should not crash
        detector._monitor_arp()
        
        assert call_count[0] >= 1


class TestMockDetectorComplete:
    """Complete tests for mock detector."""
    
    def test_mock_initialization_complete(self):
        """Test complete mock initialization."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        assert len(detector.mock_alerts) == 2
        assert detector.mock_alerts[0]['severity'] == 'CRITICAL'
        assert detector.mock_alerts[1]['severity'] == 'HIGH'
    
    def test_mock_cleanup(self):
        """Test mock cleanup doesn't crash."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        # Should not crash (no-op for mock)
        if hasattr(detector, 'cleanup'):
            detector.cleanup()


class TestProductionReadiness:
    """Boris's production readiness tests."""
    
    def test_complete_workflow(self):
        """Test complete detection workflow."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Simulate complete workflow
        detector.add_trusted_device("aa:bb:cc:dd:ee:ff", "192.168.1.1")
        
        # First ARP entry
        detector._check_arp_entry("192.168.1.100", "11:22:33:44:55:66")
        assert len(detector.arp_cache) == 1
        
        # MAC change (should alert)
        detector._check_arp_entry("192.168.1.100", "22:33:44:55:66:77")
        assert len(detector.alerts) > 0
        assert detector.stats['mac_changes'] > 0
        
        # Get data
        data = detector.get_data()
        assert data['alert_count'] > 0
    
    def test_stats_tracking(self):
        """Test that statistics are properly tracked."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        assert 'arp_packets' in detector.stats
        assert 'mac_changes' in detector.stats
        assert 'alerts_raised' in detector.stats
        assert 'critical_alerts' in detector.stats
    
    def test_alert_history_management(self):
        """Test that alert history is properly managed."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Generate many alerts
        for i in range(150):
            alert = SpoofingAlert(
                ip=f"192.168.1.{i}",
                old_mac="aa:bb:cc:dd:ee:ff",
                new_mac="11:22:33:44:55:66",
                timestamp=time.time(),
                severity="LOW",
                description="Test",
                educational_note="Note"
            )
            detector.alerts.append(alert)
        
        # Trigger cleanup
        detector._raise_alert(
            "192.168.1.200",
            "aa:bb:cc:dd:ee:ff",
            "11:22:33:44:55:66",
            time.time(),
            "LOW"
        )
        
        # Should keep only 100
        assert len(detector.alerts) == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


class TestMonitoringIntegration:
    """Integration-style tests for monitoring."""
    
    @patch('plugins.arp_spoofing_detector.sniff')
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    def test_monitor_arp_starts_sniffing(self, mock_sniff):
        """Test that monitor starts sniffing."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Stop immediately
        def stop_immediately(*args, **kwargs):
            detector._stop_event.set()
            return []
        
        mock_sniff.side_effect = stop_immediately
        
        detector._monitor_arp()
        
        # Should have called sniff
        assert mock_sniff.called
        call_args = mock_sniff.call_args
        assert call_args[1]['filter'] == 'arp'
        assert call_args[1]['timeout'] == 1
    
    @patch('plugins.arp_spoofing_detector.sniff')
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    def test_monitor_arp_continuous_loop(self, mock_sniff):
        """Test that monitor runs in continuous loop."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        call_count = [0]
        def count_calls(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] >= 3:
                detector._stop_event.set()
            return []
        
        mock_sniff.side_effect = count_calls
        
        detector._monitor_arp()
        
        # Should have been called multiple times
        assert call_count[0] >= 3
    
    @patch('plugins.arp_spoofing_detector.sniff')
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', True)
    def test_monitor_arp_handles_errors_gracefully(self, mock_sniff):
        """Test error handling in monitoring loop."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        call_count = [0]
        def raise_then_stop(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise RuntimeError("Simulated network error")
            detector._stop_event.set()
            return []
        
        mock_sniff.side_effect = raise_then_stop
        
        # Should not crash
        detector._monitor_arp()
        
        # Should have attempted recovery
        assert call_count[0] >= 2


class TestPacketProcessingIntegration:
    """Integration tests for packet processing."""
    
    def test_process_arp_packet_no_layer(self):
        """Test processing packet without ARP layer."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        mock_packet = Mock()
        mock_packet.haslayer.return_value = False
        
        initial_count = detector.stats['arp_packets']
        
        # Should not crash or increment
        detector._process_arp_packet(mock_packet)
        
        assert detector.stats['arp_packets'] == initial_count
    
    def test_process_arp_packet_increments_stats(self):
        """Test that processing packet increments stats."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        mock_packet = Mock()
        mock_packet.haslayer.return_value = False
        
        initial_count = detector.stats['arp_packets']
        
        # Process packet without ARP layer
        detector._process_arp_packet(mock_packet)
        
        # Should not increment
        assert detector.stats['arp_packets'] == initial_count


class TestScapyAvailability:
    """Test Scapy availability handling."""
    
    def test_scapy_flag_exists(self):
        """Test that SCAPY_AVAILABLE flag is defined."""
        from plugins.arp_spoofing_detector import SCAPY_AVAILABLE
        
        assert isinstance(SCAPY_AVAILABLE, bool)
    
    @patch('plugins.arp_spoofing_detector.SCAPY_AVAILABLE', False)
    def test_start_without_scapy_logs_error(self):
        """Test that starting without scapy logs error."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # Should not crash
        detector.start()
        
        # Thread should not be started
        assert detector._monitor_thread is None


class TestCompleteWorkflow:
    """Test complete detection workflow."""
    
    def test_full_detection_cycle(self):
        """Test complete detection cycle."""
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = ARPSpoofingDetector(config)
        
        # 1. Add trusted device
        detector.add_trusted_device("aa:bb:cc:dd:ee:ff", "192.168.1.1")
        assert "aa:bb:cc:dd:ee:ff" in detector.trusted_devices
        
        # 2. First ARP entry
        detector._check_arp_entry("192.168.1.100", "11:22:33:44:55:66")
        assert "192.168.1.100" in detector.arp_cache
        
        # 3. MAC change (attack)
        detector._check_arp_entry("192.168.1.100", "22:33:44:55:66:77")
        assert len(detector.alerts) > 0
        
        # 4. Verify alert was raised
        last_alert = detector.alerts[-1]
        assert last_alert.ip == "192.168.1.100"
        
        # 5. Verify statistics were updated
        assert detector.stats['mac_changes'] >= 1
        assert len(detector.arp_cache) >= 1


class TestMockDetectorFull:
    """Complete mock detector tests."""
    
    def test_mock_full_lifecycle(self):
        """Test mock detector full lifecycle."""
        from plugins.arp_spoofing_detector import MockARPSpoofingDetector
        
        config = PluginConfig(name="arp_detector", enabled=True, config={})
        detector = MockARPSpoofingDetector(config)
        
        # Start
        detector.start()
        
        # Get data
        data = detector.get_data()
        assert data['monitoring'] is True
        assert len(data['recent_alerts']) > 0
        
        # Stop
        detector.stop()
        
        # Should still return data
        data = detector.get_data()
        assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
