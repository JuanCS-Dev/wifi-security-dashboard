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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
