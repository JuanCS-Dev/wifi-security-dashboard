# 📊 DEEP RESEARCH - PARTE 1: SAMPLER & NETWORK MONITORING TOOLS

**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Projeto:** WiFi Security Education Dashboard - Aula 2
**Objetivo:** Evolução para dashboard profissional de análise de rede

---

## 🎯 ÍNDICE - PARTE 1

1. [SAMPLER - ANÁLISE COMPLETA](#sampler)
   - 1.1 [Arquitetura e Design](#arquitetura-sampler)
   - 1.2 [Componentes Visuais](#componentes-sampler)
   - 1.3 [Sistema de Configuração YAML](#yaml-sampler)
   - 1.4 [Triggers e Alertas](#triggers-sampler)
   - 1.5 [Interactive Shells](#shells-sampler)
   - 1.6 [Best Practices](#best-practices-sampler)

2. [NETWORK MONITORING TOOLS](#network-tools)
   - 2.1 [bandwhich](#bandwhich)
   - 2.2 [nethogs](#nethogs)
   - 2.3 [iftop](#iftop)
   - 2.4 [vnstat](#vnstat)
   - 2.5 [slurm](#slurm)
   - 2.6 [Comparativo Técnico](#comparativo-tools)

3. [IMPLEMENTAÇÃO PRÁTICA](#implementacao)
   - 3.1 [Replicando Sampler em Python/Rich](#python-sampler)
   - 3.2 [Integrando Network Tools](#integracao-tools)

---

<a name="sampler"></a>
## 1. SAMPLER - ANÁLISE COMPLETA

### Visão Geral

**Sampler** é uma ferramenta para visualização de comandos shell em tempo real, configurada via YAML.

**GitHub:** https://github.com/sqshq/sampler
**Linguagem:** Go
**Licença:** GPL-3.0
**Estrelas:** ~12.5k ⭐

**Filosofia de Design:**
- "Se você pode obter uma métrica via shell command, você pode visualizá-la com Sampler"
- Configuração declarativa (YAML)
- Zero dependências além do binário
- Altamente customizável

---

<a name="arquitetura-sampler"></a>
### 1.1 ARQUITETURA E DESIGN DO SAMPLER

#### Estrutura Interna

```
sampler/
├── main.go              # Entry point
├── config/
│   ├── config.go        # Parser YAML
│   └── validator.go     # Validação de config
├── component/
│   ├── component.go     # Interface base
│   ├── runchart.go      # Componente line chart
│   ├── sparkline.go     # Sparkline inline
│   ├── barchart.go      # Bar chart
│   ├── gauge.go         # Gauge/medidor
│   ├── textbox.go       # Caixa de texto
│   └── asciibox.go      # ASCII art box
├── console/
│   ├── console.go       # Gerenciador de console
│   └── palette.go       # Sistema de cores
├── data/
│   ├── sampler.go       # Executor de comandos
│   └── item.go          # Data items
├── event/
│   └── event.go         # Sistema de eventos
└── trigger/
    ├── trigger.go       # Trigger system
    └── action.go        # Actions (visual, sound, script)
```

#### Pipeline de Execução

```
┌─────────────────┐
│  YAML Config    │
│  (user-defined) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Config Parser   │
│ + Validator     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Component Init  │
│ (6 tipos)       │
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │  LOOP   │◄─────────┐
    └────┬────┘          │
         │               │
         ▼               │
┌─────────────────┐      │
│ Execute Shell   │      │
│ Commands        │      │
└────────┬────────┘      │
         │               │
         ▼               │
┌─────────────────┐      │
│ Parse Output    │      │
│ (regex/jq/etc)  │      │
└────────┬────────┘      │
         │               │
         ▼               │
┌─────────────────┐      │
│ Update Component│      │
│ Display         │      │
└────────┬────────┘      │
         │               │
         ▼               │
┌─────────────────┐      │
│ Check Triggers  │      │
│ (if any)        │      │
└────────┬────────┘      │
         │               │
         ▼               │
┌─────────────────┐      │
│ Render Screen   │      │
│ (termui)        │      │
└────────┬────────┘      │
         │               │
         └───────────────┘
         (wait refresh-rate)
```

#### Sistema de Refresh

```yaml
# Cada componente tem seu próprio refresh rate
runcharts:
  - title: CPU Usage
    rate-ms: 500        # Atualiza a cada 500ms

  - title: Network Traffic
    rate-ms: 1000       # Atualiza a cada 1s
```

**Performance:**
- Comandos executam em goroutines separadas
- Non-blocking updates
- Configurable buffer sizes
- Efficient screen redraws (apenas mudanças)

---

<a name="componentes-sampler"></a>
### 1.2 COMPONENTES VISUAIS DO SAMPLER

Sampler possui **6 tipos** de componentes visuais:

#### 1. RUNCHART (Line Chart)

**Descrição:** Gráfico de linha em tempo real para métricas que variam continuamente.

**Casos de Uso:**
- CPU/RAM usage
- Network bandwidth
- Response times
- Queue sizes
- Qualquer métrica temporal

**Exemplo YAML Completo:**

```yaml
runcharts:
  - title: CPU Usage (%)
    position:
      x: 0
      y: 0
      width: 30
      height: 15
    rate-ms: 500                    # Refresh rate
    scale: 2                        # Y-axis scale factor
    legend:
      enabled: true
      details: true
    items:
      - label: CPU
        sample: ps -A -o %cpu | awk '{s+=$1} END {print s}'
        color: 178                  # Color code (0-255)

      - label: CPU_SYSTEM
        sample: iostat | awk 'NR==4 {print $4}'
        color: 81

    triggers:
      - title: CPU Alert
        condition: echo "$CPU > 80" | bc -l
        actions:
          - type: terminal-bell
          - type: sound
            sound:
              frequency: 600
              duration: 300
```

**Características:**
- Múltiplas séries (items) no mesmo gráfico
- Auto-scaling do eixo Y
- Legenda com valores atuais
- Cores customizáveis (256 color palette)
- Grid opcional

**Output Visual:**
```
┌─ CPU Usage (%) ──────────────┐
│                              │
│ 100┤                         │
│    │       ╭─╮               │
│  75┤      ╭╯ ╰╮   ╭╮         │
│    │     ╭╯   ╰╮ ╭╯╰╮        │
│  50┤    ╭╯     ╰─╯  ╰╮       │
│    │   ╭╯            ╰╮      │
│  25┤  ╭╯              ╰╮     │
│    │ ╭╯                ╰─    │
│   0┤─╯                       │
│    └─────────────────────────┤
│    CPU: 45.2%  CPU_SYS: 12.1%│
└──────────────────────────────┘
```

---

#### 2. SPARKLINE

**Descrição:** Gráfico minúsculo inline, ideal para mostrar tendências em espaço pequeno.

**Casos de Uso:**
- Memory usage trend
- Quick metrics overview
- Inline indicators
- Dashboard summaries

**Exemplo YAML:**

```yaml
sparklines:
  - title: Network Activity
    position:
      x: 0
      y: 16
      width: 30
      height: 3
    rate-ms: 1000
    scale: 0                        # Auto-scale
    sample: |
      netstat -i | awk 'NR==3 {print $7}'
```

**Output Visual:**
```
┌─ Network Activity ───────────┐
│ ▁▂▃▅▇█▇▅▃▂▁▂▃▄▅▆▇▆▅▄▃▂▁    │
└──────────────────────────────┘
```

**Diferenças vs Runchart:**
- Mais compacto (1-3 linhas de altura)
- Apenas 1 série de dados
- Sem eixos numéricos
- Unicode block characters

---

#### 3. BARCHART

**Descrição:** Gráfico de barras, ideal para comparar valores entre categorias.

**Casos de Uso:**
- Disk usage por partição
- Top processes
- Request distribution
- Resource allocation

**Exemplo YAML:**

```yaml
barcharts:
  - title: Disk Usage by Mount
    position:
      x: 31
      y: 0
      width: 30
      height: 15
    rate-ms: 5000
    scale: 100                      # Max value
    items:
      - label: root
        sample: df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
        color: 2

      - label: home
        sample: df -h /home | awk 'NR==2 {print $5}' | sed 's/%//'
        color: 3

      - label: tmp
        sample: df -h /tmp | awk 'NR==2 {print $5}' | sed 's/%//'
        color: 4
```

**Output Visual:**
```
┌─ Disk Usage by Mount ────────┐
│                              │
│ root  ████████████░░░  75%   │
│                              │
│ home  ██████████████░  85%   │
│                              │
│ tmp   ████░░░░░░░░░░  25%   │
│                              │
└──────────────────────────────┘
```

---

#### 4. GAUGE

**Descrição:** Medidor visual semicircular, ideal para métricas de 0-100%.

**Casos de Uso:**
- CPU/RAM percentage
- Battery level
- Progress indicators
- Health scores

**Exemplo YAML:**

```yaml
gauges:
  - title: Memory Usage
    position:
      x: 62
      y: 0
      width: 20
      height: 10
    rate-ms: 1000
    scale: 100
    percent-only: false             # Show value + percentage
    color: 178
    cur:
      sample: free | awk 'NR==2 {printf "%.0f", ($3/$2)*100}'
    max:
      sample: echo 100
    min:
      sample: echo 0
```

**Output Visual:**
```
┌─ Memory Usage ──┐
│                 │
│      ╭───╮      │
│    ╱       ╲    │
│   │   85%   │   │
│   │         │   │
│    ╲       ╱    │
│      ╰───╯      │
│                 │
└─────────────────┘
```

**Opções de Cor:**
```yaml
# Pode mudar de cor baseado em thresholds via triggers
triggers:
  - title: High Memory
    condition: echo "$cur > 80" | bc -l
    actions:
      - type: visual
        color: 1                    # Muda para vermelho
```

---

#### 5. TEXTBOX

**Descrição:** Caixa de texto livre para exibir output de comandos.

**Casos de Uso:**
- Logs em tempo real
- Status messages
- Command outputs
- Multiline data

**Exemplo YAML:**

```yaml
textboxes:
  - title: Docker Containers
    position:
      x: 0
      y: 19
      width: 40
      height: 15
    rate-ms: 2000
    sample: docker ps --format "table {{.Names}}\t{{.Status}}"
    border: true
    color: 6
```

**Output Visual:**
```
┌─ Docker Containers ──────────────────┐
│ NAMES              STATUS            │
│ redis              Up 2 hours        │
│ postgres           Up 5 hours        │
│ nginx              Up 1 day          │
│ app_web_1          Up 3 hours        │
│                                      │
└──────────────────────────────────────┘
```

**Features:**
- Auto-scroll em outputs longos
- Preserva formatação (ANSI colors)
- Suporta multiline
- Word wrap opcional

---

#### 6. ASCIIBOX

**Descrição:** Similar ao textbox, mas otimizado para ASCII art/figlet.

**Casos de Uso:**
- Banners
- Large metrics display
- Status indicators
- Eye-catching alerts

**Exemplo YAML:**

```yaml
asciiboxes:
  - title: Server Status
    position:
      x: 41
      y: 19
      width: 40
      height: 15
    rate-ms: 3000
    sample: |
      uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
      uptime_days=$((uptime_seconds / 86400))
      echo "$uptime_days" | figlet -f big
    font: big                       # figlet font
    border: true
    color: 2
```

**Output Visual:**
```
┌─ Server Status ──────────────────────┐
│   ____    _____                      │
│  |___ \  |___ /                      │
│    __) |   |_ \                      │
│   / __/   ___) |                     │
│  |_____| |____/   days               │
│                                      │
└──────────────────────────────────────┘
```

---

<a name="yaml-sampler"></a>
### 1.3 SISTEMA DE CONFIGURAÇÃO YAML

#### Estrutura Básica

```yaml
# sampler-config.yml

# Variáveis globais (reutilizáveis)
variables:
  database-host: localhost
  database-port: 5432
  refresh-slow: 5000
  refresh-fast: 500

# Componentes visuais
runcharts:
  - title: ...
    # ...

sparklines:
  - title: ...
    # ...

barcharts:
  - title: ...
    # ...

gauges:
  - title: ...
    # ...

textboxes:
  - title: ...
    # ...

asciiboxes:
  - title: ...
    # ...
```

#### Sistema de Posicionamento

```yaml
position:
  x: 0          # Coluna (0 = esquerda)
  y: 0          # Linha (0 = topo)
  width: 30     # Largura em caracteres
  height: 15    # Altura em linhas
```

**Grid System:**
- Terminal dividido em grid de caracteres
- Posicionamento absoluto
- Sem overlapping (validado em startup)
- Responsive via terminal resize

**Exemplo de Layout 2x2:**

```yaml
# Top-left
position: {x: 0, y: 0, width: 40, height: 20}

# Top-right
position: {x: 41, y: 0, width: 40, height: 20}

# Bottom-left
position: {x: 0, y: 21, width: 40, height: 20}

# Bottom-right
position: {x: 41, y: 21, width: 40, height: 20}
```

#### Variáveis e Interpolação

```yaml
variables:
  db_host: localhost
  db_user: admin

textboxes:
  - title: Database Connection
    sample: |
      psql -h $db_host -U $db_user -c "SELECT version();"
```

**Scope de Variáveis:**
- Globais: definidas em `variables:`
- Locais: definidas dentro de componentes
- Ambiente: `$HOME`, `$USER`, etc. (shell env vars)

---

<a name="triggers-sampler"></a>
### 1.4 TRIGGERS E ALERTAS

#### Tipos de Triggers

Sampler suporta **4 tipos** de ações trigger:

**1. Terminal Bell**
```yaml
triggers:
  - title: High CPU Alert
    condition: echo "$CPU > 90" | bc -l
    actions:
      - type: terminal-bell
```

**2. Sound (beep)**
```yaml
triggers:
  - title: Error Detected
    condition: echo "$ERROR_COUNT > 0" | bc -l
    actions:
      - type: sound
        sound:
          frequency: 800            # Hz
          duration: 500             # ms
```

**3. Visual (color change)**
```yaml
triggers:
  - title: Warning State
    condition: echo "$TEMP > 70" | bc -l
    actions:
      - type: visual
        color: 3                    # Amarelo
```

**4. Script Execution**
```yaml
triggers:
  - title: Backup on Low Disk
    condition: echo "$DISK_USAGE > 90" | bc -l
    actions:
      - type: script
        script: /usr/local/bin/emergency-cleanup.sh
```

#### Condições (Bash Expressions)

Triggers usam **bash commands** que retornam:
- `0` = true (trigger ativa)
- `1` = false (trigger inativa)

**Exemplos:**

```bash
# Comparação numérica
echo "$value > 80" | bc -l

# String matching
echo "$status" | grep -q "ERROR"

# Existência de arquivo
test -f /tmp/alert.flag

# Combinação lógica
[[ $cpu > 80 && $ram > 80 ]]
```

#### Exemplo Completo: Sistema de Alertas Multi-Nível

```yaml
runcharts:
  - title: System Temperature
    rate-ms: 1000
    items:
      - label: CPU_TEMP
        sample: sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//;s/°C//'
        color: 2

    triggers:
      # Nível 1: Warning (70-80°C)
      - title: Temp Warning
        condition: |
          temp=$(sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//;s/°C//')
          echo "$temp > 70 && $temp < 80" | bc -l
        actions:
          - type: visual
            color: 3                # Amarelo
          - type: terminal-bell

      # Nível 2: Critical (80-90°C)
      - title: Temp Critical
        condition: |
          temp=$(sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//;s/°C//')
          echo "$temp > 80 && $temp < 90" | bc -l
        actions:
          - type: visual
            color: 1                # Vermelho
          - type: sound
            sound:
              frequency: 800
              duration: 300

      # Nível 3: Emergency (>90°C)
      - title: Temp Emergency
        condition: |
          temp=$(sensors | grep 'Core 0' | awk '{print $3}' | sed 's/+//;s/°C//')
          echo "$temp > 90" | bc -l
        actions:
          - type: visual
            color: 1
          - type: sound
            sound:
              frequency: 1200
              duration: 1000
          - type: script
            script: |
              notify-send "CRITICAL TEMPERATURE" "System temp > 90°C!"
              echo "$(date): Critical temp alert" >> /var/log/sampler-alerts.log
```

---

<a name="shells-sampler"></a>
### 1.5 INTERACTIVE SHELLS

Sampler suporta **3 modos** de execução de comandos:

#### 1. Basic (Default)

Executa comando diretamente via `sh -c`:

```yaml
sample: ps aux | grep python | wc -l
```

**Características:**
- Simples e rápido
- Sem state entre execuções
- Sem interatividade

---

#### 2. PTY Mode (Pseudo-Terminal)

Para comandos que precisam de TTY:

```yaml
sample: top -b -n 1 | head -20
pty: true
```

**Quando usar:**
- Comandos que detectam TTY (vim, less, top)
- Cores ANSI preservadas
- Comandos interativos

---

#### 3. Multistep Init

Para comandos que precisam de setup inicial:

```yaml
init-sample: |
  export API_KEY="abc123"
  cd /app
  source venv/bin/activate

sample: |
  python monitor.py --status
```

**Quando usar:**
- Login em databases/APIs
- Ativação de ambientes virtuais
- Setup de variáveis de ambiente
- Mudança de diretório

**Exemplo Real: PostgreSQL Monitor**

```yaml
textboxes:
  - title: PostgreSQL Active Queries
    position: {x: 0, y: 0, width: 80, height: 25}
    rate-ms: 3000

    init-sample: |
      export PGPASSWORD="secret"
      export PGHOST="localhost"
      export PGUSER="admin"

    sample: |
      psql -d mydb -c "
        SELECT pid, usename, state, query
        FROM pg_stat_activity
        WHERE state != 'idle'
        ORDER BY query_start DESC
        LIMIT 10;
      "
```

---

<a name="best-practices-sampler"></a>
### 1.6 BEST PRACTICES DO SAMPLER

#### Performance

**✅ DO:**
```yaml
# Cache comandos lentos
variables:
  hostname: $(hostname)             # Executado 1x no startup

# Use refresh rates apropriados
rate-ms: 5000                       # 5s para dados que mudam devagar
```

**❌ DON'T:**
```yaml
# Evite comandos muito frequentes
rate-ms: 100                        # 100ms pode sobrecarregar sistema

# Evite comandos lentos em loop
sample: curl https://api.slow.com   # Pode travar UI
```

---

#### Parsing de Output

**✅ DO:**
```yaml
# Use awk/sed para parsing eficiente
sample: ps aux | awk 'NR>1 {sum+=$3} END {print sum}'

# Use jq para JSON
sample: curl -s localhost:8080/metrics | jq '.cpu_usage'
```

**❌ DON'T:**
```yaml
# Evite múltiplos pipes desnecessários
sample: cat file | grep x | grep y | grep z | awk '{print $1}' | sed 's/a/b/'

# Simplifique:
sample: awk '/x/ && /y/ && /z/ {gsub(/a/,"b"); print $1}' file
```

---

#### Organização de Configs

```yaml
# Agrupe componentes relacionados
# Use variáveis para valores repetidos
# Documente triggers complexos

variables:
  # Database config
  db_host: localhost
  db_port: 5432

  # Refresh rates
  fast: 500
  medium: 2000
  slow: 5000

# CPU Monitoring Section
runcharts:
  - title: CPU Usage
    rate-ms: $fast
    # ...

# Disk Monitoring Section
barcharts:
  - title: Disk Usage
    rate-ms: $slow
    # ...
```

---

<a name="network-tools"></a>
## 2. NETWORK MONITORING TOOLS

Análise comparativa de ferramentas de monitoring de rede para terminal.

---

<a name="bandwhich"></a>
### 2.1 BANDWHICH

**GitHub:** https://github.com/imsnif/bandwhich
**Linguagem:** Rust
**Licença:** MIT

#### Características

- **Modern TUI** (terminal user interface)
- **Per-process bandwidth** - mostra qual processo consome o quê
- **Per-connection breakdown** - detalha cada conexão TCP/UDP
- **Per-remote IP/host** - agrupa por destino
- **DNS resolution** - resolve IPs para hostnames
- **Requires root** - precisa de CAP_NET_RAW

#### Features Principais

```
┌─ Total (download / upload) ──────────────────────────┐
│ 1.5 MB/s ↓ | 300 KB/s ↑                              │
└──────────────────────────────────────────────────────┘

┌─ Process ─────────────────────────────────────────────┐
│ Process          Download ↓   Upload ↑   Connection  │
│ firefox          1.2 MB/s     100 KB/s  15 connections│
│ chrome           200 KB/s     50 KB/s   8 connections │
│ spotify          100 KB/s     150 KB/s  2 connections │
└───────────────────────────────────────────────────────┘

┌─ Remote Address ──────────────────────────────────────┐
│ Remote                      Download ↓   Upload ↑     │
│ youtube.com (142.250.x.x)   800 KB/s    50 KB/s      │
│ github.com (140.82.x.x)     300 KB/s    20 KB/s      │
│ cloudflare.com (104.16.x.x) 200 KB/s    10 KB/s      │
└───────────────────────────────────────────────────────┘

┌─ Connection ──────────────────────────────────────────┐
│ Process    Remote              Protocol  State        │
│ firefox    youtube.com:443     TCP       ESTABLISHED  │
│ firefox    gstatic.com:443     TCP       ESTABLISHED  │
│ chrome     github.com:443      TCP       ESTABLISHED  │
└───────────────────────────────────────────────────────┘
```

#### Instalação e Uso

```bash
# Instalação (Rust)
cargo install bandwhich

# Ou via package manager
sudo apt install bandwhich

# Uso (precisa de root)
sudo bandwhich

# Com interface específica
sudo bandwhich -i wlan0

# Sem DNS resolution (mais rápido)
sudo bandwhich --no-resolve
```

#### Casos de Uso para Nosso Dashboard

**Inspirações:**
1. **Process-level tracking** - identificar qual app usa banda
2. **Connection table** - mostrar conexões ativas
3. **Remote host grouping** - agrupar por destino
4. **Real-time updates** - atualização suave

**Implementação Python Equivalente:**

```python
# Usando psutil + scapy
import psutil
from collections import defaultdict

def get_process_bandwidth():
    """Retorna bandwidth por processo"""
    connections = psutil.net_connections(kind='inet')
    process_bandwidth = defaultdict(lambda: {'sent': 0, 'recv': 0})

    for conn in connections:
        if conn.status == 'ESTABLISHED':
            try:
                proc = psutil.Process(conn.pid)
                io = proc.io_counters()
                process_bandwidth[proc.name()]['sent'] += io.write_bytes
                process_bandwidth[proc.name()]['recv'] += io.read_bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    return dict(process_bandwidth)
```

---

<a name="nethogs"></a>
### 2.2 NETHOGS

**GitHub:** https://github.com/raboof/nethogs
**Linguagem:** C++
**Licença:** GPL-2.0

#### Características

- **Per-process bandwidth monitor** (foco principal)
- **Simple, fast, lightweight**
- **Live sorting** por bandwidth
- **Minimal UI** - apenas essencial
- **Requires root**

#### Interface

```
NetHogs version 0.8.6

  PID USER     PROGRAM                DEV        SENT      RECEIVED
 1234 user     /usr/bin/firefox      wlan0      150.2 KB   1.5 MB
 5678 user     /usr/bin/chrome       wlan0       80.5 KB   500 KB
 9012 user     /usr/bin/spotify      wlan0      200.0 KB   100 KB
 3456 root     /usr/sbin/sshd        eth0         5.2 KB    10 KB

  TOTAL                                          435.9 KB   2.11 MB

m: change view  q: quit  s: sort
```

#### Features Técnicas

- **Packet capture via libpcap**
- **Process matching** via /proc filesystem
- **Sorting modes:**
  - Sent bytes
  - Received bytes
  - Total bytes
- **View modes:**
  - KB/s (kilobytes per second)
  - KB (total kilobytes)
  - B (total bytes)
  - MB (megabytes)

#### Uso

```bash
# Basic
sudo nethogs

# Specific interface
sudo nethogs wlan0

# Multiple interfaces
sudo nethogs wlan0 eth0

# Custom refresh delay (seconds)
sudo nethogs -d 2

# Trace mode (log to file)
sudo nethogs -t > nethogs.log
```

#### Casos de Uso

**Quando usar:**
- Identificar processos que consomem banda
- Debug de bandwidth hogs
- Monitoring simples e rápido
- Sistemas com poucos recursos

**Limitações:**
- Não mostra conexões individuais
- UI muito básica
- Sem gráficos históricos

---

<a name="iftop"></a>
### 2.3 IFTOP

**Website:** http://www.ex-parrot.com/~pdw/iftop/
**Linguagem:** C
**Licença:** GPL-2.0

#### Características

- **Interface-level monitoring** (eth0, wlan0, etc.)
- **Connection-based view** - mostra pares (source → dest)
- **Historical bars** - mini-gráficos de tendência
- **DNS resolution** com cache
- **Port display** opcional
- **Requires root**

#### Interface

```
                     19.5Mb          39.0Mb          58.6Mb    78.1Mb
└───────────────────┴───────────────┴───────────────┴─────────────
192.168.1.100      => 142.250.200.78   1.2Mb  800kb  1.5Mb
                   <=                   500kb 300kb  600kb

192.168.1.100      => 140.82.121.4     800kb  600kb  900kb
                   <=                   200kb 150kb  250kb

192.168.1.100      => 104.16.132.229   400kb  300kb  500kb
                   <=                   100kb  80kb  120kb

──────────────────────────────────────────────────────────────
TX:             cum:   5.2GB   peak:  15.2Mb  rates:  2.4Mb 1.7Mb 2.9Mb
RX:                   12.8GB          25.8Mb          800kb 530kb 970kb
TOTAL:                18.0GB          41.0Mb          3.2Mb 2.2Mb 3.9Mb
```

#### Features Avançadas

**Filtros BPF:**
```bash
# Apenas HTTP/HTTPS
sudo iftop -f 'port 80 or port 443'

# Apenas tráfego para/de IP específico
sudo iftop -f 'host 192.168.1.50'

# Apenas TCP
sudo iftop -f 'tcp'
```

**Teclas de Controle:**
- `n` - toggle DNS resolution
- `p` - toggle port display
- `P` - pause display
- `t` - toggle text/bar mode
- `1/2/3` - sort by 2s/10s/40s average
- `</>` - sort by source/dest
- `s/d` - toggle source/dest display
- `b` - toggle bar graph

#### Configuração (.iftoprc)

```bash
# ~/.iftoprc

dns-resolution: yes
port-resolution: yes
show-bars: yes
promiscuous: no
port-display: on
hide-source: no
hide-destination: no
use-bytes: no
sort: 2s
line-display: two-line
show-totals: yes
```

#### Uso Avançado

```bash
# Monitor wlan0 com filtro
sudo iftop -i wlan0 -f 'not port 22'

# Sem DNS (mais rápido)
sudo iftop -n

# Mostra portas
sudo iftop -P

# Modo texto (útil para scripts)
sudo iftop -t -s 5 > network_log.txt
```

---

<a name="vnstat"></a>
### 2.4 VNSTAT

**GitHub:** https://github.com/vergoh/vnstat
**Linguagem:** C
**Licença:** GPL-2.0

#### Características

- **Historical traffic statistics** (não real-time)
- **Database-backed** - mantém histórico
- **Very lightweight** - daemon consome ~1MB RAM
- **Multiple time scales** - hourly, daily, monthly, yearly
- **Does NOT require root** para consultas
- **Long-term trending**

#### Interface (CLI)

```bash
$ vnstat

Database updated: 2025-11-09 11:30:00

   wlan0 since 2025-01-01

          rx:  142.50 GiB      tx:  45.80 GiB      total:  188.30 GiB

                     rx      |     tx      |    total    |   avg. rate
    ------------------------+-------------+-------------+---------------
      today      1.20 GiB |   380 MiB   |    1.58 GiB |  158.23 kbit/s
  yesterday      2.50 GiB |   800 MiB   |    3.30 GiB |  313.45 kbit/s
   this month   45.80 GiB |  12.50 GiB  |   58.30 GiB |  195.67 kbit/s
  last month   38.20 GiB |  10.20 GiB  |   48.40 GiB |  168.92 kbit/s

       top day: 2025-10-15    5.2 GiB
```

#### Hourly Stats

```bash
$ vnstat -h

 wlan0  /  hourly

        hour        rx      |     tx      |    total
    ------------------------+-------------+------------
     10:00       120 MiB   |    50 MiB   |   170 MiB
     11:00       150 MiB   |    60 MiB   |   210 MiB
     12:00       200 MiB   |    80 MiB   |   280 MiB
     13:00       180 MiB   |    70 MiB   |   250 MiB
     14:00       160 MiB   |    65 MiB   |   225 MiB
```

#### Live Mode (Real-time)

```bash
$ vnstat -l

Monitoring wlan0...    (press CTRL-C to stop)

   rx:      1.2 Mbit/s     5 p/s          tx:    500 kbit/s     3 p/s
```

#### Gráfico (ASCII)

```bash
$ vnstat -g

 wlan0 / monthly
                               rx      |     tx

   2025-01 ████████░░  35 GiB | ██████░░░░  12 GiB
   2025-02 ██████████  42 GiB | ████████░░  15 GiB
   2025-03 ████████░░  38 GiB | ██████░░░░  13 GiB
   2025-04 █████░░░░░  28 GiB | ████░░░░░░   9 GiB
   2025-05 ███████░░░  32 GiB | ██████░░░░  11 GiB
   2025-06 ██████████  45 GiB | ████████░░  16 GiB
```

#### Configuração

```bash
# /etc/vnstat.conf

# Database location
DatabaseDir "/var/lib/vnstat"

# Update interval (seconds)
UpdateInterval 30

# Daemon user
DaemonUser "vnstat"

# Interface-specific settings
MaxBandwidth 1000    # Mbit

# How long to keep data
MonthRotate 12       # 12 months
DayRotate 30         # 30 days
HourRotate 24        # 24 hours
```

#### Casos de Uso

**Ideal para:**
- Monitorar quota de banda mensal
- Trending de longo prazo
- Identificar picos de uso
- Relatórios históricos
- Sistemas com dados limitados (mobile hotspot, etc.)

**Não ideal para:**
- Monitoring em tempo real
- Per-process tracking
- Per-connection details

#### Integração com Dashboard

```python
import subprocess
import json

def get_vnstat_data(interface='wlan0'):
    """Obtém dados do vnstat em JSON"""
    result = subprocess.run(
        ['vnstat', '-i', interface, '--json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def get_today_traffic():
    """Retorna tráfego de hoje"""
    data = get_vnstat_data()
    today = data['interfaces'][0]['traffic']['day'][0]
    return {
        'rx_gb': today['rx'] / 1024**3,
        'tx_gb': today['tx'] / 1024**3,
        'total_gb': (today['rx'] + today['tx']) / 1024**3
    }
```

---

<a name="slurm"></a>
### 2.5 SLURM

**GitHub:** https://github.com/mattthias/slurm
**Linguagem:** C
**Licença:** GPL-2.0

#### Características

- **Simple visual bandwidth monitor**
- **ASCII graph in real-time**
- **Dual-line display** (TX/RX separados)
- **Color-coded** (green RX, red TX)
- **No dependencies** além de ncurses
- **Lightweight**

#### Interface

```
Interface: wlan0

Download (RX):  1.5 Mbit/s
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄

Upload (TX):    500 kbit/s
  ▁▁▂▂▃▃▄▄▅▅▆▆▇▇██▇▇▆▆▅▅▄▄▃▃▂▂▁▁▂▂▃▃▄▄▅▅

Total: 2.0 Mbit/s  Peak RX: 5.2 Mbit/s  Peak TX: 2.1 Mbit/s
```

#### Uso

```bash
# Monitor default interface
slurm

# Specific interface
slurm -i wlan0

# Custom refresh interval (100ms default)
slurm -d 500

# Monochrome mode
slurm -m

# Classic mode (without color)
slurm -c
```

#### Teclas

- `q` - quit
- `l` - toggle TX/RX labels
- `c` - cycle color modes
- `r` - reset peak values

#### Casos de Uso

- **Quick glance** em bandwidth
- **Visual trending** simples
- **Debugging** de conexões intermitentes
- **Lightweight monitoring** em servidores

---

<a name="comparativo-tools"></a>
### 2.6 COMPARATIVO TÉCNICO

| Feature | bandwhich | nethogs | iftop | vnstat | slurm |
|---------|-----------|---------|-------|--------|-------|
| **Per-Process** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Per-Connection** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Historical Data** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Real-time Graph** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **DNS Resolution** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Requires Root** | ✅ | ✅ | ✅ | ❌ (consulta) | ❌ |
| **Resource Usage** | Médio | Baixo | Médio | Muito Baixo | Muito Baixo |
| **Modern UI** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Filtering** | ✅ | ❌ | ✅ (BPF) | ❌ | ❌ |

#### Recomendações de Uso

**bandwhich:**
- Análise detalhada de processos
- Identificar "bandwidth hogs"
- Debugging de aplicações

**nethogs:**
- Monitoramento rápido per-process
- Sistemas com poucos recursos
- Uso casual/administrativo

**iftop:**
- Análise de conexões
- Debugging de rede
- Visualizar pares source/dest

**vnstat:**
- Tracking de quota mensal
- Histórico de longo prazo
- Relatórios e trending

**slurm:**
- Quick glance visual
- Monitoramento passivo
- Terminal secundário sempre aberto

---

<a name="implementacao"></a>
## 3. IMPLEMENTAÇÃO PRÁTICA

<a name="python-sampler"></a>
### 3.1 REPLICANDO SAMPLER EM PYTHON/RICH

#### Arquitetura Base

```python
# sampler_clone/config.py

from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml

@dataclass
class Position:
    x: int
    y: int
    width: int
    height: int

@dataclass
class ComponentConfig:
    title: str
    position: Position
    rate_ms: int
    sample: str
    color: Optional[str] = None

@dataclass
class RunchartConfig(ComponentConfig):
    items: List[Dict]
    scale: int = 2
    legend: bool = True

@dataclass
class SamplerConfig:
    variables: Dict[str, str]
    runcharts: List[RunchartConfig]
    # ... outros componentes

def load_config(yaml_path: str) -> SamplerConfig:
    """Carrega e valida configuração YAML"""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    # Parsing e validação
    # ...
    return SamplerConfig(...)
```

#### Component Base Class

```python
# sampler_clone/component.py

from abc import ABC, abstractmethod
from rich.console import RenderableType
import subprocess
import time

class Component(ABC):
    """Classe base para componentes Sampler"""

    def __init__(self, config: ComponentConfig):
        self.config = config
        self.last_update = 0
        self.data = []

    def should_update(self) -> bool:
        """Verifica se é hora de atualizar"""
        now = time.time() * 1000  # ms
        if now - self.last_update >= self.config.rate_ms:
            self.last_update = now
            return True
        return False

    def execute_sample(self) -> str:
        """Executa comando shell e retorna output"""
        result = subprocess.run(
            self.config.sample,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()

    @abstractmethod
    def update(self):
        """Atualiza dados do componente"""
        pass

    @abstractmethod
    def render(self) -> RenderableType:
        """Renderiza componente para Rich"""
        pass
```

#### Runchart Implementation

```python
# sampler_clone/runchart.py

from .component import Component
from rich.panel import Panel
from rich.text import Text
from collections import deque
import plotext as plt

class Runchart(Component):
    """Implementação de line chart"""

    def __init__(self, config: RunchartConfig):
        super().__init__(config)
        self.series = {
            item['label']: deque(maxlen=60)  # 60 pontos
            for item in config.items
        }
        self.current_values = {}

    def update(self):
        """Atualiza dados executando samples"""
        for item in self.config.items:
            try:
                # Executa comando
                result = subprocess.run(
                    item['sample'],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=2
                )

                # Parse valor (assume float)
                value = float(result.stdout.strip())

                # Armazena
                label = item['label']
                self.series[label].append(value)
                self.current_values[label] = value

            except (ValueError, subprocess.TimeoutExpired) as e:
                # Log error, use 0
                self.series[label].append(0)

    def render(self) -> Panel:
        """Renderiza gráfico usando plotext"""

        # Configura plotext
        plt.clf()
        plt.plotsize(
            self.config.position.width - 4,
            self.config.position.height - 4
        )

        # Plota cada série
        for item in self.config.items:
            label = item['label']
            data = list(self.series[label])

            if data:
                x = list(range(len(data)))
                plt.plot(
                    x, data,
                    label=label,
                    color=item.get('color', 'cyan'),
                    marker='braille'
                )

        plt.theme('dark')
        plt.xlabel('Time')
        plt.ylabel('Value')

        # Gera chart
        chart_str = plt.build()
        chart_text = Text.from_ansi(chart_str)

        # Adiciona legenda
        if self.config.legend:
            legend = Text("\n")
            for label, value in self.current_values.items():
                legend.append(f"{label}: {value:.1f}  ", style="cyan")
            chart_text.append(legend)

        return Panel(
            chart_text,
            title=self.config.title,
            border_style=self.config.color or 'cyan'
        )
```

#### Main Loop

```python
# sampler_clone/main.py

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
import time

class SamplerDashboard:
    """Dashboard Sampler-like em Python"""

    def __init__(self, config: SamplerConfig):
        self.config = config
        self.console = Console()
        self.components = []

        # Inicializa componentes
        self._init_components()

    def _init_components(self):
        """Cria instâncias de componentes"""
        for rc_config in self.config.runcharts:
            self.components.append(Runchart(rc_config))

        # ... outros tipos de componentes

    def _create_layout(self) -> Layout:
        """Cria layout baseado em posições"""
        layout = Layout()

        # Grid absoluto baseado em posições
        # (implementação simplificada - na real precisa de grid system)

        for comp in self.components:
            pos = comp.config.position
            # Adiciona componente no layout
            # ...

        return layout

    def run(self):
        """Loop principal"""
        layout = self._create_layout()

        with Live(
            layout,
            console=self.console,
            screen=True,
            refresh_per_second=10
        ) as live:

            while True:
                try:
                    # Atualiza componentes que precisam
                    for comp in self.components:
                        if comp.should_update():
                            comp.update()

                    # Re-renderiza layout
                    layout = self._create_layout()
                    live.update(layout)

                    time.sleep(0.1)

                except KeyboardInterrupt:
                    break

def main():
    # Carrega config
    config = load_config('sampler-config.yml')

    # Cria dashboard
    dashboard = SamplerDashboard(config)

    # Executa
    dashboard.run()
```

---

<a name="integracao-tools"></a>
### 3.2 INTEGRANDO NETWORK TOOLS

#### Wrapper para bandwhich

```python
# network_tools/bandwhich_wrapper.py

import subprocess
import json
import re

class BandwhichWrapper:
    """Wrapper para bandwhich (parsing de output)"""

    @staticmethod
    def get_process_bandwidth(interface='wlan0'):
        """
        Retorna bandwidth por processo

        Nota: bandwhich não tem JSON output, precisa parsear text
        Alternativa: usar psutil + scapy
        """
        # bandwhich não tem modo batch/JSON
        # Implementação alternativa com psutil:

        import psutil
        from collections import defaultdict

        # Snapshot inicial
        io_initial = {}
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                io_initial[proc.pid] = proc.io_counters()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Aguarda intervalo
        time.sleep(1)

        # Snapshot final
        bandwidth = {}
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.pid in io_initial:
                    io_final = proc.io_counters()
                    io_init = io_initial[proc.pid]

                    sent_bps = io_final.write_bytes - io_init.write_bytes
                    recv_bps = io_final.read_bytes - io_init.read_bytes

                    bandwidth[proc.info['name']] = {
                        'sent_bps': sent_bps,
                        'recv_bps': recv_bps,
                        'total_bps': sent_bps + recv_bps
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return bandwidth
```

#### Wrapper para vnstat

```python
# network_tools/vnstat_wrapper.py

import subprocess
import json

class VnstatWrapper:
    """Wrapper para vnstat (usa --json)"""

    @staticmethod
    def get_interface_data(interface='wlan0'):
        """Retorna dados do vnstat em formato estruturado"""
        result = subprocess.run(
            ['vnstat', '-i', interface, '--json'],
            capture_output=True,
            text=True
        )

        data = json.loads(result.stdout)
        return data['interfaces'][0]

    @staticmethod
    def get_today_traffic(interface='wlan0'):
        """Retorna tráfego de hoje"""
        data = VnstatWrapper.get_interface_data(interface)

        # Primeiro dia no array é hoje
        today = data['traffic']['day'][0]

        return {
            'rx_bytes': today['rx'],
            'tx_bytes': today['tx'],
            'rx_gb': today['rx'] / (1024**3),
            'tx_gb': today['tx'] / (1024**3),
            'total_gb': (today['rx'] + today['tx']) / (1024**3),
            'date': today['date']
        }

    @staticmethod
    def get_hourly_traffic(interface='wlan0', hours=24):
        """Retorna tráfego das últimas N horas"""
        data = VnstatWrapper.get_interface_data(interface)

        hourly = data['traffic']['hour'][:hours]

        return [
            {
                'hour': h['time']['hour'],
                'rx_mb': h['rx'] / (1024**2),
                'tx_mb': h['tx'] / (1024**2)
            }
            for h in hourly
        ]
```

---

## 📚 CONCLUSÃO DA PARTE 1

Nesta primeira parte cobrimos:

✅ **Sampler completo:**
- Arquitetura e design
- 6 componentes visuais (Runchart, Sparkline, Barchart, Gauge, Textbox, Asciibox)
- Sistema de configuração YAML
- Triggers e alertas
- Interactive shells
- Best practices

✅ **Network Monitoring Tools:**
- bandwhich (per-process, modern UI)
- nethogs (per-process, simples)
- iftop (per-connection, BPF filters)
- vnstat (historical, lightweight)
- slurm (visual, real-time graph)
- Comparativo técnico completo

✅ **Implementação Prática:**
- Como replicar Sampler em Python/Rich
- Wrappers para integrar tools existentes

---

**PRÓXIMA PARTE:** RESEARCH_PART2_PACKET_ANALYSIS.md

Conteúdo:
- tshark, scapy, tcpdump (análise profunda)
- Wireshark display filters
- System monitors (btop++, bottom, gtop)
- Bandwidth calculation e metrics
- WiFi monitoring tools

---

**Juan-Dev - Soli Deo Gloria ✝️**
