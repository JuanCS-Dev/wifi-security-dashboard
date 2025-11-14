# Penelope Joy WF-Tool 🌟🛡️

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-success.svg)]()

**Educational WiFi Security Monitoring Tool** - Ferramenta educacional de monitoramento de segurança WiFi

> *"Uma ferramenta que ensina segurança de rede para a próxima geração"*

## 🎯 Sobre o Projeto

Uma aplicação educacional em Python que monitora e analisa a segurança de redes WiFi. Desenvolvida com foco em ensino prático de conceitos de segurança de rede, oferecendo dashboards intuitivos e modo simulado para testes sem hardware real.

## ✨ Features

- 🎨 **Interface Matrix Style** - Terminal verde/preto com design responsivo
- 📊 **12 Dashboards Especializados**
  - Sistema (CPU, RAM, Disco)
  - Rede (Tráfego, Bandwidth)
  - WiFi (SSIDs, Sinais)
  - Pacotes (Análise de protocolos)
  - Topologia (Mapeamento de rede)
  - ARP Detector (Detecção de spoofing)
  - DNS Monitor (Monitoramento DNS)
  - E mais...

- 🧪 **Modo Mock** - Testes completos sem hardware real
- 📚 **Sistema Tutorial** - Aprenda enquanto usa
- 🔒 **Educação em Segurança** - Dicas contextuais
- ⚡ **Real-time Updates** - Atualização automática
- 📱 **100% Responsivo** - Adapta-se a qualquer terminal

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- pip ou poetry

### Instalação

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/wifi_security_education.git
cd wifi_security_education

# Instalar dependências
pip install -r requirements-v2.txt
```

### Uso

```bash
# Modo Mock (recomendado para testes)
python3 app_textual.py --mode mock

# Modo Real (requer sudo)
sudo python3 app_textual.py --mode real
```

## 📁 Estrutura do Projeto

```
src/
├── plugins/          # Coletores de dados modulares
├── screens/          # Dashboards TUI
├── widgets/          # Componentes UI reutilizáveis
├── themes/           # Estilos CSS
└── utils/            # Utilitários e geradores de dados

tests/               # Suite de testes
docs/                # Documentação
config/              # Arquivos de configuração
scripts/             # Scripts auxiliares
```

## 🧪 Testes

```bash
# Executar testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src --cov-report=html

# Ver relatório
firefox htmlcov/index.html
```

## 📚 Documentação

- [QUICK_START.md](QUICK_START.md) - Guia rápido
- [CHANGELOG.md](CHANGELOG.md) - Histórico de versões
- [ROADMAP.md](ROADMAP.md) - Planos futuros
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [SECURITY.md](SECURITY.md) - Política de segurança
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Código de conduta

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## ✝️ Créditos

**Desenvolvido por:** Juan-Dev  
**Filosofia:** Soli Deo Gloria (Somente a Glória de Deus)

---

**A verdade importa. Qualidade importa. Disciplina > Genialidade.**
