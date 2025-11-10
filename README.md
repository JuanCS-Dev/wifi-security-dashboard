# 🛡️ Dashboard Educacional WiFi Security 🎓

## 🌟 O Que É Este Projeto?

Um **dashboard interativo e VISUAL** em terminal para ensinar crianças de **7-8 anos** sobre:
- 📶 Como funciona o WiFi
- 🔒 Segurança de redes
- 💻 Monitoramento de tráfego
- 📱 Dispositivos conectados
- 🎯 Aplicativos que usam internet

### Por Que Foi Criado?

Feito com ❤️ por **Juan-Dev** para seus filhos aprenderem sobre tecnologia de forma **DIVERTIDA e VISUAL**!

**Filosofia**: Educação através de visualização impressionante + dados reais

---

## ✨ Features Principais

### 📊 Dashboard em Tempo Real
- **4 FPS** de atualização (250ms)
- **Cores vibrantes** mas não agressivas
- **Emojis educacionais** para fácil compreensão
- **Gráficos impressionantes** (line charts, bar charts)

### 🌐 Monitoramento de Rede
- **Força do sinal WiFi** visual (barras 📶)
- **Tipo de segurança** (WPA3, WPA2, etc)
- **Frequência** (2.4GHz vs 5GHz explicado)
- **Dispositivos conectados** com tipo e tráfego
- **Aplicativos detectados** (YouTube, Netflix, WhatsApp, etc)

### 💻 Métricas do Sistema
- **CPU** com barra de progresso colorida
- **RAM** com status educacional
- **Temperatura** (se disponível)
- **Uptime** do dashboard

### 📈 Gráficos Educacionais
- **Tráfego de rede** (Download/Upload em tempo real)
- **Histórico de 60 segundos**
- **Multi-linha** com cores distintas

### 💡 Dicas Educacionais
- Explicações rotativas sobre conceitos de rede
- Linguagem simples para crianças
- Exemplos práticos (ex: "1 hora de Netflix HD = 3GB")

---

## 🚀 Como Usar

### Requisitos

#### **v2.0 - Plugin System** (Recomendado)

```bash
# Instalar TODAS as dependências
pip3 install -r requirements-v2.txt

# ⚠️ CRÍTICO: psutil é OBRIGATÓRIO para SystemPlugin e NetworkPlugin
# Se psutil não estiver instalado, plugins de sistema/rede NÃO funcionarão
pip3 install psutil>=5.9.0

# Verificar instalação
python3 -c "import psutil; print(f'psutil {psutil.__version__} OK')"
```

#### v1.0 - Legacy (Deprecated)

```bash
# Bibliotecas Python (v1.0 - não recomendado)
pip3 install rich plotext asciichartpy scapy netifaces
```

### Executar

#### Modo Simulado (sem root)
```bash
python3 main.py --mock
```
**Perfeito para desenvolvimento e testes!**

#### Modo Real (com root - dados REAIS)
```bash
sudo python3 main.py
```
**Captura pacotes reais da rede!**

#### Com interface específica
```bash
sudo python3 main.py -i wlan0
```

---

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| `Q` | Sair do dashboard |
| `P` | Pausar/Continuar |
| `R` | Reset estatísticas |
| `H` | Ajuda |

---

## 📁 Estrutura do Projeto

```
wifi_security_education/
├── main.py                          # 🚀 Entry point principal
│
├── models/                          # 📊 Modelos de dados
│   ├── __init__.py
│   └── network_snapshot.py          # WiFiInfo, DeviceInfo, AppInfo, SystemMetrics
│
├── data_collectors/                 # 📡 Coletores de dados
│   ├── __init__.py
│   ├── system_collector.py          # CPU, RAM, Temp (psutil)
│   ├── wifi_collector.py            # SSID, sinal, segurança (iwconfig)
│   └── network_sniffer.py           # Dispositivos e apps (Scapy)
│
├── renderers/                       # 🎨 Renderizadores visuais
│   ├── __init__.py
│   ├── chart_renderer.py            # Gráficos (plotext)
│   ├── table_renderer.py            # Tabelas (Rich)
│   └── progress_renderer.py         # Barras de progresso
│
├── themes/                          # 🎨 Sistema de cores
│   ├── __init__.py
│   └── colors.py                    # Paleta educacional
│
└── README.md                        # 📖 Este arquivo
```

---

## 🎨 Paleta de Cores Educacionais

### Cores Principais
- **Cyan brilhante** `#00D9FF` - WiFi, rede
- **Verde neon** `#00FF88` - Tudo OK, seguro
- **Laranja vibrante** `#FF6B35` - Atenção
- **Rosa forte** `#FF3366` - Perigo!
- **Amarelo ouro** `#FFD93D` - Aviso

### Cores por Tipo
- 📱 **Smartphone**: Laranja
- 💻 **Computador**: Cyan
- 🏠 **IoT/Smart**: Roxo
- ❓ **Desconhecido**: Cinza

### Cores por App
- ▶️ **YouTube**: Vermelho `#FF0000`
- 🎬 **Netflix**: Vermelho escuro `#E50914`
- 💬 **WhatsApp**: Verde `#25D366`
- 🌐 **Chrome**: Azul `#4285F4`
- 🦊 **Firefox**: Laranja `#FF7139`

---

## 📚 Conceitos Educacionais

### 🔒 Segurança WiFi

| Tipo | Segurança | Explicação |
|------|-----------|------------|
| **WPA3** | 🔒 MUITO SEGURO | Criptografia mais forte! |
| **WPA2** | 🔐 SEGURO | Boa segurança |
| **WPA** | ⚠️ FRACA | Segurança antiga |
| **Open** | 🚨 INSEGURO! | SEM proteção! |

### 📻 Frequências WiFi

| Frequência | Alcance | Velocidade | Melhor Para |
|------------|---------|------------|-------------|
| **2.4 GHz** | 🟢 Maior | 🟡 Médio | Casas grandes |
| **5 GHz** | 🟡 Menor | 🟢 Rápido | Mesma sala |
| **6 GHz** | 🔴 Pequeno | 🟢 Muito rápido | WiFi 6E |

### 📊 Unidades de Dados

```
1 KB  = 1,024 Bytes
1 MB  = 1,024 KB = 1,048,576 Bytes
1 GB  = 1,024 MB
1 TB  = 1,024 GB
```

**Exemplos práticos:**
- 📧 Email simples: ~50 KB
- 🎵 Música MP3 (3 min): ~3 MB
- 📺 Netflix HD (1 hora): ~3 GB
- 🎮 Jogo AAA: 50-100 GB

---

## 🔬 Como Funciona?

### 1. Coleta de Dados

#### Sistema (sem root)
- **psutil** para CPU, RAM, Disco, Temperatura
- Fallback: simulação realista se não disponível

#### WiFi (sem root)
- **iwconfig** para SSID, sinal, frequência
- **iw** para detalhes adicionais (canal, etc)
- **ip** para endereço IP
- Fallback: simulação se comandos não disponíveis

#### Rede (requer root para dados reais)
- **Scapy** para captura de pacotes
- Detecta dispositivos por IP/MAC
- Identifica apps por domínio DNS e portas
- Mock mode: simula 5 dispositivos + apps populares

### 2. Renderização

#### Rich Library
- **Layouts** responsivos (redimensiona com terminal)
- **Live rendering** a 4 FPS
- **Tabelas** com cores contextuais
- **Painéis** organizados

#### Plotext
- **Line charts** para tráfego em tempo real
- **Bar charts** para consumo por app
- **Histogramas** para distribuições

#### Cores Dinâmicas
- CPU: verde < 30%, amarelo 30-70%, laranja 70-90%, vermelho > 90%
- RAM: mesma lógica
- Sinal WiFi: verde > 80%, amarelo 60-80%, laranja 40-60%, vermelho < 40%

---

## 🎯 Para os Pais

### O Que Seus Filhos Vão Aprender

1. **WiFi não é mágica** - É ondas de rádio!
2. **Segurança importa** - WPA3 protege seus dados
3. **Internet tem custos** - Apps consomem dados
4. **Dispositivos conversam** - Packets viajam pela rede
5. **Monitoramento é útil** - Detectar problemas cedo

### Discussões Educacionais Sugeridas

- **Por que alguns apps usam mais dados?**
  - Vídeos HD precisam de muitos bits!
  
- **Por que WiFi 5GHz não alcança longe?**
  - Ondas altas não atravessam paredes bem
  
- **O que é criptografia?**
  - É como falar em código secreto!
  
- **Por que senha forte importa?**
  - Para que ninguém "roube" seu WiFi

---

## 🐛 Solução de Problemas

### Dashboard não inicia
```bash
# Verifica bibliotecas
python3 -c "import rich, plotext, scapy; print('OK')"

# Se falhar, reinstala
pip3 install rich plotext scapy --user
```

### "Permission denied" ao capturar pacotes
```bash
# Execute com sudo
sudo python3 main.py

# OU use modo mock
python3 main.py --mock
```

### Interface não detectada
```bash
# Lista interfaces
ip link show

# Especifica manualmente
sudo python3 main.py -i wlan0
```

### Gráficos não aparecem
- Terminal muito pequeno? Redimensione para 160x40 ou maior
- Fontes suportam Unicode? Troque fonte do terminal

---

## 📖 Referências Educacionais

### Para Crianças
- 📺 [How Does WiFi Work? (YouTube Kids)](https://youtube.com)
- 📚 Livro: "Computer Coding for Kids" (DK)
- 🎮 Code.org - Aprenda programação

### Para Pais
- 📄 [Internet Security for Families (EFF)](https://eff.org)
- 📄 [Router Security Basics](https://www.cisa.gov)

---

## 🔮 Roadmap Futuro

### v1.1 (Próxima versão)
- [ ] Histórico de 24 horas
- [ ] Exportar relatórios PDF
- [ ] Alertas sonoros (opcional)
- [ ] Modo "Explicação Detalhada"

### v2.0 (Médio prazo)
- [ ] Web interface para tablets
- [ ] Comparação com outros dias
- [ ] Quiz educacional integrado
- [ ] Modo multiplayer (irmãos competem)

### v3.0 (Longo prazo)
- [ ] Gamificação completa
- [ ] Achievements educacionais
- [ ] Mini-jogos sobre redes
- [ ] Suporte multilíngue

---

## 💖 Créditos

**Desenvolvido com amor por Juan-Dev**
- 👨‍💻 Arquiteto de Software
- 🔬 Cientista Biomédico
- 👨‍👧‍👦 Pai de 2 crianças curiosas

**Soli Deo Gloria** ✝️

### Tecnologias Usadas
- **Rich** - Terminal UIs lindas
- **Plotext** - Gráficos em terminal
- **Scapy** - Análise de pacotes
- **Python 3.10+** - Linguagem base

### Inspirações
- **Sampler** - Dashboard multi-painel
- **htop** - Monitor de recursos
- **iftop** - Monitor de rede

---

## 📜 Licença

MIT License - Livre para uso educacional!

**Condições especiais:**
- ✅ Use para ensinar seus filhos
- ✅ Modifique como quiser
- ✅ Compartilhe com outras famílias
- ❤️ Se ajudou, mande feedback!

---

## 📞 Contato & Suporte

**Issues**: GitHub Issues
**Discussões**: GitHub Discussions
**Email**: [Seu email]

---

**Feito com ❤️, ☕ e muito 🎨 para educar a próxima geração de tech-savvy kids!**

*"A melhor forma de aprender é vendo em tempo real!" - Juan-Dev*
