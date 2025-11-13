"""
DNS Query Monitor Plugin - Feature 3

Monitors all DNS queries in real-time.
Educational tool to demonstrate what websites are being accessed.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

try:
    from scapy.all import DNS, DNSQR, DNSRR, sniff, conf, IP
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class DNSQuery:
    """Represents a DNS query."""
    timestamp: float
    source_ip: str
    domain: str
    query_type: str
    resolved_ip: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DNSMonitorPlugin(Plugin):
    """
    DNS Query Monitor - Captures all DNS traffic.
    
    Educational Features:
    - Real-time DNS query stream
    - Top domains accessed
    - Query type distribution (A, AAAA, MX, etc.)
    - Privacy awareness demonstration
    - Domain categorization
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Query storage: recent queries (last 100)
        self.recent_queries: List[DNSQuery] = []
        
        # Domain tracking: {domain: count}
        self.domain_counter: Counter = Counter()
        
        # Query type tracking: {type: count}
        self.query_types: Counter = Counter()
        
        # IP resolution cache: {domain: ip}
        self.dns_cache: Dict[str, str] = {}
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.stats = {
            'total_queries': 0,
            'unique_domains': 0,
            'queries_per_minute': 0.0,
            'cache_hits': 0
        }
        
        # Rate tracking for queries/minute
        self._query_timestamps: List[float] = []
    
    def initialize(self) -> None:
        """Initialize plugin."""
        if self.config.config.get('mock_mode', False):
            logger.info("DNS Monitor initialized in MOCK mode")
            return
        
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect DNS monitoring data."""
        if self.config.config.get('mock_mode', False):
            return self._get_mock_data()
        
        return self.get_data()
    
    def start(self):
        """Start DNS monitoring."""
        logger.info("Starting DNS Monitor...")
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_dns, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop DNS monitoring."""
        logger.info("Stopping DNS Monitor...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop()
    
    def get_data(self) -> Dict[str, Any]:
        """Get current monitoring data."""
        # Update queries per minute
        current_time = time.time()
        recent_timestamps = [ts for ts in self._query_timestamps if current_time - ts < 60]
        self._query_timestamps = recent_timestamps
        self.stats['queries_per_minute'] = len(recent_timestamps)
        
        # Update unique domains count
        self.stats['unique_domains'] = len(self.domain_counter)
        
        # Get top 10 domains
        top_domains = self.domain_counter.most_common(10)
        
        # Get recent queries (last 20)
        recent = [q.to_dict() for q in self.recent_queries[-20:]]
        
        return {
            'monitoring': not self._stop_event.is_set(),
            'stats': self.stats.copy(),
            'recent_queries': recent,
            'top_domains': top_domains,
            'query_types': dict(self.query_types),
            'dns_cache_size': len(self.dns_cache),
            'educational_tip': self._get_educational_tip()
        }
    
    def requires_root(self) -> bool:
        """DNS sniffing requires root privileges."""
        return True
    
    def _monitor_dns(self):
        """Monitor DNS traffic continuously."""
        while not self._stop_event.is_set():
            try:
                # Sniff DNS packets (port 53)
                sniff(
                    filter="udp port 53",
                    prn=self._process_dns_packet,
                    store=0,
                    timeout=1
                )
            except Exception as e:
                logger.error(f"DNS monitoring error: {e}")
                time.sleep(1)
    
    def _process_dns_packet(self, packet):
        """Process individual DNS packet."""
        if not packet.haslayer(DNS):
            return
        
        dns_layer = packet[DNS]
        
        # DNS Query (Question)
        if dns_layer.qr == 0 and packet.haslayer(DNSQR):
            self._process_dns_query(packet)
        
        # DNS Response (Answer)
        elif dns_layer.qr == 1 and packet.haslayer(DNSRR):
            self._process_dns_response(packet)
    
    def _process_dns_query(self, packet):
        """Process DNS query packet."""
        try:
            source_ip = packet[IP].src if packet.haslayer(IP) else "unknown"
            dns_qr = packet[DNSQR]
            
            domain = dns_qr.qname.decode('utf-8').rstrip('.')
            query_type = self._get_query_type_name(dns_qr.qtype)
            
            # Create query object
            query = DNSQuery(
                timestamp=time.time(),
                source_ip=source_ip,
                domain=domain,
                query_type=query_type,
                resolved_ip=None
            )
            
            # Store query
            self.recent_queries.append(query)
            if len(self.recent_queries) > 100:
                self.recent_queries = self.recent_queries[-100:]
            
            # Update counters
            self.domain_counter[domain] += 1
            self.query_types[query_type] += 1
            self.stats['total_queries'] += 1
            
            # Track for rate calculation
            self._query_timestamps.append(query.timestamp)
            
            logger.debug(f"DNS Query: {domain} ({query_type}) from {source_ip}")
            
        except Exception as e:
            logger.error(f"Error processing DNS query: {e}")
    
    def _process_dns_response(self, packet):
        """Process DNS response packet."""
        try:
            dns_rr = packet[DNSRR]
            domain = dns_rr.rrname.decode('utf-8').rstrip('.')
            
            # Get resolved IP (if A or AAAA record)
            if dns_rr.type in [1, 28]:  # A or AAAA
                resolved_ip = dns_rr.rdata
                if isinstance(resolved_ip, bytes):
                    resolved_ip = resolved_ip.decode('utf-8')
                else:
                    resolved_ip = str(resolved_ip)
                
                # Update cache
                self.dns_cache[domain] = resolved_ip
                
                # Update recent query if exists
                for query in reversed(self.recent_queries):
                    if query.domain == domain and query.resolved_ip is None:
                        query.resolved_ip = resolved_ip
                        break
                
                logger.debug(f"DNS Response: {domain} -> {resolved_ip}")
                
        except Exception as e:
            logger.error(f"Error processing DNS response: {e}")
    
    def _get_query_type_name(self, qtype: int) -> str:
        """Convert query type number to name."""
        type_map = {
            1: 'A',       # IPv4 address
            2: 'NS',      # Name server
            5: 'CNAME',   # Canonical name
            6: 'SOA',     # Start of authority
            12: 'PTR',    # Pointer
            15: 'MX',     # Mail exchange
            16: 'TXT',    # Text
            28: 'AAAA',   # IPv6 address
            33: 'SRV',    # Service
            255: 'ANY'    # Any type
        }
        return type_map.get(qtype, f'TYPE{qtype}')
    
    def _get_educational_tip(self) -> str:
        """Generate educational tip based on current data."""
        total = self.stats['total_queries']
        
        if total == 0:
            return "💡 DNS = Domain Name System - traduz nomes (google.com) para IPs (142.250.185.46)"
        elif total < 10:
            return "👀 Cada site visitado gera múltiplas queries DNS (imagens, scripts, ads...)"
        elif total < 50:
            return "🔒 Use DNS criptografado (DoH/DoT) para proteger sua privacidade!"
        else:
            return "📊 Seu ISP pode ver TODOS os sites que você visita via DNS!"
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Generate mock DNS data for testing."""
        current_time = time.time()
        
        mock_queries = [
            {
                'timestamp': current_time - 5,
                'source_ip': '192.168.1.100',
                'domain': 'www.google.com',
                'query_type': 'A',
                'resolved_ip': '142.250.185.46'
            },
            {
                'timestamp': current_time - 10,
                'source_ip': '192.168.1.100',
                'domain': 'www.youtube.com',
                'query_type': 'A',
                'resolved_ip': '142.251.40.46'
            },
            {
                'timestamp': current_time - 15,
                'source_ip': '192.168.1.50',
                'domain': 'api.github.com',
                'query_type': 'A',
                'resolved_ip': '140.82.113.5'
            },
            {
                'timestamp': current_time - 20,
                'source_ip': '192.168.1.100',
                'domain': 'fonts.googleapis.com',
                'query_type': 'A',
                'resolved_ip': '142.250.185.42'
            },
            {
                'timestamp': current_time - 25,
                'source_ip': '192.168.1.75',
                'domain': 'www.facebook.com',
                'query_type': 'A',
                'resolved_ip': '157.240.241.35'
            }
        ]
        
        top_domains = [
            ('www.google.com', 45),
            ('www.youtube.com', 32),
            ('fonts.googleapis.com', 28),
            ('api.github.com', 15),
            ('www.facebook.com', 12),
            ('cdn.jsdelivr.net', 8),
            ('www.wikipedia.org', 6),
            ('stackoverflow.com', 5)
        ]
        
        query_types = {
            'A': 142,
            'AAAA': 38,
            'MX': 5,
            'TXT': 3,
            'CNAME': 12
        }
        
        return {
            'monitoring': True,
            'stats': {
                'total_queries': 200,
                'unique_domains': 45,
                'queries_per_minute': 12.5,
                'cache_hits': 78
            },
            'recent_queries': mock_queries,
            'top_domains': top_domains,
            'query_types': query_types,
            'dns_cache_size': 45,
            'educational_tip': '💡 DNS queries reveal your browsing history - use encrypted DNS!'
        }
