# 🎓 WiFi Security Education Dashboard v3.0

**Framework:** Textual 6.6.0+ (Modern Terminal UI)
**Author:** Juan-Dev - Soli Deo Gloria ✝️
**Status:** 🚧 Em Desenvolvimento Ativo (Sprint 3/6)

---

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install textual textual-dev psutil

# 2. Rodar dashboard (modo educacional com dados simulados)
python3 app_textual.py --mock

# 3. Controles
# Pressione 'q' para sair
# Mouse funciona! (scroll, select, etc.)
```

---

## ✨ O que é este projeto?

Dashboard educacional de monitoramento WiFi e rede para **ensinar segurança de redes** de forma visual e interativa, projetado para crianças e iniciantes.

**Features:**
- 📊 Monitoramento em tempo real (CPU, RAM, Disco, WiFi)
- 🎨 Interface colorida e responsiva
- 🎓 Modo educacional com dicas contextuais
- 🔍 Análise de pacotes (Wireshark-style) - Em desenvolvimento
- 💡 Zero flickering, ANSI-native
- 🖱️ Suporte a mouse

---

## 📸 Screenshot

```
╔════════════════════════════════════════════════════════════════════════╗
║  WiFi Security Dashboard v3.0 - Textual              ⏰ 14:03:56       ║
╠═══════════════╦════════════════════════════════════════════════════════╣
║               ║                                                        ║
║ ┌───────────┐ ║  ┌──────────────────────────────────────────────┐    ║
║ │💻 CPU     │ ║  │  📈 NETWORK CHART                           │    ║
║ │████░░░░░░ │ ║  │  (Coming soon - Sparkline ou plotext)       │    ║
║ │45.2% NORMAL│ ║  │                                              │    ║
║ └───────────┘ ║  └──────────────────────────────────────────────┘    ║
║               ║                                                        ║
║ ┌───────────┐ ║  ┌──────────────────────────────────────────────┐    ║
║ │📊 RAM     │ ║  │  📦 PACKET TABLE                            │    ║
║ │███████░░░ │ ║  │  Time     │ Source   │ Dest    │ Protocol   │    ║
║ │72.5% HIGH │ ║  │  10:30:45 │ 192.168… │ 8.8.8.8 │ HTTPS ✓   │    ║
║ └───────────┘ ║  └──────────────────────────────────────────────┘    ║
╚═══════════════╩════════════════════════════════════════════════════════╝
```

---

## 🏗️ Arquitetura

```
wifi_security_education/
├── app_textual.py              # 🎯 ENTRY POINT (Textual v3.0)
│
├── src/
│   ├── plugins/                # 📊 Data collection
│   │   ├── base.py             # Plugin base class
│   │   ├── system_plugin.py    # CPU, RAM, Disk (psutil)
│   │   ├── wifi_plugin.py      # WiFi monitoring
│   │   ├── network_plugin.py   # Network traffic
│   │   └── packet_analyzer_plugin.py  # Packet capture (Scapy)
│   │
│   ├── utils/
│   │   └── mock_data_generator.py  # Realistic mock data
│   │
│   ├── educational/            # 🎓 Para implementar (Sprint 5)
│   ├── triggers/               # 🔔 Para implementar (Sprint 5)
│   ├── layout/                 # 📐 Para implementar (Sprint 4)
│   └── renderers/              # 🎨 Para implementar (Sprint 4)
│
├── config/
│   └── dashboard.yml           # Main config
│
├── tests/                      # 🧪 Unit & integration tests
│
└── docs/                       # 📚 Documentation
    └── REFACTORING_PLAN.md     # Architecture & roadmap
```

---

## ✅ Sprint Progress

| Sprint | Objetivo | Status | Completude |
|--------|----------|--------|------------|
| Sprint 1 | Fundação (Header, Footer, Layout) | ✅ Done | 100% |
| Sprint 2 | Widgets Core (CPU, RAM, Disk, WiFi) | ✅ Done | 100% |
| Sprint 3 | Charts & Tables | ✅ Done | 100% |
| Sprint 4 | Integração Plugins Reais | ⏳ Pendente | 0% |
| Sprint 5 | Educational Features | ⏳ Pendente | 0% |
| Sprint 6 | Polish & Launch | ⏳ Pendente | 0% |

**Overall:** 50% completo (3/6 sprints)

---

## ✅ Sprint 3 - Concluído! 

### Tarefas Completadas:
- [x] NetworkChart widget (plotext com gráficos RX/TX)
- [x] PacketTable widget (Textual DataTable com estilo Wireshark)
- [x] Integração com NetworkPlugin
- [x] Integração com PacketAnalyzerPlugin
- [x] Network Dashboard completo (gráfico + estatísticas)
- [x] Packets Dashboard completo (tabela + análise + educational tips)

### Funcionalidades Implementadas:
- **NetworkChart**: Gráfico de bandwidth RX/TX em tempo real com histórico de 60s
- **PacketTable**: Tabela de pacotes com flags educacionais (🔒 HTTPS seguro, ⚠️ HTTP inseguro)
- **Educational Tips**: Widget com dicas de segurança de protocolos
- **Auto-scaling**: Gráficos adaptam-se automaticamente aos valores
- **Color coding**: Protocolos coloridos para identificação rápida

---

## 📋 Roadmap Completo

### v3.1 (Sprint 3-4) - Charts & Tables
- [ ] NetworkChart com Sparkline
- [ ] PacketTable com DataTable
- [ ] Gráficos de bandwidth em tempo real

### v3.2 (Sprint 5-6) - Interatividade
- [ ] Keyboard shortcuts completos
- [ ] Modal de ajuda educacional
- [ ] Settings screen (dark/light theme)
- [ ] Command palette (fuzzy search)

### v3.3 (Sprint 7+) - Advanced
- [ ] Browser mode (`textual serve app_textual.py`)
- [ ] Export de relatórios (CSV, JSON)
- [ ] Multiple screens (Dashboard, Packets, Settings, About)
- [ ] Custom themes (crianças podem escolher cores!)

---

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run specific test
pytest tests/unit/test_system_plugin.py

# Coverage report
pytest --cov=src tests/
```

---

## 🐛 Troubleshooting

### Problema: "textual: command not found"
```bash
pip install textual textual-dev --break-system-packages
```

### Problema: Terminal mostra códigos estranhos
**Causa:** Terminal não suporta ANSI true color
**Solução:** Use terminal moderno (iTerm2, Windows Terminal, GNOME Terminal)

### Problema: Dashboard não atualiza
**Causa:** SystemPlugin não inicializou
**Solução:**
```bash
pip install psutil
```

---

## 📚 Documentação Adicional

- **README_TEXTUAL.md** - Guia detalhado do Textual v3.0
- **STATUS_SESSION_2025-11-11.md** - Status da última sessão
- **docs/REFACTORING_PLAN.md** - Plano arquitetural completo
- **../LEGADO/** - Código histórico (v1.0 Rich, v2.0 py_cui)

---

## 🎯 Sprint 4 - Próximos Passos

### Objetivo:
Integração completa com plugins reais (sem fallback para mock)

### Tarefas Planejadas:
- [ ] Refinar WiFiPlugin para captura real de dados wireless
- [ ] Melhorar NetworkPlugin para métricas mais detalhadas
- [ ] Adicionar permissões e documentação para modo real
- [ ] Implementar tratamento de erros robusto para situações sem permissão
- [ ] Adicionar modo "demo" que funciona mesmo sem permissões root

### Desafios Técnicos:
- Captura de pacotes requer permissões root (Scapy/PyShark)
- WiFi monitoring pode não funcionar em todos os sistemas
- Necessário documentar setup de permissões (setcap, sudo, etc.)

---

## 🎓 Objetivos Educacionais

Este dashboard ensina:
1. **Monitoramento de Sistemas** - Como recursos (CPU, RAM) são usados
2. **Redes WiFi** - Força do sinal, canais, segurança
3. **Protocolos de Rede** - HTTP vs HTTPS, TCP vs UDP
4. **Análise de Pacotes** - Como dados trafegam pela rede
5. **Segurança** - Identificar tráfego inseguro (HTTP, DNS)

**Público-alvo:** Crianças, estudantes, iniciantes em TI

---

## 🤝 Contributing

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Ver `CONTRIBUTING.md` para detalhes.

---

## 📜 License

Educational Use License - Ver `LICENSE` para detalhes.

---

## 🙏 Créditos

**Framework:** [Textual](https://github.com/Textualize/textual) by Textualize
**Inspiração:** Sampler, btop++, htop, Wireshark
**Author:** Juan-Dev

**Soli Deo Gloria** ✝️

---

## 📞 Suporte

- 📖 **Docs:** Ver `README_TEXTUAL.md`
- 🐛 **Issues:** GitHub Issues
- 💬 **Discussões:** GitHub Discussions

---

**v3.0 - Textual Refactor** | 2025-11-11
