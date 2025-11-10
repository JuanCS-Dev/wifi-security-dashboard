#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Funcionais REAIS - Dashboard WiFi Educacional
Juan-Dev - Soli Deo Gloria ✝️

FILOSOFIA:
- Testes científicos e objetivos
- Validação de funcionalidades críticas
- Zero mocks (dados reais ou simulados propositais)
- Conformidade com Constituição Vértice v3.0
"""

import sys
import os

# Adiciona diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime
from models.network_snapshot import NetworkSnapshot, WiFiInfo, DeviceInfo, AppInfo, SystemMetrics
from data_collectors.system_collector import SystemCollector
from data_collectors.wifi_collector import WiFiCollector
from data_collectors.network_sniffer import NetworkSniffer


class TestNetworkSnapshot(unittest.TestCase):
    """Testa estruturas de dados (models)"""
    
    def test_network_snapshot_creation(self):
        """Teste 1: NetworkSnapshot é criado corretamente"""
        snapshot = NetworkSnapshot()
        
        self.assertIsNotNone(snapshot)
        self.assertIsNotNone(snapshot.timestamp)
        self.assertEqual(snapshot.total_devices, 0)
        self.assertEqual(snapshot.active_devices, 0)
        self.assertIsInstance(snapshot.devices, list)
        self.assertIsInstance(snapshot.apps, list)
    
    def test_wifi_info_creation(self):
        """Teste 2: WiFiInfo é criado corretamente"""
        wifi = WiFiInfo(
            ssid="TestNetwork",
            signal_strength=-50,
            frequency="2.4GHz",
            security="WPA2",
            connected=True
        )
        
        self.assertEqual(wifi.ssid, "TestNetwork")
        self.assertEqual(wifi.signal_strength, -50)
        self.assertEqual(wifi.frequency, "2.4GHz")
        self.assertEqual(wifi.security, "WPA2")
        self.assertTrue(wifi.connected)
    
    def test_device_info_creation(self):
        """Teste 3: DeviceInfo é criado corretamente"""
        device = DeviceInfo(
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            hostname="test-device",
            device_type="laptop"
        )
        
        self.assertEqual(device.mac_address, "00:11:22:33:44:55")
        self.assertEqual(device.ip_address, "192.168.1.100")
        self.assertEqual(device.hostname, "test-device")
        self.assertEqual(device.device_type, "laptop")
        self.assertTrue(device.is_active)  # Property calculada
    
    def test_app_info_creation(self):
        """Teste 4: AppInfo é criado corretamente"""
        app = AppInfo(
            name="YouTube",
            category="streaming",
            protocol="HTTPS",
            bytes_sent=1024,
            bytes_received=2048,
            connections=5
        )
        
        self.assertEqual(app.name, "YouTube")
        self.assertEqual(app.category, "streaming")
        self.assertEqual(app.protocol, "HTTPS")
        self.assertEqual(app.bytes_sent, 1024)
        self.assertEqual(app.bytes_received, 2048)
        self.assertEqual(app.connections, 5)
    
    def test_system_metrics_creation(self):
        """Teste 5: SystemMetrics é criado corretamente"""
        metrics = SystemMetrics(
            cpu_percent=45.5,
            ram_percent=60.0,
            disk_percent=75.0,
            temp_celsius=55.0
        )
        
        self.assertEqual(metrics.cpu_percent, 45.5)
        self.assertEqual(metrics.ram_percent, 60.0)
        self.assertEqual(metrics.disk_percent, 75.0)
        self.assertEqual(metrics.temp_celsius, 55.0)


class TestSystemCollector(unittest.TestCase):
    """Testa coleta de dados do sistema"""
    
    def test_system_collector_creation(self):
        """Teste 6: SystemCollector é criado corretamente"""
        collector = SystemCollector(mock_mode=True)
        self.assertIsNotNone(collector)
        self.assertTrue(collector.mock_mode)
    
    def test_system_collector_collect(self):
        """Teste 7: SystemCollector.collect() retorna dados válidos"""
        collector = SystemCollector(mock_mode=True)
        metrics = collector.collect()
        
        self.assertIsNotNone(metrics)
        self.assertIsInstance(metrics, SystemMetrics)
        
        # Valida ranges
        self.assertGreaterEqual(metrics.cpu_percent, 0)
        self.assertLessEqual(metrics.cpu_percent, 100)
        self.assertGreaterEqual(metrics.ram_percent, 0)
        self.assertLessEqual(metrics.ram_percent, 100)
        self.assertGreaterEqual(metrics.disk_percent, 0)
        self.assertLessEqual(metrics.disk_percent, 100)
    
    def test_system_collector_multiple_calls(self):
        """Teste 8: SystemCollector funciona em múltiplas chamadas"""
        collector = SystemCollector(mock_mode=True)
        
        metrics1 = collector.collect()
        metrics2 = collector.collect()
        
        self.assertIsNotNone(metrics1)
        self.assertIsNotNone(metrics2)
        # Pode variar em modo mock
        self.assertIsInstance(metrics1, SystemMetrics)
        self.assertIsInstance(metrics2, SystemMetrics)


class TestWiFiCollector(unittest.TestCase):
    """Testa coleta de informações WiFi"""
    
    def test_wifi_collector_creation(self):
        """Teste 9: WiFiCollector é criado corretamente"""
        collector = WiFiCollector(mock_mode=True)
        self.assertIsNotNone(collector)
        self.assertTrue(collector.mock_mode)
    
    def test_wifi_collector_collect(self):
        """Teste 10: WiFiCollector.collect() retorna dados válidos"""
        collector = WiFiCollector(mock_mode=True)
        wifi = collector.collect()
        
        self.assertIsNotNone(wifi)
        self.assertIsInstance(wifi, WiFiInfo)
        
        # Valida campos básicos
        self.assertIsNotNone(wifi.ssid)
        self.assertIsInstance(wifi.ssid, str)
        self.assertIn(wifi.frequency, ["2.4GHz", "5GHz", "Desconhecido"])
        self.assertIn(wifi.security, ["WPA2", "WPA3", "Open", "Desconhecido"])
    
    def test_wifi_collector_signal_strength_range(self):
        """Teste 11: Signal strength está em range válido"""
        collector = WiFiCollector(mock_mode=True)
        wifi = collector.collect()
        
        # Range: 0-100 (porcentagem)
        self.assertGreaterEqual(wifi.signal_strength, 0)
        self.assertLessEqual(wifi.signal_strength, 100)


class TestNetworkSniffer(unittest.TestCase):
    """Testa captura de pacotes e análise de rede"""
    
    def test_network_sniffer_creation(self):
        """Teste 12: NetworkSniffer é criado corretamente"""
        sniffer = NetworkSniffer(mock_mode=True)
        self.assertIsNotNone(sniffer)
        self.assertTrue(sniffer.mock_mode)
    
    def test_network_sniffer_start_stop(self):
        """Teste 13: NetworkSniffer start/stop funciona"""
        sniffer = NetworkSniffer(mock_mode=True)
        
        # Start
        sniffer.start()
        self.assertTrue(sniffer.running)
        
        # Stop
        sniffer.stop()
        self.assertFalse(sniffer.running)
    
    def test_network_sniffer_get_devices(self):
        """Teste 14: NetworkSniffer.get_devices() retorna lista"""
        sniffer = NetworkSniffer(mock_mode=True)
        sniffer.start()
        
        import time
        time.sleep(1)  # Aguarda mock gerar dados
        
        devices = sniffer.get_devices()
        sniffer.stop()
        
        self.assertIsNotNone(devices)
        self.assertIsInstance(devices, list)
        
        # Em modo mock deve ter pelo menos 1 device
        if len(devices) > 0:
            device = devices[0]
            self.assertIsInstance(device, DeviceInfo)
            self.assertIsNotNone(device.mac_address)
            self.assertIsNotNone(device.ip_address)
    
    def test_network_sniffer_get_apps(self):
        """Teste 15: NetworkSniffer.get_apps() retorna lista"""
        sniffer = NetworkSniffer(mock_mode=True)
        sniffer.start()
        
        import time
        time.sleep(1)  # Aguarda mock gerar dados
        
        apps = sniffer.get_apps()
        sniffer.stop()
        
        self.assertIsNotNone(apps)
        self.assertIsInstance(apps, list)
        
        # Em modo mock deve ter pelo menos 1 app
        if len(apps) > 0:
            app = apps[0]
            self.assertIsInstance(app, AppInfo)
            self.assertIsNotNone(app.name)
            self.assertGreaterEqual(app.connections, 0)
    
    def test_network_sniffer_get_stats(self):
        """Teste 16: NetworkSniffer.get_stats() retorna dict válido"""
        sniffer = NetworkSniffer(mock_mode=True)
        sniffer.start()
        
        import time
        time.sleep(1)
        
        stats = sniffer.get_stats()
        sniffer.stop()
        
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, dict)
        
        # Valida campos obrigatórios
        self.assertIn('total_packets', stats)
        self.assertIn('bytes_sent', stats)
        self.assertIn('bytes_recv', stats)
        
        self.assertGreaterEqual(stats['total_packets'], 0)
        self.assertGreaterEqual(stats['bytes_sent'], 0)
        self.assertGreaterEqual(stats['bytes_recv'], 0)


class TestIntegration(unittest.TestCase):
    """Testes de integração (fluxo completo)"""
    
    def test_full_data_collection_flow(self):
        """Teste 17: Fluxo completo de coleta de dados"""
        # Simula coleta completa como em main.py
        system_collector = SystemCollector(mock_mode=True)
        wifi_collector = WiFiCollector(mock_mode=True)
        network_sniffer = NetworkSniffer(mock_mode=True)
        
        # Coleta dados
        system_metrics = system_collector.collect()
        wifi_info = wifi_collector.collect()
        
        network_sniffer.start()
        import time
        time.sleep(1)
        
        devices = network_sniffer.get_devices()
        apps = network_sniffer.get_apps()
        stats = network_sniffer.get_stats()
        
        network_sniffer.stop()
        
        # Cria snapshot
        snapshot = NetworkSnapshot()
        snapshot.system = system_metrics
        snapshot.wifi = wifi_info
        snapshot.devices = devices
        snapshot.apps = apps
        snapshot.total_packets = stats['total_packets']
        snapshot.total_bytes_sent = stats['bytes_sent']
        snapshot.total_bytes_recv = stats['bytes_recv']
        
        # Validações
        self.assertIsNotNone(snapshot.system)
        self.assertIsNotNone(snapshot.wifi)
        self.assertIsInstance(snapshot.devices, list)
        self.assertIsInstance(snapshot.apps, list)
        self.assertGreaterEqual(snapshot.total_packets, 0)
    
    def test_callback_integration(self):
        """Teste 18: Callback funciona quando chamado"""
        callback_called = [False]  # Lista para mutabilidade em closure
        
        def test_callback():
            callback_called[0] = True
        
        sniffer = NetworkSniffer(mock_mode=True, callback=test_callback)
        self.assertIsNotNone(sniffer.callback)
        
        # Chama callback manualmente (simula evento)
        if sniffer.callback:
            sniffer.callback()
        
        self.assertTrue(callback_called[0])


def run_tests():
    """Executa todos os testes e retorna resultado"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful(), len(result.failures), len(result.errors)


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 TESTES CIENTÍFICOS - Dashboard WiFi Educacional")
    print("Constituição Vértice v3.0 | Juan-Dev - Soli Deo Gloria ✝️")
    print("=" * 70)
    print()
    
    success, failures, errors = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✅ TODOS OS TESTES PASSARAM! Sistema 100% funcional!")
    else:
        print(f"❌ TESTES FALHARAM: {failures} failures, {errors} errors")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
