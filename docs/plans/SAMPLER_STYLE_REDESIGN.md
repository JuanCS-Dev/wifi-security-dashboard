# Sampler-Style Redesign Plan

**Inspiração:** sqshq/sampler (14.3k stars) - Professional terminal dashboard

## 🎯 Características do Sampler

### Visual
- ✅ Grid layout preciso com posições definidas
- ✅ Componentes especializados (charts, gauges, textbox)
- ✅ Bordas minimalistas ou sem borda
- ✅ Títulos em CAPS
- ✅ Layout compacto e eficiente
- ✅ Sem emojis excessivos
- ✅ Cores sutis e profissionais

### Arquitetura
- Widget-based modular
- Rate-based updates (cada widget tem seu rate-ms)
- YAML config-driven
- Shell command execution

## 🔨 Implementação no nosso projeto

### 1. Landing Screen - Estilo Sampler
```
┌─────────────────────────────────────────────────────┐
│  WIFI SECURITY EDUCATION DASHBOARD                  │
│  v3.0.0                                             │
└─────────────────────────────────────────────────────┘

MODE: ● MOCK

DASHBOARDS
─────────────────────────────────────────────────────
 0  Consolidated     All metrics
 1  System           CPU, RAM, Disk
 2  Network          Bandwidth, connections
 3  WiFi             Signal, security
 4  Packets          Protocol analysis

CONTROLS
─────────────────────────────────────────────────────
 t  Toggle mode      Mock ↔ Real
 h  Help             Show keybindings
 q  Quit             Exit application
```

### 2. Dashboard Widgets - Estilo Sampler

**Antes (Brega):**
- Bordas grossas duplas
- Emojis em títulos
- Cores berrantes
- Padding excessivo

**Depois (Sampler):**
- Bordas finas round ou sem borda
- Títulos limpos em CAPS
- Cores profissionais (#00cc66, #00aa55)
- Layout compacto

### 3. Color Palette - Profissional

```css
Background:     #000000 (puro preto)
Primary text:   #00cc66 (verde fosco)
Secondary text: #00aa55 (verde dim)
Dim text:       #008855 (verde escuro)
Borders:        #00aa55 (verde suave)
Warning:        #ccaa00 (amarelo fosco)
Critical:       #cc6600 (laranja fosco)
```

### 4. Componentes Sampler-style

#### CPU Widget
```
┌─ CPU ───────────────┐
│  87.3%  ████████▌   │
│  Core 1: 45%        │
│  Core 2: 89%        │
│  Core 3: 92%        │
│  Core 4: 67%        │
└─────────────────────┘
```

#### Network Chart
```
┌─ NETWORK BANDWIDTH ─────────────────────┐
│                                          │
│  ↑ 1.2 MB/s    ▂▃▅▇█▇▅▃▂                │
│  ↓ 3.4 MB/s    ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁          │
│                                          │
└──────────────────────────────────────────┘
```

#### WiFi Signal
```
┌─ WIFI SIGNAL ───────┐
│  HomeNetwork        │
│  -45 dBm  ████████  │
│  WPA2-PSK           │
└─────────────────────┘
```

## 5. Layout Grid System

Consolidated Dashboard:
```
┌──────────────┬──────────────┬──────────────┐
│   CPU        │    RAM       │    DISK      │
│   Widget     │    Widget    │    Widget    │
│   20x6       │    20x6      │    20x6      │
├──────────────┴──────────────┴──────────────┤
│            NETWORK CHART                   │
│                 60x10                      │
├──────────────┬──────────────┬──────────────┤
│  WIFI        │   PACKETS    │   TIPS       │
│  Signal      │   Stats      │   Educational│
│  20x8        │   20x8       │   20x8       │
└──────────────┴──────────────┴──────────────┘
```

## ✅ Checklist de Implementação

- [ ] Redesign landing_screen.py (banner minimalista)
- [ ] Update terminal_native.tcss (cores profissionais)
- [ ] Redesign widgets (bordas finas, títulos CAPS)
- [ ] Remove emojis excessivos dos títulos
- [ ] Implementar grid system compacto
- [ ] Ajustar padding/spacing (mais compacto)
- [ ] Testar visual final

## 🎯 Resultado Esperado

**Visual profissional estilo Sampler:**
- Clean e minimalista
- Layout eficiente
- Cores suaves e legíveis
- Parece ferramenta profissional (htop, tmux, sampler)
- Não parece brinquedo brega

---

**Filosofia:** "Boris-level execution - Study the best, then build better"
