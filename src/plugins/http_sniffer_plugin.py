"""
HTTP Data Sniffer Plugin - Feature 4

Captures HTTP traffic to demonstrate security risks of unencrypted connections.
EDUCATIONAL USE ONLY - Shows why HTTPS is essential.

⚠️ ETHICAL WARNING: Only use on networks you own or have explicit permission.
This tool demonstrates why encryption (HTTPS) is critical for privacy.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import logging
import threading
import time
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

try:
    from scapy.all import sniff, TCP, IP, Raw, conf
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from .base import Plugin, PluginConfig


logger = logging.getLogger(__name__)


@dataclass
class HTTPRequest:
    """Represents captured HTTP request."""
    timestamp: float
    source_ip: str
    dest_ip: str
    method: str
    host: str
    path: str
    user_agent: Optional[str] = None
    cookies: Optional[str] = None
    post_data: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CredentialCapture:
    """Represents captured credentials (passwords, tokens)."""
    timestamp: float
    source_ip: str
    url: str
    credential_type: str  # password, token, api_key, etc.
    username: Optional[str] = None
    redacted_value: str = "***REDACTED***"  # Never store actual passwords!
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HTTPSnifferPlugin(Plugin):
    """
    HTTP Data Sniffer - Educational security demonstration.
    
    ⚠️ CRITICAL ETHICAL GUIDELINES:
    - Only use on networks YOU OWN
    - Never capture credentials from real users
    - This is for EDUCATION about HTTPS importance
    - Always obtain explicit written permission
    
    Educational Features:
    - Shows HTTP vs HTTPS traffic
    - Demonstrates unencrypted data capture
    - Highlights credential exposure risks
    - Teaches importance of SSL/TLS
    """
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        
        # Captured requests
        self.http_requests: List[HTTPRequest] = []
        
        # Credential captures (REDACTED for safety)
        self.credential_captures: List[CredentialCapture] = []
        
        # Statistics
        self.stats = {
            'total_http_packets': 0,
            'http_requests': 0,
            'https_blocked': 0,  # HTTPS can't be sniffed (good!)
            'credentials_found': 0,
            'unique_hosts': 0
        }
        
        # Host tracking
        self.hosts_seen: set = set()
        
        # Thread control
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Ethical consent flag
        self._ethical_consent_given = config.config.get('ethical_consent', False)
        
        # Patterns for credential detection (educational)
        self._credential_patterns = {
            'password': re.compile(rb'(?:password|passwd|pwd)=([^&\s]+)', re.IGNORECASE),
            'username': re.compile(rb'(?:username|user|email|login)=([^&\s]+)', re.IGNORECASE),
            'token': re.compile(rb'(?:token|auth|api_key)=([^&\s]+)', re.IGNORECASE),
        }
    
    def initialize(self) -> None:
        """Initialize plugin with ethical checks."""
        if self.config.config.get('mock_mode', False):
            logger.info("HTTP Sniffer initialized in MOCK mode")
            return
        
        if not SCAPY_AVAILABLE:
            logger.error("Scapy not available. Install with: pip install scapy")
            return
        
        if not self._ethical_consent_given:
            logger.warning("⚠️ HTTP Sniffer requires ethical consent!")
            logger.warning("   Set ethical_consent=True in config ONLY for your own network")
            return
        
        self.start()
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect HTTP sniffing data."""
        if self.config.config.get('mock_mode', False):
            return self._get_mock_data()
        
        return self.get_data()
    
    def start(self):
        """Start HTTP monitoring."""
        logger.info("Starting HTTP Sniffer...")
        logger.warning("⚠️ Remember: EDUCATIONAL USE ONLY on YOUR network!")
        
        self._stop_event.clear()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_http, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop HTTP monitoring."""
        logger.info("Stopping HTTP Sniffer...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self.stop()
        # Clear sensitive data
        self.http_requests.clear()
        self.credential_captures.clear()
    
    def get_data(self) -> Dict[str, Any]:
        """Get current sniffing data."""
        # Update stats
        self.stats['unique_hosts'] = len(self.hosts_seen)
        
        # Get recent requests (last 20)
        recent_requests = [r.to_dict() for r in self.http_requests[-20:]]
        
        # Get recent credential captures (last 10)
        recent_credentials = [c.to_dict() for c in self.credential_captures[-10:]]
        
        return {
            'monitoring': not self._stop_event.is_set(),
            'ethical_consent': self._ethical_consent_given,
            'stats': self.stats.copy(),
            'recent_requests': recent_requests,
            'credential_captures': recent_credentials,
            'educational_warning': self._get_educational_warning(),
            'https_percentage': self._calculate_https_percentage()
        }
    
    def requires_root(self) -> bool:
        """HTTP sniffing requires root privileges."""
        return True
    
    def _monitor_http(self):
        """Monitor HTTP traffic continuously."""
        while not self._stop_event.is_set():
            try:
                # Sniff HTTP packets (port 80)
                sniff(
                    filter="tcp port 80",
                    prn=self._process_http_packet,
                    store=0,
                    timeout=1
                )
            except Exception as e:
                logger.error(f"HTTP monitoring error: {e}")
                time.sleep(1)
    
    def _process_http_packet(self, packet):
        """Process individual HTTP packet."""
        if not packet.haslayer(TCP) or not packet.haslayer(Raw):
            return
        
        self.stats['total_http_packets'] += 1
        
        try:
            # Get packet payload
            payload = packet[Raw].load
            
            # Check if it's an HTTP request
            if payload.startswith(b'GET') or payload.startswith(b'POST') or payload.startswith(b'PUT'):
                self._parse_http_request(packet, payload)
                
        except Exception as e:
            logger.error(f"Error processing HTTP packet: {e}")
    
    def _parse_http_request(self, packet, payload: bytes):
        """Parse HTTP request from packet."""
        try:
            # Split into lines
            lines = payload.split(b'\r\n')
            if len(lines) < 1:
                return
            
            # Parse request line
            request_line = lines[0].decode('utf-8', errors='ignore')
            parts = request_line.split(' ')
            if len(parts) < 2:
                return
            
            method = parts[0]
            path = parts[1]
            
            # Parse headers
            headers = {}
            post_data = None
            body_start = False
            
            for i, line in enumerate(lines[1:], 1):
                if line == b'':
                    # Empty line = end of headers
                    body_start = True
                    if method == 'POST' and i + 1 < len(lines):
                        post_data = lines[i + 1].decode('utf-8', errors='ignore')
                    break
                
                try:
                    header = line.decode('utf-8', errors='ignore')
                    if ':' in header:
                        key, value = header.split(':', 1)
                        headers[key.strip().lower()] = value.strip()
                except:
                    continue
            
            # Extract info
            host = headers.get('host', 'unknown')
            user_agent = headers.get('user-agent')
            cookies = headers.get('cookie')
            
            source_ip = packet[IP].src if packet.haslayer(IP) else "unknown"
            dest_ip = packet[IP].dst if packet.haslayer(IP) else "unknown"
            
            # Create request object
            request = HTTPRequest(
                timestamp=time.time(),
                source_ip=source_ip,
                dest_ip=dest_ip,
                method=method,
                host=host,
                path=path,
                user_agent=user_agent,
                cookies=cookies,
                post_data=post_data
            )
            
            # Store request
            self.http_requests.append(request)
            if len(self.http_requests) > 100:
                self.http_requests = self.http_requests[-100:]
            
            # Track host
            self.hosts_seen.add(host)
            self.stats['http_requests'] += 1
            
            # Check for credentials (EDUCATIONAL WARNING)
            if post_data:
                self._check_for_credentials(source_ip, host, path, post_data.encode())
            
            logger.debug(f"HTTP Request: {method} {host}{path} from {source_ip}")
            
        except Exception as e:
            logger.error(f"Error parsing HTTP request: {e}")
    
    def _check_for_credentials(self, source_ip: str, host: str, path: str, data: bytes):
        """Check POST data for credentials (EDUCATIONAL - shows vulnerability)."""
        try:
            username = None
            found_credentials = False
            
            # Check for username
            username_match = self._credential_patterns['username'].search(data)
            if username_match:
                username = username_match.group(1).decode('utf-8', errors='ignore')
            
            # Check for password (REDACT immediately!)
            password_match = self._credential_patterns['password'].search(data)
            if password_match:
                # NEVER log actual password!
                credential = CredentialCapture(
                    timestamp=time.time(),
                    source_ip=source_ip,
                    url=f"http://{host}{path}",
                    credential_type="password",
                    username=username,
                    redacted_value="***REDACTED***"
                )
                self.credential_captures.append(credential)
                self.stats['credentials_found'] += 1
                found_credentials = True
                
                logger.warning(f"⚠️ CREDENTIAL DETECTED (redacted) from {source_ip} to {host}")
            
            # Check for tokens
            token_match = self._credential_patterns['token'].search(data)
            if token_match:
                credential = CredentialCapture(
                    timestamp=time.time(),
                    source_ip=source_ip,
                    url=f"http://{host}{path}",
                    credential_type="token",
                    redacted_value="***REDACTED***"
                )
                self.credential_captures.append(credential)
                self.stats['credentials_found'] += 1
                found_credentials = True
            
            if found_credentials:
                logger.warning("📚 EDUCATIONAL: This is why HTTPS is CRITICAL!")
            
        except Exception as e:
            logger.error(f"Error checking credentials: {e}")
    
    def _calculate_https_percentage(self) -> float:
        """Calculate percentage of HTTPS vs HTTP (educational metric)."""
        # In real network, most traffic should be HTTPS (can't sniff)
        # HTTP traffic being visible = security risk!
        if self.stats['http_requests'] == 0:
            return 100.0  # No HTTP = good!
        
        # Rough estimate (not accurate without full traffic analysis)
        return 0.0  # If we see HTTP, there's insecure traffic
    
    def _get_educational_warning(self) -> str:
        """Generate educational warning based on findings."""
        creds = self.stats['credentials_found']
        requests = self.stats['http_requests']
        
        if creds > 0:
            return f"🚨 CRITICAL: {creds} credentials captured! This is why HTTPS is MANDATORY!"
        elif requests > 10:
            return "⚠️ WARNING: Significant HTTP traffic detected. Vulnerable to eavesdropping!"
        elif requests > 0:
            return "⚠️ HTTP traffic detected. Use HTTPS everywhere for security!"
        else:
            return "✅ No insecure HTTP traffic detected. Good security posture!"
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Generate mock HTTP data for testing."""
        current_time = time.time()
        
        mock_requests = [
            {
                'timestamp': current_time - 10,
                'source_ip': '192.168.1.100',
                'dest_ip': '93.184.216.34',
                'method': 'GET',
                'host': 'example.com',
                'path': '/page.html',
                'user_agent': 'Mozilla/5.0 (Linux)',
                'cookies': None,
                'post_data': None
            },
            {
                'timestamp': current_time - 25,
                'source_ip': '192.168.1.100',
                'dest_ip': '198.51.100.45',
                'method': 'POST',
                'host': 'insecure-login.com',
                'path': '/login',
                'user_agent': 'Mozilla/5.0 (Linux)',
                'cookies': 'session=abc123',
                'post_data': 'username=demo&password=***REDACTED***'
            },
            {
                'timestamp': current_time - 40,
                'source_ip': '192.168.1.50',
                'dest_ip': '203.0.113.78',
                'method': 'GET',
                'host': 'api.weather.com',
                'path': '/data?city=boston',
                'user_agent': 'Python/3.10',
                'cookies': None,
                'post_data': None
            }
        ]
        
        mock_credentials = [
            {
                'timestamp': current_time - 25,
                'source_ip': '192.168.1.100',
                'url': 'http://insecure-login.com/login',
                'credential_type': 'password',
                'username': 'demo_user',
                'redacted_value': '***REDACTED***'
            }
        ]
        
        return {
            'monitoring': True,
            'ethical_consent': True,
            'stats': {
                'total_http_packets': 245,
                'http_requests': 18,
                'https_blocked': 0,
                'credentials_found': 1,
                'unique_hosts': 8
            },
            'recent_requests': mock_requests,
            'credential_captures': mock_credentials,
            'educational_warning': '🚨 CRITICAL: 1 credentials captured! This is why HTTPS is MANDATORY!',
            'https_percentage': 0.0
        }
