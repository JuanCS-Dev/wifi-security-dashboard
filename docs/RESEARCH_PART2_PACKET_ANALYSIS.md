# 📊 DEEP RESEARCH - PARTE 2: PACKET ANALYSIS & SYSTEM MONITORS

**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Projeto:** WiFi Security Education Dashboard - Aula 2
**Objetivo:** Análise profunda de pacotes e visualização de sistema

---

## 🎯 ÍNDICE - PARTE 2

1. [PACKET ANALYSIS PROFUNDO](#packet-analysis)
   - 1.1 [tshark (Wireshark CLI)](#tshark)
   - 1.2 [Wireshark Display Filters](#wireshark-filters)
   - 1.3 [Scapy (Python Packet Manipulation)](#scapy)
   - 1.4 [tcpdump & BPF Filters](#tcpdump)
   - 1.5 [Padrões de Análise de Tráfego](#traffic-patterns)

2. [SYSTEM MONITORS TUI](#system-monitors)
   - 2.1 [btop++ (C++)](#btop)
   - 2.2 [bottom (Rust)](#bottom)
   - 2.3 [gtop (Node.js)](#gtop)
   - 2.4 [Análise Comparativa](#monitor-comparison)

3. [BANDWIDTH CALCULATION & METRICS](#bandwidth)
   - 3.1 [Cálculo de Bandwidth](#bandwidth-calc)
   - 3.2 [Métricas de Rede](#network-metrics)
   - 3.3 [Performance Measurement](#performance)

4. [WIFI MONITORING TOOLS](#wifi-tools)
   - 4.1 [aircrack-ng Suite](#aircrack)
   - 4.2 [iwconfig/iw](#iwconfig)
   - 4.3 [wavemon](#wavemon)
   - 4.4 [WiFi Security Analysis](#wifi-security)

---

<a name="packet-analysis"></a>
## 1. PACKET ANALYSIS PROFUNDO

<a name="tshark"></a>
### 1.1 TSHARK (Wireshark CLI)

**Website:** https://www.wireshark.org/docs/man-pages/tshark.html
**Linguagem:** C
**Licença:** GPL-2.0

#### Visão Geral

**tshark** é a versão command-line do Wireshark. Extremamente poderoso para análise automatizada de pacotes.

#### Instalação

```bash
# Debian/Ubuntu
sudo apt install tshark

# Fedora/RHEL
sudo dnf install wireshark-cli

# macOS
brew install wireshark

# Permitir non-root capture (Linux)
sudo dpkg-reconfigure wireshark-common
sudo usermod -a -G wireshark $USER
```

---

#### Capture Básico

```bash
# Captura em interface específica
tshark -i wlan0

# Captura N pacotes
tshark -i wlan0 -c 100

# Salva em arquivo pcap
tshark -i wlan0 -w capture.pcap

# Lê de arquivo pcap
tshark -r capture.pcap
```

---

#### Display Filters (Poderosos!)

**Filtros de Protocolo:**

```bash
# Apenas HTTP
tshark -i wlan0 -Y "http"

# Apenas DNS
tshark -i wlan0 -Y "dns"

# Apenas TLS/SSL
tshark -i wlan0 -Y "tls"

# Apenas TCP
tshark -i wlan0 -Y "tcp"

# Apenas UDP
tshark -i wlan0 -Y "udp"
```

**Filtros de IP:**

```bash
# Tráfego de/para IP específico
tshark -i wlan0 -Y "ip.addr == 192.168.1.100"

# Apenas source IP
tshark -i wlan0 -Y "ip.src == 192.168.1.100"

# Apenas destination IP
tshark -i wlan0 -Y "ip.dst == 8.8.8.8"

# Range de IPs
tshark -i wlan0 -Y "ip.addr >= 192.168.1.0 and ip.addr <= 192.168.1.255"
```

**Filtros de Porta:**

```bash
# Porta específica (TCP ou UDP)
tshark -i wlan0 -Y "tcp.port == 443 or udp.port == 443"

# Apenas porta source
tshark -i wlan0 -Y "tcp.srcport == 443"

# Apenas porta dest
tshark -i wlan0 -Y "tcp.dstport == 80"

# Múltiplas portas
tshark -i wlan0 -Y "tcp.port in {80 443 8080 8443}"
```

**Filtros Avançados:**

```bash
# HTTP GET requests
tshark -i wlan0 -Y "http.request.method == GET"

# HTTP responses com erro
tshark -i wlan0 -Y "http.response.code >= 400"

# DNS queries para domínio específico
tshark -i wlan0 -Y "dns.qry.name contains google.com"

# TCP SYN packets (port scanning)
tshark -i wlan0 -Y "tcp.flags.syn == 1 and tcp.flags.ack == 0"

# Pacotes grandes (> 1000 bytes)
tshark -i wlan0 -Y "frame.len > 1000"

# TLS handshake
tshark -i wlan0 -Y "tls.handshake.type == 1"
```

**Combinações Lógicas:**

```bash
# AND
tshark -i wlan0 -Y "ip.src == 192.168.1.100 and tcp.port == 443"

# OR
tshark -i wlan0 -Y "http or dns"

# NOT
tshark -i wlan0 -Y "not arp and not icmp"

# Complexo
tshark -i wlan0 -Y "(http.request or http.response) and ip.addr == 192.168.1.100"
```

---

#### Output Customizado

**Campos Específicos:**

```bash
# Mostra apenas campos específicos
tshark -i wlan0 -T fields \
  -e frame.time \
  -e ip.src \
  -e ip.dst \
  -e tcp.srcport \
  -e tcp.dstport \
  -e frame.len

# Output:
# 2025-11-09 12:30:45.123456  192.168.1.100  142.250.200.78  52341  443  1420
```

**Formato JSON:**

```bash
# Output em JSON (Wireshark 2.6+)
tshark -i wlan0 -T json -c 10

# JSON com campos específicos
tshark -i wlan0 -T json -e ip.src -e ip.dst -c 10

# Salva JSON em arquivo
tshark -i wlan0 -T json -c 100 > capture.json
```

**Formato CSV:**

```bash
# CSV customizado
tshark -i wlan0 -T fields -E separator=, -E quote=d \
  -e frame.time \
  -e ip.src \
  -e ip.dst \
  -e tcp.srcport \
  -e tcp.dstport \
  > capture.csv
```

---

#### Estatísticas

**Conversas (Top Talkers):**

```bash
# Top conversas TCP
tshark -r capture.pcap -q -z conv,tcp

# Output:
# TCP Conversations
# Filter:<No Filter>
#                                                |       <-      | |       ->      | |     Total     |
# 192.168.1.100:52341 <-> 142.250.200.78:443      15 MB   1200     2 MB    800      17 MB    2000
# 192.168.1.100:52342 <-> 140.82.121.4:443        8 MB    600      1 MB    400      9 MB     1000

# Top conversas UDP
tshark -r capture.pcap -q -z conv,udp

# Top conversas IP (todas)
tshark -r capture.pcap -q -z conv,ip
```

**Endpoints (Hosts):**

```bash
# Top endpoints IP
tshark -r capture.pcap -q -z endpoints,ip

# Output:
# IPv4 Endpoints
# Filter:<No Filter>
#                        | Packets | |  Bytes  |
# 192.168.1.100            5000        50 MB
# 142.250.200.78           3000        40 MB
# 140.82.121.4             1500        15 MB
```

**Protocolo Distribution:**

```bash
# Hierarquia de protocolos
tshark -r capture.pcap -q -z io,phs

# Output:
# Protocol Hierarchy Statistics
# Filter: <No Filter>
#
# eth                    frames:10000 bytes:12MB
#   ip                   frames:9500 bytes:11.5MB
#     tcp                frames:8000 bytes:10MB
#       http             frames:2000 bytes:3MB
#       tls              frames:5000 bytes:6MB
#     udp                frames:1500 bytes:1.5MB
#       dns              frames:1000 bytes:500KB
```

**HTTP Statistics:**

```bash
# HTTP requests por host
tshark -r capture.pcap -q -z http,tree

# HTTP status codes
tshark -r capture.pcap -q -z http_srv,tree
```

**DNS Statistics:**

```bash
# DNS queries
tshark -r capture.pcap -q -z dns,tree
```

---

#### Análise em Tempo Real

**Monitorar Bandwidth:**

```bash
# Bytes por segundo
tshark -i wlan0 -q -z io,stat,1

# Output (atualiza a cada 1s):
# | Interval |  Frames  |  Bytes   |
# |  0 <> 1  |   1234   |  1.5 MB  |
# |  1 <> 2  |   1456   |  1.8 MB  |
# |  2 <> 3  |   1123   |  1.3 MB  |
```

**Detectar Port Scans:**

```bash
# Detecta TCP SYN flood
tshark -i wlan0 -Y "tcp.flags.syn == 1 and tcp.flags.ack == 0" \
  -T fields -e ip.src -e tcp.dstport | \
  awk '{count[$1]++} END {for (ip in count) if (count[ip] > 100) print ip, count[ip]}'
```

**Monitorar DNS Queries:**

```bash
# Live DNS monitoring
tshark -i wlan0 -Y "dns.flags.response == 0" \
  -T fields -e dns.qry.name | \
  sort | uniq -c | sort -nr
```

---

#### Integração Python

```python
import subprocess
import json

def capture_packets_json(interface='wlan0', count=100, display_filter=None):
    """
    Captura pacotes usando tshark e retorna JSON

    Args:
        interface: Interface de rede
        count: Número de pacotes
        display_filter: Filtro Wireshark (ex: "http")

    Returns:
        Lista de pacotes em formato dict
    """
    cmd = [
        'tshark',
        '-i', interface,
        '-c', str(count),
        '-T', 'json'
    ]

    if display_filter:
        cmd.extend(['-Y', display_filter])

    result = subprocess.run(cmd, capture_output=True, text=True)
    packets = json.loads(result.stdout)

    return packets

def get_top_talkers(interface='wlan0', duration_sec=10):
    """
    Retorna top talkers (IPs que mais geram tráfego)

    Returns:
        Dict com {ip: bytes_count}
    """
    # Captura por N segundos
    cmd = [
        'tshark',
        '-i', interface,
        '-a', f'duration:{duration_sec}',
        '-T', 'fields',
        '-e', 'ip.src',
        '-e', 'frame.len'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse output
    talkers = {}
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) == 2:
            ip, bytes_str = parts
            talkers[ip] = talkers.get(ip, 0) + int(bytes_str)

    # Ordena por bytes
    return dict(sorted(talkers.items(), key=lambda x: x[1], reverse=True))

def detect_port_scan(interface='wlan0', threshold=50):
    """
    Detecta possível port scan

    Args:
        interface: Interface
        threshold: Número de SYNs para considerar scan

    Returns:
        Lista de IPs suspeitos
    """
    cmd = [
        'tshark',
        '-i', interface,
        '-a', 'duration:60',  # 1 minuto
        '-Y', 'tcp.flags.syn == 1 and tcp.flags.ack == 0',
        '-T', 'fields',
        '-e', 'ip.src',
        '-e', 'tcp.dstport'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Conta SYNs por IP
    syn_count = {}
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue

        ip = line.split('\t')[0]
        syn_count[ip] = syn_count.get(ip, 0) + 1

    # Filtra IPs acima do threshold
    suspicious = [ip for ip, count in syn_count.items() if count >= threshold]

    return suspicious
```

---

<a name="wireshark-filters"></a>
### 1.2 WIRESHARK DISPLAY FILTERS

#### Sintaxe Geral

```
protocol.field operator value
```

**Operadores:**
- `==` - igual
- `!=` - diferente
- `>` - maior
- `<` - menor
- `>=` - maior ou igual
- `<=` - menor ou igual
- `contains` - contém string
- `matches` - regex match
- `in` - dentro de conjunto

---

#### Filtros por Layer

**Layer 2 (Data Link):**

```
# Endereço MAC específico
eth.addr == aa:bb:cc:dd:ee:ff

# MAC source
eth.src == aa:bb:cc:dd:ee:ff

# MAC dest
eth.dst == aa:bb:cc:dd:ee:ff

# Broadcast
eth.dst == ff:ff:ff:ff:ff:ff

# VLAN específico
vlan.id == 100
```

**Layer 3 (Network):**

```
# IP específico
ip.addr == 192.168.1.100

# Subnet
ip.addr == 192.168.1.0/24

# IPv6
ipv6.addr == 2001:db8::1

# TTL baixo (suspeito)
ip.ttl < 10

# Fragmentação
ip.flags.mf == 1
```

**Layer 4 (Transport):**

```
# TCP port
tcp.port == 443

# TCP flags
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.rst == 1
tcp.flags.fin == 1

# TCP window size (QoS)
tcp.window_size < 1000

# TCP retransmissions
tcp.analysis.retransmission

# UDP port
udp.port == 53

# UDP length
udp.length > 1000
```

**Layer 7 (Application):**

```
# HTTP
http.request.method == "GET"
http.request.method == "POST"
http.request.uri contains "/api/"
http.host == "google.com"
http.user_agent contains "Chrome"
http.response.code == 200
http.response.code >= 400

# HTTPS/TLS
tls.handshake.type == 1          # Client Hello
tls.handshake.extensions_server_name contains "google.com"
tls.record.version == 0x0303     # TLS 1.2

# DNS
dns.qry.name == "google.com"
dns.qry.type == 1                # A record
dns.qry.type == 28               # AAAA record
dns.flags.response == 0          # Query
dns.flags.response == 1          # Response

# ICMP
icmp.type == 8                   # Echo request (ping)
icmp.type == 0                   # Echo reply

# ARP
arp.opcode == 1                  # Request
arp.opcode == 2                  # Reply
```

---

#### Filtros de Análise (Wireshark Expert)

```
# Erros TCP
tcp.analysis.flags

# Retransmissões
tcp.analysis.retransmission

# Duplicate ACKs
tcp.analysis.duplicate_ack

# Zero window (congestion)
tcp.analysis.zero_window

# Conexões resetadas
tcp.flags.reset == 1

# Checksum errors
ip.checksum_bad == 1
tcp.checksum_bad == 1
udp.checksum_bad == 1
```

---

#### Filtros de Segurança

**Detectar Ataques:**

```
# SYN flood
tcp.flags.syn == 1 and tcp.flags.ack == 0

# NULL scan
tcp.flags == 0x00

# XMAS scan
tcp.flags.fin == 1 and tcp.flags.push == 1 and tcp.flags.urg == 1

# ARP spoofing (duplicate IPs)
arp.duplicate-address-detected

# DNS amplification
dns and udp.length > 512

# ICMP flood
icmp and frame.time_delta < 0.001
```

**Detectar Data Exfiltration:**

```
# Uploads grandes
http.request.method == "POST" and http.content_length > 1000000

# DNS tunneling (queries grandes)
dns.qry.name.len > 100

# ICMP tunneling (payloads incomuns)
icmp.data.len > 100
```

---

#### Filtros Úteis para Dashboard

**Bandwidth Hogs:**

```
# Top 10 maiores pacotes
frame.len > 1400

# Streaming (grandes transferências)
tcp.len > 1400 and tcp.flags.push == 1
```

**Latência:**

```
# TCP handshake lento
tcp.time_delta > 0.5 and tcp.flags.syn == 1

# HTTP response time
http.time > 1.0
```

**Aplicações Comuns:**

```
# YouTube
http.host contains "youtube.com" or http.host contains "googlevideo.com"

# Netflix
http.host contains "netflix.com" or http.host contains "nflxvideo.net"

# Spotify
http.host contains "spotify.com" or http.host contains "scdn.co"

# WhatsApp
ip.dst == 31.13.64.0/18 or ip.dst == 157.240.0.0/16

# Zoom
udp.port >= 8801 and udp.port <= 8810
```

---

<a name="scapy"></a>
### 1.3 SCAPY (Python Packet Manipulation)

**Website:** https://scapy.net/
**GitHub:** https://github.com/secdev/scapy
**Linguagem:** Python
**Licença:** GPL-2.0

#### Visão Geral

**Scapy** é uma biblioteca Python poderosa para manipulação de pacotes de rede.

**Capabilities:**
- Packet crafting (criar pacotes customizados)
- Packet sniffing
- Packet dissection
- Network scanning
- Traceroute
- Attack simulation (para educação/testes)

---

#### Instalação

```bash
pip install scapy

# Ou via apt
sudo apt install python3-scapy
```

---

#### Sniffing Básico

```python
from scapy.all import *

# Captura 10 pacotes
packets = sniff(count=10)

# Captura em interface específica
packets = sniff(iface='wlan0', count=10)

# Captura com timeout (segundos)
packets = sniff(timeout=10)

# Captura com filtro BPF
packets = sniff(filter='tcp port 80', count=10)

# Captura com callback
def packet_callback(packet):
    print(f"Pacote capturado: {packet.summary()}")

sniff(prn=packet_callback, count=10)
```

---

#### BPF Filters em Scapy

```python
# Apenas TCP
sniff(filter='tcp', count=10)

# Porta específica
sniff(filter='port 443', count=10)

# IP específico
sniff(filter='host 192.168.1.100', count=10)

# HTTP
sniff(filter='tcp port 80', count=10)

# Combinação
sniff(filter='tcp and port 443 and host 192.168.1.100', count=10)
```

---

#### Análise de Pacotes

```python
# Captura pacotes
packets = sniff(count=100)

# Acessa pacote específico
pkt = packets[0]

# Mostra resumo
print(pkt.summary())

# Mostra detalhes
pkt.show()

# Acessa layers
if pkt.haslayer(IP):
    print(f"IP Source: {pkt[IP].src}")
    print(f"IP Dest: {pkt[IP].dst}")

if pkt.haslayer(TCP):
    print(f"TCP Source Port: {pkt[TCP].sport}")
    print(f"TCP Dest Port: {pkt[TCP].dport}")
    print(f"TCP Flags: {pkt[TCP].flags}")

if pkt.haslayer(Raw):
    print(f"Payload: {pkt[Raw].load}")
```

---

#### Filtros Python (mais flexíveis que BPF)

```python
def is_http_get(packet):
    """Retorna True se é HTTP GET"""
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode('utf-8', errors='ignore')
        return payload.startswith('GET ')
    return False

# Captura apenas HTTP GETs
packets = sniff(lfilter=is_http_get, count=10)

# Outro exemplo: apenas pacotes grandes
def is_large(packet):
    return len(packet) > 1000

large_packets = sniff(lfilter=is_large, count=10)
```

---

#### Análise Estatística

```python
from collections import Counter

# Captura tráfego
packets = sniff(timeout=60)

# Top source IPs
src_ips = [pkt[IP].src for pkt in packets if pkt.haslayer(IP)]
top_sources = Counter(src_ips).most_common(10)
print("Top Source IPs:")
for ip, count in top_sources:
    print(f"  {ip}: {count} packets")

# Top destination ports
dst_ports = [pkt[TCP].dport for pkt in packets if pkt.haslayer(TCP)]
top_ports = Counter(dst_ports).most_common(10)
print("\nTop Destination Ports:")
for port, count in top_ports:
    print(f"  {port}: {count} packets")

# Protocol distribution
protocols = []
for pkt in packets:
    if pkt.haslayer(TCP):
        protocols.append('TCP')
    elif pkt.haslayer(UDP):
        protocols.append('UDP')
    elif pkt.haslayer(ICMP):
        protocols.append('ICMP')
    else:
        protocols.append('Other')

proto_dist = Counter(protocols)
print("\nProtocol Distribution:")
for proto, count in proto_dist.items():
    print(f"  {proto}: {count} packets")
```

---

#### Bandwidth Calculation

```python
import time

def measure_bandwidth(interface='wlan0', duration=10):
    """
    Mede bandwidth em tempo real

    Returns:
        Dict com download/upload em bytes/second
    """
    start_time = time.time()

    download_bytes = 0
    upload_bytes = 0

    def count_bytes(packet):
        nonlocal download_bytes, upload_bytes

        if packet.haslayer(IP):
            # Assume que interface local está em 192.168.1.0/24
            # (ajustar para seu caso)
            local_net = '192.168.1.'

            if packet[IP].dst.startswith(local_net):
                download_bytes += len(packet)
            elif packet[IP].src.startswith(local_net):
                upload_bytes += len(packet)

    # Captura por N segundos
    sniff(iface=interface, prn=count_bytes, timeout=duration, store=False)

    elapsed = time.time() - start_time

    return {
        'download_bps': download_bytes / elapsed,
        'upload_bps': upload_bytes / elapsed,
        'download_mbps': (download_bytes / elapsed) / (1024**2),
        'upload_mbps': (upload_bytes / elapsed) / (1024**2)
    }

# Uso
result = measure_bandwidth(duration=10)
print(f"Download: {result['download_mbps']:.2f} MB/s")
print(f"Upload: {result['upload_mbps']:.2f} MB/s")
```

---

#### Detecção de Aplicações

```python
def detect_application(packet):
    """
    Detecta aplicação baseado em padrões

    Returns:
        String com nome da aplicação ou 'Unknown'
    """
    if not packet.haslayer(TCP) or not packet.haslayer(Raw):
        return 'Unknown'

    payload = packet[Raw].load

    # HTTP
    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
        if b'GET ' in payload or b'POST ' in payload:
            # Tenta extrair Host header
            try:
                payload_str = payload.decode('utf-8', errors='ignore')
                if 'youtube.com' in payload_str or 'googlevideo.com' in payload_str:
                    return 'YouTube'
                elif 'netflix.com' in payload_str:
                    return 'Netflix'
                elif 'spotify.com' in payload_str:
                    return 'Spotify'
                else:
                    return 'HTTP'
            except:
                return 'HTTP'

    # HTTPS (TLS)
    elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
        # TLS Client Hello contém SNI (Server Name Indication)
        if b'\x16\x03' in payload[:2]:  # TLS handshake
            try:
                # Parse SNI (simplificado - na real precisa de parsing completo)
                if b'youtube' in payload:
                    return 'YouTube (HTTPS)'
                elif b'netflix' in payload:
                    return 'Netflix (HTTPS)'
                elif b'spotify' in payload:
                    return 'Spotify (HTTPS)'
                else:
                    return 'HTTPS'
            except:
                return 'HTTPS'

    # SSH
    elif packet[TCP].dport == 22 or packet[TCP].sport == 22:
        return 'SSH'

    # FTP
    elif packet[TCP].dport == 21 or packet[TCP].sport == 21:
        return 'FTP'

    # DNS
    elif packet.haslayer(UDP) and (packet[UDP].dport == 53 or packet[UDP].sport == 53):
        return 'DNS'

    return 'Unknown'

# Captura e classifica
packets = sniff(count=100)
app_counts = Counter([detect_application(pkt) for pkt in packets])

print("Application Distribution:")
for app, count in app_counts.most_common():
    print(f"  {app}: {count} packets")
```

---

#### Port Scan Detection

```python
from collections import defaultdict
import time

class PortScanDetector:
    """Detecta port scans em tempo real"""

    def __init__(self, threshold=50, window=60):
        """
        Args:
            threshold: Número de SYNs para considerar scan
            window: Janela de tempo (segundos)
        """
        self.threshold = threshold
        self.window = window
        self.syn_tracker = defaultdict(lambda: {'ports': set(), 'first_seen': None})

    def process_packet(self, packet):
        """Processa pacote e detecta scan"""
        if not packet.haslayer(TCP) or not packet.haslayer(IP):
            return

        # Apenas SYN packets (não SYN-ACK)
        if packet[TCP].flags == 'S':
            src_ip = packet[IP].src
            dst_port = packet[TCP].dport
            now = time.time()

            tracker = self.syn_tracker[src_ip]

            # Primeira vez vendo esse IP
            if tracker['first_seen'] is None:
                tracker['first_seen'] = now

            # Limpa se passou a janela
            if now - tracker['first_seen'] > self.window:
                tracker['ports'] = set()
                tracker['first_seen'] = now

            # Adiciona porta
            tracker['ports'].add(dst_port)

            # Detecta scan
            if len(tracker['ports']) >= self.threshold:
                print(f"⚠️  PORT SCAN DETECTED from {src_ip}! ({len(tracker['ports'])} ports in {self.window}s)")
                # Reset para não alertar múltiplas vezes
                tracker['ports'] = set()
                tracker['first_seen'] = now

    def start_monitoring(self, interface='wlan0'):
        """Inicia monitoring"""
        print(f"Monitoring {interface} for port scans...")
        sniff(iface=interface, prn=self.process_packet, store=False)

# Uso
detector = PortScanDetector(threshold=20, window=60)
detector.start_monitoring()
```

---

<a name="tcpdump"></a>
### 1.4 TCPDUMP & BPF FILTERS

**Website:** https://www.tcpdump.org/
**Linguagem:** C
**Licença:** BSD

#### Visão Geral

**tcpdump** é a ferramenta clássica de capture de pacotes. Mais leve que tshark, ideal para sistemas com poucos recursos.

---

#### Captura Básica

```bash
# Captura em interface padrão
sudo tcpdump

# Interface específica
sudo tcpdump -i wlan0

# N pacotes
sudo tcpdump -c 100

# Salva em arquivo
sudo tcpdump -w capture.pcap

# Lê de arquivo
tcpdump -r capture.pcap

# Verbose output
sudo tcpdump -v
sudo tcpdump -vv
sudo tcpdump -vvv
```

---

#### BPF Filters (Berkeley Packet Filter)

**Sintaxe:**
```
primitive [operator primitive]...
```

**Primitives:**

```bash
# Host
tcpdump host 192.168.1.100

# Network
tcpdump net 192.168.1.0/24

# Port
tcpdump port 443

# Protocol
tcpdump tcp
tcpdump udp
tcpdump icmp

# Direction
tcpdump src 192.168.1.100
tcpdump dst 8.8.8.8
tcpdump src port 443
tcpdump dst port 80
```

**Operators:**

```bash
# AND
tcpdump tcp and port 443

# OR
tcpdump port 80 or port 443

# NOT
tcpdump not port 22

# Parênteses (grouping)
tcpdump '(tcp and port 443) or (udp and port 53)'
```

---

#### Filtros Avançados

**Por Flags TCP:**

```bash
# SYN packets
tcpdump 'tcp[tcpflags] & tcp-syn != 0'

# SYN-ACK
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-ack) == (tcp-syn|tcp-ack)'

# RST packets
tcpdump 'tcp[tcpflags] & tcp-rst != 0'

# FIN packets
tcpdump 'tcp[tcpflags] & tcp-fin != 0'

# PSH-ACK (dados)
tcpdump 'tcp[tcpflags] & (tcp-push|tcp-ack) == (tcp-push|tcp-ack)'
```

**Por Tamanho:**

```bash
# Pacotes maiores que 1000 bytes
tcpdump 'greater 1000'

# Pacotes menores que 100 bytes
tcpdump 'less 100'

# Range
tcpdump 'greater 500 and less 1500'
```

**Por Conteúdo (Payload):**

```bash
# HTTP GET (procura por "GET " nos primeiros bytes)
tcpdump 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'

# Simplified: HTTP on port 80
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

---

#### Output Formatting

```bash
# Mostra conteúdo em HEX e ASCII
sudo tcpdump -X

# Apenas HEX
sudo tcpdump -xx

# Com timestamps absolutos
sudo tcpdump -tttt

# Sem resolução de nomes (mais rápido)
sudo tcpdump -n

# Sem resolução de portas
sudo tcpdump -nn

# Print cada pacote em uma linha
sudo tcpdump -l
```

---

#### Exemplos Práticos

**Monitorar HTTP:**

```bash
sudo tcpdump -i wlan0 -nn -s0 -A 'tcp port 80'
```

**Capturar DNS queries:**

```bash
sudo tcpdump -i wlan0 -nn 'udp port 53'
```

**Detectar SYN flood:**

```bash
sudo tcpdump -i wlan0 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0'
```

**Tráfego SSH:**

```bash
sudo tcpdump -i wlan0 'tcp port 22'
```

**Broadcast/Multicast:**

```bash
# Broadcast
sudo tcpdump -i wlan0 'ether dst ff:ff:ff:ff:ff:ff'

# Multicast
sudo tcpdump -i wlan0 'ether multicast'
```

---

#### Estatísticas com tcpdump + awk

**Bandwidth por IP:**

```bash
sudo tcpdump -i wlan0 -nn -l | \
  awk '{print $3}' | \
  cut -d. -f1-4 | \
  sort | uniq -c | sort -nr
```

**Top destination ports:**

```bash
sudo tcpdump -i wlan0 -nn -l | \
  awk '{print $5}' | \
  cut -d. -f5 | \
  cut -d: -f1 | \
  sort | uniq -c | sort -nr | head -10
```

---

<a name="traffic-patterns"></a>
### 1.5 PADRÕES DE ANÁLISE DE TRÁFEGO

#### Top Talkers

**Definição:** Hosts que geram mais tráfego.

**Métrica:**
- Total bytes sent/received
- Packet count
- Bandwidth usage (bytes/second)

**Implementação:**

```python
from collections import defaultdict

def get_top_talkers(packets, top_n=10):
    """
    Retorna top N talkers

    Args:
        packets: Lista de pacotes Scapy
        top_n: Quantos retornar

    Returns:
        Lista de (ip, bytes_total)
    """
    ip_bytes = defaultdict(int)

    for pkt in packets:
        if pkt.haslayer(IP):
            ip_bytes[pkt[IP].src] += len(pkt)

    # Ordena por bytes
    sorted_ips = sorted(ip_bytes.items(), key=lambda x: x[1], reverse=True)

    return sorted_ips[:top_n]
```

---

#### Protocol Distribution

**Definição:** Distribuição percentual de protocolos.

**Métricas:**
- TCP %
- UDP %
- ICMP %
- Others %

**Implementação:**

```python
from collections import Counter

def get_protocol_distribution(packets):
    """
    Retorna distribuição de protocolos

    Returns:
        Dict com {protocol: percentage}
    """
    protocols = []

    for pkt in packets:
        if pkt.haslayer(TCP):
            protocols.append('TCP')
        elif pkt.haslayer(UDP):
            protocols.append('UDP')
        elif pkt.haslayer(ICMP):
            protocols.append('ICMP')
        elif pkt.haslayer(ARP):
            protocols.append('ARP')
        else:
            protocols.append('Other')

    total = len(protocols)
    counts = Counter(protocols)

    distribution = {
        proto: (count / total) * 100
        for proto, count in counts.items()
    }

    return distribution
```

---

#### Bandwidth Analysis Per Application

**Definição:** Quanto de banda cada aplicação consome.

**Implementação:**

```python
def get_app_bandwidth(packets, duration_seconds):
    """
    Calcula bandwidth por aplicação

    Returns:
        Dict com {app_name: mbps}
    """
    app_bytes = defaultdict(int)

    for pkt in packets:
        app = detect_application(pkt)  # Função definida anteriormente
        app_bytes[app] += len(pkt)

    # Converte para Mbps
    app_bandwidth = {
        app: (bytes_total / duration_seconds) / (1024**2)
        for app, bytes_total in app_bytes.items()
    }

    return dict(sorted(app_bandwidth.items(), key=lambda x: x[1], reverse=True))
```

---

#### Connection State Tracking

**Definição:** Rastrear estado de conexões TCP.

**Estados:**
- SYN_SENT
- ESTABLISHED
- FIN_WAIT
- CLOSE_WAIT
- TIME_WAIT

**Implementação:**

```python
from collections import defaultdict

class ConnectionTracker:
    """Rastreia estado de conexões TCP"""

    def __init__(self):
        self.connections = defaultdict(lambda: {'state': 'UNKNOWN', 'packets': []})

    def _get_conn_key(self, packet):
        """Cria chave única para conexão"""
        src = f"{packet[IP].src}:{packet[TCP].sport}"
        dst = f"{packet[IP].dst}:{packet[TCP].dport}"
        return (src, dst)

    def process_packet(self, packet):
        """Processa pacote e atualiza estado"""
        if not packet.haslayer(TCP) or not packet.haslayer(IP):
            return

        key = self._get_conn_key(packet)
        conn = self.connections[key]
        flags = packet[TCP].flags

        # State machine simplificado
        if flags & 0x02:  # SYN
            if flags & 0x10:  # SYN-ACK
                conn['state'] = 'SYN_RECEIVED'
            else:
                conn['state'] = 'SYN_SENT'

        elif flags & 0x10 and conn['state'] == 'SYN_RECEIVED':  # ACK
            conn['state'] = 'ESTABLISHED'

        elif flags & 0x01:  # FIN
            if conn['state'] == 'ESTABLISHED':
                conn['state'] = 'FIN_WAIT'

        elif flags & 0x04:  # RST
            conn['state'] = 'CLOSED'

        conn['packets'].append(packet)

    def get_active_connections(self):
        """Retorna conexões ativas (ESTABLISHED)"""
        return {
            key: conn
            for key, conn in self.connections.items()
            if conn['state'] == 'ESTABLISHED'
        }
```

---

#### Anomaly Detection (Baseline)

**Definição:** Detectar tráfego anormal comparado com baseline.

**Técnicas:**
- Statistical (média + desvio padrão)
- Z-score
- Threshold-based

**Implementação:**

```python
import numpy as np
from collections import deque

class AnomalyDetector:
    """Detecta anomalias baseado em baseline estatístico"""

    def __init__(self, window_size=100, threshold_sigma=3):
        """
        Args:
            window_size: Tamanho da janela para baseline
            threshold_sigma: Quantos desvios padrão para considerar anomalia
        """
        self.window_size = window_size
        self.threshold_sigma = threshold_sigma
        self.bandwidth_history = deque(maxlen=window_size)

    def add_measurement(self, bytes_per_second):
        """Adiciona medição de bandwidth"""
        self.bandwidth_history.append(bytes_per_second)

    def is_anomaly(self, current_bps):
        """
        Verifica se valor atual é anomalia

        Returns:
            (is_anomaly: bool, z_score: float)
        """
        if len(self.bandwidth_history) < 10:
            return False, 0.0  # Não há baseline ainda

        # Calcula baseline (média e desvio padrão)
        mean = np.mean(self.bandwidth_history)
        std = np.std(self.bandwidth_history)

        if std == 0:
            return False, 0.0

        # Calcula z-score
        z_score = (current_bps - mean) / std

        # Anomalia se |z_score| > threshold
        is_anomaly = abs(z_score) > self.threshold_sigma

        return is_anomaly, z_score

# Uso
detector = AnomalyDetector(window_size=100, threshold_sigma=3)

# Simula medições
import random
for i in range(200):
    # Tráfego normal: 1-5 MB/s
    bps = random.uniform(1e6, 5e6)

    # Injeta anomalia
    if i == 150:
        bps = 50e6  # 50 MB/s (spike!)

    is_anomaly, z_score = detector.is_anomaly(bps)

    if is_anomaly:
        print(f"⚠️  ANOMALIA DETECTADA! {bps/1e6:.2f} MB/s (z-score: {z_score:.2f})")

    detector.add_measurement(bps)
```

---

<a name="system-monitors"></a>
## 2. SYSTEM MONITORS TUI

<a name="btop"></a>
### 2.1 BTOP++ (C++)

**GitHub:** https://github.com/aristocratos/btop
**Linguagem:** C++
**Licença:** Apache-2.0
**Estrelas:** ~19k ⭐

#### Visão Geral

**btop++** é um monitor de recursos moderno, bonito e rico em features para Linux/macOS/FreeBSD.

**Features Principais:**
- Interface linda com temas
- Gráficos usando Braille characters (alta resolução)
- CPU, Memory, Disk, Network monitoring
- Process management (kill, nice, etc.)
- GPU monitoring (Nvidia, AMD, Intel)
- Docker container stats
- Mouse support
- Vim keybindings

---

#### Arquitetura Visual

```
┌─ btop++ Layout ─────────────────────────────────────────────────────────┐
│                                                                          │
│  ┌─ CPU ─────────────────┐  ┌─ Memory ──────────────────────────────┐  │
│  │ Total: 45%            │  │ Used: 8.5 / 16.0 GB (53%)             │  │
│  │ ⡏⠉⠉⠉⢹⢇⠀⠀⠀⠀⠀⢸⡇⢀⡠⠤⠤⠤⢄⡀        │  │ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        │  │
│  │ ⡇⠀⠀⠀⢸⡜⡄⠀⠀⠀⠀⢸⢀⠃⠀⠀⠀⠀⠀⠈⡇       │  │                                        │  │
│  │ Per-Core:             │  │ Swap: 0.2 / 4.0 GB (5%)               │  │
│  │ 1:[████░░] 40%        │  │ ⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        │  │
│  │ 2:[█████░] 50%        │  └────────────────────────────────────────┘  │
│  │ 3:[███░░░] 30%        │                                              │
│  │ 4:[██░░░░] 20%        │  ┌─ Network ──────────────────────────────┐  │
│  └───────────────────────┘  │ wlan0                                  │  │
│                              │ Download: ⡀⢀⠀⠀⠀⢀⡀⢀⡀   1.5 MB/s        │  │
│  ┌─ Disk ────────────────┐  │ Upload:   ⠈⠁⠀⠀⠀⠈⠁⠈⠁   500 KB/s       │  │
│  │ / (sda1)              │  │                                        │  │
│  │ ⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀  75%  │  │ Total: 2.0 MB/s                         │  │
│  │ 150 / 200 GB          │  └────────────────────────────────────────┘  │
│  │ IO: R 10MB/s W 5MB/s  │                                              │
│  └───────────────────────┘                                              │
│                                                                          │
│  ┌─ Processes ──────────────────────────────────────────────────────┐   │
│  │ PID   User   CPU%   MEM%   Command                               │   │
│  │ 1234  user   15.2   8.5    /usr/bin/firefox                      │   │
│  │ 5678  user   10.1   5.2    /usr/bin/code                         │   │
│  │ 9012  user    5.5   3.1    /usr/bin/spotify                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

#### Características Técnicas

**1. Braille Characters para Gráficos:**

btop++ usa caracteres Braille Unicode (U+2800 - U+28FF) para criar gráficos de alta resolução:

```
Normal ASCII: ▂▃▄▅▆▇█  (8 níveis)
Braille:     ⠀⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇  (256 combinações!)
```

Isso permite gráficos muito mais suaves e detalhados.

**2. Layout Modular:**

```cpp
// Pseudo-código da arquitetura
class Box {
    virtual void draw() = 0;
    virtual void update() = 0;
    Position pos;
    Size size;
};

class CPUBox : public Box { /* ... */ };
class MemBox : public Box { /* ... */ };
class NetBox : public Box { /* ... */ };
class ProcBox : public Box { /* ... */ };

class Layout {
    vector<shared_ptr<Box>> boxes;

    void render() {
        for (auto& box : boxes) {
            box->update();
            box->draw();
        }
    }
};
```

**3. Multi-threaded:**

- Thread 1: Input handling
- Thread 2: Data collection (CPU, mem, etc.)
- Thread 3: Network monitoring
- Thread 4: Rendering

**4. Configurável via Config File:**

```conf
# ~/.config/btop/btop.conf

color_theme = "Default"
theme_background = True
truecolor = True
force_tty = False
presets = "cpu:1:default,mem:1:default,net:0:default,proc:0:default"
vim_keys = True
rounded_corners = True
graph_symbol = "braille"  # ou "block", "tty"
graph_symbol_cpu = "default"
graph_symbol_mem = "default"
graph_symbol_net = "default"
shown_boxes = "cpu mem net proc"
update_ms = 2000
proc_sorting = "cpu"  # cpu, mem, pid, program
proc_reversed = False
proc_tree = False
check_temp = True
cpu_graph_upper = "total"
cpu_graph_lower = "total"
cpu_sensor = "Auto"
show_battery = True
```

---

#### Temas

btop++ vem com vários temas built-in:

```
- Default (dark)
- Default Light
- TTY
- Ayu
- Dracula
- Gruvbox Dark
- Monokai
- Nord
- Solarized Dark
- Solarized Light
- Tokyo Night
```

**Estrutura de Tema:**

```conf
# theme "Custom"
theme[main_bg]="#1e1e2e"
theme[main_fg]="#cdd6f4"
theme[title]="#89b4fa"
theme[hi_fg]="#f38ba8"
theme[selected_bg]="#45475a"
theme[selected_fg]="#cdd6f4"
theme[inactive_fg]="#6c7086"
theme[graph_text]="#f9e2af"
theme[meter_bg]="#313244"
theme[proc_misc]="#f5c2e7"
theme[cpu_box]="#89b4fa"
theme[mem_box]="#a6e3a1"
theme[net_box]="#fab387"
theme[proc_box]="#cba6f7"
theme[div_line]="#6c7086"
theme[temp_start]="#a6e3a1"
theme[temp_mid]="#f9e2af"
theme[temp_end]="#f38ba8"
```

---

#### Inspirações para Nosso Dashboard

**1. Braille Graphs:**

```python
# Implementação simplificada de gráfico Braille
def create_braille_graph(data: List[float], width: int, height: int) -> str:
    """
    Cria gráfico usando caracteres Braille

    Braille pattern (8 dots):
    ⠁⠂⠄⡀ (left column)
    ⠈⠐⠠⢀ (right column)
    """
    # Normaliza dados para altura
    max_val = max(data) if data else 1
    normalized = [int((val / max_val) * height * 4) for val in data]

    # Grid Braille (cada char = 2x4 dots)
    rows = [''] * height

    for x, val in enumerate(normalized[:width * 2]):
        col = x // 2
        side = x % 2

        # Calcula dots para essa posição
        dots_height = val
        for y in range(height):
            # ... lógica de mapeamento para Braille
            pass

    return '\n'.join(rows)
```

**2. Layout Presets:**

Permitir usuário configurar layouts via YAML:

```yaml
layouts:
  - name: "default"
    boxes:
      - type: cpu
        position: {x: 0, y: 0, width: 40, height: 10}
      - type: memory
        position: {x: 41, y: 0, width: 40, height: 10}
      - type: network
        position: {x: 0, y: 11, width: 80, height: 15}

  - name: "network-focused"
    boxes:
      - type: network
        position: {x: 0, y: 0, width: 80, height: 25}
      - type: processes
        position: {x: 0, y: 26, width: 80, height: 15}
```

**3. Process Filtering:**

```python
# Filtrar processos por critério
def filter_processes(processes, criterion):
    """
    Filtros úteis:
    - Top CPU consumers
    - Top Memory consumers
    - Network-heavy processes
    - User-specific processes
    """
    if criterion == 'cpu':
        return sorted(processes, key=lambda p: p.cpu_percent, reverse=True)[:10]
    elif criterion == 'memory':
        return sorted(processes, key=lambda p: p.memory_percent, reverse=True)[:10]
    # ...
```

---

<a name="bottom"></a>
### 2.2 BOTTOM (Rust)

**GitHub:** https://github.com/ClementTsang/bottom
**Linguagem:** Rust
**Licença:** MIT
**Estrelas:** ~9k ⭐

#### Visão Geral

**bottom** (comando: `btm`) é um monitor de sistema customizável, cross-platform, em Rust.

**Features:**
- Extremamente customizável (cores, widgets, layouts)
- Baixo uso de recursos (Rust é eficiente)
- Widgets modulares e combináveis
- Filtros e buscas poderosos
- Zoom em gráficos
- Exportação de dados

---

#### Arquitetura de Widgets

bottom usa sistema de **widgets** modulares:

```
Available Widgets:
├── CPU (per-core ou total)
├── Memory (RAM + Swap)
├── Network (download/upload)
├── Temperature (sensors)
├── Disk (usage + I/O)
├── Process (table com sort/filter)
└── Battery (laptops)
```

**Layout via TOML:**

```toml
# ~/.config/bottom/bottom.toml

[flags]
hide_avg_cpu = false
dot_marker = false
left_legend = false
current_usage = false
group_processes = false
case_sensitive = false
whole_word = false
regex = false
basic = false
default_time_value = 60000
time_delta = 15000
rate = 1000
default_widget_type = "proc"
default_widget_count = 1
use_old_network_legend = false
hide_table_gap = false
battery = false
disable_click = false
no_write = false
color = "default"

# Layout customizado
[[row]]
  [[row.child]]
  type = "cpu"

[[row]]
  ratio = 2
  [[row.child]]
    ratio = 4
    type = "mem"
  [[row.child]]
    ratio = 3
    [[row.child.child]]
      type = "temp"
    [[row.child.child]]
      type = "disk"

[[row]]
  ratio = 2
  [[row.child]]
    type = "net"
  [[row.child]]
    type = "proc"
    default = true
```

---

#### Filtros e Busca

bottom tem sistema de filtros muito poderoso:

**Process Filters:**
```
# Busca simples
firefox

# Case-insensitive
(?i)firefox

# Regex
^fire.*

# Múltiplos termos (OR)
firefox|chrome|code

# Filtro por CPU > X%
cpu > 50

# Filtro por memória
mem > 1GB

# Combinação
(firefox or chrome) and cpu > 10
```

**Implementação de Filtro:**

```rust
// Pseudo-Rust
pub enum FilterType {
    Name(String),
    Cpu(f64),
    Memory(u64),
    Pid(u32),
}

impl Process {
    fn matches_filter(&self, filter: &FilterType) -> bool {
        match filter {
            FilterType::Name(pattern) => {
                self.name.contains(pattern)
            },
            FilterType::Cpu(threshold) => {
                self.cpu_percent > *threshold
            },
            FilterType::Memory(threshold) => {
                self.memory_bytes > *threshold
            },
            FilterType::Pid(pid) => {
                self.pid == *pid
            },
        }
    }
}
```

---

#### Inspirações

**1. Filtros Avançados:**

Implementar sistema de query language para filtrar dados no dashboard:

```python
class QueryFilter:
    """Sistema de filtros tipo bottom"""

    @staticmethod
    def parse_query(query: str):
        """
        Exemplos:
        - "cpu > 50"
        - "name contains firefox"
        - "(app == youtube or app == netflix) and bandwidth > 1MB"
        """
        # Parser simplificado
        # Na real, usar pyparsing ou similar
        pass

    @staticmethod
    def apply_filter(data: List[Dict], query: str) -> List[Dict]:
        """Aplica filtro nos dados"""
        filter_ast = QueryFilter.parse_query(query)
        return [item for item in data if filter_ast.evaluate(item)]
```

**2. Widget System:**

```python
# Sistema modular de widgets
class Widget(ABC):
    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def render(self) -> Panel:
        pass

class CPUWidget(Widget):
    def collect_data(self):
        self.cpu_percent = psutil.cpu_percent(interval=0.1)

    def render(self) -> Panel:
        # Renderiza gráfico CPU
        pass

class NetworkWidget(Widget):
    def collect_data(self):
        io = psutil.net_io_counters()
        self.bytes_sent = io.bytes_sent
        self.bytes_recv = io.bytes_recv

    def render(self) -> Panel:
        # Renderiza network stats
        pass

# Dashboard agregado
class Dashboard:
    def __init__(self, widgets: List[Widget]):
        self.widgets = widgets

    def update(self):
        for widget in self.widgets:
            widget.collect_data()

    def render(self):
        layout = Layout()
        for widget in self.widgets:
            layout.add(widget.render())
        return layout
```

---

<a name="gtop"></a>
### 2.3 GTOP (Node.js)

**GitHub:** https://github.com/aksakalli/gtop
**Linguagem:** Node.js (JavaScript)
**Licença:** MIT
**Estrelas:** ~9.6k ⭐

#### Visão Geral

**gtop** é um monitor de sistema para terminal escrito em Node.js, usando **blessed-contrib**.

**Features:**
- Interface colorida e clean
- CPU, Memory, Network, Disk monitoring
- Gráficos em tempo real
- Cross-platform (Linux, macOS, Windows)

---

#### blessed-contrib (Library de Gráficos)

**GitHub:** https://github.com/yaronn/blessed-contrib

blessed-contrib fornece widgets prontos para dashboards TUI:

**Widgets Disponíveis:**
- Line Chart
- Bar Chart
- Stacked Bar Chart
- Map (world map!)
- Gauge
- LCD Display
- Donut Chart
- Log
- Table
- Tree
- Markdown
- Picture (ASCII art de imagem!)

**Exemplo de Uso:**

```javascript
const blessed = require('blessed');
const contrib = require('blessed-contrib');

// Cria screen
const screen = blessed.screen();

// Cria grid layout
const grid = new contrib.grid({rows: 12, cols: 12, screen: screen});

// Line chart
const line = grid.set(0, 0, 4, 12, contrib.line, {
  style: {
    line: "yellow",
    text: "green",
    baseline: "black"
  },
  xLabelPadding: 3,
  xPadding: 5,
  showLegend: true,
  wholeNumbersOnly: false,
  label: 'Network Traffic'
});

// Atualiza dados
const seriesDownload = { title: 'Download', x: [], y: [], style: {line: 'green'} };
const seriesUpload = { title: 'Upload', x: [], y: [], style: {line: 'red'} };

setInterval(() => {
  // Coleta dados
  const download = getDownloadSpeed();
  const upload = getUploadSpeed();

  seriesDownload.x.push(new Date().toLocaleTimeString());
  seriesDownload.y.push(download);

  seriesUpload.x.push(new Date().toLocaleTimeString());
  seriesUpload.y.push(upload);

  // Limita histórico
  if (seriesDownload.x.length > 60) {
    seriesDownload.x.shift();
    seriesDownload.y.shift();
    seriesUpload.x.shift();
    seriesUpload.y.shift();
  }

  // Renderiza
  line.setData([seriesDownload, seriesUpload]);
  screen.render();
}, 1000);

// Quit com 'q'
screen.key(['escape', 'q', 'C-c'], () => process.exit(0));

screen.render();
```

**Gauge Widget:**

```javascript
const gauge = grid.set(4, 0, 2, 6, contrib.gauge, {
  label: 'CPU Usage',
  stroke: 'green',
  fill: 'white'
});

setInterval(() => {
  const cpuUsage = getCPUUsage();
  gauge.setPercent(cpuUsage);
  screen.render();
}, 1000);
```

**Bar Chart:**

```javascript
const bar = grid.set(6, 0, 4, 6, contrib.bar, {
  label: 'Disk Usage',
  barWidth: 4,
  barSpacing: 6,
  xOffset: 0,
  maxHeight: 9
});

bar.setData({
  titles: ['/', '/home', '/tmp'],
  data: [75, 85, 25]
});
```

---

#### Python Equivalente: blessed (urwid)

Em Python, equivalente seria **urwid** ou **py-cui**:

```python
import urwid

# Criar widgets
cpu_text = urwid.Text("CPU: 0%")
mem_progress = urwid.ProgressBar('pg normal', 'pg complete')

# Layout
pile = urwid.Pile([
    urwid.Text("System Monitor", align='center'),
    urwid.Divider(),
    cpu_text,
    mem_progress,
])

# Main loop
loop = urwid.MainLoop(urwid.Filler(pile, 'top'))

def update(loop, user_data):
    # Atualiza dados
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent

    cpu_text.set_text(f"CPU: {cpu_percent}%")
    mem_progress.set_completion(mem_percent)

    # Reagenda
    loop.set_alarm_in(1, update)

loop.set_alarm_in(0, update)
loop.run()
```

**Mas melhor ainda: Rich com Live:**

```python
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
import psutil
import time

def generate_table():
    table = Table(title="System Stats")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("CPU", f"{psutil.cpu_percent()}%")
    table.add_row("Memory", f"{psutil.virtual_memory().percent}%")
    table.add_row("Disk", f"{psutil.disk_usage('/').percent}%")

    return table

with Live(generate_table(), refresh_per_second=4) as live:
    while True:
        time.sleep(0.25)
        live.update(generate_table())
```

---

<a name="monitor-comparison"></a>
### 2.4 ANÁLISE COMPARATIVA

| Feature | btop++ | bottom | gtop |
|---------|--------|--------|------|
| **Linguagem** | C++ | Rust | JavaScript |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Customização** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Gráficos** | Braille (alta res) | Bloco/Braille | Bloco |
| **Mouse Support** | ✅ | ✅ | ❌ |
| **Themes** | ✅ (built-in) | ✅ (customizável) | ✅ (limitado) |
| **Process Kill** | ✅ | ✅ | ❌ |
| **Filters** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| **GPU Monitoring** | ✅ | ❌ | ❌ |
| **Docker Stats** | ✅ | ❌ | ❌ |
| **Config File** | ✅ (.conf) | ✅ (TOML) | ❌ |
| **Cross-platform** | Linux/macOS/BSD | All | All |

**Recomendações:**

- **btop++:** Melhor visual, mais features, ideal para uso diário
- **bottom:** Mais customizável, filtros poderosos, ideal para power users
- **gtop:** Mais simples, fácil de hackear (JS), ideal para protótipos

---

<a name="bandwidth"></a>
## 3. BANDWIDTH CALCULATION & METRICS

<a name="bandwidth-calc"></a>
### 3.1 CÁLCULO DE BANDWIDTH

#### Conceitos Fundamentais

**Bandwidth vs Throughput:**
- **Bandwidth:** Capacidade máxima do canal (ex: 100 Mbps)
- **Throughput:** Taxa real de dados transferidos (ex: 85 Mbps)

**Unidades:**
- **Bits por segundo (bps):** 1 Kbps = 1000 bps
- **Bytes por segundo (B/s):** 1 KB/s = 1024 bytes/s
- **Conversão:** 1 Byte = 8 bits

---

#### Método 1: psutil (Python)

```python
import psutil
import time

def calculate_bandwidth_psutil(interface='wlan0', duration=1):
    """
    Calcula bandwidth usando psutil

    Returns:
        Dict com bytes_sent_per_sec, bytes_recv_per_sec
    """
    # Snapshot inicial
    io_start = psutil.net_io_counters(pernic=True)[interface]

    # Aguarda
    time.sleep(duration)

    # Snapshot final
    io_end = psutil.net_io_counters(pernic=True)[interface]

    # Calcula diferença
    bytes_sent = io_end.bytes_sent - io_start.bytes_sent
    bytes_recv = io_end.bytes_recv - io_start.bytes_recv

    # Bytes por segundo
    sent_per_sec = bytes_sent / duration
    recv_per_sec = bytes_recv / duration

    return {
        'bytes_sent_per_sec': sent_per_sec,
        'bytes_recv_per_sec': recv_per_sec,
        'mbps_sent': (sent_per_sec * 8) / (1024 * 1024),  # Mbps
        'mbps_recv': (recv_per_sec * 8) / (1024 * 1024)
    }

# Uso
result = calculate_bandwidth_psutil()
print(f"Download: {result['mbps_recv']:.2f} Mbps")
print(f"Upload: {result['mbps_sent']:.2f} Mbps")
```

---

#### Método 2: Lendo /proc/net/dev (Linux)

```python
def read_net_dev(interface='wlan0'):
    """
    Lê /proc/net/dev

    Formato:
    Inter-|   Receive                                                |  Transmit
     face |bytes packets errs drop fifo frame compressed multicast|bytes packets ...
     wlan0: 123456789  500000    0    0    0     0          0         0 987654321  ...
    """
    with open('/proc/net/dev', 'r') as f:
        lines = f.readlines()

    for line in lines:
        if interface in line:
            parts = line.split()
            return {
                'rx_bytes': int(parts[1]),
                'tx_bytes': int(parts[9])
            }

    return None

def calculate_bandwidth_proc(interface='wlan0', duration=1):
    """Calcula bandwidth lendo /proc/net/dev"""
    start = read_net_dev(interface)
    time.sleep(duration)
    end = read_net_dev(interface)

    rx_bps = (end['rx_bytes'] - start['rx_bytes']) / duration
    tx_bps = (end['tx_bytes'] - start['tx_bytes']) / duration

    return {
        'download_mbps': (rx_bps * 8) / (1024 * 1024),
        'upload_mbps': (tx_bps * 8) / (1024 * 1024)
    }
```

---

#### Método 3: Packet Counting (Scapy)

```python
from scapy.all import sniff
import time
from threading import Thread

class BandwidthMonitor:
    """Monitor de bandwidth usando Scapy"""

    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.bytes_recv = 0
        self.bytes_sent = 0
        self.running = False
        self.local_ip = None

    def _get_local_ip(self):
        """Obtém IP local da interface"""
        import socket
        # Simplificado - assumir 192.168.1.x
        return '192.168.1.'

    def _packet_handler(self, packet):
        """Callback para cada pacote"""
        if packet.haslayer('IP'):
            packet_len = len(packet)

            if self.local_ip and packet['IP'].dst.startswith(self.local_ip):
                self.bytes_recv += packet_len
            elif self.local_ip and packet['IP'].src.startswith(self.local_ip):
                self.bytes_sent += packet_len

    def start(self):
        """Inicia monitoring"""
        self.running = True
        self.local_ip = self._get_local_ip()

        # Thread de sniffing
        def sniff_loop():
            sniff(
                iface=self.interface,
                prn=self._packet_handler,
                store=False,
                stop_filter=lambda x: not self.running
            )

        thread = Thread(target=sniff_loop, daemon=True)
        thread.start()

    def get_bandwidth(self, reset=True):
        """
        Retorna bandwidth desde última chamada

        Returns:
            Dict com mbps_download, mbps_upload
        """
        result = {
            'mbps_download': (self.bytes_recv * 8) / (1024 * 1024),
            'mbps_upload': (self.bytes_sent * 8) / (1024 * 1024)
        }

        if reset:
            self.bytes_recv = 0
            self.bytes_sent = 0

        return result

    def stop(self):
        """Para monitoring"""
        self.running = False

# Uso
monitor = BandwidthMonitor()
monitor.start()

time.sleep(5)
bandwidth = monitor.get_bandwidth()
print(f"Download: {bandwidth['mbps_download']:.2f} Mbps")
print(f"Upload: {bandwidth['mbps_upload']:.2f} Mbps")

monitor.stop()
```

---

<a name="network-metrics"></a>
### 3.2 MÉTRICAS DE REDE

#### Latência (Ping)

```python
import subprocess
import re

def measure_latency(host='8.8.8.8', count=4):
    """
    Mede latência via ping

    Returns:
        Dict com min, avg, max, mdev (ms)
    """
    result = subprocess.run(
        ['ping', '-c', str(count), host],
        capture_output=True,
        text=True
    )

    # Parse output
    # Exemplo: rtt min/avg/max/mdev = 10.123/15.456/20.789/3.456 ms
    match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', result.stdout)

    if match:
        return {
            'min_ms': float(match.group(1)),
            'avg_ms': float(match.group(2)),
            'max_ms': float(match.group(3)),
            'mdev_ms': float(match.group(4))
        }

    return None
```

---

#### Packet Loss

```python
def measure_packet_loss(host='8.8.8.8', count=100):
    """
    Mede packet loss

    Returns:
        Porcentagem de perda (0-100)
    """
    result = subprocess.run(
        ['ping', '-c', str(count), host],
        capture_output=True,
        text=True
    )

    # Parse: "100 packets transmitted, 98 received, 2% packet loss"
    match = re.search(r'(\d+)% packet loss', result.stdout)

    if match:
        return float(match.group(1))

    return None
```

---

#### Jitter

```python
def measure_jitter(host='8.8.8.8', count=20):
    """
    Mede jitter (variação de latência)

    Returns:
        Jitter em ms
    """
    result = subprocess.run(
        ['ping', '-c', str(count), host],
        capture_output=True,
        text=True
    )

    # Extrai todos os tempos
    times = re.findall(r'time=([\d.]+)', result.stdout)
    times = [float(t) for t in times]

    if len(times) < 2:
        return None

    # Calcula diferenças entre pings consecutivos
    diffs = [abs(times[i+1] - times[i]) for i in range(len(times)-1)]

    # Jitter = média das diferenças
    jitter = sum(diffs) / len(diffs)

    return jitter
```

---

<a name="performance"></a>
### 3.3 PERFORMANCE MEASUREMENT

#### Iperf3 Integration

```python
import subprocess
import json

def run_iperf3_test(server='iperf.he.net', duration=10):
    """
    Executa teste de bandwidth com iperf3

    Returns:
        Dict com resultados detalhados
    """
    result = subprocess.run(
        ['iperf3', '-c', server, '-t', str(duration), '-J'],
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    return {
        'sent_mbps': data['end']['sum_sent']['bits_per_second'] / 1e6,
        'received_mbps': data['end']['sum_received']['bits_per_second'] / 1e6,
        'retransmits': data['end']['sum_sent']['retransmits'],
        'jitter_ms': data['end']['sum']['jitter_ms']
    }
```

---

<a name="wifi-tools"></a>
## 4. WIFI MONITORING TOOLS

<a name="aircrack"></a>
### 4.1 AIRCRACK-NG SUITE

**Website:** https://www.aircrack-ng.org/
**Licença:** GPL-2.0

#### Ferramentas da Suite

```
aircrack-ng suite:
├── airmon-ng     - Enable monitor mode
├── airodump-ng   - Capture packets / Scan networks
├── aireplay-ng   - Packet injection
├── aircrack-ng   - WEP/WPA cracking (EDUCATIONAL ONLY!)
└── airdecap-ng   - Decrypt WEP/WPA captures
```

---

#### Monitor Mode (Educational)

```bash
# Listar interfaces
airmon-ng

# Ativar monitor mode
sudo airmon-ng start wlan0

# Interface criada: wlan0mon

# Desativar monitor mode
sudo airmon-ng stop wlan0mon
```

---

#### Scan Networks

```bash
# Scan todas as redes
sudo airodump-ng wlan0mon

# Output:
# BSSID              PWR  Beacons  #Data  CH  MB   ENC  CIPHER AUTH ESSID
# AA:BB:CC:DD:EE:FF  -45      100    500   6  54e  WPA2 CCMP   PSK  MyNetwork
# 11:22:33:44:55:66  -67       50     10  11  54e  WPA2 CCMP   PSK  Neighbor_WiFi

# Scan canal específico
sudo airodump-ng -c 6 wlan0mon

# Salvar captura
sudo airodump-ng -c 6 -w capture --output-format pcap wlan0mon
```

---

#### Python Wrapper

```python
import subprocess
import re

def scan_wifi_networks(interface='wlan0mon', timeout=10):
    """
    Scan redes WiFi usando airodump-ng

    Returns:
        Lista de dicts com info de cada rede
    """
    # Executa airodump-ng por N segundos
    proc = subprocess.Popen(
        ['sudo', 'airodump-ng', interface, '--output-format', 'csv', '-w', '/tmp/scan'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(timeout)
    proc.terminate()

    # Parse CSV
    networks = []
    with open('/tmp/scan-01.csv', 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() and not line.startswith('BSSID'):
                parts = line.split(',')
                if len(parts) >= 14:
                    networks.append({
                        'bssid': parts[0].strip(),
                        'power': int(parts[8].strip()) if parts[8].strip().lstrip('-').isdigit() else None,
                        'beacons': int(parts[9].strip()) if parts[9].strip().isdigit() else 0,
                        'data': int(parts[10].strip()) if parts[10].strip().isdigit() else 0,
                        'channel': int(parts[3].strip()) if parts[3].strip().isdigit() else None,
                        'encryption': parts[5].strip(),
                        'ssid': parts[13].strip()
                    })

    return networks
```

---

<a name="iwconfig"></a>
### 4.2 IWCONFIG/IW

#### iwconfig (Legacy)

```bash
# Informações da interface
iwconfig wlan0

# Output:
# wlan0     IEEE 802.11  ESSID:"MyNetwork"
#           Mode:Managed  Frequency:5.18 GHz  Access Point: AA:BB:CC:DD:EE:FF
#           Bit Rate=866.7 Mb/s   Tx-Power=20 dBm
#           Retry short limit:7   RTS thr:off   Fragment thr:off
#           Power Management:on
#           Link Quality=70/70  Signal level=-40 dBm
#           Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
#           Tx excessive retries:0  Invalid misc:0   Missed beacon:0
```

#### iw (Modern)

```bash
# Informações gerais
iw dev wlan0 info

# Scan de redes
sudo iw dev wlan0 scan

# Link statistics
iw dev wlan0 link

# Station statistics
iw dev wlan0 station dump
```

---

#### Python Wrapper

```python
def get_wifi_info(interface='wlan0'):
    """
    Obtém informações WiFi usando iw

    Returns:
        Dict com SSID, BSSID, frequency, signal, etc.
    """
    result = subprocess.run(
        ['iw', 'dev', interface, 'link'],
        capture_output=True,
        text=True
    )

    info = {}

    # Parse output
    for line in result.stdout.split('\n'):
        if 'SSID:' in line:
            info['ssid'] = line.split('SSID:')[1].strip()
        elif 'freq:' in line:
            info['frequency'] = int(line.split('freq:')[1].strip().split()[0])
        elif 'signal:' in line:
            signal_str = line.split('signal:')[1].strip().split()[0]
            info['signal_dbm'] = int(signal_str)
        elif 'Connected to' in line:
            info['bssid'] = line.split()[2]

    return info
```

---

<a name="wavemon"></a>
### 4.3 WAVEMON

**GitHub:** https://github.com/uoaerg/wavemon
**Linguagem:** C
**Licença:** GPL-3.0

#### Features

- Real-time signal level monitoring
- Histogram de sinal
- Info sobre AP
- Scan de redes
- TUI interativo

#### Uso

```bash
# Instalar
sudo apt install wavemon

# Executar
wavemon
```

**Interface:**
```
┌─ Signal Level ────────────────────────────────┐
│                                               │
│  -40 dBm  ████████████████████░░░░░░  80%    │
│                                               │
│  Link Quality: 70/70                          │
│  Frequency: 5180 MHz (Channel 36)             │
│  Bit Rate: 866.7 Mb/s                         │
│                                               │
│  Histogram (last 60s):                        │
│  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁                │
│                                               │
└───────────────────────────────────────────────┘
```

---

<a name="wifi-security"></a>
### 4.4 WIFI SECURITY ANALYSIS

#### Análise de Segurança

```python
def analyze_wifi_security(network_info):
    """
    Analisa segurança de rede WiFi

    Returns:
        Dict com score e recomendações
    """
    score = 100
    issues = []
    recommendations = []

    # Verifica encryption
    encryption = network_info.get('encryption', '')

    if 'WPA3' in encryption:
        # Ótimo!
        pass
    elif 'WPA2' in encryption:
        score -= 10
        recommendations.append("Upgrade para WPA3 se disponível")
    elif 'WPA' in encryption and 'WPA2' not in encryption:
        score -= 40
        issues.append("WPA1 é inseguro!")
        recommendations.append("URGENTE: Upgrade para WPA2/WPA3")
    elif 'WEP' in encryption:
        score -= 80
        issues.append("WEP é extremamente inseguro!")
        recommendations.append("CRÍTICO: WEP pode ser quebrado em minutos!")
    else:
        score -= 100
        issues.append("Rede aberta (sem criptografia)!")
        recommendations.append("CRÍTICO: Configure WPA2/WPA3 imediatamente!")

    # Verifica força do sinal
    signal_dbm = network_info.get('signal_dbm', -100)
    if signal_dbm > -50:
        # Sinal forte
        pass
    elif signal_dbm > -70:
        score -= 5
        recommendations.append("Sinal OK, mas pode melhorar")
    else:
        score -= 20
        issues.append("Sinal fraco")
        recommendations.append("Aproxime-se do roteador ou use repetidor")

    # Verifica canal (2.4 GHz vs 5 GHz)
    frequency = network_info.get('frequency', 0)
    if frequency > 5000:
        # 5 GHz - melhor
        pass
    else:
        score -= 10
        recommendations.append("Considere usar 5 GHz para melhor performance")

    return {
        'score': max(0, score),
        'level': 'EXCELLENT' if score >= 90 else 'GOOD' if score >= 70 else 'FAIR' if score >= 50 else 'POOR',
        'issues': issues,
        'recommendations': recommendations
    }
```

---

## 📚 CONCLUSÃO DA PARTE 2

Nesta segunda parte cobrimos:

✅ **Packet Analysis Profundo:**
- tshark (Wireshark CLI) com display filters avançados
- Wireshark display filters completos
- Scapy para packet manipulation em Python
- tcpdump e BPF filters
- Padrões de análise (top talkers, protocol distribution, anomaly detection)

✅ **System Monitors TUI:**
- btop++ (C++) - visual impressionante com Braille graphs
- bottom (Rust) - altamente customizável com filtros poderosos
- gtop (Node.js) - blessed-contrib para gráficos
- Análise comparativa completa

✅ **Bandwidth Calculation & Metrics:**
- Métodos de cálculo (psutil, /proc/net/dev, Scapy)
- Métricas de rede (latência, packet loss, jitter)
- Performance measurement (iperf3)

✅ **WiFi Monitoring Tools:**
- aircrack-ng suite (educational)
- iwconfig/iw para info WiFi
- wavemon para monitoring visual
- Análise de segurança WiFi

---

**PRÓXIMA PARTE:** RESEARCH_PART3_ARCHITECTURE.md

Conteúdo:
- Arquiteturas modulares (Plugin, Composite, Observer, MVC)
- Python libraries (Rich, Textual, blessed-contrib)
- Features priorizadas com roadmap
- Padrões de design para dashboards
- Sistema de configuração YAML
- Hot-reload e dependency injection

---

**Juan-Dev - Soli Deo Gloria ✝️**
