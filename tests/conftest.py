"""
Pytest configuration and fixtures for WiFi Security Education Platform.

Boris's Testing Philosophy:
- Real tests, not fake assertions
- Mock only external dependencies (network, hardware)
- Test behavior, not implementation details
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def mock_network_interface():
    """Mock network interface for testing without hardware."""
    return "wlan0"


@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls for system commands."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout="mock output",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def mock_scapy():
    """Mock Scapy for packet capture testing."""
    with patch("scapy.all.sniff") as mock_sniff, \
         patch("scapy.all.ARP") as mock_arp, \
         patch("scapy.all.Ether") as mock_ether:
        
        mock_sniff.return_value = []
        yield {
            "sniff": mock_sniff,
            "ARP": mock_arp,
            "Ether": mock_ether
        }


@pytest.fixture
def mock_network_data():
    """Real-looking mock network data."""
    return {
        "devices": [
            {
                "ip": "192.168.1.1",
                "mac": "aa:bb:cc:dd:ee:ff",
                "hostname": "router.local",
                "vendor": "TP-Link"
            },
            {
                "ip": "192.168.1.50",
                "mac": "11:22:33:44:55:66",
                "hostname": "laptop.local",
                "vendor": "Dell"
            }
        ],
        "gateway": {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff"
        }
    }


@pytest.fixture
def sample_pcap_path(tmp_path):
    """Create temporary pcap file for testing."""
    pcap_file = tmp_path / "test_capture.pcap"
    pcap_file.write_bytes(b"")  # Empty pcap
    return str(pcap_file)


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    yield
    # Clear any cached plugin instances
    from plugins.base import BasePlugin
    if hasattr(BasePlugin, "_instances"):
        BasePlugin._instances.clear()


# Boris's test markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, no I/O)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (may require hardware)"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests (>1s)"
    )
    config.addinivalue_line(
        "markers", "requires_root: Tests requiring root privileges"
    )
    config.addinivalue_line(
        "markers", "requires_hardware: Tests requiring specific hardware"
    )
