# 🔬 SAMPLER DEEP DIVE - Análise Completa e Guia de Implementação

**Projeto:** WiFi Security Education Dashboard v2.0
**Autor:** Juan-Dev - Soli Deo Gloria ✝️
**Data:** 2025-11-09
**Propósito:** Deep dive completo no Sampler com 20+ exemplos YAML e estratégias de replicação em Python/Rich

---

## 📑 Índice

1. [Visão Geral do Sampler](#1-visão-geral-do-sampler)
2. [Arquitetura Interna Detalhada](#2-arquitetura-interna-detalhada)
3. [Estrutura YAML Completa](#3-estrutura-yaml-completa)
4. [Componentes - Análise Detalhada](#4-componentes---análise-detalhada)
5. [Sistema de Triggers e Alertas](#5-sistema-de-triggers-e-alertas)
6. [Interactive Shells](#6-interactive-shells)
7. [Replicação em Python/Rich](#7-replicação-em-pythonrich)
8. [Padrões Avançados](#8-padrões-avançados)
9. [Best Practices & Anti-patterns](#9-best-practices--anti-patterns)
10. [Estratégia de Implementação](#10-estratégia-de-implementação)

---

## 1. Visão Geral do Sampler

### 1.1 O que é Sampler?

**Sampler** é uma ferramenta de **visualização de dados em tempo real no terminal** desenvolvida em Go. Sua filosofia central é:

> **"Script anything, visualize in a sophisticated way"**

### 1.2 Características Distintivas

| Característica | Descrição |
|----------------|-----------|
| **Configuração declarativa** | YAML puro - zero código Go necessário |
| **Componentes modulares** | 6 tipos de componentes visuais reutilizáveis |
| **Rate-based updates** | Cada componente tem seu próprio intervalo de atualização |
| **Trigger system** | Alertas visuais e sonoros baseados em condições |
| **Interactive shells** | Capacidade de executar comandos interativos de dentro do dashboard |
| **Layout flexível** | Grid system responsivo similar a CSS Grid |
| **Zero dependencies** | Binário único e portável |

### 1.3 Filosofia de Design

```
┌─────────────────────────────────────────────────────┐
│                  SAMPLER PHILOSOPHY                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Declarativo > Imperativo                        │
│     - Descreva "o que", não "como"                  │
│                                                     │
│  2. Composição > Herança                            │
│     - Componentes pequenos e combináveis            │
│                                                     │
│  3. Configuração > Código                           │
│     - YAML como linguagem de dashboard              │
│                                                     │
│  4. Reatividade > Polling                           │
│     - Atualizações baseadas em rate, não loops      │
│                                                     │
│  5. Visualização > Logs                             │
│     - Gráficos e métricas > texto puro              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 2. Arquitetura Interna Detalhada

### 2.1 Pipeline de Execução

```
┌──────────────────────────────────────────────────────────────────┐
│                    SAMPLER EXECUTION PIPELINE                    │
└──────────────────────────────────────────────────────────────────┘

1. CONFIG LOADING
   ┌─────────────┐
   │ config.yml  │──┐
   └─────────────┘  │
                    ├──> YAML Parser ──> Validation
   ┌─────────────┐  │                      │
   │ ~/.sampler  │──┘                      ▼
   └─────────────┘                    Config Object

2. COMPONENT INITIALIZATION
   Config Object ──> ComponentFactory
                           │
                           ├──> Runchart instances
                           ├──> Sparkline instances
                           ├──> Barchart instances
                           ├──> Gauge instances
                           ├──> Textbox instances
                           └──> Asciibox instances

3. LAYOUT CALCULATION
   Components ──> Layout Engine ──> Terminal Size
                                         │
                                         ▼
                                    Grid Layout
                                    (x, y, w, h)

4. UPDATE LOOP (Main Goroutine)
   ┌─────────────────────────────────────────────┐
   │  for {                                      │
   │    components.ForEach(func(c Component) {   │
   │      if c.ShouldUpdate() {                  │
   │        go c.Update()  // Goroutine!         │
   │      }                                      │
   │    })                                       │
   │                                             │
   │    render()                                 │
   │    sleep(config.RefreshRate)                │
   │  }                                          │
   └─────────────────────────────────────────────┘

5. RENDER PIPELINE
   Component.Data ──> Renderer ──> TUI Library ──> Terminal
                                    (termui)
```

### 2.2 Estrutura de Componente (Pseudo-código Go)

```go
// Interface base de todos os componentes
type Component interface {
    // Verifica se deve atualizar baseado em rate_ms
    ShouldUpdate() bool

    // Executa o script e atualiza dados
    Update()

    // Renderiza o componente visual
    Render() Drawable

    // Processa triggers após atualização
    CheckTriggers()
}

// Implementação base compartilhada
type BaseComponent struct {
    Config      ComponentConfig
    LastUpdate  time.Time
    Data        interface{}
    Triggers    []Trigger
}

func (c *BaseComponent) ShouldUpdate() bool {
    now := time.Now()
    elapsed := now.Sub(c.LastUpdate)

    return elapsed >= time.Duration(c.Config.RateMs) * time.Millisecond
}

func (c *BaseComponent) Update() {
    // 1. Executa script shell
    output := exec.Command("bash", "-c", c.Config.Sample).CombinedOutput()

    // 2. Processa output baseado no tipo de componente
    c.Data = c.Parse(output)

    // 3. Atualiza timestamp
    c.LastUpdate = time.Now()

    // 4. Verifica triggers
    c.CheckTriggers()
}

// Exemplo de componente específico
type Runchart struct {
    BaseComponent
    Points []Point
    Legend string
}

func (r *Runchart) Parse(output []byte) interface{} {
    value := parseFloat(string(output))

    // Adiciona ponto à série temporal
    r.Points = append(r.Points, Point{
        Time:  time.Now(),
        Value: value,
    })

    // Mantém apenas últimos N pontos baseado em width
    if len(r.Points) > r.Config.Size.Width {
        r.Points = r.Points[1:]
    }

    return r.Points
}

func (r *Runchart) Render() Drawable {
    // Usa termui para criar gráfico de linha
    chart := widgets.NewPlot()
    chart.Data = convertToXY(r.Points)
    chart.LineColors = []Color{r.Config.Color}

    return chart
}
```

### 2.3 Sistema de Rate-Based Updates

**Problema:** Como atualizar múltiplos componentes em diferentes taxas sem criar deadlocks ou race conditions?

**Solução do Sampler:**

```go
// Cada componente tem sua própria goroutine de atualização
type ComponentScheduler struct {
    components []Component
    ticker     *time.Ticker
}

func (s *ComponentScheduler) Start() {
    // Ticker principal (ex: 100ms - a menor rate_ms)
    s.ticker = time.NewTicker(100 * time.Millisecond)

    go func() {
        for range s.ticker.C {
            // Verifica TODOS os componentes a cada tick
            for _, component := range s.components {
                // Cada componente decide se deve atualizar
                if component.ShouldUpdate() {
                    // Atualização assíncrona
                    go component.Update()
                }
            }
        }
    }()
}

// Componente individual com lógica de rate
type SampledComponent struct {
    lastUpdate time.Time
    rateMs     int64
}

func (c *SampledComponent) ShouldUpdate() bool {
    elapsed := time.Since(c.lastUpdate).Milliseconds()
    return elapsed >= c.rateMs
}
```

**Vantagens:**
- ✅ Sem busy-waiting
- ✅ Componentes independentes
- ✅ Fácil adicionar/remover componentes
- ✅ Performance escalável

---

## 3. Estrutura YAML Completa

### 3.1 Anatomia do config.yml

```yaml
# ============================================================================
#                        SAMPLER CONFIG.YML STRUCTURE
# ============================================================================

# 1. VARIÁVEIS GLOBAIS (opcional)
variables:
  # Variáveis de ambiente que podem ser referenciadas em scripts
  monitoring_interval: 1000
  alert_threshold: 80
  log_path: /var/log/app.log

  # Podem ser usadas como: $monitoring_interval, $alert_threshold

# 2. CONFIGURAÇÕES GLOBAIS (opcional)
refresh_rate_ms: 100  # Taxa de refresh do UI (não dos componentes!)
theme: dark           # dark | light

# 3. RUNBOOKS (opcional)
# Comandos interativos que podem ser invocados via hotkeys
runbooks:
  - title: Restart Nginx
    key: r
    command: sudo systemctl restart nginx

  - title: Clear Cache
    key: c
    command: rm -rf /tmp/cache/*

# 4. COMPONENTES (obrigatório)
# Lista de todos os componentes a serem exibidos
runcharts:
  - title: CPU Usage
    position:
      x: 0
      y: 0
      width: 20
      height: 10
    rate-ms: 1000
    sample: echo "scale=2; $(ps aux | awk '{sum+=$3} END {print sum}')"
    color: 178  # Cor ANSI
    legend:
      enabled: true
      details: false
    triggers:
      - title: High CPU
        condition: echo "$sample > 80" | bc -l
        actions:
          terminal-bell: true
          sound: true
          visual: true

sparklines:
  - title: Memory %
    position: {x: 20, y: 0, width: 20, height: 5}
    rate-ms: 2000
    sample: free | grep Mem | awk '{print ($3/$2) * 100.0}'

barcharts:
  - title: Disk Usage
    position: {x: 0, y: 10, width: 30, height: 10}
    rate-ms: 5000
    sample: df -h | awk 'NR>1 {print $6 ":" $5}' | sed 's/%//'

gauges:
  - title: Network Latency
    position: {x: 40, y: 0, width: 20, height: 10}
    rate-ms: 1000
    sample: ping -c 1 8.8.8.8 | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}'
    min: 0
    max: 100
    cur:
      color: 2  # Verde

textboxes:
  - title: System Info
    position: {x: 0, y: 20, width: 40, height: 5}
    rate-ms: 10000
    sample: uname -a
    color: 7  # Branco

asciiboxes:
  - title: Logo
    position: {x: 40, y: 20, width: 20, height: 10}
    rate-ms: 0  # Estático
    sample: cat /etc/motd
    color: 6  # Ciano
```

### 3.2 Sistema de Coordenadas e Layout

```
Terminal: 120x40 caracteres

   X: 0                                              X: 120
   ┌──────────────────────────────────────────────────────┐
Y:0│  ┌──────────────┐ ┌──────────────┐                  │
   │  │  Runchart    │ │  Sparkline   │                  │
   │  │  (0,0,20,10) │ │  (20,0,20,5) │                  │
   │  │              │ └──────────────┘                  │
   │  │              │                                    │
   │  │              │ ┌──────────────┐                  │
   │  │              │ │   Gauge      │                  │
   │  └──────────────┘ │  (20,5,20,5) │                  │
   │                   └──────────────┘                  │
   │  ┌───────────────────────────────┐                  │
   │  │        Barchart               │                  │
   │  │        (0,10,40,10)           │                  │
   │  │                               │                  │
   │  └───────────────────────────────┘                  │
   │                                                      │
Y:40└──────────────────────────────────────────────────────┘

Coordenadas: (x, y, width, height)
- x: Coluna inicial (0-based)
- y: Linha inicial (0-based)
- width: Largura em caracteres
- height: Altura em linhas
```

### 3.3 Sistema de Cores

```yaml
# Sampler usa ANSI 256 colors
# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit

# Cores básicas (0-15)
color: 0   # Preto
color: 1   # Vermelho
color: 2   # Verde
color: 3   # Amarelo
color: 4   # Azul
color: 5   # Magenta
color: 6   # Ciano
color: 7   # Branco
color: 8   # Cinza
color: 9   # Vermelho brilhante
color: 10  # Verde brilhante
# ... até 15

# Extended colors (16-255)
color: 178  # Laranja dourado (usado em exemplos Sampler)
color: 214  # Laranja
color: 220  # Amarelo ouro
color: 196  # Vermelho forte

# Mapeamento para Rich (Python)
# Rich aceita:
# - Nomes: "red", "green", "blue"
# - Hex: "#FF5733"
# - RGB: "rgb(255,87,51)"
# - ANSI: Precisa converter via tabela

# Tabela de conversão ANSI → Rich
ansi_to_rich = {
    0: "black",
    1: "red",
    2: "green",
    3: "yellow",
    4: "blue",
    5: "magenta",
    6: "cyan",
    7: "white",
    178: "#D7AF00",  # Dourado
    214: "#FFAF00",  # Laranja
    # ...
}
```

---

## 4. Componentes - Análise Detalhada

### 4.1 RUNCHART - Gráfico de Linha Temporal

**Propósito:** Visualizar séries temporais (valores numéricos ao longo do tempo)

#### Exemplo 1: CPU Usage Básico

```yaml
runcharts:
  - title: CPU Usage %
    position:
      x: 0
      y: 0
      width: 40
      height: 10
    rate-ms: 1000  # Atualiza a cada 1 segundo
    scale: 0       # Auto-scale (ajusta Y automaticamente)

    # Script que retorna um número
    sample: ps aux | awk '{sum+=$3} END {print sum}'

    color: 178  # Dourado

    legend:
      enabled: true   # Mostra legenda
      details: false  # Não mostra min/max/avg
```

**Output visual:**
```
┌─ CPU Usage % ──────────────────────────────────┐
│                                          ╭─╮   │
│                                      ╭───╯ ╰─╮ │
│                                  ╭───╯        │ │
│                              ╭───╯            │ │
│                          ╭───╯                │ │
│                      ╭───╯                    │ │
│                  ╭───╯                        │ │
│              ╭───╯                            │ │
│          ╭───╯                                │ │
│ ╭────────╯                                    │ │
└────────────────────────────────────────────────┘
  Current: 45.2%
```

#### Exemplo 2: Network Throughput com Múltiplas Linhas

```yaml
runcharts:
  - title: Network Throughput (Mbps)
    position: {x: 0, y: 0, width: 60, height: 15}
    rate-ms: 500
    scale: 2  # Escala fixa 0-2 Mbps

    # Script que retorna múltiplos valores separados por espaço
    # Formato: <valor_linha1> <valor_linha2> ...
    sample: |
      RX=$(cat /sys/class/net/wlan0/statistics/rx_bytes)
      TX=$(cat /sys/class/net/wlan0/statistics/tx_bytes)
      sleep 0.5
      RX2=$(cat /sys/class/net/wlan0/statistics/rx_bytes)
      TX2=$(cat /sys/class/net/wlan0/statistics/tx_bytes)

      RX_RATE=$(echo "scale=2; ($RX2 - $RX) * 8 / 1024 / 1024 / 0.5" | bc)
      TX_RATE=$(echo "scale=2; ($TX2 - $TX) * 8 / 1024 / 1024 / 0.5" | bc)

      echo "$RX_RATE $TX_RATE"

    # Múltiplas linhas - uma por valor retornado
    color: 2     # Verde (RX)
    color: 1     # Vermelho (TX)

    legend:
      enabled: true
      details: true  # Mostra estatísticas
```

**Output visual:**
```
┌─ Network Throughput (Mbps) ────────────────────────────────────────┐
│ 2.0                                                        ╭───RX  │
│     ╭╮                                              ╭──────╯       │
│ 1.5 │╰╮                                         ╭───╯              │
│     │ ╰╮                                    ╭───╯                  │
│ 1.0 │  ╰╮                               ╭───╯                      │
│     │   ╰╮                          ╭───╯                          │
│ 0.5 │    ╰╮╭╮                   ╭───╯        ╭───TX               │
│     │     ╰╯╰╮              ╭───╯        ╭───╯                     │
│ 0.0 ╰────────╰──────────────╯────────────╯                        │
└─────────────────────────────────────────────────────────────────────┘
  RX: 1.85 Mbps  (min: 0.12  max: 1.95  avg: 1.23)
  TX: 0.42 Mbps  (min: 0.08  max: 0.68  avg: 0.35)
```

#### Exemplo 3: Temperatura com Triggers

```yaml
runcharts:
  - title: CPU Temperature °C
    position: {x: 0, y: 15, width: 40, height: 10}
    rate-ms: 2000
    scale: 2  # 0-100°C

    sample: |
      # Lê temperatura do sensor (Linux)
      cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}'

    color: 2  # Verde por padrão

    triggers:
      # Trigger 1: Warning (>70°C)
      - title: High Temperature Warning
        condition: echo "$sample > 70" | bc -l
        actions:
          terminal-bell: true
          visual: true  # Muda cor do componente

      # Trigger 2: Critical (>85°C)
      - title: Critical Temperature
        condition: echo "$sample > 85" | bc -l
        actions:
          terminal-bell: true
          sound: true
          visual: true
          # Poderia executar comando:
          # command: notify-send "CRITICAL TEMP!" "$sample°C"
```

#### Replicação em Python/Rich

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import plotext as plt
from collections import deque
import subprocess
import time

class Runchart:
    def __init__(self, title, width, height, rate_ms, sample_command, color="#FFD93D"):
        self.title = title
        self.width = width
        self.height = height
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.color = color

        # Buffer circular para dados
        self.data = deque(maxlen=width)
        self.last_update = 0

    def should_update(self):
        now = time.time() * 1000
        return (now - self.last_update) >= self.rate_ms

    def update(self):
        try:
            # Executa comando shell
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse output como float
            value = float(result.stdout.strip())
            self.data.append(value)
            self.last_update = time.time() * 1000

        except Exception as e:
            print(f"Error updating runchart: {e}")

    def render(self):
        if not self.data:
            return Panel("No data", title=self.title)

        # Configura plotext
        plt.clf()
        plt.theme('dark')
        plt.plot_size(self.width - 4, self.height - 4)

        # Plot dados
        x = list(range(len(self.data)))
        y = list(self.data)
        plt.plot(x, y, color=self.color)

        # Labels
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("")  # Título vai no Panel

        # Gera chart string
        chart_str = plt.build()
        chart_text = Text.from_ansi(chart_str)

        # Adiciona legenda
        current = self.data[-1] if self.data else 0
        legend = f"\nCurrent: {current:.2f}"

        return Panel(
            chart_text + Text(legend, style="bright_white"),
            title=self.title,
            border_style=self.color
        )

# Uso
cpu_chart = Runchart(
    title="CPU Usage %",
    width=40,
    height=10,
    rate_ms=1000,
    sample_command="ps aux | awk '{sum+=$3} END {print sum}'",
    color="green"
)

# Loop principal
console = Console()
while True:
    if cpu_chart.should_update():
        cpu_chart.update()

    console.clear()
    console.print(cpu_chart.render())
    time.sleep(0.1)  # 100ms refresh rate
```

---

### 4.2 SPARKLINE - Gráfico Compacto em Linha

**Propósito:** Mostrar tendência de valores em espaço mínimo (caracteres Unicode: ▁▂▃▄▅▆▇█)

#### Exemplo 4: Memory Usage Compacto

```yaml
sparklines:
  - title: Memory %
    position: {x: 40, y: 0, width: 30, height: 5}
    rate-ms: 2000

    sample: free | grep Mem | awk '{printf "%.1f", ($3/$2) * 100.0}'

    color: 178
```

**Output visual:**
```
┌─ Memory % ─────────────────────┐
│ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█  75.3% │
└─────────────────────────────────┘
```

#### Exemplo 5: Múltiplas Métricas Compactas

```yaml
sparklines:
  - title: System Overview
    position: {x: 0, y: 0, width: 60, height: 8}
    rate-ms: 1000

    # Retorna múltiplas linhas (uma sparkline por linha)
    sample: |
      echo "CPU: $(ps aux | awk '{sum+=$3} END {print sum}')"
      echo "MEM: $(free | grep Mem | awk '{printf "%.1f", ($3/$2)*100}')"
      echo "DISK: $(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')"
      echo "NET: $(cat /sys/class/net/wlan0/operstate | grep -q up && echo 100 || echo 0)"

    color: 2
```

**Output visual:**
```
┌─ System Overview ──────────────────────────────────────┐
│ CPU:  ▃▄▅▆▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆  65.2%                     │
│ MEM:  ▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇█▇▇  82.5%                     │
│ DISK: ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  45.0%                     │
│ NET:  ████████████████████  100% (UP)                 │
└─────────────────────────────────────────────────────────┘
```

#### Replicação em Python/Rich

```python
from rich.panel import Panel
from rich.text import Text
from collections import deque

class Sparkline:
    # Caracteres Unicode para sparklines
    SPARKS = "▁▂▃▄▅▆▇█"

    def __init__(self, title, width, rate_ms, sample_command, color="green"):
        self.title = title
        self.width = width
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.color = color

        # Buffer para últimos N valores
        self.data = deque(maxlen=width - 10)  # Reserva espaço para texto
        self.last_update = 0
        self.current_value = 0

    def update(self):
        try:
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            value = float(result.stdout.strip())
            self.data.append(value)
            self.current_value = value
            self.last_update = time.time() * 1000

        except Exception as e:
            pass

    def _value_to_spark(self, value, min_val, max_val):
        """Converte valor numérico para caractere sparkline"""
        if max_val == min_val:
            return self.SPARKS[4]  # Meio termo

        # Normaliza valor para 0-7 (índices do SPARKS)
        normalized = (value - min_val) / (max_val - min_val)
        index = int(normalized * 7)
        index = max(0, min(7, index))

        return self.SPARKS[index]

    def render(self):
        if not self.data:
            return Panel("No data", title=self.title)

        # Calcula min/max para normalização
        min_val = min(self.data)
        max_val = max(self.data)

        # Converte cada valor para caractere spark
        sparks = "".join(
            self._value_to_spark(v, min_val, max_val)
            for v in self.data
        )

        # Cria texto colorido
        spark_text = Text(sparks, style=self.color)
        value_text = Text(f"  {self.current_value:.1f}%", style="bright_white")

        content = spark_text + value_text

        return Panel(
            content,
            title=self.title,
            border_style=self.color
        )

# Uso
memory_spark = Sparkline(
    title="Memory %",
    width=30,
    rate_ms=2000,
    sample_command="free | grep Mem | awk '{printf \"%.1f\", ($3/$2)*100}'",
    color="yellow"
)
```

---

### 4.3 BARCHART - Gráfico de Barras

**Propósito:** Comparar valores categóricos

#### Exemplo 6: Disk Usage por Partição

```yaml
barcharts:
  - title: Disk Usage by Partition
    position: {x: 0, y: 10, width: 50, height: 15}
    rate-ms: 5000

    # Formato do output: "label:value" (uma linha por barra)
    sample: df -h | awk 'NR>1 {print $6":"$5}' | sed 's/%//'

    color: 178
    scale: 0  # Auto-scale
```

**Output esperado do script:**
```
/:45
/home:78
/var:62
/tmp:12
```

**Output visual:**
```
┌─ Disk Usage by Partition ────────────────────────┐
│ /        ████████████████░░░░░░░░░░ 45%          │
│ /home    ███████████████████████████░ 78%         │
│ /var     ██████████████████░░░░░░░░░ 62%         │
│ /tmp     ███░░░░░░░░░░░░░░░░░░░░░░░░ 12%         │
└────────────────────────────────────────────────────┘
```

#### Exemplo 7: Top Processos por CPU

```yaml
barcharts:
  - title: Top 5 CPU Consumers
    position: {x: 0, y: 25, width: 60, height: 12}
    rate-ms: 3000

    sample: |
      ps aux --sort=-%cpu | \
      awk 'NR>1 {printf "%s:%.1f\n", $11, $3}' | \
      head -n 5

    color: 1  # Vermelho (alta atenção)
```

**Output visual:**
```
┌─ Top 5 CPU Consumers ───────────────────────────────────┐
│ firefox        ████████████████████████░░ 82.5%         │
│ python3        ███████████████░░░░░░░░░░░ 45.2%         │
│ Xorg           ███████████░░░░░░░░░░░░░░░ 32.8%         │
│ chrome         ████████░░░░░░░░░░░░░░░░░░ 25.1%         │
│ gnome-shell    ████░░░░░░░░░░░░░░░░░░░░░░ 12.3%         │
└──────────────────────────────────────────────────────────┘
```

#### Exemplo 8: Network Connections por Host

```yaml
barcharts:
  - title: Active Connections by Remote Host
    position: {x: 60, y: 10, width: 60, height: 20}
    rate-ms: 2000

    sample: |
      # Lista todas as conexões TCP estabelecidas
      # Agrupa por IP remoto e conta
      netstat -tn 2>/dev/null | \
      grep ESTABLISHED | \
      awk '{print $5}' | \
      sed 's/:[0-9]*$//' | \
      sort | uniq -c | \
      awk '{printf "%s:%d\n", $2, $1}' | \
      head -n 10

    color: 6  # Ciano
```

**Output visual:**
```
┌─ Active Connections by Remote Host ────────────────────┐
│ 142.250.185.46  ████████████████░░░░ 12 conns         │
│ 52.84.221.98    ███████████░░░░░░░░░ 8 conns          │
│ 192.168.1.50    ████████░░░░░░░░░░░░ 6 conns          │
│ 13.107.42.14    █████░░░░░░░░░░░░░░░ 4 conns          │
│ 104.26.12.173   ███░░░░░░░░░░░░░░░░░ 3 conns          │
└─────────────────────────────────────────────────────────┘
```

#### Replicação em Python/Rich

```python
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text

class Barchart:
    def __init__(self, title, width, height, rate_ms, sample_command, color="yellow"):
        self.title = title
        self.width = width
        self.height = height
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.color = color

        self.data = {}  # {label: value}
        self.last_update = 0

    def update(self):
        try:
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse output "label:value"
            self.data = {}
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    label, value = line.split(':', 1)
                    self.data[label.strip()] = float(value.strip())

            self.last_update = time.time() * 1000

        except Exception as e:
            pass

    def render(self):
        if not self.data:
            return Panel("No data", title=self.title)

        # Encontra valor máximo para escala
        max_value = max(self.data.values()) if self.data else 100

        # Cria conteúdo com barras
        content = Text()
        bar_width = self.width - 25  # Espaço para label e valor

        for label, value in self.data.items():
            # Calcula quantos caracteres █ mostrar
            filled = int((value / max_value) * bar_width)
            empty = bar_width - filled

            # Cria barra
            bar = "█" * filled + "░" * empty

            # Formata linha
            line = f"{label:15} {bar} {value:.1f}%\n"
            content.append(line)

        return Panel(
            content,
            title=self.title,
            border_style=self.color
        )

# Alternativa usando Rich Progress
class BarchartRichProgress:
    def __init__(self, title, width, height, rate_ms, sample_command):
        self.title = title
        self.width = width
        self.height = height
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.data = {}
        self.last_update = 0

    def update(self):
        # Mesmo código de parse
        pass

    def render(self):
        if not self.data:
            return Panel("No data", title=self.title)

        max_value = max(self.data.values()) if self.data else 100

        # Usa Rich Table + Progress Bars
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", width=15)
        table.add_column("Bar", width=self.width - 30)
        table.add_column("Value", width=10, justify="right")

        for label, value in self.data.items():
            # Cria barra de progresso
            bar_width = int((value / max_value) * (self.width - 30))
            bar = "█" * bar_width

            table.add_row(
                label,
                Text(bar, style="yellow"),
                f"{value:.1f}%"
            )

        return Panel(table, title=self.title, border_style="yellow")
```

---

### 4.4 GAUGE - Medidor (Tipo Velocímetro)

**Propósito:** Mostrar valor único com visualização de "velocímetro"

#### Exemplo 9: Network Latency Gauge

```yaml
gauges:
  - title: Ping Latency to 8.8.8.8
    position: {x: 60, y: 0, width: 30, height: 10}
    rate-ms: 1000

    sample: ping -c 1 8.8.8.8 | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}'

    min: 0
    max: 100  # ms

    # Configuração de cores por faixa
    cur:
      color: 2  # Verde (padrão)

    triggers:
      - title: High Latency
        condition: echo "$sample > 50" | bc -l
        actions:
          visual: true  # Muda cor para amarelo

      - title: Critical Latency
        condition: echo "$sample > 80" | bc -l
        actions:
          visual: true  # Muda cor para vermelho
          terminal-bell: true
```

**Output visual:**
```
┌─ Ping Latency to 8.8.8.8 ──┐
│                             │
│        ╭───────╮            │
│      ╱           ╲          │
│    ╱      35ms    ╲         │
│   │         ↑      │        │
│   │    ╭────┼────╮ │        │
│    ╲   │ ░░█│░░░ │╱         │
│      ╲ ╰────┴────╯          │
│        ╰───────╯            │
│   0ms            100ms      │
└─────────────────────────────┘
```

#### Exemplo 10: CPU Temperature Gauge

```yaml
gauges:
  - title: CPU Temp
    position: {x: 90, y: 0, width: 30, height: 10}
    rate-ms: 2000

    sample: cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}'

    min: 30
    max: 100

    cur:
      color: 2  # Verde

    triggers:
      - condition: echo "$sample > 70" | bc -l
        actions:
          visual: true  # Amarelo

      - condition: echo "$sample > 85" | bc -l
        actions:
          visual: true  # Vermelho
          sound: true
```

#### Exemplo 11: Battery Level Gauge

```yaml
gauges:
  - title: Battery
    position: {x: 0, y: 30, width: 25, height: 8}
    rate-ms: 10000

    sample: |
      # Linux
      cat /sys/class/power_supply/BAT0/capacity

      # macOS
      # pmset -g batt | grep -Eo "\d+%" | sed 's/%//'

    min: 0
    max: 100

    cur:
      color: 2  # Verde quando >20%

    triggers:
      - title: Low Battery
        condition: echo "$sample < 20" | bc -l
        actions:
          visual: true  # Amarelo

      - title: Critical Battery
        condition: echo "$sample < 10" | bc -l
        actions:
          visual: true  # Vermelho
          terminal-bell: true
          command: notify-send "Critical Battery!" "$sample%"
```

#### Replicação em Python/Rich

```python
from rich.panel import Panel
from rich.text import Text
import math

class Gauge:
    def __init__(self, title, width, height, rate_ms, sample_command,
                 min_val=0, max_val=100, color="green"):
        self.title = title
        self.width = width
        self.height = height
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.min_val = min_val
        self.max_val = max_val
        self.color = color

        self.current_value = 0
        self.last_update = 0

    def update(self):
        try:
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            self.current_value = float(result.stdout.strip())
            self.last_update = time.time() * 1000

        except Exception as e:
            pass

    def render(self):
        # Normaliza valor para 0-1
        normalized = (self.current_value - self.min_val) / (self.max_val - self.min_val)
        normalized = max(0, min(1, normalized))

        # Cria representação visual simples
        # Barra de progresso circular-ish
        bar_width = self.width - 10
        filled = int(normalized * bar_width)
        empty = bar_width - filled

        gauge_visual = "█" * filled + "░" * empty

        # Adiciona labels
        content = Text()
        content.append(f"\n  {self.min_val}", style="dim")
        content.append(" " * (bar_width - 5))
        content.append(f"{self.max_val}\n\n", style="dim")
        content.append(f"  {gauge_visual}\n\n", style=self.color)
        content.append(f"     {self.current_value:.1f}", style="bold bright_white")

        return Panel(
            content,
            title=self.title,
            border_style=self.color
        )

# Versão mais sofisticada usando caracteres Unicode
class GaugeAdvanced:
    def render_gauge_arc(self, normalized):
        """
        Renderiza um arco de gauge usando caracteres Unicode
        """
        # Caracteres para desenhar arco
        # ╭ ╮ ╰ ╯ │ ─ ╱ ╲

        # Calcula ângulo (0° = esquerda, 180° = direita)
        angle = normalized * 180

        # Gera visualização ASCII art do gauge
        lines = []
        lines.append("     ╭───────╮     ")
        lines.append("   ╱           ╲   ")
        lines.append("  │             │  ")

        # Desenha ponteiro baseado no ângulo
        if angle < 45:
            pointer = "  │      ↙      │  "
        elif angle < 90:
            pointer = "  │      ↓      │  "
        elif angle < 135:
            pointer = "  │      ↘      │  "
        else:
            pointer = "  │      →      │  "

        lines.append(pointer)
        lines.append("   ╲           ╱   ")
        lines.append("     ╰───────╯     ")

        return "\n".join(lines)

    def render(self):
        normalized = (self.current_value - self.min_val) / (self.max_val - self.min_val)
        normalized = max(0, min(1, normalized))

        gauge_art = self.render_gauge_arc(normalized)

        content = Text.from_markup(gauge_art)
        content.append(f"\n\n  {self.current_value:.1f} / {self.max_val}",
                      style="bold bright_white")

        return Panel(content, title=self.title, border_style=self.color)
```

---

### 4.5 TEXTBOX - Texto Dinâmico

**Propósito:** Exibir texto plano (logs, info, status)

#### Exemplo 12: System Info

```yaml
textboxes:
  - title: System Information
    position: {x: 0, y: 35, width: 60, height: 8}
    rate-ms: 0  # Estático (atualiza apenas uma vez)

    sample: |
      echo "Hostname: $(hostname)"
      echo "Kernel:   $(uname -r)"
      echo "Uptime:   $(uptime -p)"
      echo "Users:    $(who | wc -l)"

    color: 7  # Branco
    border: true
```

**Output visual:**
```
┌─ System Information ────────────────────────────────────┐
│ Hostname: maximus-laptop                                │
│ Kernel:   6.14.0-34-generic                             │
│ Uptime:   up 2 days, 5 hours, 32 minutes                │
│ Users:    2                                              │
└──────────────────────────────────────────────────────────┘
```

#### Exemplo 13: Live Log Tail

```yaml
textboxes:
  - title: Application Logs (last 10 lines)
    position: {x: 60, y: 20, width: 60, height: 20}
    rate-ms: 1000

    sample: tail -n 10 /var/log/myapp.log

    color: 6  # Ciano
    border: true
```

#### Exemplo 14: Git Status

```yaml
textboxes:
  - title: Git Repository Status
    position: {x: 0, y: 0, width: 50, height: 12}
    rate-ms: 5000

    sample: |
      cd /home/user/project
      echo "Branch: $(git branch --show-current)"
      echo "Status:"
      git status --short
      echo ""
      echo "Last commit:"
      git log -1 --oneline

    color: 5  # Magenta
```

#### Exemplo 15: Docker Containers Status

```yaml
textboxes:
  - title: Docker Containers
    position: {x: 50, y: 0, width: 70, height: 15}
    rate-ms: 3000

    sample: |
      echo "=== RUNNING CONTAINERS ==="
      docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
      echo ""
      echo "=== STATS ==="
      echo "Total: $(docker ps -a | wc -l) | Running: $(docker ps | wc -l)"

    color: 4  # Azul
```

#### Replicação em Python/Rich

```python
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

class Textbox:
    def __init__(self, title, width, height, rate_ms, sample_command, color="white"):
        self.title = title
        self.width = width
        self.height = height
        self.rate_ms = rate_ms
        self.sample_command = sample_command
        self.color = color

        self.text_content = ""
        self.last_update = 0

    def update(self):
        try:
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            self.text_content = result.stdout
            self.last_update = time.time() * 1000

        except Exception as e:
            self.text_content = f"Error: {str(e)}"

    def render(self):
        # Limita ao número de linhas disponíveis
        lines = self.text_content.split('\n')
        max_lines = self.height - 2  # Reserva para bordas

        if len(lines) > max_lines:
            lines = lines[-max_lines:]  # Últimas N linhas (tail behavior)

        content = Text("\n".join(lines))

        return Panel(
            content,
            title=self.title,
            border_style=self.color,
            width=self.width,
            height=self.height
        )

# Versão com syntax highlighting (para logs)
class TextboxWithSyntax:
    def render(self):
        from rich.syntax import Syntax

        # Se for código, usa Syntax
        if self.sample_command.endswith('.py'):
            syntax = Syntax(
                self.text_content,
                "python",
                theme="monokai",
                line_numbers=False
            )
            return Panel(syntax, title=self.title, border_style=self.color)

        # Se for log, destaca levels
        content = Text()
        for line in self.text_content.split('\n'):
            if 'ERROR' in line or 'FATAL' in line:
                content.append(line + "\n", style="bold red")
            elif 'WARN' in line:
                content.append(line + "\n", style="bold yellow")
            elif 'INFO' in line:
                content.append(line + "\n", style="blue")
            else:
                content.append(line + "\n")

        return Panel(content, title=self.title, border_style=self.color)
```

---

### 4.6 ASCIIBOX - Arte ASCII Estática

**Propósito:** Exibir arte ASCII (logos, diagramas)

#### Exemplo 16: Logo Estático

```yaml
asciiboxes:
  - title: ""  # Sem título
    position: {x: 0, y: 0, width: 40, height: 12}
    rate-ms: 0  # Estático

    sample: |
      cat << 'EOF'
       __      ___________   ____
       \ \    / /  ____\ \ / /\ \
        \ \  / /| |__   \ V /  \ \
         \ \/ / |  __|   > <   / /
          \  /  | |     / . \ / /
           \/   |_|    /_/ \_/_/

         WiFi Security Dashboard
      EOF

    color: 6  # Ciano
    border: false
```

#### Exemplo 17: Network Topology

```yaml
asciiboxes:
  - title: Network Topology
    position: {x: 80, y: 20, width: 40, height: 20}
    rate-ms: 0

    sample: |
      cat << 'EOF'
              [Internet]
                  │
                  │
              ┌───┴───┐
              │Router │
              │Gateway│
              └───┬───┘
                  │
         ┌────────┼────────┐
         │        │        │
      [PC-1]   [PC-2]   [AP]
                          │
                     ┌────┴────┐
                     │         │
                 [Phone]   [Laptop]
      EOF

    color: 2  # Verde
```

#### Exemplo 18: Dashboard Banner

```yaml
asciiboxes:
  - title: ""
    position: {x: 0, y: 0, width: 120, height: 6}
    rate-ms: 0

    sample: |
      figlet -f slant "WiFi Monitor" | boxes -d stone

    color: 178  # Dourado
    border: false
```

#### Replicação em Python/Rich

```python
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

class Asciibox:
    def __init__(self, title, width, height, sample_command, color="cyan", border=True):
        self.title = title
        self.width = width
        self.height = height
        self.sample_command = sample_command
        self.color = color
        self.border = border

        self.ascii_art = ""
        self.load_art()

    def load_art(self):
        """Carrega arte ASCII uma única vez (rate-ms: 0)"""
        try:
            result = subprocess.run(
                self.sample_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            self.ascii_art = result.stdout
        except Exception as e:
            self.ascii_art = f"Failed to load ASCII art: {e}"

    def render(self):
        content = Text(self.ascii_art, style=self.color)

        # Centraliza arte se couber
        if self.width > len(max(self.ascii_art.split('\n'), key=len)):
            content = Align.center(content)

        if self.border:
            return Panel(
                content,
                title=self.title if self.title else None,
                border_style=self.color,
                width=self.width,
                height=self.height
            )
        else:
            # Sem borda, apenas o texto
            return content

# Uso com pyfiglet
class AsciiboxFiglet:
    def __init__(self, text, font="slant", color="cyan"):
        import pyfiglet

        self.ascii_art = pyfiglet.figlet_format(text, font=font)
        self.color = color

    def render(self):
        return Text(self.ascii_art, style=self.color, justify="center")
```

---

## 5. Sistema de Triggers e Alertas

### 5.1 Anatomia de um Trigger

```yaml
triggers:
  - title: Nome descritivo do alerta

    # Condição: comando shell que retorna 0 (true) ou 1 (false)
    # Variável $sample contém o último valor capturado
    condition: echo "$sample > 80" | bc -l

    # Ações a executar quando condição é verdadeira
    actions:
      # Toca sino do terminal
      terminal-bell: true

      # Toca som do sistema (beep)
      sound: true

      # Muda cor do componente (vermelho)
      visual: true

      # Executa comando arbitrário
      command: notify-send "Alerta!" "CPU: $sample%"
```

### 5.2 Exemplos Avançados de Triggers

#### Exemplo 19: Triggers Múltiplos com Níveis

```yaml
runcharts:
  - title: CPU Usage
    rate-ms: 1000
    sample: ps aux | awk '{sum+=$3} END {print sum}'
    color: 2  # Verde por padrão

    triggers:
      # Nível 1: Warning (70-85%)
      - title: CPU High (Warning)
        condition: |
          VALUE=$sample
          echo "$VALUE > 70 && $VALUE <= 85" | bc -l
        actions:
          visual: true  # Muda para amarelo

      # Nível 2: Critical (85-95%)
      - title: CPU Very High (Critical)
        condition: |
          VALUE=$sample
          echo "$VALUE > 85 && $VALUE <= 95" | bc -l
        actions:
          visual: true  # Muda para laranja
          terminal-bell: true
          command: |
            notify-send -u critical "CPU Critical" "$sample%"

      # Nível 3: Emergency (>95%)
      - title: CPU Emergency
        condition: echo "$sample > 95" | bc -l
        actions:
          visual: true  # Muda para vermelho
          sound: true
          terminal-bell: true
          command: |
            # Loga alerta
            echo "$(date): CPU EMERGENCY $sample%" >> /var/log/alerts.log

            # Notificação desktop
            notify-send -u critical "CPU EMERGENCY!" "$sample% - System may freeze!"

            # Mata processo mais pesado (CUIDADO!)
            # ps aux --sort=-%cpu | awk 'NR==2 {print $2}' | xargs kill -TERM
```

#### Exemplo 20: Trigger com Debounce

```yaml
runcharts:
  - title: Network Latency
    rate-ms: 1000
    sample: ping -c 1 8.8.8.8 | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}'

    triggers:
      # Só alerta se latência > 100ms por 5 segundos consecutivos
      - title: High Latency Sustained
        condition: |
          # Usa arquivo temp para contar ocorrências
          COUNTER_FILE="/tmp/latency_counter"

          if [ $(echo "$sample > 100" | bc -l) -eq 1 ]; then
            # Incrementa contador
            COUNT=$(cat $COUNTER_FILE 2>/dev/null || echo 0)
            COUNT=$((COUNT + 1))
            echo $COUNT > $COUNTER_FILE

            # Trigger após 5 ocorrências (5 segundos)
            [ $COUNT -ge 5 ]
          else
            # Reset contador
            echo 0 > $COUNTER_FILE
            false
          fi
        actions:
          terminal-bell: true
          visual: true
          command: |
            notify-send "Sustained High Latency" "Latency > 100ms for 5 seconds!"
```

#### Exemplo 21: Trigger com Comparação entre Valores

```yaml
runcharts:
  - title: Disk Usage Growth Rate
    rate-ms: 5000
    sample: df -h / | awk 'NR==2 {print $5}' | sed 's/%//'

    triggers:
      # Alerta se cresceu mais de 5% desde último check
      - title: Rapid Disk Growth
        condition: |
          LAST_VALUE_FILE="/tmp/last_disk_value"
          LAST_VALUE=$(cat $LAST_VALUE_FILE 2>/dev/null || echo 0)

          echo $sample > $LAST_VALUE_FILE

          DIFF=$(echo "$sample - $LAST_VALUE" | bc)
          echo "$DIFF > 5" | bc -l
        actions:
          visual: true
          command: |
            notify-send "Rapid Disk Growth!" "Increased ${DIFF}% in 5 seconds"
```

### 5.3 Replicação em Python/Rich

```python
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class TriggerAction:
    terminal_bell: bool = False
    sound: bool = False
    visual: bool = False
    command: Optional[str] = None

@dataclass
class Trigger:
    title: str
    condition: str  # Shell command que retorna 0 (true) ou 1 (false)
    actions: TriggerAction

    # Estado interno para debounce
    trigger_count: int = 0
    last_triggered: float = 0

class TriggerSystem:
    @staticmethod
    def evaluate_condition(condition: str, sample_value: float) -> bool:
        """
        Executa condição shell com $sample disponível
        """
        try:
            # Cria ambiente com $sample
            env = os.environ.copy()
            env['sample'] = str(sample_value)

            # Executa condição
            result = subprocess.run(
                condition,
                shell=True,
                env=env,
                capture_output=True,
                timeout=2
            )

            # Retorna True se exit code == 0
            return result.returncode == 0

        except Exception as e:
            print(f"Error evaluating trigger condition: {e}")
            return False

    @staticmethod
    def execute_actions(actions: TriggerAction, sample_value: float):
        """
        Executa ações do trigger
        """
        # Terminal bell
        if actions.terminal_bell:
            print('\a', end='', flush=True)

        # Sound (usa beep se disponível)
        if actions.sound:
            subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/bell.oga'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Visual é tratado pelo componente (muda cor)

        # Command
        if actions.command:
            try:
                env = os.environ.copy()
                env['sample'] = str(sample_value)

                subprocess.run(
                    actions.command,
                    shell=True,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                print(f"Error executing trigger command: {e}")

# Integração com componente
class ComponentWithTriggers:
    def __init__(self, config):
        self.config = config
        self.triggers = []
        self.current_value = 0
        self.triggered = False  # Estado visual

    def add_trigger(self, trigger: Trigger):
        self.triggers.append(trigger)

    def update(self):
        # Atualiza valor (mesmo código anterior)
        self.current_value = self.fetch_data()

        # Verifica triggers
        self.check_triggers()

    def check_triggers(self):
        any_triggered = False

        for trigger in self.triggers:
            # Avalia condição
            if TriggerSystem.evaluate_condition(trigger.condition, self.current_value):
                # Trigger ativado!
                TriggerSystem.execute_actions(trigger.actions, self.current_value)
                any_triggered = True

                trigger.last_triggered = time.time()
                trigger.trigger_count += 1

        # Atualiza estado visual
        self.triggered = any_triggered

    def render(self):
        # Muda cor se algum trigger ativo
        color = "red" if self.triggered else self.config.color

        # ... renderização normal com cor ajustada
```

#### Exemplo de Uso

```python
# Cria componente com triggers
cpu_chart = Runchart(
    title="CPU Usage",
    width=40,
    height=10,
    rate_ms=1000,
    sample_command="ps aux | awk '{sum+=$3} END {print sum}'",
    color="green"
)

# Adiciona trigger
cpu_chart.add_trigger(Trigger(
    title="High CPU",
    condition='echo "$sample > 80" | bc -l',
    actions=TriggerAction(
        terminal_bell=True,
        visual=True,
        command='notify-send "High CPU" "$sample%"'
    )
))

# Loop
while True:
    if cpu_chart.should_update():
        cpu_chart.update()  # Atualiza dados E checa triggers

    console.clear()
    console.print(cpu_chart.render())  # Cor muda se triggered
    time.sleep(0.1)
```

---

## 6. Interactive Shells

### 6.1 O que são Interactive Shells?

**Interactive Shells** permitem executar comandos interativos de dentro do dashboard via hotkeys.

**Casos de uso:**
- Restart de serviços
- Limpeza de cache
- Deployment de código
- Troubleshooting rápido
- Operações administrativas

### 6.2 Configuração YAML

#### Exemplo 22: Runbooks Básicos

```yaml
# Definidos no nível raiz do config
runbooks:
  # Runbook 1: Restart Nginx
  - title: Restart Nginx Service
    key: r  # Pressionar 'r' no dashboard
    command: sudo systemctl restart nginx

  # Runbook 2: Clear Cache
  - title: Clear Application Cache
    key: c
    command: |
      echo "Clearing cache..."
      rm -rf /tmp/cache/*
      echo "Cache cleared!"
      sleep 2

  # Runbook 3: Git Pull
  - title: Update from Git
    key: u
    command: |
      cd /home/user/project
      git pull origin main
      echo "Repository updated!"
      sleep 3

  # Runbook 4: Docker Restart
  - title: Restart Docker Container
    key: d
    command: |
      docker restart myapp
      echo "Container restarted!"
```

#### Exemplo 23: Runbooks Interativos

```yaml
runbooks:
  # Shell interativo completo
  - title: Open Bash Shell
    key: s
    command: bash

  # Editor de configuração
  - title: Edit Nginx Config
    key: e
    command: sudo nano /etc/nginx/nginx.conf

  # Logs interativos
  - title: Follow Application Logs
    key: l
    command: tail -f /var/log/myapp.log

  # htop para troubleshooting
  - title: Open htop
    key: h
    command: htop
```

### 6.3 Comportamento Runtime

**Fluxo:**
1. Usuário pressiona hotkey ('r', 'c', etc.)
2. Sampler **pausa o dashboard**
3. Executa comando em shell
4. Mostra output do comando em tela cheia
5. Aguarda comando terminar (ou Ctrl+C)
6. Retorna ao dashboard

**Exemplo de interação:**

```
┌─────────────────────────────────────────────────────┐
│                   SAMPLER DASHBOARD                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CPU:  45% ▄▅▆▇█▇▆▅▄                               │
│  MEM:  78% ██████████░░░░░                          │
│                                                     │
│  Press 'r' to restart nginx                         │
│  Press 'c' to clear cache                           │
│  Press 'q' to quit                                  │
└─────────────────────────────────────────────────────┘

Usuário pressiona 'r'
↓
┌─────────────────────────────────────────────────────┐
│  Running: Restart Nginx Service                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  $ sudo systemctl restart nginx                     │
│  [sudo] password for user: ****                     │
│  nginx.service restarted successfully               │
│                                                     │
│  Press ENTER to return to dashboard                 │
└─────────────────────────────────────────────────────┘

Usuário pressiona ENTER
↓
Volta ao dashboard
```

### 6.4 Replicação em Python/Rich

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import subprocess
import sys
import tty
import termios

class Runbook:
    def __init__(self, title: str, key: str, command: str):
        self.title = title
        self.key = key
        self.command = command

    def execute(self, console: Console):
        """
        Executa runbook e mostra output
        """
        # Limpa tela
        console.clear()

        # Mostra header
        console.print(Panel(
            f"[bold]Executing: {self.title}[/bold]\n\n"
            f"Command: [cyan]{self.command}[/cyan]",
            title="Runbook",
            border_style="yellow"
        ))
        console.print()

        # Executa comando em subprocess interativo
        try:
            # IMPORTANTE: Usa sys.stdin/stdout/stderr para interatividade
            subprocess.run(
                self.command,
                shell=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr
            )

            console.print()
            console.print("[green]✓ Command completed successfully[/green]")

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Command failed with exit code {e.returncode}[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]✗ Command interrupted[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")

        # Aguarda usuário pressionar ENTER
        console.print()
        console.input("[dim]Press ENTER to return to dashboard...[/dim]")

class RunbookManager:
    def __init__(self):
        self.runbooks: dict[str, Runbook] = {}
        self.console = Console()

    def add_runbook(self, runbook: Runbook):
        self.runbooks[runbook.key] = runbook

    def get_help_text(self) -> str:
        """Retorna texto de ajuda com todos os runbooks"""
        if not self.runbooks:
            return ""

        lines = ["Available runbooks:"]
        for key, runbook in sorted(self.runbooks.items()):
            lines.append(f"  [{key}] {runbook.title}")

        return "\n".join(lines)

    def handle_key(self, key: str) -> bool:
        """
        Processa tecla pressionada
        Retorna True se foi um runbook
        """
        if key in self.runbooks:
            self.runbooks[key].execute(self.console)
            return True
        return False

# Integração com dashboard
class DashboardWithRunbooks:
    def __init__(self):
        self.console = Console()
        self.runbook_manager = RunbookManager()
        self.running = True

        # Setup runbooks
        self.setup_runbooks()

    def setup_runbooks(self):
        """Configura runbooks disponíveis"""
        self.runbook_manager.add_runbook(Runbook(
            title="Restart Nginx",
            key="r",
            command="sudo systemctl restart nginx"
        ))

        self.runbook_manager.add_runbook(Runbook(
            title="Clear Cache",
            key="c",
            command="rm -rf /tmp/cache/* && echo 'Cache cleared!'"
        ))

        self.runbook_manager.add_runbook(Runbook(
            title="Open htop",
            key="h",
            command="htop"
        ))

    def get_single_key(self) -> str:
        """
        Captura single keypress (non-blocking)
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def render_dashboard(self):
        """Renderiza dashboard completo"""
        self.console.clear()

        # ... renderiza componentes normais ...

        # Adiciona ajuda de runbooks no footer
        help_text = self.runbook_manager.get_help_text()
        self.console.print(Panel(
            help_text + "\n[q] Quit",
            title="Controls",
            border_style="dim"
        ))

    def run(self):
        """Main loop"""
        while self.running:
            # Renderiza dashboard
            self.render_dashboard()

            # Aguarda input (com timeout para updates)
            # (Usa select ou threading para non-blocking)
            key = self.get_single_key()

            # Processa tecla
            if key == 'q':
                self.running = False
            elif not self.runbook_manager.handle_key(key):
                # Tecla não reconhecida
                pass

            time.sleep(0.1)
```

#### Exemplo Completo

```python
# Config
runbooks_config = [
    {
        'title': 'Restart Service',
        'key': 'r',
        'command': 'sudo systemctl restart myapp'
    },
    {
        'title': 'View Logs',
        'key': 'l',
        'command': 'tail -f /var/log/myapp.log'
    },
    {
        'title': 'System Monitor',
        'key': 'h',
        'command': 'htop'
    }
]

# Setup
dashboard = DashboardWithRunbooks()

for cfg in runbooks_config:
    dashboard.runbook_manager.add_runbook(Runbook(
        title=cfg['title'],
        key=cfg['key'],
        command=cfg['command']
    ))

# Run
dashboard.run()
```

---

## 7. Replicação em Python/Rich

### 7.1 Arquitetura Completa de Replicação

```
┌─────────────────────────────────────────────────────────────┐
│              SAMPLER-LIKE ARCHITECTURE IN PYTHON            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 1. CONFIG LAYER                                             │
├─────────────────────────────────────────────────────────────┤
│ - YAML Parser (PyYAML)                                      │
│ - Config validation (pydantic)                              │
│ - Variable substitution                                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. COMPONENT FACTORY                                        │
├─────────────────────────────────────────────────────────────┤
│ - ComponentFactory.create(type, config)                     │
│ - Returns: Runchart | Sparkline | Barchart | ...           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. COMPONENT LAYER (Abstract Base)                          │
├─────────────────────────────────────────────────────────────┤
│ class Component(ABC):                                       │
│   - should_update() -> bool                                 │
│   - update() -> None                                        │
│   - render() -> Panel                                       │
│   - check_triggers() -> None                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────┬───────────────┬────────────────┬───────────┐
│ Runchart       │ Sparkline     │ Barchart       │ Gauge     │
│ (plotext)      │ (▁▂▃▄▅▆▇█)    │ (█████░░░)     │ (arc)     │
└────────────────┴───────────────┴────────────────┴───────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LAYOUT ENGINE                                            │
├─────────────────────────────────────────────────────────────┤
│ - GridLayout                                                │
│ - Converts (x, y, w, h) → Rich Layout                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. RENDER LOOP                                              │
├─────────────────────────────────────────────────────────────┤
│ while True:                                                 │
│   for component in components:                              │
│     if component.should_update():                           │
│       component.update()                                    │
│   layout.render_all()                                       │
│   console.print(layout)                                     │
│   sleep(refresh_rate_ms)                                    │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Implementação Base Completa

```python
# ============================================================================
#                     SAMPLER-LIKE DASHBOARD IN PYTHON
# ============================================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import subprocess
import time
import yaml
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
import plotext as plt
from collections import deque

# ============================================================================
# 1. CONFIG MODELS
# ============================================================================

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
    color: str

# ============================================================================
# 2. COMPONENT BASE CLASS
# ============================================================================

class Component(ABC):
    """Base class para todos os componentes Sampler"""

    def __init__(self, config: ComponentConfig):
        self.config = config
        self.last_update = 0
        self.data = None

    def should_update(self) -> bool:
        """Verifica se deve atualizar baseado em rate_ms"""
        now = time.time() * 1000
        elapsed = now - self.last_update
        return elapsed >= self.config.rate_ms

    def update(self):
        """Executa sample command e atualiza dados"""
        try:
            result = subprocess.run(
                self.config.sample,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse output (cada subclasse implementa)
            self.data = self.parse_output(result.stdout.strip())
            self.last_update = time.time() * 1000

        except Exception as e:
            print(f"Error updating {self.config.title}: {e}")

    @abstractmethod
    def parse_output(self, output: str) -> Any:
        """Parse output do comando"""
        pass

    @abstractmethod
    def render(self) -> Panel:
        """Renderiza componente visual"""
        pass

# ============================================================================
# 3. CONCRETE COMPONENTS
# ============================================================================

class Runchart(Component):
    def __init__(self, config: ComponentConfig):
        super().__init__(config)
        self.points = deque(maxlen=config.position.width - 4)

    def parse_output(self, output: str) -> float:
        value = float(output)
        self.points.append(value)
        return value

    def render(self) -> Panel:
        if not self.points:
            return Panel("No data", title=self.config.title)

        # Setup plotext
        plt.clf()
        plt.theme('dark')
        plt.plot_size(
            self.config.position.width - 4,
            self.config.position.height - 4
        )

        # Plot
        x = list(range(len(self.points)))
        y = list(self.points)
        plt.plot(x, y, color=self.config.color)

        # Generate chart
        chart_str = plt.build()
        chart_text = Text.from_ansi(chart_str)

        # Add legend
        current = self.points[-1] if self.points else 0
        chart_text.append(f"\nCurrent: {current:.2f}", style="bright_white")

        return Panel(
            chart_text,
            title=self.config.title,
            border_style=self.config.color
        )

class Sparkline(Component):
    SPARKS = "▁▂▃▄▅▆▇█"

    def __init__(self, config: ComponentConfig):
        super().__init__(config)
        self.values = deque(maxlen=config.position.width - 10)

    def parse_output(self, output: str) -> float:
        value = float(output)
        self.values.append(value)
        return value

    def _to_spark(self, value: float, min_val: float, max_val: float) -> str:
        if max_val == min_val:
            return self.SPARKS[4]
        normalized = (value - min_val) / (max_val - min_val)
        index = int(normalized * 7)
        return self.SPARKS[max(0, min(7, index))]

    def render(self) -> Panel:
        if not self.values:
            return Panel("No data", title=self.config.title)

        min_val = min(self.values)
        max_val = max(self.values)

        sparks = "".join(
            self._to_spark(v, min_val, max_val)
            for v in self.values
        )

        content = Text(sparks, style=self.config.color)
        content.append(f"  {self.data:.1f}%", style="bright_white")

        return Panel(content, title=self.config.title, border_style=self.config.color)

class Barchart(Component):
    def parse_output(self, output: str) -> Dict[str, float]:
        data = {}
        for line in output.split('\n'):
            if ':' in line:
                label, value = line.split(':', 1)
                data[label.strip()] = float(value.strip())
        return data

    def render(self) -> Panel:
        if not self.data:
            return Panel("No data", title=self.config.title)

        max_val = max(self.data.values())
        bar_width = self.config.position.width - 25

        content = Text()
        for label, value in self.data.items():
            filled = int((value / max_val) * bar_width)
            empty = bar_width - filled
            bar = "█" * filled + "░" * empty
            content.append(f"{label:15} {bar} {value:.1f}%\n")

        return Panel(content, title=self.config.title, border_style=self.config.color)

class Textbox(Component):
    def parse_output(self, output: str) -> str:
        return output

    def render(self) -> Panel:
        content = Text(self.data or "No data")
        return Panel(
            content,
            title=self.config.title,
            border_style=self.config.color,
            width=self.config.position.width,
            height=self.config.position.height
        )

# ============================================================================
# 4. COMPONENT FACTORY
# ============================================================================

class ComponentFactory:
    @staticmethod
    def create(component_type: str, config: Dict) -> Component:
        """Factory method para criar componentes"""

        position = Position(
            x=config['position']['x'],
            y=config['position']['y'],
            width=config['position']['width'],
            height=config['position']['height']
        )

        comp_config = ComponentConfig(
            title=config['title'],
            position=position,
            rate_ms=config['rate-ms'],
            sample=config['sample'],
            color=config.get('color', 'green')
        )

        if component_type == 'runcharts':
            return Runchart(comp_config)
        elif component_type == 'sparklines':
            return Sparkline(comp_config)
        elif component_type == 'barcharts':
            return Barchart(comp_config)
        elif component_type == 'textboxes':
            return Textbox(comp_config)
        else:
            raise ValueError(f"Unknown component type: {component_type}")

# ============================================================================
# 5. CONFIG LOADER
# ============================================================================

class ConfigLoader:
    @staticmethod
    def load_from_yaml(yaml_path: str) -> List[Component]:
        """Carrega config YAML e cria componentes"""
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        components = []

        # Processa cada tipo de componente
        for comp_type in ['runcharts', 'sparklines', 'barcharts', 'gauges',
                          'textboxes', 'asciiboxes']:
            if comp_type in config:
                for comp_config in config[comp_type]:
                    component = ComponentFactory.create(comp_type, comp_config)
                    components.append(component)

        return components

# ============================================================================
# 6. LAYOUT ENGINE
# ============================================================================

class GridLayout:
    """
    Converte posições (x, y, w, h) em Rich Layout
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layout = Layout()

    def place_components(self, components: List[Component]):
        """
        Posiciona componentes no grid
        """
        # TODO: Implementar grid positioning real
        # Por enquanto, usa Rich Layout simples

        # Divide em rows
        rows = {}
        for comp in components:
            y = comp.config.position.y
            if y not in rows:
                rows[y] = []
            rows[y].append(comp)

        # Cria sublayouts
        for y, comps in sorted(rows.items()):
            row_layout = Layout()
            for comp in comps:
                row_layout.split_row(comp.render())
            self.layout.split_column(row_layout)

    def render(self, components: List[Component]) -> Layout:
        """Renderiza todos os componentes no layout"""
        self.place_components(components)
        return self.layout

# ============================================================================
# 7. MAIN DASHBOARD
# ============================================================================

class SamplerDashboard:
    def __init__(self, config_path: str, refresh_rate_ms: int = 100):
        self.config_path = config_path
        self.refresh_rate_ms = refresh_rate_ms
        self.console = Console()

        # Load components
        self.components = ConfigLoader.load_from_yaml(config_path)

        # Setup layout
        terminal_size = self.console.size
        self.layout_engine = GridLayout(terminal_size.width, terminal_size.height)

    def update_components(self):
        """Atualiza componentes que precisam"""
        for component in self.components:
            if component.should_update():
                component.update()

    def run(self):
        """Main loop com Rich Live"""
        with Live(console=self.console, screen=True, auto_refresh=False) as live:
            while True:
                # Update components
                self.update_components()

                # Render layout
                layout = self.layout_engine.render(self.components)

                # Update display
                live.update(layout, refresh=True)

                # Sleep
                time.sleep(self.refresh_rate_ms / 1000)

# ============================================================================
# 8. USAGE
# ============================================================================

if __name__ == "__main__":
    dashboard = SamplerDashboard("config.yml", refresh_rate_ms=100)
    dashboard.run()
```

---

## 8. Padrões Avançados

### 8.1 Variáveis e Templating

```yaml
variables:
  # Definir variáveis globais
  log_path: /var/log/app.log
  monitoring_host: 192.168.1.100
  alert_email: admin@example.com
  cpu_threshold: 80
  mem_threshold: 85

runcharts:
  - title: CPU on $monitoring_host
    sample: ssh $monitoring_host "ps aux | awk '{sum+=\$3} END {print sum}'"
    rate-ms: $monitoring_interval

    triggers:
      - condition: echo "$sample > $cpu_threshold" | bc -l
        actions:
          command: echo "CPU alert" | mail -s "Alert" $alert_email

textboxes:
  - title: Application Logs
    sample: tail -n 20 $log_path
```

### 8.2 Composição de Dashboards

```yaml
# dashboard-main.yml
runcharts:
  - title: Main Metrics
    sample: ./scripts/get_metrics.sh

# scripts/get_metrics.sh
#!/bin/bash
# Compõe múltiplas métricas
CPU=$(ps aux | awk '{sum+=$3} END {print sum}')
MEM=$(free | grep Mem | awk '{print ($3/$2)*100}')
DISK=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

# Retorna valores separados por espaço (múltiplas linhas no gráfico)
echo "$CPU $MEM $DISK"
```

### 8.3 Conditional Rendering

```yaml
runcharts:
  - title: Service Status
    sample: |
      # Retorna 100 se serviço UP, 0 se DOWN
      systemctl is-active myapp.service >/dev/null 2>&1 && echo 100 || echo 0

    color: 2  # Verde por padrão

    triggers:
      - title: Service Down
        condition: echo "$sample < 50" | bc -l
        actions:
          visual: true  # Muda para vermelho
          command: systemctl start myapp.service  # Auto-restart!
```

### 8.4 Data Aggregation

```yaml
barcharts:
  - title: Top 5 Network Consumers
    sample: |
      # Usa nethogs para capturar tráfego por processo
      sudo nethogs -t -d 1 | \
      awk '/^[^-]/ {print $1":"$3}' | \
      sort -t: -k2 -rn | \
      head -n 5
```

---

## 9. Best Practices & Anti-patterns

### 9.1 Best Practices ✅

#### 1. Rate-ms Adequado

```yaml
# ✅ BOM: Rates apropriados para cada tipo de dado
runcharts:
  - title: CPU (muda frequentemente)
    rate-ms: 1000  # 1 segundo

  - title: Disk Usage (muda lentamente)
    rate-ms: 30000  # 30 segundos

  - title: System Info (estático)
    rate-ms: 0  # Nunca atualiza
```

```yaml
# ❌ RUIM: Tudo com 100ms
runcharts:
  - title: Disk Usage
    rate-ms: 100  # Overkill! Desperdiça CPU
```

#### 2. Comandos Eficientes

```yaml
# ✅ BOM: Comando leve e rápido
sample: ps aux | awk '{sum+=$3} END {print sum}'

# ❌ RUIM: Comando pesado que demora
sample: find / -type f -exec du -h {} \; | sort -rh | head -1
```

#### 3. Error Handling

```yaml
# ✅ BOM: Fallback se comando falhar
sample: cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null || echo "0"

# ❌ RUIM: Sem tratamento de erro
sample: cat /sys/class/thermal/thermal_zone0/temp
```

#### 4. Trigger Debouncing

```yaml
# ✅ BOM: Trigger só após condição persistir
triggers:
  - condition: |
      # Usa contador para debounce
      COUNTER_FILE="/tmp/alert_counter"
      if [ $(echo "$sample > 80" | bc -l) -eq 1 ]; then
        COUNT=$(($(cat $COUNTER_FILE 2>/dev/null || echo 0) + 1))
        echo $COUNT > $COUNTER_FILE
        [ $COUNT -ge 5 ]  # Trigger após 5 vezes
      else
        echo 0 > $COUNTER_FILE
        false
      fi

# ❌ RUIM: Trigger a cada spike momentâneo
triggers:
  - condition: echo "$sample > 80" | bc -l
    actions:
      command: echo "ALERT!" | mail admin  # Spam de emails!
```

#### 5. Componentes Modulares

```yaml
# ✅ BOM: Scripts externos reutilizáveis
runcharts:
  - title: CPU
    sample: ./scripts/get_cpu.sh

# ❌ RUIM: Lógica complexa inline no YAML
runcharts:
  - title: CPU
    sample: |
      # 50 linhas de bash aqui...
      # Difícil de testar e manter
```

### 9.2 Anti-patterns ❌

#### 1. Blocking Commands

```yaml
# ❌ ANTI-PATTERN: Comando que bloqueia indefinidamente
sample: tail -f /var/log/app.log  # Nunca termina!

# ✅ CORRETO: Usa head/tail com limite
sample: tail -n 20 /var/log/app.log
```

#### 2. Comandos que Precisam de Interação

```yaml
# ❌ ANTI-PATTERN: Comando interativo
sample: sudo systemctl restart nginx  # Pede senha!

# ✅ CORRETO: Usa runbook para interação
runbooks:
  - title: Restart Nginx
    key: r
    command: sudo systemctl restart nginx
```

#### 3. Parsing Frágil

```yaml
# ❌ ANTI-PATTERN: Parsing dependente de locale/formato
sample: free -h | grep Mem | awk '{print $3}'  # Retorna "2.5G" (string!)

# ✅ CORRETO: Usa formato numérico
sample: free | grep Mem | awk '{print ($3/$2)*100}'  # Retorna "75.3"
```

#### 4. Excesso de Componentes

```yaml
# ❌ ANTI-PATTERN: 50 componentes atualizando a cada 100ms
# Mata performance!

# ✅ CORRETO: Agrupe métricas relacionadas
barcharts:
  - title: System Overview
    sample: |
      echo "CPU:$(get_cpu)"
      echo "MEM:$(get_mem)"
      echo "DISK:$(get_disk)"
```

#### 5. Triggers Recursivos

```yaml
# ❌ ANTI-PATTERN: Trigger que pode causar loop infinito
triggers:
  - condition: echo "$sample > 80" | bc -l
    actions:
      command: stress-ng --cpu 8  # Aumenta CPU, causa mais triggers!

# ✅ CORRETO: Ações que resolvem o problema
triggers:
  - condition: echo "$sample > 80" | bc -l
    actions:
      command: killall high_cpu_process  # Resolve causa
```

---

## 10. Estratégia de Implementação

### 10.1 Roadmap de Implementação para WiFi Dashboard

**Fase 1: Core Architecture (Sprint 1)**
- [ ] Implementar classe base `Component` com `should_update()` e `update()`
- [ ] Criar `ComponentFactory`
- [ ] Implementar `ConfigLoader` para YAML
- [ ] Setup do loop principal com rate-based updates

**Fase 2: Componentes Básicos (Sprint 2)**
- [ ] Implementar `Runchart` com plotext
- [ ] Implementar `Sparkline` com caracteres Unicode
- [ ] Implementar `Textbox`
- [ ] Testar com dados mock

**Fase 3: Layout System (Sprint 3)**
- [ ] Implementar `GridLayout` básico
- [ ] Converter `(x, y, w, h)` para Rich Layout
- [ ] Testar posicionamento de múltiplos componentes

**Fase 4: Componentes Avançados (Sprint 4)**
- [ ] Implementar `Barchart`
- [ ] Implementar `Gauge`
- [ ] Implementar `Asciibox`

**Fase 5: Triggers (Sprint 5)**
- [ ] Implementar `TriggerSystem`
- [ ] Adicionar `terminal-bell`, `sound`, `visual`
- [ ] Testar triggers com condições reais

**Fase 6: Runbooks (Sprint 6)**
- [ ] Implementar `RunbookManager`
- [ ] Adicionar captura de teclas
- [ ] Testar execução de comandos interativos

### 10.2 Exemplo de Config para WiFi Dashboard

```yaml
# wifi_dashboard.yml
# Configuração Sampler-style para WiFi Security Education Dashboard

variables:
  interface: wlan0
  refresh_interval: 1000

# ============================================================================
# ROW 1: WiFi + System (lado a lado)
# ============================================================================

runcharts:
  - title: WiFi Signal Strength
    position: {x: 0, y: 0, width: 60, height: 12}
    rate-ms: $refresh_interval
    sample: iw dev $interface link | grep signal | awk '{print $2}'
    color: green
    legend:
      enabled: true
      details: false

sparklines:
  - title: System Resources
    position: {x: 60, y: 0, width: 60, height: 12}
    rate-ms: 2000
    sample: |
      echo "CPU: $(ps aux | awk '{sum+=$3} END {print sum}')"
      echo "RAM: $(free | grep Mem | awk '{printf \"%.1f\", ($3/$2)*100}')"
    color: yellow

# ============================================================================
# ROW 2: Traffic Chart (full width)
# ============================================================================

runcharts:
  - title: Network Throughput (Mbps)
    position: {x: 0, y: 12, width: 120, height: 15}
    rate-ms: 500
    sample: ./scripts/get_bandwidth.sh $interface
    color: cyan

# ============================================================================
# ROW 3: Devices + Top Apps
# ============================================================================

barcharts:
  - title: Connected Devices
    position: {x: 0, y: 27, width: 60, height: 10}
    rate-ms: 5000
    sample: arp -a | grep -c $interface
    color: magenta

barcharts:
  - title: Top Network Apps
    position: {x: 60, y: 27, width: 60, height: 10}
    rate-ms: 3000
    sample: |
      sudo nethogs -t -d 1 | \
      awk '/^[^-]/ {print $1":"$3}' | \
      head -n 5
    color: blue

# ============================================================================
# ROW 4: Educational Tips
# ============================================================================

textboxes:
  - title: Educational Tip
    position: {x: 0, y: 37, width: 120, height: 6}
    rate-ms: 30000  # Muda a cada 30s
    sample: shuf -n 1 /home/user/tips.txt
    color: green

# ============================================================================
# TRIGGERS
# ============================================================================

# (Triggers são definidos em cada componente acima)

# ============================================================================
# RUNBOOKS
# ============================================================================

runbooks:
  - title: Restart NetworkManager
    key: r
    command: sudo systemctl restart NetworkManager

  - title: Scan Networks
    key: s
    command: sudo iwlist $interface scan | grep ESSID

  - title: View Connection Info
    key: i
    command: nmcli device show $interface
```

---

## 🎯 Conclusão

Este documento fornece uma análise completa do Sampler e estratégias detalhadas para replicar suas funcionalidades em Python/Rich para o WiFi Security Education Dashboard.

**Pontos-chave:**
1. ✅ Sampler usa **rate-based updates** (cada componente tem seu próprio intervalo)
2. ✅ **6 tipos de componentes** visuais (Runchart, Sparkline, Barchart, Gauge, Textbox, Asciibox)
3. ✅ **Sistema de triggers** poderoso com alertas visuais/sonoros
4. ✅ **Interactive shells** (runbooks) para executar comandos via hotkeys
5. ✅ **Configuração YAML** declarativa - zero código necessário
6. ✅ **Replicável em Python** usando Rich, plotext, subprocess

**Próximos passos:**
- Implementar arquitetura base (Component, Factory, Loader)
- Criar componentes um por vez
- Testar com dados mock
- Adicionar triggers
- Implementar runbooks

**Juan-Dev - Soli Deo Gloria ✝️**
