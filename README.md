# WiFi Security Education Platform 🛡️

[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](VERSION)
[![Tests](https://img.shields.io/badge/tests-65%20passing-brightgreen.svg)](docs/TEST_COVERAGE_REPORT.md)
[![Coverage](https://img.shields.io/badge/coverage-48%25-yellow.svg)](htmlcov/index.html)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Sistema educacional de monitoramento e análise de segurança WiFi em tempo real.

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

- 🎨 **Visual Matrix Style** - Interface verde/preto estilo terminal clássico
- 📊 **5 Dashboards Especializados**
  - Consolidado - Visão geral do sistema
  - Sistema - CPU, memória, disco
  - Rede - Tráfego, bandwidth, conexões
  - WiFi - SSIDs, força de sinal, segurança
  - Pacotes - Análise de protocolos em tempo real
- 🧪 **Modo Mock** - Teste completo sem hardware real
- 🎓 **Sistema Tutorial** - Aprenda enquanto usa
- 🔒 **Educação em Segurança** - Dicas contextuais sobre HTTPS, WPA2, etc.
- ⚡ **Real-time Updates** - Atualização automática a cada 1-2s

## 📦 Arquitetura

```
src/
├── plugins/          # Coletores de dados modulares
│   ├── system_plugin.py      # CPU, RAM, Disk (88% tested)
│   ├── network_plugin.py     # Bandwidth, conexões (86% tested)
│   ├── wifi_plugin.py        # SSIDs, sinais (40% tested)
│   └── packet_analyzer_plugin.py  # Protocolos (44% tested)
├── screens/          # Dashboards TUI
│   ├── landing_screen.py     # Menu principal (83% tested)
│   ├── consolidated_dashboard.py
│   ├── system_dashboard.py
│   ├── network_dashboard.py
│   ├── wifi_dashboard.py
│   └── packets_dashboard.py
├── widgets/          # Componentes UI
│   ├── network_chart.py      # Gráfico de bandwidth
│   ├── packet_table.py       # Tabela de pacotes
│   └── tooltip_widget.py     # Dicas educacionais (77% tested)
└── utils/
    └── mock_data_generator.py  # Gerador de dados (87% tested)
```

## 🧪 Testes e Qualidade

**Coverage: 48%** (científico e real-world)

- ✅ **Core Plugins:** 86% coverage médio
- ✅ **65 testes** passando com rigor
- ✅ **Disciplina > Genialidade** - Testes reais, não fake assertions

```bash
# Executar suite de testes
python3 -m pytest tests/ -v --cov=src --cov-report=html

# Ver relatório detalhado
firefox htmlcov/index.html
```

Ver [docs/TEST_COVERAGE_REPORT.md](docs/TEST_COVERAGE_REPORT.md) para análise completa.

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
