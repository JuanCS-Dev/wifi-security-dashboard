# 📦 Analisador de Pacotes (Wireshark-style)

## 🎯 O Que É?

O **PacketTable** é um componente visual inspirado no Wireshark que ensina crianças sobre:
- 📊 Protocolos de internet (HTTPS, HTTP, DNS, etc.)
- 🔒 Segurança de navegação (criptografado vs não criptografado)
- 📦 Fluxo de dados na rede doméstica
- ⚠️ Riscos de sites HTTP não seguros

### 🎓 Objetivo Educacional

Mostrar de forma **visual e compreensível** como os dados trafegam pela internet, destacando:
- Protocolos seguros (HTTPS com ✅)
- Protocolos inseguros (HTTP com ⚠️ warnings)
- Tipos de tráfego (vídeo, mensagens, navegação)

---

## 📸 Exemplo Visual

```
╭───────────────────── Packet Analyzer (Wireshark-style) ─────────────────────╮
│                                                                              │
│  📊 Rate: 85.5 pkts/s  |  Total: 803  |  Backend: mock                       │
│                                                                              │
│  🔝 Top Protocols:                                                           │
│    HTTPS    █████ 442 pkts (55%)                                             │
│    H264     █ 154 pkts (19%)                                                 │
│    DNS      █ 89 pkts (11%)                                                  │
│    QUIC      76 pkts (9%)                                                    │
│    HTTP      31 pkts (4%) ⚠️ Unencrypted!                                     │
│    MDNS      11 pkts (1%)                                                    │
│                                                                              │
│                          📦 Recent Packets                                   │
│  ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓ │
│  ┃ Time       ┃ Source        ┃ Destination   ┃ Protocol ┃ Info            ┃ │
│  ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩ │
│  │ 14:32:15.2 │ 192.168.1.102 │ 142.250.185.4 │ HTTPS    │ Gmail - ✅      │ │
│  │ 14:32:15.4 │ 192.168.1.104 │ 93.184.216.34 │ HTTP     │ ⚠️ Unencrypted!  │ │
│  │ 14:32:15.6 │ 192.168.1.105 │ 54.192.147.14 │ H264     │ Netflix - ✅    │ │
│  │ 14:32:15.8 │ 192.168.1.100 │ 31.13.86.36   │ QUIC     │ WhatsApp - ✅   │ │
│  │ 14:32:16.0 │ 192.168.1.112 │ 142.250.185.4 │ HTTPS    │ YouTube Kids ✅ │ │
│  └────────────┴───────────────┴───────────────┴──────────┴─────────────────┘ │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## 🏗️ Arquitetura

### 1. PacketAnalyzerPlugin

**Localização:** `src/plugins/packet_analyzer_plugin.py`

**Responsabilidade:** Coletar dados de pacotes de rede usando um dos 3 backends:

#### Backends Disponíveis

1. **Scapy** (Preferencial - Real Mode)
   - Análise detalhada de pacotes
   - Requer privilégios elevados
   - Suporte completo a protocolos

2. **PyShark** (Fallback - Real Mode)
   - Wrapper do TShark/Wireshark
   - Dissectores completos
   - Requer instalação do Wireshark

3. **Mock** (Educacional - Mock Mode)
   - Dados simulados coerentes
   - Não requer permissões especiais
   - Perfeito para demonstração

#### Dados Coletados

```python
{
    "top_protocols": {       # Top 10 protocolos por contagem
        "HTTPS": 442,
        "H264": 154,
        "DNS": 89,
        # ...
    },
    "top_sources": {         # Top 10 IPs de origem
        "192.168.1.102": 45,
        # ...
    },
    "top_destinations": {    # Top 10 IPs de destino
        "142.250.185.46": 120,
        # ...
    },
    "packet_rate": 85.5,     # Pacotes por segundo
    "total_packets": 803,    # Total capturado
    "recent_packets": [      # Últimos 5-10 pacotes
        {
            "time": "14:32:15.234",
            "src": "192.168.1.102",
            "dst": "142.250.185.46",
            "protocol": "HTTPS",
            "info": "Gmail - Encrypted ✅",
            "safe": True
        },
        # ...
    ],
    "backend": "mock"        # Backend utilizado
}
```

### 2. PacketTable Component

**Localização:** `src/components/packet_table.py`

**Responsabilidade:** Renderizar visualmente os dados de pacotes coletados

#### Seções Renderizadas

1. **Header** (📊 Rate, Total, Backend)
   - Taxa de pacotes/segundo
   - Total de pacotes capturados
   - Backend utilizado (mock/scapy/pyshark)

2. **Top Protocols** (🔝 Section)
   - Protocolos mais comuns
   - Barras visuais proporcionais
   - Percentuais
   - ⚠️ Warnings para protocolos inseguros

3. **Recent Packets** (📦 Table)
   - Tabela Rich com 5 colunas:
     - **Time**: Timestamp do pacote
     - **Source**: IP de origem
     - **Destination**: IP de destino
     - **Protocol**: Protocolo identificado
     - **Info**: Descrição educacional + segurança

#### Configuração (dashboard.yml)

```yaml
- type: packettable
  title: 'Packet Analyzer (Wireshark-style)'
  position:
    x: 0
    y: 43
    width: 120
    height: 18
  rate_ms: 2000              # Atualizar a cada 2 segundos
  plugin: packet_analyzer    # Plugin de origem
  data_field: all            # Usar todos os dados do plugin
  color: red                 # Cor da borda
  extra:
    show_protocols: true     # Mostrar seção de protocolos
    show_recent: true        # Mostrar tabela de pacotes
    max_protocols: 6         # Máximo de protocolos a mostrar
    max_recent: 5            # Máximo de pacotes recentes
```

---

## 🚀 Como Usar

### Modo Mock (Demonstração)

```bash
# Executar com dados simulados (não requer root)
python3 main_v2.py --mock
```

O PacketTable aparecerá automaticamente mostrando tráfego simulado de uma família típica.

### Modo Real (Captura Real)

⚠️ **Requer privilégios elevados ou configuração de captura sem root**

```bash
# Opção 1: Com sudo (mais simples)
sudo python3 main_v2.py

# Opção 2: Configurar captura sem root (recomendado)
# Ver seção "Configuração Sem Root" abaixo
```

### Configuração Sem Root (Linux)

Para capturar pacotes sem sudo, configure capabilities:

```bash
# Dar permissões ao Python para captura de pacotes
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Verificar
getcap $(which python3)
# Deve mostrar: cap_net_admin,cap_net_raw=eip

# Agora pode executar sem sudo
python3 main_v2.py
```

⚠️ **Atenção:** Isso dá permissões de rede ao binário Python. Use com cautela.

---

## 📊 Dados Educacionais (Mock Mode)

### Protocolos Simulados

O mock mode simula tráfego realista de uma família brasileira:

| Protocolo | % | Descrição Educacional |
|-----------|---|----------------------|
| **HTTPS** | 55% | Sites seguros (cadeado 🔒) |
| **H264** | 19% | Vídeos (Netflix, YouTube) |
| **DNS** | 11% | "Tradutor" de nomes para IPs |
| **QUIC** | 9% | Protocolo moderno (Google) |
| **HTTP** | 4% | ⚠️ Sites SEM criptografia! |
| **MDNS** | 1% | Descoberta de dispositivos locais |

### Dispositivos Simulados

- **192.168.1.100** - Pai-Phone (WhatsApp, Gmail)
- **192.168.1.102** - Dad-Laptop (Trabalho)
- **192.168.1.104** - Smart-TV-Sala (Netflix)
- **192.168.1.105** - Filho-Tablet (YouTube Kids)
- **192.168.1.112** - Filha-Tablet (Netflix Kids)
- **192.168.1.1** - Roteador

### Cenários Educacionais

#### ✅ Seguro (HTTPS)
```
Time: 14:32:15.234
Source: 192.168.1.102 (Laptop do Pai)
Destination: 142.250.185.46 (Google)
Protocol: HTTPS
Info: Gmail - Encrypted ✅

Explicação: "Os emails estão protegidos! Ninguém pode ler no meio do caminho."
```

#### ⚠️ Inseguro (HTTP)
```
Time: 14:32:15.456
Source: 192.168.1.104 (Smart TV)
Destination: 93.184.216.34
Protocol: HTTP
Info: ⚠️ Unencrypted website! Passwords visible!

Explicação: "CUIDADO! Este site não tem cadeado. Senhas podem ser vistas!"
```

---

## 🧪 Testing

### Testes Unitários

```bash
# Rodar todos os testes do PacketAnalyzerPlugin
python3 -m pytest tests/unit/test_packet_analyzer_plugin.py -v

# Rodar testes específicos
python3 -m pytest tests/unit/test_packet_analyzer_plugin.py::TestPacketAnalyzerPluginMock -v
```

### Teste de Integração

```bash
# Executar teste completo de integração PacketTable + Plugin
python3 test_packet_table_integration.py
```

**Saída esperada:**
```
================================================================================
✅ INTEGRAÇÃO COMPLETA: PacketTable renderizado com sucesso!
✅ FASE 1.4 CONCLUÍDA: Validação visual programática OK
================================================================================
```

### Cobertura

```bash
# Gerar relatório de cobertura
python3 -m pytest tests/ --cov=src.plugins.packet_analyzer_plugin --cov=src.components.packet_table --cov-report=html
```

---

## 🎓 Para os Pais: Como Usar Educacionalmente

### Conversas com as Crianças

#### 1. Sobre HTTPS vs HTTP

**Pergunta:** "Por que alguns sites têm ⚠️ vermelho?"

**Resposta:**
> "Vê aquele cadeado 🔒 no navegador? Quando ele está lá, os dados viajam em uma 'caixa trancada' (HTTPS).
>
> Sites sem cadeado (HTTP) são como enviar uma carta ABERTA - qualquer um pode ler no meio do caminho!
>
> NUNCA coloque senhas em sites sem cadeado!"

#### 2. Sobre Protocolos

**Pergunta:** "O que é H264?"

**Resposta:**
> "É o jeito que vídeos viajam pela internet! Quando você assiste Netflix, os dados vêm comprimidos
> (como apertar uma esponja) para caber melhor no WiFi. H264 é o nome dessa 'compressão'."

#### 3. Sobre DNS

**Pergunta:** "Para que serve DNS?"

**Resposta:**
> "Imagine que você quer ligar para a vovó, mas não sabe o número. DNS é como a agenda de contatos da internet!
>
> Você digita 'google.com' (o nome), e o DNS encontra o 'número de telefone' (142.250.185.46) para você."

### Atividades Práticas

#### Atividade 1: Caça aos Protocolos
1. Abrir o dashboard em modo mock
2. Pedir para a criança contar quantos pacotes HTTPS aparecem em 1 minuto
3. Comparar com HTTP
4. **Aprendizado:** "Viu? A maioria dos sites hoje usa HTTPS (seguro)!"

#### Atividade 2: Descobrir Dispositivos
1. Olhar os IPs de origem (Source)
2. Identificar cada dispositivo da família
3. **Aprendizado:** "Cada aparelho tem seu próprio 'endereço' na rede!"

#### Atividade 3: Taxa de Pacotes
1. Observar a taxa de pacotes/segundo
2. Abrir YouTube ou Netflix
3. Ver a taxa aumentar
4. **Aprendizado:** "Vídeo precisa de MUITOS pacotes porque tem muita informação!"

---

## 🔧 Troubleshooting

### Problema: "Permission denied" ao capturar pacotes

**Solução 1:** Executar com sudo
```bash
sudo python3 main_v2.py
```

**Solução 2:** Usar Mock Mode
```bash
python3 main_v2.py --mock
```

**Solução 3:** Configurar capabilities (ver seção "Configuração Sem Root")

### Problema: "ModuleNotFoundError: No module named 'scapy'"

**Solução:**
```bash
pip3 install scapy
# ou
pip3 install -r requirements-v2.txt
```

### Problema: PacketTable mostra "No data"

**Causa:** Plugin não conseguiu coletar pacotes

**Solução:**
1. Verificar se o plugin está habilitado em `config/dashboard.yml`
2. Verificar permissões de captura
3. Tentar Mock Mode para teste:
```bash
python3 main_v2.py --mock
```

### Problema: PyShark não funciona

**Solução:**
```bash
# Ubuntu/Debian
sudo apt-get install tshark wireshark

# Verificar instalação
which tshark
```

---

## 📚 Referências Técnicas

### Protocolos Analisados

- **HTTPS (HTTP Secure):** HTTP sobre TLS/SSL - criptografado
- **HTTP (HyperText Transfer Protocol):** Protocolo web sem criptografia
- **H264 (Advanced Video Coding):** Codec de compressão de vídeo
- **DNS (Domain Name System):** Resolução de nomes para IPs
- **QUIC (Quick UDP Internet Connections):** Protocolo moderno do Google
- **MDNS (Multicast DNS):** Descoberta de serviços locais
- **TLS (Transport Layer Security):** Camada de segurança para HTTPS

### Ferramentas Relacionadas

- **Wireshark:** Analisador de protocolos profissional (inspiração do PacketTable)
- **Scapy:** Biblioteca Python para manipulação de pacotes
- **PyShark:** Wrapper Python do TShark (versão CLI do Wireshark)
- **TShark:** Wireshark em linha de comando

### Documentação Externa

- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [RFC 2818 - HTTP Over TLS](https://tools.ietf.org/html/rfc2818)
- [RFC 1035 - DNS](https://tools.ietf.org/html/rfc1035)

---

## 🎯 Roadmap Futuro

### Sprint 5 (Planejado)

- [ ] Filtros de protocolo (mostrar só HTTPS, só HTTP, etc.)
- [ ] Estatísticas por dispositivo
- [ ] Gráfico de linha temporal de protocolos
- [ ] Exportação de capturas para análise (formato PCAP)

### Sprint 6 (Planejado)

- [ ] Alertas quando HTTP detectado (educacional)
- [ ] Detecção de padrões suspeitos
- [ ] Integração com triggers (visual, som, comando)
- [ ] Dashboard de segurança consolidado

---

## 👨‍💻 Autor

**Juan-Dev** - Soli Deo Gloria ✝️

Criado com ❤️ para ensinar crianças sobre tecnologia e segurança de forma visual e divertida!

---

## 📝 Licença

Projeto educacional - livre para uso educacional e pessoal.

Para uso comercial, favor consultar o autor.

---

## 🙏 Agradecimentos

- **Wireshark Foundation** - Pela inspiração do design
- **Scapy Community** - Pela biblioteca incrível
- **Rich Library (Will McGugan)** - Pela rendering engine maravilhosa
- **Meus filhos** - Por serem a motivação deste projeto! 👨‍👧‍👦
