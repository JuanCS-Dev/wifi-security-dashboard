# Penelope Joy WF-Tool 🌟🛡️

[![Version](https://img.shields.io/badge/version-1.0.0--penelope-pink.svg)](VERSION)
[![Tests](https://img.shields.io/badge/tests-376%20passing-brightgreen.svg)](TEST_RESULTS.md)
[![Coverage](https://img.shields.io/badge/coverage-57%25-yellow.svg)](htmlcov/index.html)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Quality](https://img.shields.io/badge/quality-production%20ready-success.svg)](TEST_RESULTS.md)

**Educational WiFi Security Monitoring Tool** - Created with ❤️ for Penelope Joy

> *"A ferramenta que ensina segurança de rede para a próxima geração"*  
> Powered by Maximus AI 🤖

![Matrix Style Terminal](screenshots/banner-matrix.png)

## 🚀 Quick Start

```bash
# Instalar dependências
pip install -r requirements-v2.txt

# Executar (modo mock - sem hardware)
python3 app_textual.py --mode mock

# Executar (modo real - requer sudo para captura de pacotes)
sudo python3 app_textual.py --mode real
```

## ✨ Features v3.0

- 🎨 **Visual Matrix Style** - Interface verde/preto estilo terminal clássico, totalmente responsiva
- 📊 **12 Dashboards Especializados Sampler-Style**
  - **0** Consolidado - Visão geral do sistema
  - **1** Sistema - CPU, memória, disco
  - **2** Rede - Tráfego, bandwidth, conexões
  - **3** WiFi - SSIDs, força de sinal, segurança
  - **4** Pacotes - Análise de protocolos em tempo real
  - **5** Topologia - Mapeamento de rede
  - **6** ARP Detector - Detecção de spoofing
  - **7** Traffic Stats - Estatísticas por dispositivo
  - **8** DNS Monitor - Monitoramento de queries DNS
  - **9** HTTP Sniffer - Análise de tráfego HTTP (⚠️ uso ético)
  - **a** Rogue AP - Detecção de access points falsos
  - **b** Handshake - Captura educacional (⚖️ legal warnings)
- 🧪 **Modo Mock** - Teste completo sem hardware real com dados realísticos
- 🎓 **Sistema Tutorial** - Aprenda enquanto usa
- 🔒 **Educação em Segurança** - Dicas contextuais sobre HTTPS, WPA2, ARP, DNS
- ⚡ **Real-time Updates** - Atualização automática a cada 1-2s
- 📱 **100% Responsivo** - Adapta-se a qualquer tamanho de terminal

## 📦 Arquitetura

```
src/
├── plugins/          # 12 coletores de dados modulares
│   ├── system_plugin.py           # CPU, RAM, Disk
│   ├── network_plugin.py          # Bandwidth, conexões
│   ├── wifi_plugin.py             # SSIDs, sinais
│   ├── packet_analyzer_plugin.py  # Protocolos
│   ├── network_topology_plugin.py # Mapeamento de rede
│   ├── arp_spoofing_detector.py   # Detecção ARP spoofing
│   ├── traffic_statistics.py      # Tráfego por dispositivo
│   ├── dns_monitor_plugin.py      # Queries DNS
│   ├── http_sniffer_plugin.py     # Análise HTTP
│   ├── rogue_ap_detector.py       # Access points falsos
│   └── handshake_capturer.py      # Captura WPA handshakes
├── screens/          # 12 Dashboards TUI (Sampler-style)
│   ├── landing_screen.py          # Landing page interativa
│   ├── consolidated_dashboard.py  # Overview
│   ├── system_dashboard.py        # Sistema
│   ├── network_dashboard.py       # Rede
│   ├── wifi_dashboard.py          # WiFi
│   ├── packets_dashboard.py       # Pacotes
│   ├── topology_dashboard.py      # Topologia
│   ├── arp_detector_dashboard.py  # ARP Detector
│   ├── traffic_dashboard.py       # Traffic Stats
│   ├── dns_dashboard.py           # DNS Monitor
│   ├── http_sniffer_dashboard.py  # HTTP Sniffer
│   ├── rogue_ap_dashboard.py      # Rogue AP
│   ├── handshake_dashboard.py     # Handshake
│   ├── help_screen.py             # Sistema de ajuda
│   └── tutorial_screen.py         # Tutorial interativo
├── widgets/          # Componentes UI reutilizáveis
│   ├── network_chart.py           # Gráfico de bandwidth
│   ├── packet_table.py            # Tabela de pacotes
│   └── sampler_components.py      # Widgets Sampler-style
├── themes/
│   └── terminal_native.tcss       # CSS Matrix style
└── utils/
    └── mock_data_generator.py     # Dados realísticos para demo
```

## 🧪 Testes e Qualidade

**Coverage: 48%** (científico e real-world)

- ✅ **Core Plugins:** 86% coverage médio
- ✅ **65 testes** passando com rigor
- ✅ **Disciplina > Genialidade** - Testes reais, não fake assertions

```bash
# Executar suite de testes
python3 -m pytest tests/test_app_structure.py tests/test_app_functional.py -v

# Com coverage
python3 -m pytest tests/ -v --cov=src --cov-report=html

# Ver relatório detalhado
firefox htmlcov/index.html
```

**Status:** ✅ 27/27 testes passando | Coverage: 28%  
Ver [TEST_RESULTS.md](TEST_RESULTS.md) para análise científica completa.

## 🎯 Uso

### Navegação

- `1-6` - Trocar entre dashboards
- `t` - Toggle modo (mock/real)
- `h` - Ajuda
- `q` - Sair

### Modos

**Mock Mode (Recomendado para testes)**
- ✅ Não requer permissões root
- ✅ Dados realistas simulados
- ✅ Ideal para desenvolvimento/demonstração

**Real Mode**
- ⚠️ Requer `sudo` para captura de pacotes
- 📡 Lê dados reais de hardware
- 🔍 Análise verdadeira de tráfego

## 📚 Documentação

- [CHANGELOG.md](CHANGELOG.md) - Histórico de versões
- [ROADMAP.md](ROADMAP.md) - Planos futuros
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [SECURITY.md](SECURITY.md) - Política de segurança
- [docs/TEST_COVERAGE_REPORT.md](docs/TEST_COVERAGE_REPORT.md) - Relatório de testes

## 🤝 Contribuindo

Contribuições são bem-vindas! Ver [CONTRIBUTING.md](CONTRIBUTING.md).

### Desenvolvido com disciplina

Este projeto segue a filosofia: **"Genialidade sem disciplina = fracasso"**

- ✅ Testes científicos reais
- ✅ Cobertura honesta (não inflada)
- ✅ Documentação completa
- ✅ Código limpo e organizado

## 📄 Licença

MIT License - Ver [LICENSE](LICENSE)

## ✝️ Créditos

**Autor:** Juan-Dev  
**Filosofia:** Soli Deo Gloria (Somente a Glória de Deus)

---

**A verdade importa. Testes reais importam. Disciplina > Genialidade.**
