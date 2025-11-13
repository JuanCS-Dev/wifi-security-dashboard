"""
Tests for DNS Monitor Plugin - Feature 3

Tests DNS query monitoring and educational features.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import pytest
import time
from unittest.mock import Mock, patch

from src.plugins.base import PluginConfig
from src.plugins.dns_monitor_plugin import DNSMonitorPlugin, DNSQuery


class TestDNSMonitorPlugin:
    """Test DNS Monitor Plugin functionality."""
    
    def test_plugin_initialization_mock_mode(self):
        """Test plugin initializes correctly in mock mode."""
        config = PluginConfig(
            name="dns_monitor",
            rate_ms=500,
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        plugin.initialize()
        
        assert plugin is not None
        assert plugin.config.name == "dns_monitor"
    
    def test_collect_mock_data(self):
        """Test collecting mock DNS data."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()
        
        # Verify mock data structure
        assert 'monitoring' in data
        assert 'stats' in data
        assert 'recent_queries' in data
        assert 'top_domains' in data
        assert 'query_types' in data
        assert 'educational_tip' in data
        
        # Verify stats
        assert data['stats']['total_queries'] > 0
        assert data['stats']['unique_domains'] > 0
        
        # Verify queries
        assert len(data['recent_queries']) > 0
        query = data['recent_queries'][0]
        assert 'timestamp' in query
        assert 'source_ip' in query
        assert 'domain' in query
        assert 'query_type' in query
    
    def test_dns_query_dataclass(self):
        """Test DNSQuery dataclass."""
        query = DNSQuery(
            timestamp=time.time(),
            source_ip="192.168.1.100",
            domain="google.com",
            query_type="A",
            resolved_ip="142.250.185.46"
        )
        
        assert query.source_ip == "192.168.1.100"
        assert query.domain == "google.com"
        assert query.query_type == "A"
        assert query.resolved_ip == "142.250.185.46"
        
        # Test to_dict
        query_dict = query.to_dict()
        assert isinstance(query_dict, dict)
        assert query_dict['domain'] == "google.com"
    
    def test_query_type_mapping(self):
        """Test query type number to name mapping."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        
        # Test known types
        assert plugin._get_query_type_name(1) == 'A'
        assert plugin._get_query_type_name(28) == 'AAAA'
        assert plugin._get_query_type_name(15) == 'MX'
        assert plugin._get_query_type_name(16) == 'TXT'
        
        # Test unknown type
        assert plugin._get_query_type_name(999) == 'TYPE999'
    
    def test_educational_tips(self):
        """Test educational tip generation."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        
        # Test with no queries
        plugin.stats['total_queries'] = 0
        tip = plugin._get_educational_tip()
        assert 'DNS' in tip or 'Domain Name System' in tip
        
        # Test with few queries
        plugin.stats['total_queries'] = 5
        tip = plugin._get_educational_tip()
        assert isinstance(tip, str)
        assert len(tip) > 0
        
        # Test with many queries
        plugin.stats['total_queries'] = 100
        tip = plugin._get_educational_tip()
        assert isinstance(tip, str)
    
    def test_requires_root(self):
        """Test that plugin requires root for real mode."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": False}
        )
        
        plugin = DNSMonitorPlugin(config)
        assert plugin.requires_root() is True
    
    def test_mock_data_structure(self):
        """Test mock data has correct structure."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        data = plugin._get_mock_data()
        
        # Verify top domains
        assert len(data['top_domains']) > 0
        domain, count = data['top_domains'][0]
        assert isinstance(domain, str)
        assert isinstance(count, int)
        assert count > 0
        
        # Verify query types
        assert 'A' in data['query_types']
        assert data['query_types']['A'] > 0
    
    def test_plugin_lifecycle(self):
        """Test plugin start/stop lifecycle."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        plugin.initialize()
        
        # Mock mode doesn't start threads
        assert plugin._monitor_thread is None
        
        # Cleanup should work
        plugin.cleanup()
        assert plugin._stop_event.is_set()
    
    def test_stats_tracking(self):
        """Test statistics tracking."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        
        # Initial stats
        assert plugin.stats['total_queries'] == 0
        assert plugin.stats['unique_domains'] == 0
        assert plugin.stats['queries_per_minute'] == 0.0
    
    def test_domain_counter(self):
        """Test domain counting functionality."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        
        # Simulate adding domains
        plugin.domain_counter['google.com'] += 1
        plugin.domain_counter['google.com'] += 1
        plugin.domain_counter['facebook.com'] += 1
        
        assert plugin.domain_counter['google.com'] == 2
        assert plugin.domain_counter['facebook.com'] == 1
        
        # Get top domains
        top = plugin.domain_counter.most_common(2)
        assert len(top) == 2
        assert top[0][0] == 'google.com'
        assert top[0][1] == 2


class TestDNSMonitorIntegration:
    """Integration tests for DNS Monitor."""
    
    def test_full_data_collection_cycle(self):
        """Test complete data collection cycle."""
        config = PluginConfig(
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
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
            name="dns_monitor",
            config={"mock_mode": True}
        )
        
        plugin = DNSMonitorPlugin(config)
        plugin.initialize()
        
        # Simulate concurrent access
        results = []
        for _ in range(5):
            data = plugin.collect_data()
            results.append(data)
        
        # All should succeed
        assert len(results) == 5
        assert all(r is not None for r in results)
