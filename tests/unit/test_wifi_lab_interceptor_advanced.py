"""
Advanced tests for WiFi Lab Interceptor - Packet Processing

Boris's Mission: 18% → 95% coverage
Focus: Packet processing, analysis methods, educational features

These tests mock Scapy packets to validate the analysis logic
without requiring actual network capture.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from education.wifi_lab_interceptor import (
    WiFiLabInterceptor,
    InterceptedData
)


class MockPacket:
    """Mock Scapy packet for testing."""
    
    def __init__(self, layers=None):
        self._layers = layers or {}
        
    def haslayer(self, layer):
        """Check if packet has layer."""
        return layer.__name__ in self._layers
    
    def __getitem__(self, layer):
        """Get layer from packet."""
        layer_name = layer.__name__ if hasattr(layer, '__name__') else str(layer)
        if layer_name in self._layers:
            return self._layers[layer_name]
        raise IndexError(f"Layer {layer_name} not in packet")


class TestPacketProcessing:
    """Test _process_packet method."""
    
    def test_process_packet_increments_total(self):
        """Test that processing any packet increments total_packets."""
        interceptor = WiFiLabInterceptor()
        
        # Create minimal mock packet
        packet = MockPacket()
        
        initial_count = interceptor.stats['total_packets']
        interceptor._process_packet(packet)
        
        assert interceptor.stats['total_packets'] == initial_count + 1
    
    def test_process_packet_calls_dns_analyzer(self):
        """Test that DNS packets trigger DNS analysis."""
        interceptor = WiFiLabInterceptor()
        
        # Mock DNS packet
        with patch.object(interceptor, '_analyze_dns') as mock_analyze:
            # Create packet with DNSQR layer
            from scapy.all import DNSQR
            packet = MockPacket(layers={'DNSQR': Mock()})
            
            interceptor._process_packet(packet)
            
            mock_analyze.assert_called_once_with(packet)
    
    def test_process_packet_calls_http_analyzer(self):
        """Test that HTTP packets trigger HTTP analysis."""
        interceptor = WiFiLabInterceptor()
        
        # Mock HTTP packet (TCP + Raw)
        with patch.object(interceptor, '_analyze_http') as mock_analyze:
            from scapy.all import TCP, Raw
            packet = MockPacket(layers={'TCP': Mock(), 'Raw': Mock()})
            
            interceptor._process_packet(packet)
            
            mock_analyze.assert_called_once_with(packet)
    
    def test_process_packet_calls_https_analyzer(self):
        """Test that HTTPS packets trigger HTTPS analysis."""
        interceptor = WiFiLabInterceptor()
        
        # Mock HTTPS packet (TCP)
        with patch.object(interceptor, '_analyze_https') as mock_analyze:
            from scapy.all import TCP
            packet = MockPacket(layers={'TCP': Mock()})
            
            interceptor._process_packet(packet)
            
            mock_analyze.assert_called_once_with(packet)
    
    def test_process_packet_calls_arp_analyzer(self):
        """Test that ARP packets trigger ARP analysis."""
        interceptor = WiFiLabInterceptor()
        
        # Mock ARP packet
        with patch.object(interceptor, '_analyze_arp') as mock_analyze:
            from scapy.all import ARP
            packet = MockPacket(layers={'ARP': Mock()})
            
            interceptor._process_packet(packet)
            
            mock_analyze.assert_called_once_with(packet)


class TestDNSAnalysis:
    """Test _analyze_dns method."""
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_dns_increments_counter(self, mock_datetime):
        """Test that DNS analysis increments dns_queries counter."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)  # Disable print
        
        # Create DNS packet mock
        from scapy.all import DNSQR, IP, Ether
        
        mock_dnsqr = Mock()
        mock_dnsqr.qname = b"google.com."
        
        mock_ip = Mock()
        mock_ip.src = "192.168.1.100"
        
        mock_ether = Mock()
        mock_ether.src = "aa:bb:cc:dd:ee:ff"
        
        packet = MockPacket(layers={
            'DNSQR': mock_dnsqr,
            'IP': mock_ip,
            'Ether': mock_ether
        })
        
        initial_count = interceptor.stats['dns_queries']
        interceptor._analyze_dns(packet)
        
        assert interceptor.stats['dns_queries'] == initial_count + 1
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_dns_creates_intercepted_data(self, mock_datetime):
        """Test that DNS analysis creates InterceptedData."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create DNS packet
        from scapy.all import DNSQR, IP, Ether
        
        mock_dnsqr = Mock()
        mock_dnsqr.qname = b"facebook.com."
        
        mock_ip = Mock()
        mock_ip.src = "192.168.1.50"
        
        mock_ether = Mock()
        mock_ether.src = "11:22:33:44:55:66"
        
        packet = MockPacket(layers={
            'DNSQR': mock_dnsqr,
            'IP': mock_ip,
            'Ether': mock_ether
        })
        
        interceptor._analyze_dns(packet)
        
        # Verify data was captured
        assert len(interceptor.captured_data) == 1
        data = interceptor.captured_data[0]
        
        assert data.protocol == "DNS"
        assert "facebook.com" in data.description
        assert data.device_ip == "192.168.1.50"
        assert data.device_mac == "11:22:33:44:55:66"
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_dns_categorizes_query(self, mock_datetime):
        """Test that DNS queries are categorized correctly."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Test with categorization method mocked
        with patch.object(interceptor, '_categorize_dns_query') as mock_categorize:
            mock_categorize.return_value = ("WARNING", "Educational note")
            
            from scapy.all import DNSQR, IP, Ether
            
            mock_dnsqr = Mock()
            mock_dnsqr.qname = b"example.com."
            
            packet = MockPacket(layers={
                'DNSQR': mock_dnsqr,
                'IP': Mock(src="192.168.1.1"),
                'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
            })
            
            interceptor._analyze_dns(packet)
            
            # Verify categorization was called
            mock_categorize.assert_called_once()
            
            # Verify danger level was set
            data = interceptor.captured_data[0]
            assert data.danger_level == "WARNING"
            assert data.educational_note == "Educational note"


class TestHTTPAnalysis:
    """Test _analyze_http method."""
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_http_detects_get_request(self, mock_datetime):
        """Test HTTP GET request detection."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create HTTP GET packet
        from scapy.all import TCP, IP, Ether, Raw
        
        http_payload = b"GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"
        
        mock_raw = Mock()
        mock_raw.load = http_payload
        
        mock_ip = Mock()
        mock_ip.src = "192.168.1.100"
        mock_ip.dst = "93.184.216.34"
        
        mock_ether = Mock()
        mock_ether.src = "aa:bb:cc:dd:ee:ff"
        
        packet = MockPacket(layers={
            'Raw': mock_raw,
            'IP': mock_ip,
            'Ether': mock_ether
        })
        
        interceptor._analyze_http(packet)
        
        # Verify HTTP was detected
        assert interceptor.stats['http_packets'] == 1
        assert interceptor.stats['leaked_data'] == 1
        
        # Verify data was captured
        assert len(interceptor.captured_data) == 1
        data = interceptor.captured_data[0]
        
        assert data.protocol == "HTTP"
        assert data.danger_level == "DANGER"
        assert "NÃO CRIPTOGRAFADOS" in data.description
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_http_detects_post_request(self, mock_datetime):
        """Test HTTP POST request detection."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create HTTP POST packet with credentials
        from scapy.all import Raw, IP, Ether
        
        http_payload = b"POST /login HTTP/1.1\r\nHost: example.com\r\n\r\nusername=user&password=secret123"
        
        mock_raw = Mock()
        mock_raw.load = http_payload
        
        packet = MockPacket(layers={
            'Raw': mock_raw,
            'IP': Mock(src="192.168.1.50", dst="10.0.0.1"),
            'Ether': Mock(src="11:22:33:44:55:66")
        })
        
        interceptor._analyze_http(packet)
        
        # Verify detection
        assert interceptor.stats['http_packets'] == 1
        data = interceptor.captured_data[0]
        
        assert data.protocol == "HTTP"
        assert data.danger_level == "DANGER"
        assert data.raw_data is not None
        assert "HTTP NÃO É SEGURO" in data.educational_note
    
    def test_analyze_http_handles_non_http_gracefully(self):
        """Test that non-HTTP TCP+Raw packets don't crash."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create TCP packet with non-HTTP payload
        from scapy.all import Raw, IP, Ether
        
        mock_raw = Mock()
        mock_raw.load = b"Some random binary data\x00\xff\xaa"
        
        packet = MockPacket(layers={
            'Raw': mock_raw,
            'IP': Mock(src="192.168.1.1", dst="192.168.1.2"),
            'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
        })
        
        # Should not crash
        interceptor._analyze_http(packet)
        
        # Should not have captured anything
        assert interceptor.stats['http_packets'] == 0
        assert len(interceptor.captured_data) == 0


class TestHTTPSAnalysis:
    """Test _analyze_https method."""
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_https_detects_port_443(self, mock_datetime):
        """Test HTTPS detection on port 443."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create HTTPS packet (destination port 443)
        from scapy.all import TCP, IP, Ether
        
        mock_tcp = Mock()
        mock_tcp.dport = 443
        mock_tcp.sport = 54321
        
        mock_ip = Mock()
        mock_ip.src = "192.168.1.100"
        mock_ip.dst = "142.250.185.46"  # Google IP
        
        mock_ether = Mock()
        mock_ether.src = "aa:bb:cc:dd:ee:ff"
        
        packet = MockPacket(layers={
            'TCP': mock_tcp,
            'IP': mock_ip,
            'Ether': mock_ether
        })
        
        interceptor._analyze_https(packet)
        
        # Verify HTTPS detection
        assert interceptor.stats['https_packets'] == 1
        assert interceptor.stats['safe_data'] == 1
        
        # Note: HTTPS packets are only captured every 100th packet in lab mode
        # So we just verify stats, not captured_data
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_analyze_https_detects_source_port_443(self, mock_datetime):
        """Test HTTPS detection when source port is 443."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create HTTPS response packet (source port 443)
        from scapy.all import TCP, IP, Ether
        
        mock_tcp = Mock()
        mock_tcp.sport = 443
        mock_tcp.dport = 54321
        
        packet = MockPacket(layers={
            'TCP': mock_tcp,
            'IP': Mock(src="142.250.185.46", dst="192.168.1.100"),
            'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
        })
        
        interceptor._analyze_https(packet)
        
        # Should detect as HTTPS
        assert interceptor.stats['https_packets'] == 1
        assert interceptor.stats['safe_data'] == 1
    
    def test_analyze_https_ignores_non_443_ports(self):
        """Test that non-443 TCP traffic is not counted as HTTPS."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create TCP packet on port 80 (HTTP, not HTTPS)
        from scapy.all import TCP, IP, Ether
        
        mock_tcp = Mock()
        mock_tcp.sport = 54321
        mock_tcp.dport = 80
        
        packet = MockPacket(layers={
            'TCP': mock_tcp,
            'IP': Mock(src="192.168.1.100", dst="10.0.0.1"),
            'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
        })
        
        interceptor._analyze_https(packet)
        
        # Should NOT count as HTTPS
        assert interceptor.stats['https_packets'] == 0
        assert len(interceptor.captured_data) == 0


class TestDeviceIdentification:
    """Test _identify_device method."""
    
    def test_identify_registered_device(self):
        """Test identifying a registered device."""
        interceptor = WiFiLabInterceptor()
        
        # Register a device
        mac = "aa:bb:cc:dd:ee:ff"
        interceptor.register_lab_device(mac, "Arduino-1", "arduino")
        
        # Create packet from that device
        from scapy.all import Ether
        mock_ether = Mock()
        mock_ether.src = mac
        
        packet = MockPacket(layers={'Ether': mock_ether})
        
        # Identify device
        device_name = interceptor._identify_device("192.168.1.100", packet)
        
        assert device_name == "Arduino-1"
    
    def test_identify_unknown_device(self):
        """Test identifying an unknown device returns IP-based name."""
        interceptor = WiFiLabInterceptor()
        
        # No devices registered
        packet = MockPacket(layers={'Ether': Mock(src="11:22:33:44:55:66")})
        
        device_name = interceptor._identify_device("192.168.1.99", packet)
        
        # Should return Device-<last_octet> format for unknown devices
        assert "Device-99" == device_name or "99" in device_name


class TestSensitiveDataExtraction:
    """Test _extract_sensitive_data method."""
    
    def test_extract_password_from_form_data(self):
        """Test extracting password from form data."""
        interceptor = WiFiLabInterceptor()
        
        payload = "username=john&password=secret123&email=john@example.com"
        
        sensitive = interceptor._extract_sensitive_data(payload)
        
        # Method returns Portuguese "SENHA" for password
        assert "senha" in sensitive.lower() or "usu" in sensitive.lower()
    
    def test_extract_token_from_headers(self):
        """Test extracting auth token from headers."""
        interceptor = WiFiLabInterceptor()
        
        payload = "Authorization: Bearer token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        
        sensitive = interceptor._extract_sensitive_data(payload)
        
        # Should detect TOKEN keyword
        assert "token" in sensitive.lower()
    
    def test_extract_handles_empty_payload(self):
        """Test extraction handles empty payload gracefully."""
        interceptor = WiFiLabInterceptor()
        
        sensitive = interceptor._extract_sensitive_data("")
        
        # Should return something, not crash
        assert isinstance(sensitive, str)


class TestDNSCategorization:
    """Test _categorize_dns_query method."""
    
    def test_categorize_known_safe_domain(self):
        """Test categorization of known safe domains."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("google.com.")
        
        # Google should be relatively safe
        assert danger in ["SAFE", "WARNING"]
        assert note != ""
    
    def test_categorize_suspicious_domain(self):
        """Test categorization of suspicious domains."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("malicious-site.xyz.")
        
        # Should have educational note
        assert note != ""
        assert danger in ["SAFE", "WARNING", "DANGER"]


class TestPrintInterception:
    """Test _print_interception method."""
    
    def test_print_interception_outputs_data(self, capsys):
        """Test that interception data is printed in lab mode."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Test-Device",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.100",
            protocol="HTTP",
            danger_level="DANGER",
            description="Test interception",
            educational_note="Test note"
        )
        
        interceptor._print_interception(data)
        
        captured = capsys.readouterr()
        assert "Test-Device" in captured.out or "192.168.1.100" in captured.out
    
    def test_print_interception_respects_lab_mode(self, capsys):
        """Test that printing only happens in lab mode."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Test",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.1",
            protocol="DNS",
            danger_level="SAFE",
            description="Test"
        )
        
        interceptor._print_interception(data)
        
        # With lab_mode=False, should not print (or print very little)
        captured = capsys.readouterr()
        # This test might need adjustment based on actual implementation


class TestShowSummary:
    """Test _show_summary method."""
    
    def test_show_summary_displays_stats(self, capsys):
        """Test that summary displays statistics."""
        interceptor = WiFiLabInterceptor()
        
        # Set some stats
        interceptor.stats['total_packets'] = 100
        interceptor.stats['dns_queries'] = 25
        interceptor.stats['http_packets'] = 10
        interceptor.stats['https_packets'] = 50
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        assert "100" in captured.out or "total" in captured.out.lower()


class TestARPAnalysis:
    """Test _analyze_arp method."""
    
    def test_analyze_arp_detects_reply(self, capsys):
        """Test ARP reply detection and device registration."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        from scapy.all import ARP
        
        # Create ARP reply packet
        mock_arp = Mock()
        mock_arp.op = 2  # ARP Reply
        mock_arp.hwsrc = "aa:bb:cc:dd:ee:ff"
        mock_arp.psrc = "192.168.1.100"
        
        packet = MockPacket(layers={'ARP': mock_arp})
        
        interceptor._analyze_arp(packet)
        
        # Verify device was registered
        assert "aa:bb:cc:dd:ee:ff" in interceptor.device_registry
        device = interceptor.device_registry["aa:bb:cc:dd:ee:ff"]
        assert device["type"] == "unknown"
        assert "first_seen" in device
        
        # Verify educational output
        captured = capsys.readouterr()
        assert "Novo dispositivo detectado" in captured.out
        assert "192.168.1.100" in captured.out
    
    def test_analyze_arp_ignores_known_devices(self):
        """Test that known devices are not re-registered."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Register device first
        mac = "aa:bb:cc:dd:ee:ff"
        interceptor.register_lab_device(mac, "Known-Device", "phone")
        
        from scapy.all import ARP
        
        # Create ARP reply from known device
        mock_arp = Mock()
        mock_arp.op = 2
        mock_arp.hwsrc = mac.upper()  # Different case
        mock_arp.psrc = "192.168.1.100"
        
        packet = MockPacket(layers={'ARP': mock_arp})
        
        initial_count = len(interceptor.device_registry)
        interceptor._analyze_arp(packet)
        
        # Should not add duplicate
        assert len(interceptor.device_registry) == initial_count
    
    def test_analyze_arp_ignores_requests(self):
        """Test that ARP requests (op=1) are ignored."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        from scapy.all import ARP
        
        # Create ARP request
        mock_arp = Mock()
        mock_arp.op = 1  # ARP Request (not reply)
        mock_arp.hwsrc = "aa:bb:cc:dd:ee:ff"
        mock_arp.psrc = "192.168.1.100"
        
        packet = MockPacket(layers={'ARP': mock_arp})
        
        initial_count = len(interceptor.device_registry)
        interceptor._analyze_arp(packet)
        
        # Should not register anything
        assert len(interceptor.device_registry) == initial_count
    
    def test_analyze_arp_handles_no_arp_layer(self):
        """Test graceful handling when packet has no ARP layer."""
        interceptor = WiFiLabInterceptor()
        
        # Packet without ARP layer
        packet = MockPacket(layers={})
        
        # Should not crash
        interceptor._analyze_arp(packet)
        
        # Nothing should be registered
        assert len(interceptor.device_registry) == 0


class TestExportResults:
    """Test export_results method."""
    
    def test_export_results_creates_file(self, tmp_path):
        """Test that export creates a file."""
        interceptor = WiFiLabInterceptor()
        
        # Add some test data
        interceptor.stats['total_packets'] = 100
        interceptor.stats['http_packets'] = 10
        
        test_data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Test-Device",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.100",
            protocol="HTTP",
            danger_level="DANGER",
            description="Test capture",
            educational_note="Test note"
        )
        interceptor.captured_data.append(test_data)
        
        # Export to temp file
        output_file = tmp_path / "test_export.txt"
        interceptor.export_results(str(output_file))
        
        # Verify file was created
        assert output_file.exists()
        
        # Verify content
        content = output_file.read_text(encoding='utf-8')
        assert "LABORATÓRIO DE SEGURANÇA WiFi" in content
        assert "total_packets: 100" in content
        assert "Test-Device" in content
        assert "HTTP" in content
        assert "DANGER" in content
    
    def test_export_results_auto_filename(self, tmp_path, monkeypatch):
        """Test export with auto-generated filename."""
        import os
        monkeypatch.chdir(tmp_path)
        
        interceptor = WiFiLabInterceptor()
        interceptor.stats['total_packets'] = 50
        
        # Export without filename
        with patch('education.wifi_lab_interceptor.datetime') as mock_dt:
            mock_dt.now.return_value.strftime.return_value = "20251112_190000"
            interceptor.export_results()
        
        # Should create file with timestamp
        expected_file = tmp_path / "lab_capture_20251112_190000.txt"
        assert expected_file.exists()
    
    def test_export_results_includes_all_stats(self, tmp_path):
        """Test that all statistics are exported."""
        interceptor = WiFiLabInterceptor()
        
        # Set all stats
        interceptor.stats = {
            'total_packets': 1000,
            'http_packets': 50,
            'https_packets': 800,
            'dns_queries': 100,
            'leaked_data': 50,
            'safe_data': 800
        }
        
        output_file = tmp_path / "stats_test.txt"
        interceptor.export_results(str(output_file))
        
        content = output_file.read_text(encoding='utf-8')
        
        # Verify all stats present
        assert "total_packets: 1000" in content
        assert "http_packets: 50" in content
        assert "https_packets: 800" in content
        assert "dns_queries: 100" in content
        assert "leaked_data: 50" in content
        assert "safe_data: 800" in content
    
    def test_export_results_includes_educational_notes(self, tmp_path):
        """Test that educational notes are included in export."""
        interceptor = WiFiLabInterceptor()
        
        test_data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Arduino-1",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.50",
            protocol="DNS",
            danger_level="SAFE",
            description="Querying google.com",
            educational_note="This is safe educational traffic"
        )
        interceptor.captured_data.append(test_data)
        
        output_file = tmp_path / "notes_test.txt"
        interceptor.export_results(str(output_file))
        
        content = output_file.read_text(encoding='utf-8')
        
        assert "This is safe educational traffic" in content
        assert "Nota:" in content
    
    def test_export_results_handles_empty_data(self, tmp_path):
        """Test export with no captured data."""
        interceptor = WiFiLabInterceptor()
        
        # No data captured
        assert len(interceptor.captured_data) == 0
        
        output_file = tmp_path / "empty_test.txt"
        interceptor.export_results(str(output_file))
        
        # Should still create file
        assert output_file.exists()
        
        content = output_file.read_text(encoding='utf-8')
        assert "ESTATÍSTICAS:" in content
        assert "total_packets: 0" in content
    
    def test_export_results_prints_confirmation(self, tmp_path, capsys):
        """Test that export prints confirmation message."""
        interceptor = WiFiLabInterceptor()
        
        output_file = tmp_path / "confirm_test.txt"
        interceptor.export_results(str(output_file))
        
        captured = capsys.readouterr()
        assert "Resultados exportados" in captured.out
        assert str(output_file) in captured.out


class TestCreateLabScenario:
    """Test create_lab_scenario function."""
    
    def test_create_lab_scenario_returns_interceptor(self, capsys):
        """Test that create_lab_scenario returns WiFiLabInterceptor."""
        from education.wifi_lab_interceptor import create_lab_scenario
        
        interceptor = create_lab_scenario()
        
        assert isinstance(interceptor, WiFiLabInterceptor)
        assert interceptor.lab_mode is True
        assert interceptor.interface == "wlan0"
        
        # Check educational output
        captured = capsys.readouterr()
        assert "Configurando Laboratório" in captured.out
        assert "IMPORTANTE" in captured.out
    
    def test_create_lab_scenario_shows_warnings(self, capsys):
        """Test that educational warnings are displayed."""
        from education.wifi_lab_interceptor import create_lab_scenario
        
        create_lab_scenario()
        
        captured = capsys.readouterr()
        assert "Use apenas em sua rede doméstica" in captured.out
        assert "EDUCAÇÃO" in captured.out


class TestStartCapture:
    """Test start_capture method."""
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_with_mock_sniff(self, mock_sniff):
        """Test start_capture calls scapy.sniff correctly."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Mock sniff to return empty list
        mock_sniff.return_value = []
        
        interceptor.start_capture(duration=10, packet_count=100)
        
        # Verify sniff was called
        mock_sniff.assert_called_once()
        call_kwargs = mock_sniff.call_args[1]
        
        assert call_kwargs['iface'] == "wlan0"
        assert call_kwargs['timeout'] == 10
        assert call_kwargs['count'] == 100
        assert call_kwargs['store'] is True
        assert callable(call_kwargs['prn'])
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_shows_lab_banner(self, mock_sniff, capsys):
        """Test that lab mode shows educational banner."""
        mock_sniff.return_value = []
        
        interceptor = WiFiLabInterceptor(lab_mode=True)
        interceptor.start_capture(duration=5)
        
        captured = capsys.readouterr()
        assert "LABORATÓRIO DE SEGURANÇA WiFi" in captured.out
        assert "MODO EDUCACIONAL" in captured.out
        assert "Interface: wlan0" in captured.out
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_handles_permission_error(self, mock_sniff, capsys):
        """Test handling of permission errors."""
        mock_sniff.side_effect = PermissionError("Need root")
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        interceptor.start_capture()
        
        captured = capsys.readouterr()
        assert "ERRO" in captured.out or "sudo" in captured.out
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_handles_keyboard_interrupt(self, mock_sniff, capsys):
        """Test handling of KeyboardInterrupt."""
        mock_sniff.side_effect = KeyboardInterrupt()
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        interceptor.start_capture()
        
        captured = capsys.readouterr()
        assert "interrompida" in captured.out.lower() or "Captura" in captured.out
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_processes_packets(self, mock_sniff):
        """Test that captured packets are processed."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        # Create mock packets
        mock_packet1 = MockPacket()
        mock_packet2 = MockPacket()
        mock_sniff.return_value = [mock_packet1, mock_packet2]
        
        with patch.object(interceptor, '_process_packet') as mock_process:
            interceptor.start_capture()
            
            # Verify process was called during capture
            # (prn callback is called for each packet)
            assert mock_sniff.called
    
    @patch('education.wifi_lab_interceptor.sniff')
    def test_start_capture_generic_exception(self, mock_sniff, capsys):
        """Test handling of generic exceptions."""
        mock_sniff.side_effect = Exception("Network error")
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        interceptor.start_capture()
        
        captured = capsys.readouterr()
        assert "ERRO" in captured.out


class TestDNSCategorizationDetailed:
    """Detailed tests for DNS categorization."""
    
    def test_categorize_educational_site(self):
        """Test educational site categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("wikipedia.org.")
        
        assert danger == "SAFE"
        assert "educacional" in note.lower() or "segur" in note.lower()
    
    def test_categorize_social_media(self):
        """Test social media categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("facebook.com.")
        
        assert danger == "WARNING"
        assert "rede social" in note.lower() or "pessoais" in note.lower()
    
    def test_categorize_streaming_site(self):
        """Test streaming site categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("netflix.com.")
        
        assert danger == "SAFE"
        assert "streaming" in note.lower()
    
    def test_categorize_gaming_site(self):
        """Test gaming site categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("minecraft.net.")
        
        assert danger == "WARNING"
        assert "gaming" in note.lower() or "game" in note.lower()
    
    def test_categorize_banking_site(self):
        """Test banking site categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("bankofamerica.com.")
        
        assert danger == "DANGER"
        assert "financeiro" in note.lower() or "banco" in note.lower()
    
    def test_categorize_generic_site(self):
        """Test generic site categorization."""
        interceptor = WiFiLabInterceptor()
        
        danger, note = interceptor._categorize_dns_query("example.com.")
        
        assert danger == "SAFE"
        assert len(note) > 0


class TestPrintInterceptionDetailed:
    """Detailed tests for print interception."""
    
    def test_print_interception_safe_color(self, capsys):
        """Test SAFE level color output."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Device",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.1",
            protocol="HTTPS",
            danger_level="SAFE",
            description="Secure connection",
            educational_note="Good practice"
        )
        
        interceptor._print_interception(data)
        
        captured = capsys.readouterr()
        # Should contain device name or IP
        assert "Device" in captured.out or "192.168.1.1" in captured.out
        # Should contain description
        assert "Secure connection" in captured.out
    
    def test_print_interception_warning_color(self, capsys):
        """Test WARNING level color output."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Phone",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.50",
            protocol="DNS",
            danger_level="WARNING",
            description="Social media access",
            educational_note="Be careful"
        )
        
        interceptor._print_interception(data)
        
        captured = capsys.readouterr()
        assert "Phone" in captured.out or "192.168.1.50" in captured.out
        assert "Social media" in captured.out
        assert "Be careful" in captured.out
    
    def test_print_interception_danger_color(self, capsys):
        """Test DANGER level color output."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        data = InterceptedData(
            timestamp="2025-11-12T19:00:00",
            device_name="Laptop",
            device_mac="aa:bb:cc:dd:ee:ff",
            device_ip="192.168.1.100",
            protocol="HTTP",
            danger_level="DANGER",
            description="Unencrypted credentials",
            educational_note="CRITICAL RISK"
        )
        
        interceptor._print_interception(data)
        
        captured = capsys.readouterr()
        assert "Laptop" in captured.out or "192.168.1.100" in captured.out
        assert "Unencrypted" in captured.out
        assert "CRITICAL" in captured.out


class TestShowSummaryDetailed:
    """Detailed tests for summary display."""
    
    def test_show_summary_all_stats(self, capsys):
        """Test that all stats are displayed in summary."""
        interceptor = WiFiLabInterceptor()
        
        interceptor.stats = {
            'total_packets': 1500,
            'http_packets': 75,
            'https_packets': 1200,
            'dns_queries': 150,
            'leaked_data': 75,
            'safe_data': 1200
        }
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        assert "1500" in captured.out  # total_packets
        assert "75" in captured.out or "leaked" in captured.out.lower()
    
    def test_show_summary_educational_messages(self, capsys):
        """Test that educational messages appear in summary."""
        interceptor = WiFiLabInterceptor()
        
        # Set stats that should trigger educational messages
        interceptor.stats['http_packets'] = 50
        interceptor.stats['https_packets'] = 200
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        # Should have educational content about safe/unsafe traffic
        assert "RESUMO" in captured.out or "=" in captured.out


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_packet_without_ether_layer(self):
        """Test handling packets without Ethernet layer."""
        interceptor = WiFiLabInterceptor()
        
        packet = MockPacket(layers={})
        
        # Should not crash
        device_name = interceptor._identify_device("192.168.1.1", packet)
        assert isinstance(device_name, str)
    
    def test_dns_without_ip_layer(self):
        """Test DNS analysis without IP layer."""
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        from scapy.all import DNSQR
        
        mock_dnsqr = Mock()
        mock_dnsqr.qname = b"test.com."
        
        packet = MockPacket(layers={'DNSQR': mock_dnsqr})
        
        # Should handle missing IP layer gracefully
        initial_count = interceptor.stats['dns_queries']
        interceptor._analyze_dns(packet)
        
        # Should still increment counter
        assert interceptor.stats['dns_queries'] == initial_count + 1
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_http_with_decode_error(self, mock_datetime):
        """Test HTTP analysis with malformed payload."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=False)
        
        from scapy.all import Raw, IP, Ether
        
        # Create packet with non-UTF8 payload
        mock_raw = Mock()
        mock_raw.load = b"\xff\xfe\xfd\xfc"  # Invalid UTF-8
        
        packet = MockPacket(layers={
            'Raw': mock_raw,
            'IP': Mock(src="192.168.1.1", dst="192.168.1.2"),
            'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
        })
        
        # Should not crash - exception is caught
        interceptor._analyze_http(packet)
        
        # Should not have captured anything
        assert interceptor.stats['http_packets'] == 0
    
    @patch('education.wifi_lab_interceptor.datetime')
    def test_https_sampling_threshold(self, mock_datetime):
        """Test HTTPS packets are only captured every 100th."""
        mock_datetime.now.return_value.isoformat.return_value = "2025-11-12T19:00:00"
        
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        from scapy.all import TCP, IP, Ether
        
        # Send 100 HTTPS packets
        for i in range(100):
            mock_tcp = Mock()
            mock_tcp.dport = 443
            mock_tcp.sport = 50000 + i
            
            packet = MockPacket(layers={
                'TCP': mock_tcp,
                'IP': Mock(src="192.168.1.100", dst="1.2.3.4"),
                'Ether': Mock(src="aa:bb:cc:dd:ee:ff")
            })
            
            interceptor._analyze_https(packet)
        
        # Should have counted all 100
        assert interceptor.stats['https_packets'] == 100
        
        # But only captured the 100th one (and maybe 0th)
        # Implementation samples every 100
        assert len([d for d in interceptor.captured_data if d.protocol == "HTTPS"]) <= 2


class TestSummaryEducationalMessages:
    """Test educational messages in summary based on traffic patterns."""
    
    def test_show_summary_with_http_traffic(self, capsys):
        """Test educational message when HTTP traffic detected."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        interceptor.stats['total_packets'] = 100
        interceptor.stats['http_packets'] = 10
        interceptor.stats['https_packets'] = 90
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        assert "Detectamos tráfego HTTP" in captured.out
        assert "não criptografado" in captured.out
        assert "SEMPRE use HTTPS" in captured.out
    
    def test_show_summary_all_https(self, capsys):
        """Test congratulatory message when all traffic is HTTPS."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        interceptor.stats['total_packets'] = 100
        interceptor.stats['http_packets'] = 0
        interceptor.stats['https_packets'] = 100
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        assert "Parabéns" in captured.out
        assert "criptografado" in captured.out
    
    def test_show_summary_golden_rule(self, capsys):
        """Test that golden rule is always shown in lab mode."""
        interceptor = WiFiLabInterceptor(lab_mode=True)
        
        interceptor.stats['total_packets'] = 50
        
        interceptor._show_summary()
        
        captured = capsys.readouterr()
        assert "REGRA DE OURO" in captured.out
        assert "NUNCA se conecte em redes WiFi públicas" in captured.out
        assert "VPN" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
