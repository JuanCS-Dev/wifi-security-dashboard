# 📚 REFERENCES - WiFi Security Education Dashboard v2.0

**Projeto:** WiFi Security Education Dashboard
**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Propósito:** Lista organizada de todas as referências utilizadas na pesquisa e desenvolvimento

---

## 📑 Índice

1. [Sampler](#1-sampler)
2. [Network Monitoring Tools](#2-network-monitoring-tools)
3. [System Monitoring Tools](#3-system-monitoring-tools)
4. [Packet Analysis Tools](#4-packet-analysis-tools)
5. [WiFi Monitoring Tools](#5-wifi-monitoring-tools)
6. [Python Libraries](#6-python-libraries)
7. [Go Libraries (Sampler)](#7-go-libraries-sampler)
8. [Documentation & Tutorials](#8-documentation--tutorials)
9. [Research Papers & Articles](#9-research-papers--articles)
10. [Educational Resources](#10-educational-resources)

---

## 1. Sampler

### 1.1 Official Repository

**sqshq/sampler**
- **URL:** https://github.com/sqshq/sampler
- **Stars:** ~12.2k
- **Language:** Go
- **Description:** Tool for shell commands execution, visualization and alerting. Configured with a simple YAML file.
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐ (Core inspiration do projeto)
- **Uso:** Arquitetura base, YAML config, componentes visuais, rate-based updates

**Key Files:**
- `config.yml` - Exemplo de configuração
- `main.go` - Entry point
- `/component` - Implementação dos 6 componentes
- `/console` - TUI rendering

---

## 2. Network Monitoring Tools

### 2.1 bandwhich

**imsnif/bandwhich**
- **URL:** https://github.com/imsnif/bandwhich
- **Stars:** ~9.5k
- **Language:** Rust
- **Description:** Terminal bandwidth utilization tool
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - Shows current network utilization by process
  - Shows connections by process
  - Uses `libpcap` for packet capture
  - TUI com `tui-rs`
- **Comandos:**
  ```bash
  sudo bandwhich
  sudo bandwhich -i wlan0
  ```

### 2.2 nethogs

**raboof/nethogs**
- **URL:** https://github.com/raboof/nethogs
- **Stars:** ~3k
- **Language:** C++
- **Description:** Linux network bandwidth monitor per process
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Groups bandwidth by process
  - Works with libpcap
  - Real-time updates
- **Comandos:**
  ```bash
  sudo nethogs wlan0
  sudo nethogs -t  # Text mode
  sudo nethogs -d 5  # Delay 5s
  ```

### 2.3 iftop

**pdw-mb/iftop**
- **URL:** https://code.blinkace.com/pdw/iftop
- **Mirror:** https://github.com/topics/iftop
- **Language:** C
- **Description:** Display bandwidth usage on an interface by host
- **License:** GPL
- **Relevância:** ⭐⭐⭐
- **Features:**
  - Shows connections between hosts
  - Real-time bandwidth usage
  - Filter by network/host
- **Comandos:**
  ```bash
  sudo iftop -i wlan0
  sudo iftop -n  # No DNS resolution
  sudo iftop -B  # Display in bytes
  ```

### 2.4 vnstat

**vergoh/vnstat**
- **URL:** https://github.com/vergoh/vnstat
- **Stars:** ~1.3k
- **Language:** C
- **Description:** Console-based network traffic monitor
- **License:** GPL
- **Relevância:** ⭐⭐⭐
- **Features:**
  - Historical data storage
  - Daily/monthly statistics
  - Lightweight daemon
- **Comandos:**
  ```bash
  vnstat -i wlan0
  vnstat -l  # Live mode
  vnstat -d  # Daily stats
  vnstat -m  # Monthly stats
  ```

### 2.5 slurm

**mattthias/slurm**
- **URL:** https://github.com/mattthias/slurm
- **Language:** C
- **Description:** Simple, curses-based network load monitor
- **License:** GPL
- **Relevância:** ⭐⭐
- **Features:**
  - Real-time graph of network traffic
  - Very lightweight
  - Classic ncurses interface

---

## 3. System Monitoring Tools

### 3.1 btop++

**aristocratos/btop**
- **URL:** https://github.com/aristocratos/btop
- **Stars:** ~20k
- **Language:** C++
- **Description:** Resource monitor that shows usage and stats for processor, memory, disks, network and processes
- **License:** Apache 2.0
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - Beautiful TUI com Braille characters
  - Mouse support
  - Customizable themes
  - Game mode (hides btop from top lists)
  - Process tree view
- **Tech Stack:**
  - Custom TUI renderer
  - `/proc` filesystem parsing
  - `termios` para terminal control
- **Comandos:**
  ```bash
  btop
  btop --utf-force  # Force UTF-8
  ```

**Relevância para projeto:**
- Inspiração visual para gráficos
- Uso de caracteres Braille para densidade
- Arquitetura de rendering

### 3.2 bottom (btm)

**ClementTsang/bottom**
- **URL:** https://github.com/ClementTsang/bottom
- **Stars:** ~10k
- **Language:** Rust
- **Description:** Graphical process/system monitor
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Customizable via TOML
  - Cross-platform (Linux, macOS, Windows)
  - Graph-based visualization
  - Process filtering
- **Tech Stack:**
  - `tui-rs` (Rust TUI library)
  - `sysinfo` crate para system info
  - TOML config
- **Comandos:**
  ```bash
  btm
  btm -b  # Basic mode
  btm -c config.toml
  ```

### 3.3 gtop

**aksakalli/gtop**
- **URL:** https://github.com/aksakalli/gtop
- **Stars:** ~9.5k
- **Language:** JavaScript (Node.js)
- **Description:** System monitoring dashboard for terminal
- **License:** MIT
- **Relevância:** ⭐⭐⭐
- **Features:**
  - CPU history graph
  - Memory history graph
  - Network history graph
  - Process list
- **Tech Stack:**
  - `blessed` (Node.js TUI)
  - `blessed-contrib` (widgets)
  - `systeminformation` (system data)
- **Comandos:**
  ```bash
  npm install -g gtop
  gtop
  ```

**Relevância para projeto:**
- JavaScript TUI architecture similar to Python
- Component-based rendering

### 3.4 htop

**htop-dev/htop**
- **URL:** https://github.com/htop-dev/htop
- **Stars:** ~6.3k
- **Language:** C
- **Description:** Interactive process viewer
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Classic ncurses interface
  - Process tree
  - Customizable columns
  - Mouse support
- **Comandos:**
  ```bash
  htop
  htop -u maximus  # Filter by user
  ```

---

## 4. Packet Analysis Tools

### 4.1 Wireshark

**wireshark/wireshark**
- **URL:** https://github.com/wireshark/wireshark
- **Website:** https://www.wireshark.org/
- **Stars:** ~7k
- **Language:** C, C++
- **Description:** Network protocol analyzer
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - Deep inspection of hundreds of protocols
  - Live capture and offline analysis
  - Rich display filters
  - VoIP analysis
- **Comandos:**
  ```bash
  # tshark (CLI version)
  tshark -i wlan0
  tshark -i wlan0 -Y "http.request"
  tshark -r capture.pcap -T fields -e ip.src -e ip.dst
  ```

**Display Filters Examples:**
- `wlan` - WiFi packets only
- `wlan.fc.type == 0` - Management frames
- `wlan.ssid == "MyNetwork"` - Specific SSID
- `http.request.method == "GET"` - HTTP GET requests
- `tcp.port == 443` - HTTPS traffic

### 4.2 Scapy

**secdev/scapy**
- **URL:** https://github.com/secdev/scapy
- **Docs:** https://scapy.readthedocs.io/
- **Stars:** ~10k
- **Language:** Python
- **Description:** Python-based interactive packet manipulation program
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - Build/decode packets of many protocols
  - Send/capture packets
  - PCAP read/write
  - Network scanning
- **Exemplos:**
  ```python
  from scapy.all import *

  # Sniff WiFi packets
  packets = sniff(iface="wlan0", count=10)

  # Filter by protocol
  http_packets = sniff(iface="wlan0", filter="tcp port 80")

  # Analyze packet
  packet = packets[0]
  if packet.haslayer(Dot11):
      print(packet[Dot11].addr2)  # Source MAC
  ```

### 4.3 tcpdump

**the-tcpdump-group/tcpdump**
- **URL:** https://github.com/the-tcpdump-group/tcpdump
- **Website:** https://www.tcpdump.org/
- **Language:** C
- **Description:** Command-line packet analyzer
- **License:** BSD
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Classic packet capture tool
  - BPF filters
  - PCAP output
- **Comandos:**
  ```bash
  sudo tcpdump -i wlan0
  sudo tcpdump -i wlan0 port 80
  sudo tcpdump -i wlan0 -w capture.pcap
  sudo tcpdump -r capture.pcap
  ```

**BPF Filters:**
- `host 192.168.1.1` - Traffic to/from host
- `net 192.168.0.0/16` - Network range
- `port 443` - Specific port
- `tcp and port 80` - TCP on port 80
- `not port 22` - Exclude SSH

### 4.4 ngrep

**jpr5/ngrep**
- **URL:** https://github.com/jpr5/ngrep
- **Language:** C
- **Description:** Network grep - search network packets
- **License:** BSD
- **Relevância:** ⭐⭐⭐
- **Features:**
  - Regex pattern matching on packet payloads
  - BPF filters
  - Human-readable output
- **Comandos:**
  ```bash
  sudo ngrep -d wlan0 "GET"
  sudo ngrep -W byline -q "^GET|^POST"
  ```

---

## 5. WiFi Monitoring Tools

### 5.1 aircrack-ng suite

**aircrack-ng/aircrack-ng**
- **URL:** https://github.com/aircrack-ng/aircrack-ng
- **Website:** https://www.aircrack-ng.org/
- **Stars:** ~5.5k
- **Language:** C
- **Description:** Complete suite of tools to assess WiFi network security
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐⭐ (Educational context)
- **Tools:**
  - `airmon-ng` - Monitor mode setup
  - `airodump-ng` - Packet capture
  - `aireplay-ng` - Packet injection
  - `aircrack-ng` - WEP/WPA cracking
- **Comandos:**
  ```bash
  sudo airmon-ng start wlan0
  sudo airodump-ng wlan0mon
  sudo airodump-ng --bssid XX:XX:XX:XX:XX:XX -c 6 -w capture wlan0mon
  ```

**Relevância para projeto:**
- Captura de frames de management/data
- Análise de redes WiFi
- Educational context: mostrar vulnerabilidades

### 5.2 wavemon

**uoaerg/wavemon**
- **URL:** https://github.com/uoaerg/wavemon
- **Language:** C
- **Description:** Wireless device monitoring application
- **License:** GPL
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - ncurses-based interface
  - Signal level monitoring
  - Network statistics
  - Scan for access points
- **Comandos:**
  ```bash
  wavemon
  wavemon -i wlan0
  ```

### 5.3 iw / iwconfig

**linux-wireless/iw**
- **URL:** https://git.kernel.org/pub/scm/linux/kernel/git/jberg/iw.git
- **Language:** C
- **Description:** Tool for configuring Linux wireless devices
- **License:** ISC
- **Relevância:** ⭐⭐⭐⭐
- **Comandos:**
  ```bash
  iw dev wlan0 info
  iw dev wlan0 link
  iw dev wlan0 scan
  iw dev wlan0 station dump

  # Legacy (deprecated but still common)
  iwconfig wlan0
  ```

---

## 6. Python Libraries

### 6.1 Rich

**Textualize/rich**
- **URL:** https://github.com/Textualize/rich
- **Docs:** https://rich.readthedocs.io/
- **Stars:** ~49k
- **Language:** Python
- **Description:** Python library for rich text and beautiful formatting in the terminal
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐ (Core library do projeto atual)
- **Features:**
  - Tables, panels, syntax highlighting
  - Progress bars, spinners
  - Markdown rendering
  - Emoji support
  - ANSI color support
- **Instalação:**
  ```bash
  pip install rich
  ```
- **Exemplos:**
  ```python
  from rich.console import Console
  from rich.table import Table

  console = Console()
  console.print("[bold red]Error![/bold red]")

  table = Table()
  table.add_column("Name")
  table.add_row("Alice")
  console.print(table)
  ```

### 6.2 Textual

**Textualize/textual**
- **URL:** https://github.com/Textualize/textual
- **Docs:** https://textual.textualize.io/
- **Stars:** ~25k
- **Language:** Python
- **Description:** Rapid Application Development framework for Python TUI
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Widget-based architecture
  - CSS-like styling
  - Reactive programming
  - Mouse support
  - Hot reload
- **Instalação:**
  ```bash
  pip install textual textual-dev
  ```

**Consideração:** Alternativa mais robusta ao Rich puro, mas com mais complexidade.

### 6.3 plotext

**piccolomo/plotext**
- **URL:** https://github.com/piccolomo/plotext
- **Docs:** https://github.com/piccolomo/plotext/blob/master/readme/basic.md
- **Stars:** ~2.8k
- **Language:** Python
- **Description:** Plotting library for terminal
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - Line plots, bar charts, scatter plots
  - Subplots
  - Date plotting
  - Matrix plots
  - Works in any terminal
- **Instalação:**
  ```bash
  pip install plotext
  ```
- **Exemplos:**
  ```python
  import plotext as plt

  plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
  plt.title("My Plot")
  plt.show()

  # For integration with Rich
  chart_str = plt.build()
  ```

### 6.4 psutil

**giampaolo/psutil**
- **URL:** https://github.com/giampaolo/psutil
- **Docs:** https://psutil.readthedocs.io/
- **Stars:** ~10k
- **Language:** Python (C extensions)
- **Description:** Cross-platform library for process and system monitoring
- **License:** BSD
- **Relevância:** ⭐⭐⭐⭐⭐
- **Features:**
  - CPU, memory, disk, network stats
  - Process management
  - Cross-platform
  - No external dependencies
- **Instalação:**
  ```bash
  pip install psutil
  ```
- **Exemplos:**
  ```python
  import psutil

  # CPU
  psutil.cpu_percent(interval=1)
  psutil.cpu_count()

  # Memory
  mem = psutil.virtual_memory()
  mem.percent

  # Network
  net = psutil.net_io_counters(pernic=True)
  net['wlan0'].bytes_sent
  ```

### 6.5 PyYAML

**yaml/pyyaml**
- **URL:** https://github.com/yaml/pyyaml
- **Docs:** https://pyyaml.org/wiki/PyYAMLDocumentation
- **Stars:** ~2.5k
- **Language:** Python
- **Description:** YAML parser and emitter
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐
- **Instalação:**
  ```bash
  pip install pyyaml
  ```
- **Exemplos:**
  ```python
  import yaml

  with open('config.yml', 'r') as f:
      config = yaml.safe_load(f)
  ```

### 6.6 pydantic

**pydantic/pydantic**
- **URL:** https://github.com/pydantic/pydantic
- **Docs:** https://docs.pydantic.dev/
- **Stars:** ~20k
- **Language:** Python
- **Description:** Data validation using Python type hints
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐
- **Features:**
  - Type validation
  - Schema generation
  - JSON parsing
  - Settings management
- **Instalação:**
  ```bash
  pip install pydantic
  ```

### 6.7 urwid

**urwid/urwid**
- **URL:** https://github.com/urwid/urwid
- **Docs:** https://urwid.org/
- **Stars:** ~2.8k
- **Language:** Python
- **Description:** Console user interface library
- **License:** LGPL
- **Relevância:** ⭐⭐⭐
- **Features:**
  - Widget-based
  - Event loop
  - Mouse support
  - Classic ncurses-like
- **Consideração:** Mais antigo que Textual, mas battle-tested.

---

## 7. Go Libraries (Sampler)

### 7.1 termui

**gizak/termui**
- **URL:** https://github.com/gizak/termui
- **Stars:** ~13k
- **Language:** Go
- **Description:** Golang terminal dashboard
- **License:** MIT
- **Relevância:** ⭐⭐⭐⭐⭐ (Usado pelo Sampler)
- **Features:**
  - Cross-platform
  - Multiple widgets (Line chart, bar chart, gauge, etc.)
  - Grid layout
  - Event system

**Usado por Sampler para:**
- Rendering de componentes visuais
- Layout system
- Event handling

### 7.2 yaml.v2

**go-yaml/yaml**
- **URL:** https://github.com/go-yaml/yaml
- **Language:** Go
- **Description:** YAML support for Go
- **License:** Apache 2.0
- **Relevância:** ⭐⭐⭐⭐⭐ (Config parsing do Sampler)

---

## 8. Documentation & Tutorials

### 8.1 Wireshark Display Filters Reference

- **URL:** https://www.wireshark.org/docs/dfref/
- **Description:** Complete reference of all display filters
- **Relevância:** ⭐⭐⭐⭐⭐

**Key sections:**
- IEEE 802.11 (WLAN) filters
- TCP/IP filters
- HTTP filters

### 8.2 Scapy Documentation

- **URL:** https://scapy.readthedocs.io/en/latest/
- **Relevância:** ⭐⭐⭐⭐⭐

**Key sections:**
- Building packets
- Sniffing
- Layers reference
- Advanced usage

### 8.3 Rich Documentation

- **URL:** https://rich.readthedocs.io/en/stable/
- **Relevância:** ⭐⭐⭐⭐⭐

**Key sections:**
- Console API
- Tables
- Panels
- Layout
- Live display
- ANSI/Markup

### 8.4 BPF Syntax Guide

- **URL:** https://biot.com/capstats/bpf.html
- **Description:** Berkeley Packet Filter syntax reference
- **Relevância:** ⭐⭐⭐⭐

### 8.5 Linux Wireless Wiki

- **URL:** https://wireless.wiki.kernel.org/
- **Description:** Official Linux wireless documentation
- **Relevância:** ⭐⭐⭐⭐

**Key pages:**
- `iw` documentation
- Monitor mode
- WiFi drivers

### 8.6 /proc Filesystem Documentation

- **URL:** https://www.kernel.org/doc/html/latest/filesystems/proc.html
- **Description:** Linux /proc filesystem documentation
- **Relevância:** ⭐⭐⭐⭐

**Key files:**
- `/proc/net/dev` - Network statistics
- `/proc/stat` - System statistics
- `/proc/meminfo` - Memory information

---

## 9. Research Papers & Articles

### 9.1 IEEE 802.11 Standard

- **Title:** IEEE 802.11 Wireless LAN Standard
- **URL:** https://standards.ieee.org/standard/802_11-2020.html
- **Relevância:** ⭐⭐⭐⭐⭐ (Educational context)
- **Topics:**
  - Frame types (Management, Control, Data)
  - CSMA/CA protocol
  - Security (WPA2, WPA3)

### 9.2 Aircrack-ng Tutorial

- **URL:** https://www.aircrack-ng.org/doku.php?id=tutorial
- **Relevância:** ⭐⭐⭐⭐ (Educational context)
- **Topics:**
  - WiFi packet capture
  - Frame injection
  - Security auditing

### 9.3 "Building Terminal Dashboards with Rich"

- **Author:** Will McGugan (creator of Rich)
- **URL:** https://www.willmcgugan.com/blog/tech/post/building-rich-terminal-dashboards/
- **Relevância:** ⭐⭐⭐⭐⭐
- **Topics:**
  - Live rendering
  - Layout system
  - Performance tips

---

## 10. Educational Resources

### 10.1 Network Traffic Analysis Course

- **Platform:** Wireshark University
- **URL:** https://www.wireshark.org/training/
- **Relevância:** ⭐⭐⭐⭐
- **Topics:**
  - Packet analysis fundamentals
  - Protocol analysis
  - Network troubleshooting

### 10.2 WiFi Security

- **Book:** "Wi-Foo: The Secrets of Wireless Hacking"
- **Authors:** A. Vladimirov, K. Gavrilenko, A. Mikhailovsky
- **Relevância:** ⭐⭐⭐⭐ (Educational context)

### 10.3 Python TUI Development

- **Article:** "Building Beautiful Terminal UIs in Python"
- **URL:** https://www.textualize.io/blog/
- **Relevância:** ⭐⭐⭐⭐

### 10.4 Understanding Network Protocols

- **Platform:** Coursera - "The Bits and Bytes of Computer Networking"
- **Provider:** Google
- **URL:** https://www.coursera.org/learn/computer-networking
- **Relevância:** ⭐⭐⭐⭐

---

## 📊 Resumo por Categoria

| Categoria | Quantidade | Relevância Alta (⭐⭐⭐⭐⭐) |
|-----------|------------|-------------------------|
| Sampler | 1 | 1 |
| Network Tools | 5 | 1 |
| System Tools | 4 | 1 |
| Packet Analysis | 4 | 2 |
| WiFi Tools | 3 | 1 |
| Python Libraries | 7 | 5 |
| Go Libraries | 2 | 2 |
| Documentation | 6 | 4 |
| Papers/Articles | 3 | 2 |
| Educational | 4 | 0 |
| **TOTAL** | **39** | **19** |

---

## 🔗 Quick Reference Links

### Must-Read Documentation
1. [Sampler GitHub](https://github.com/sqshq/sampler)
2. [Rich Documentation](https://rich.readthedocs.io/)
3. [Wireshark Filters](https://www.wireshark.org/docs/dfref/)
4. [Scapy Docs](https://scapy.readthedocs.io/)
5. [plotext Examples](https://github.com/piccolomo/plotext)

### Essential Tools to Install
```bash
# Network monitoring
sudo apt install bandwhich nethogs iftop vnstat

# System monitoring
sudo apt install btop htop

# Packet analysis
sudo apt install wireshark tshark tcpdump

# WiFi tools
sudo apt install aircrack-ng wavemon iw

# Python dependencies
pip install rich textual plotext psutil pyyaml scapy
```

### Quick Command Reference
```bash
# Network monitoring
sudo bandwhich -i wlan0
sudo nethogs wlan0

# Packet capture
sudo tshark -i wlan0 -Y "wlan"
sudo tcpdump -i wlan0 port 80

# WiFi info
iw dev wlan0 link
iw dev wlan0 station dump
wavemon

# System monitoring
btop
htop
```

---

## 📝 Notas de Atualização

**2025-11-09:** Versão inicial com 39 referências organizadas
- Todas as ferramentas da pesquisa documentadas
- Links verificados e funcionais
- Comandos de exemplo incluídos
- Ratings de relevância adicionados

---

## 🎯 Próximos Passos

Para manter este documento atualizado:
1. ✅ Adicionar novas ferramentas descobertas durante desenvolvimento
2. ✅ Verificar links periodicamente (algumas ferramentas podem mudar de repo)
3. ✅ Atualizar star counts mensalmente
4. ✅ Adicionar novos tutoriais/artigos relevantes
5. ✅ Documentar lessons learned durante implementação

---

**Juan-Dev - Soli Deo Gloria ✝️**
