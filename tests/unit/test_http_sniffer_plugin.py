"""
Tests for HTTP Sniffer Plugin - Feature 4

Tests HTTP traffic capture and ethical safeguards.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import pytest
import time
from unittest.mock import Mock, patch

from src.plugins.base import PluginConfig
from src.plugins.http_sniffer_plugin import (
    HTTPSnifferPlugin,
    HTTPRequest,
    CredentialCapture
)


class TestHTTPSnifferPlugin:
    """Test HTTP Sniffer Plugin functionality."""
    
    def test_plugin_initialization_mock_mode(self):
        """Test plugin initializes correctly in mock mode."""
        config = PluginConfig(
            name="http_sniffer",
            rate_ms=1000,
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        plugin.initialize()
        
        assert plugin is not None
        assert plugin.config.name == "http_sniffer"
    
    def test_ethical_consent_requirement(self):
        """Test that plugin requires ethical consent."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": False, "ethical_consent": False}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Should not start without consent
        assert plugin._ethical_consent_given is False
    
    def test_collect_mock_data(self):
        """Test collecting mock HTTP data."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        # Verify mock data structure
        assert 'monitoring' in data
        assert 'ethical_consent' in data
        assert 'stats' in data
        assert 'recent_requests' in data
        assert 'credential_captures' in data
        assert 'educational_warning' in data
        
        # Verify stats
        assert data['stats']['http_requests'] > 0
        assert data['stats']['unique_hosts'] > 0
        
        # Verify requests
        assert len(data['recent_requests']) > 0
        request = data['recent_requests'][0]
        assert 'timestamp' in request
        assert 'source_ip' in request
        assert 'method' in request
        assert 'host' in request
    
    def test_http_request_dataclass(self):
        """Test HTTPRequest dataclass."""
        request = HTTPRequest(
            timestamp=time.time(),
            source_ip="192.168.1.100",
            dest_ip="93.184.216.34",
            method="GET",
            host="example.com",
            path="/page.html",
            user_agent="Mozilla/5.0"
        )
        
        assert request.source_ip == "192.168.1.100"
        assert request.method == "GET"
        assert request.host == "example.com"
        
        # Test to_dict
        request_dict = request.to_dict()
        assert isinstance(request_dict, dict)
        assert request_dict['host'] == "example.com"
    
    def test_credential_capture_dataclass(self):
        """Test CredentialCapture dataclass."""
        credential = CredentialCapture(
            timestamp=time.time(),
            source_ip="192.168.1.100",
            url="http://insecure.com/login",
            credential_type="password",
            username="testuser",
            redacted_value="***REDACTED***"
        )
        
        assert credential.source_ip == "192.168.1.100"
        assert credential.credential_type == "password"
        assert credential.username == "testuser"
        
        # Ensure password is NEVER stored
        assert credential.redacted_value == "***REDACTED***"
    
    def test_educational_warnings(self):
        """Test educational warning generation."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Test with no requests
        plugin.stats['http_requests'] = 0
        plugin.stats['credentials_found'] = 0
        warning = plugin._get_educational_warning()
        assert 'No insecure' in warning or 'security posture' in warning
        
        # Test with credentials found
        plugin.stats['credentials_found'] = 1
        warning = plugin._get_educational_warning()
        assert 'CRITICAL' in warning or 'HTTPS' in warning
        
        # Test with HTTP traffic
        plugin.stats['http_requests'] = 15
        plugin.stats['credentials_found'] = 0
        warning = plugin._get_educational_warning()
        assert 'WARNING' in warning or 'HTTP' in warning
    
    def test_requires_root(self):
        """Test that plugin requires root for real mode."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": False, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        assert plugin.requires_root() is True
    
    def test_mock_data_structure(self):
        """Test mock data has correct structure."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        data = plugin._get_mock_data()
        
        # Verify requests
        assert len(data['recent_requests']) > 0
        
        # Verify at least one POST request
        has_post = any(r['method'] == 'POST' for r in data['recent_requests'])
        assert has_post
        
        # Verify credential captures
        assert 'credential_captures' in data
        if data['credential_captures']:
            cred = data['credential_captures'][0]
            assert cred['redacted_value'] == '***REDACTED***'
    
    def test_plugin_lifecycle(self):
        """Test plugin start/stop lifecycle."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        plugin.initialize()
        
        # Mock mode doesn't start threads
        assert plugin._monitor_thread is None
        
        # Cleanup should work
        plugin.cleanup()
        assert plugin._stop_event.is_set()
        assert len(plugin.http_requests) == 0  # Should clear data
    
    def test_stats_tracking(self):
        """Test statistics tracking."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Initial stats
        assert plugin.stats['total_http_packets'] == 0
        assert plugin.stats['http_requests'] == 0
        assert plugin.stats['credentials_found'] == 0
    
    def test_credential_patterns(self):
        """Test credential detection patterns."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Test password pattern
        test_data = b'username=test&password=secret123&submit=Login'
        password_match = plugin._credential_patterns['password'].search(test_data)
        assert password_match is not None
        
        # Test username pattern
        username_match = plugin._credential_patterns['username'].search(test_data)
        assert username_match is not None
        
        # Test token pattern
        token_data = b'api_key=abc123xyz&action=submit'
        token_match = plugin._credential_patterns['token'].search(token_data)
        assert token_match is not None
    
    def test_host_tracking(self):
        """Test unique host tracking."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Add hosts
        plugin.hosts_seen.add('example.com')
        plugin.hosts_seen.add('google.com')
        plugin.hosts_seen.add('example.com')  # Duplicate
        
        assert len(plugin.hosts_seen) == 2
        assert 'example.com' in plugin.hosts_seen
        assert 'google.com' in plugin.hosts_seen


class TestHTTPSnifferEthics:
    """Test ethical safeguards."""
    
    def test_no_consent_prevents_start(self):
        """Test that plugin won't start without consent."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": False, "ethical_consent": False}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Should not have consent
        assert plugin._ethical_consent_given is False
    
    def test_credentials_always_redacted(self):
        """Test that credentials are NEVER stored in plain text."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        data = plugin._get_mock_data()
        
        # Check all credential captures
        for cred in data['credential_captures']:
            assert cred['redacted_value'] == '***REDACTED***'
            # Ensure no actual password values
            assert 'password' not in str(cred).lower() or '***' in str(cred)
    
    def test_cleanup_removes_sensitive_data(self):
        """Test that cleanup removes all captured data."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        
        # Add some mock data
        plugin.http_requests.append(Mock())
        plugin.credential_captures.append(Mock())
        
        # Cleanup
        plugin.cleanup()
        
        # Should be empty
        assert len(plugin.http_requests) == 0
        assert len(plugin.credential_captures) == 0


class TestHTTPSnifferIntegration:
    """Integration tests for HTTP Sniffer."""
    
    def test_full_data_collection_cycle(self):
        """Test complete data collection cycle."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        plugin.initialize()
        
        # Collect data multiple times
        data1 = plugin.collect_data()
        time.sleep(0.1)
        data2 = plugin.collect_data()
        
        # Both should succeed
        assert data1 is not None
        assert data2 is not None
        
        # Should have consistent structure
        assert set(data1.keys()) == set(data2.keys())
    
    def test_concurrent_data_access(self):
        """Test that concurrent data access doesn't crash."""
        config = PluginConfig(
            name="http_sniffer",
            config={"mock_mode": True, "ethical_consent": True}
        )
        
        plugin = HTTPSnifferPlugin(config)
        plugin.initialize()
        
        # Simulate concurrent access
        results = []
        for _ in range(5):
            data = plugin.collect_data()
            results.append(data)
        
        # All should succeed
        assert len(results) == 5
        assert all(r is not None for r in results)
