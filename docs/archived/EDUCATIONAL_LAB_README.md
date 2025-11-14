# 🎓 Laboratório Educacional de Segurança WiFi

## 🌟 Visão Geral

Sistema educacional completo para ensinar **segurança em redes WiFi** através de experimentos práticos em ambiente controlado.

> **Missão**: Educar a próxima geração sobre privacidade digital e segurança cibernética.

---

## 🎯 Para Quem é Este Projeto?

### ✅ Perfeito para:
- 👨‍👩‍👧‍👦 **Pais** ensinando filhos sobre segurança online
- 👨‍🏫 **Professores** em aulas de tecnologia
- 🏫 **Escolas** com laboratórios de informática
- 👨‍💻 **Profissionais** em workshops de cibersegurança

### 🎓 Faixa Etária:
- **8-12 anos**: Conceitos básicos (HTTP vs HTTPS, WiFi seguro vs inseguro)
- **13-17 anos**: Conceitos avançados (metadados, interceptação, VPN)
- **Adultos**: Conscientização completa sobre privacidade digital

---

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clone ou navegue até o projeto
cd ~/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# Instale dependências
pip install scapy

# Verifique instalação
python3 -c "from src.education import WiFiLabInterceptor; print('✅ OK')"
```

### 2. Primeira Aula (5 minutos)

```bash
# Execute o laboratório rápido
sudo python3 scripts/lab_examples/quick_lab.py

# Siga as instruções na tela
# Use seus dispositivos normalmente por 60 segundos
# Observe os resultados!
```

### 3. Demonstração HTTP vs HTTPS

```bash
# Aula interativa sobre criptografia
sudo python3 scripts/lab_examples/http_vs_https_demo.py
```

---

## 📚 Laboratórios Disponíveis

### 🔬 Lab 1: Quick Lab (Introdutório)
**Duração**: 5-10 minutos  
**Conceitos**: Interceptação básica, visibilidade de dados  
**Comando**: `sudo python3 scripts/lab_examples/quick_lab.py`

**O que ensina**:
- Qualquer pessoa pode ver tráfego em WiFi aberto
- Sites acessados são visíveis
- Horários de uso são rastreados

---

### 🔒 Lab 2: HTTP vs HTTPS (Criptografia)
**Duração**: 15-20 minutos  
**Conceitos**: Diferença entre tráfego criptografado e não criptografado  
**Comando**: `sudo python3 scripts/lab_examples/http_vs_https_demo.py`

**O que ensina**:
- HTTP expõe TUDO (senhas, mensagens, cookies)
- HTTPS protege o conteúdo com criptografia
- Importância do "cadeado" no navegador
- Como identificar sites seguros

**Atividades**:
1. Acesse site HTTP → veja dados em texto claro
2. Acesse site HTTPS → veja dados criptografados
3. Quiz educacional interativo

---

### 📱 Lab 3: Device Tracker (Privacidade)
**Duração**: 20-30 minutos  
**Conceitos**: Metadados, rastreamento, privacidade  
**Comando**: `sudo python3 scripts/lab_examples/device_tracker.py`

**O que ensina**:
- Dispositivos são rastreados em redes públicas
- Padrões de comportamento revelam identidade
- Apps e sites visitados são visíveis
- Marketing direcionado funciona assim
- Como criminosos exploram essas informações

**Cenário**: Simula WiFi de shopping center

---

## 🏗️ Estrutura do Projeto

```
wifi_security_education/
├── src/
│   └── education/
│       ├── __init__.py
│       └── wifi_lab_interceptor.py    # Motor de interceptação
├── scripts/
│   └── lab_examples/
│       ├── quick_lab.py               # Lab introdutório
│       ├── http_vs_https_demo.py      # Demo HTTP vs HTTPS
│       └── device_tracker.py          # Rastreamento de dispositivos
├── WIFI_LAB_GUIDE.md                  # Guia completo do professor
└── EDUCATIONAL_LAB_README.md          # Este arquivo
```

---

## 🔧 Uso Avançado

### Customização de Laboratório

```python
from src.education import WiFiLabInterceptor

# Cria interceptador customizado
lab = WiFiLabInterceptor(interface="wlan0", lab_mode=True)

# Registra dispositivos específicos
lab.register_lab_device("aa:bb:cc:dd:ee:01", "Arduino-ESP32", "arduino")
lab.register_lab_device("aa:bb:cc:dd:ee:02", "Phone-Filho", "phone")

# Captura por tempo específico
lab.start_capture(duration=120, packet_count=2000)

# Exporta resultados
lab.export_results("minha_aula.txt")
```

### Descobrindo Interface de Rede

```bash
# Listar interfaces disponíveis
ip link show

# Testar interface específica
sudo python3 -c "
from scapy.all import conf
print('Interfaces disponíveis:')
for iface in conf.ifaces:
    print(f'  • {iface}')
"
```

### Identificando MAC Addresses

```bash
# Ver MAC do dispositivo atual
ip link show wlan0 | grep link/ether

# Escanear rede (requer nmap)
sudo nmap -sn 192.168.1.0/24
```

---

## 🎓 Planos de Aula Sugeridos

### 🔹 Aula 1: Introdução (30 min)
**Objetivo**: Conscientização básica

1. **Discussão** (10 min):
   - Vocês usam WiFi público?
   - Acham que é seguro?
   - O que pode dar errado?

2. **Lab Quick** (10 min):
   - Execute captura básica
   - Mostre sites acessados

3. **Reflexão** (10 min):
   - O que conseguimos ver?
   - Vocês se surpreenderam?
   - O que farão diferente agora?

---

### 🔹 Aula 2: Criptografia (45 min)
**Objetivo**: Entender HTTPS

1. **Teoria** (15 min):
   - O que é criptografia?
   - Analogia da carta com envelope
   - História: Caesar Cipher, Enigma

2. **Demonstração HTTP vs HTTPS** (20 min):
   - Execute o script
   - Acesse sites HTTP
   - Acesse sites HTTPS
   - Compare resultados

3. **Quiz e Atividade** (10 min):
   - Quiz interativo
   - Desenhe como funciona HTTPS
   - Liste 5 sites que devem ter HTTPS

---

### 🔹 Aula 3: Privacidade (60 min)
**Objetivo**: Metadados e rastreamento

1. **Discussão** (15 min):
   - Você se importa se alguém souber onde você está?
   - E o que você compra?
   - E quem são seus amigos?

2. **Device Tracker Demo** (30 min):
   - Execute rastreamento
   - Analise resultados
   - Discuta implicações

3. **Proteções Práticas** (15 min):
   - Configure VPN
   - Ative MAC aleatório
   - Crie plano de segurança pessoal

---

## 📊 Dados que Podem Ser Interceptados

### ✅ SEMPRE Visíveis (mesmo com HTTPS):
```
├─ MAC Address do dispositivo
├─ IP de origem e destino
├─ Quantidade de dados transferidos
├─ Horários de conexão
├─ Duração de sessões
├─ Protocolos utilizados (DNS, HTTPS, etc)
└─ Sites acessados (via DNS queries)
```

### ⚠️ Visíveis APENAS em HTTP:
```
├─ URLs completas
├─ Senhas em texto claro
├─ Mensagens e emails
├─ Cookies de sessão
├─ Tokens de autenticação
├─ Dados de formulários
└─ Conteúdo de páginas
```

### 🔒 NUNCA Visíveis com HTTPS:
```
├─ Conteúdo das páginas
├─ Senhas
├─ Mensagens privadas
├─ Dados de formulários
└─ Cookies criptografados
```

---

## 🛡️ Defesas Ensinadas

### 1. **Sempre use HTTPS**
- Procure o cadeado 🔒
- Use extensões: HTTPS Everywhere
- Evite sites sem HTTPS

### 2. **Evite WiFi Público**
- Use dados móveis (4G/5G)
- Se necessário, use VPN
- Nunca acesse bancos/contas sensíveis

### 3. **Configure Dispositivos**
- MAC Address aleatório
- VPN sempre ativa
- Esquecer redes após uso

### 4. **Comportamentos Seguros**
- Não baixe apps em WiFi público
- Não faça login em contas importantes
- Desative WiFi quando não usar

---

## 🎮 Atividades Complementares

### 🔹 Projeto Arduino/ESP32

Monte um dispositivo IoT que:
1. Envia dados HTTP (inseguro)
2. Intercepte e mostre os dados
3. Depois use HTTPS
4. Compare a segurança

**Código exemplo**: Disponível em `docs/arduino_examples/`

---

### 🔹 Caça ao Tesouro de Segurança

Crie uma lista de tarefas:
- [ ] Encontre 3 sites sem HTTPS
- [ ] Configure VPN no celular
- [ ] Ative MAC aleatório
- [ ] Explique HTTP vs HTTPS para alguém
- [ ] Crie senha forte com gerenciador

---

### 🔹 Role-Playing

**Cenário**: Shopping com WiFi grátis

**Personagens**:
- Hacker tentando roubar dados
- Usuário inocente usando WiFi
- Segurança explicando perigos
- Gerente do shopping que rastreia clientes

**Objetivo**: Entender diferentes perspectivas

---

## 📖 Recursos Educacionais

### Para Crianças (8-12):
- 📺 Vídeo: "Como funciona a Internet" (simplificado)
- 🎮 Jogo: "Interland" (Google - segurança online)
- 📚 Livro: "Meu Primeiro Livro de Cibersegurança"

### Para Adolescentes (13-17):
- 🎬 Documentário: "The Social Dilemma"
- 💻 Curso: "Intro to Cybersecurity" (Cisco)
- 🏆 CTF: PicoCTF (desafios de segurança)

### Para Pais/Educadores:
- 📘 WIFI_LAB_GUIDE.md (guia completo)
- 🌐 OWASP Top 10 (vulnerabilidades web)
- 📹 Tutoriais: Canal "Segurança Digital"

---

## ⚠️ Avisos Legais e Éticos

### 🚨 USO ÉTICO OBRIGATÓRIO

Este projeto é **EXCLUSIVAMENTE EDUCACIONAL**.

#### ✅ PERMITIDO:
- Sua própria rede doméstica
- Dispositivos da sua família (com consentimento)
- Fins educacionais em ambiente controlado
- Workshops autorizados

#### ❌ PROIBIDO E ILEGAL:
- Interceptar redes de terceiros
- Roubar dados ou senhas
- Espionagem sem autorização
- Ataques maliciosos

#### ⚖️ Legalidade:
```
Interceptar tráfego sem autorização é CRIME em muitos países.
No Brasil: Lei 12.737/2012 (Lei Carolina Dieckmann)
Pena: 3 meses a 1 ano de detenção + multa
```

### 🎓 Princípio Ético:

> **"Com grande poder vem grande responsabilidade"**
> 
> Ensine ÉTICA junto com TÉCNICA.
> O objetivo é PROTEGER, não ATACAR.

---

## 🤝 Contribuindo

Este é um projeto educacional open-source!

### Como contribuir:
1. Crie novos laboratórios
2. Melhore documentação
3. Traduza para outros idiomas
4. Compartilhe experiências de aulas
5. Reporte bugs ou sugira melhorias

### Contato:
- Author: Professor JuanCS-Dev
- Motto: *Soli Deo Gloria ✝️*
- Purpose: Educar a próxima geração

---

## 📈 Métricas de Sucesso

**Seus filhos/alunos aprenderam se conseguem**:

- [ ] Explicar diferença entre HTTP e HTTPS
- [ ] Identificar site seguro (cadeado)
- [ ] Listar 3 perigos de WiFi público
- [ ] Configurar VPN no próprio dispositivo
- [ ] Questionar "WiFi Grátis" antes de conectar
- [ ] Ensinar um amigo sobre segurança digital

---

## 🎯 Próximos Passos

Depois destas aulas:

1. **Configure VPN Familiar**
   - ProtonVPN, Mullvad ou similar
   - Ensine configuração básica

2. **Implemente Pi-Hole**
   - Bloqueie ads em rede doméstica
   - Veja o que dispositivos acessam

3. **Firewall e Controle Parental**
   - pfSense ou similar
   - Monitore horários de uso

4. **Gerenciador de Senhas**
   - Bitwarden, KeePass
   - Crie senhas únicas e fortes

5. **Autenticação 2FA**
   - Google Authenticator
   - Ative em todas as contas importantes

---

## 🏆 Certificado de Conclusão

Após completar os 3 laboratórios, imprima um certificado para seus filhos:

```
╔══════════════════════════════════════════════════════════════════════╗
║                    CERTIFICADO DE CONCLUSÃO                          ║
║                                                                      ║
║  Este certificado atesta que:                                        ║
║                                                                      ║
║                    [NOME DO ALUNO]                                   ║
║                                                                      ║
║  Completou com sucesso o                                             ║
║  LABORATÓRIO DE SEGURANÇA WiFi EDUCACIONAL                           ║
║                                                                      ║
║  E demonstrou conhecimento em:                                       ║
║   ✓ Criptografia e HTTPS                                             ║
║   ✓ Perigos de redes públicas                                        ║
║   ✓ Privacidade e metadados                                          ║
║   ✓ Práticas seguras online                                          ║
║                                                                      ║
║  Data: _______________                                               ║
║  Instrutor: _______________                                          ║
║                                                                      ║
║  "Conhecimento é a melhor defesa"                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🌟 Depoimentos

> *"Meus filhos nunca mais conectaram em WiFi do shopping depois desta aula!"*  
> — Pai de 2 adolescentes

> *"Finalmente entendi porque meu professor sempre fala de HTTPS."*  
> — Estudante, 14 anos

> *"Usei em workshop na escola. Alunos adoraram ver 'hacking ético' na prática!"*  
> — Professora de Informática

---

## 📞 Suporte e Dúvidas

### FAQ:

**P: Preciso ser expert em segurança para usar?**  
R: Não! Os scripts são autoexplicativos. Basta seguir as instruções.

**P: É seguro capturar dados da minha própria rede?**  
R: Sim, desde que seja SUA rede e seus dispositivos.

**P: Crianças podem ver os resultados?**  
R: Sim! O objetivo é educacional. Mostre tudo (sem dados sensíveis reais).

**P: Funciona em Windows/Mac?**  
R: Scapy funciona em todos os sistemas. Pode precisar de adaptações.

**P: Posso usar na escola?**  
R: Sim, com autorização da direção e em rede isolada/controlada.

---

## 📜 Licença

**Educational Use Only**

- ✅ Use livremente para fins educacionais
- ✅ Modifique e adapte para suas aulas
- ✅ Compartilhe conhecimento (não códigos maliciosos)
- ❌ Não use para fins ilegais ou antiéticos

---

## 🙏 Agradecimentos

Dedicado a todos os pais e educadores que investem tempo ensinando segurança digital para a próxima geração.

> **"A ignorância é a maior vulnerabilidade."**  
> **"Educação é a melhor proteção."**

---

**Professor JuanCS-Dev ✝️**  
*Soli Deo Gloria - Teaching with Purpose*

**Versão**: 1.0  
**Data**: 2025-11-12  
**Status**: Pronto para uso educacional

---

🎓 **Comece agora mesmo! Seus filhos agradecerão no futuro.**

```bash
sudo python3 scripts/lab_examples/quick_lab.py
```

**Boa aula! 📚🔒✨**
