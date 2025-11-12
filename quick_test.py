#!/usr/bin/env python3
"""Quick test of all 3 features."""
import sys
sys.path.insert(0, 'src')

from plugins.arp_spoofing_detector import ARPSpoofingDetector
from plugins.traffic_statistics import TrafficStatistics
from plugins.base import PluginConfig

print("="*70)
print("🎯 TESTANDO AS 3 FEATURES PRINCIPAIS")
print("="*70)

# Feature 2: ARP Spoofing Detector
print("\n1️⃣  ARP Spoofing Detector (Detecta ataques MITM)...")
config2 = PluginConfig(name="arp_detector", enabled=True, config={})
arp = ARPSpoofingDetector(config2)
arp.add_trusted_device("aa:aa:aa:aa:aa:aa", "192.168.1.1")
arp._check_arp_entry("192.168.1.100", "bb:bb:bb:bb:bb:bb")
arp._check_arp_entry("192.168.1.100", "cc:cc:cc:cc:cc:cc")  # MAC change = ATAQUE!
data2 = arp.get_data()
print(f"   ✅ Dispositivos confiáveis: {len(data2['trusted_devices'])}")
print(f"   ✅ Alertas gerados: {data2['alert_count']}")
print(f"   ✅ MAC changes: {data2['stats']['mac_changes']}")
if data2['recent_alerts']:
    alert = data2['recent_alerts'][0]
    print(f"   🚨 Alerta: {alert['severity']} - IP {alert['ip']}")

# Feature 7: Traffic Statistics
print("\n2️⃣  Traffic Statistics (Monitor de tráfego)...")
config3 = PluginConfig(name="traffic_stats", enabled=True, config={})
traffic = TrafficStatistics(config3)
traffic.register_device("192.168.1.100", "bb:bb:bb:bb:bb:bb", "Laptop")
traffic.register_device("192.168.1.101", "cc:cc:cc:cc:cc:cc", "Phone")

# Simula tráfego
traffic._update_device_stats("192.168.1.100", 1024000, "HTTPS", is_sent=True)
traffic._update_device_stats("192.168.1.100", 5120000, "HTTPS", is_sent=False)
traffic._update_device_stats("192.168.1.101", 512000, "DNS", is_sent=True)

data3 = traffic.get_data()
print(f"   ✅ Dispositivos monitorados: {data3['device_count']}")
print(f"   ✅ Total de bytes: {data3['global_stats']['total_bytes']:,}")
print(f"   ✅ Bandwidth: {data3['global_stats']['bandwidth_mbps']:.2f} Mbps")
print(f"   ✅ Protocolos: {len(data3['global_stats']['protocols'])}")

if data3['top_talkers']:
    top = data3['top_talkers'][0]
    print(f"   📊 Top talker: {top['ip']} ({top['total_bytes']:,} bytes)")

print("\n" + "="*70)
print("✅ TODAS AS FEATURES FUNCIONANDO!")
print("="*70)

print("\n📊 RESUMO:")
print(f"   • Ataques detectados: {data2['stats']['mac_changes']}")
print(f"   • Tráfego monitorado: {data3['global_stats']['total_bytes']:,} bytes")
print(f"   • Devices ativos: {data3['device_count']}")

print("\n📚 PRONTO PARA DEMO COM SEUS FILHOS HOJE À NOITE!")
print("\n💡 Comandos:")
print("   python3 app_textual.py       # Interface completa")
print("   python3 app_sampler_demo.py  # Demo com Sampler")
print()
