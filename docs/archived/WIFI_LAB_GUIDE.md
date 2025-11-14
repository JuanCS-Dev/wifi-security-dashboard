# 🎓 Guia do Laboratório WiFi Educacional

## 📚 Objetivo

Ensinar crianças/adolescentes sobre **segurança em redes WiFi** através de experimentos práticos em ambiente controlado.

> **⚠️ IMPORTANTE**: Use APENAS em sua rede doméstica com seus próprios dispositivos!

---

## 🎯 Lições que seus filhos aprenderão

### 1. **HTTP vs HTTPS** - A diferença entre seguro e inseguro
- ✅ HTTPS criptografa dados (cadeado no navegador)
- ❌ HTTP envia tudo em texto claro (qualquer um pode ler)

### 2. **Redes Públicas são PERIGOSAS**
- Demonstra o que pode ser interceptado
- Mostra sites acessados, apps usados
- Explica porque NUNCA usar WiFi de shopping/café

### 3. **Metadados sempre vazam**
- Mesmo HTTPS expõe: horários, IPs, quantidade de dados
- Padrões revelam comportamento

---

## 🛠️ Setup do Laboratório

### Requisitos

1. **Hardware**:
   - Router WiFi (sua rede doméstica)
   - Arduino/ESP32 (opcional, para simular dispositivos IoT)
   - Dispositivos dos filhos (tablets/phones)
   - Laptop para captura

2. **Software**:
   ```bash
   # Instalar dependências
   pip install scapy
   
   # Verificar interface de rede
   ip link show
   ```

### Configuração Inicial

```bash
# 1. Entre no diretório do projeto
cd ~/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# 2. Execute o setup
sudo python3 -m src.education.wifi_lab_interceptor
```

---

## 🎬 Como Conduzir a Aula

### Preparação (5 minutos)

1. **Explique o contexto**:
   ```
   "Vamos fazer um experimento. Vou mostrar o que alguém MAL 
   INTENCIONADO pode ver quando vocês usam WiFi público."
   ```

2. **Registre os dispositivos**:
   ```python
   from src.education import WiFiLabInterceptor
   
   lab = WiFiLabInterceptor(interface="wlan0", lab_mode=True)
   
   # Adicione MAC dos dispositivos (use: ip link show)
   lab.register_lab_device("aa:bb:cc:dd:ee:01", "Phone-Filho1", "phone")
   lab.register_lab_device("aa:bb:cc:dd:ee:02", "Tablet-Filho2", "tablet")
   ```

### Experimento 1: Sites HTTP (10 minutos)

**Objetivo**: Mostrar perigo de sites sem HTTPS

1. **Inicie a captura**:
   ```bash
   sudo python3 lab_session.py
   ```

2. **Peça para acessarem** (em outro dispositivo):
   - Site HTTP: `http://neverssl.com`
   - Observem a captura mostrando TUDO

3. **Depois acesse**:
   - Site HTTPS: `https://google.com`
   - Mostre que dados ficam criptografados

4. **Discussão**:
   ```
   "Viram a diferença? HTTP mostra tudo que vocês digitam.
   SEMPRE procurem o cadeado 🔒 no navegador!"
   ```

### Experimento 2: Apps e DNS (10 minutos)

**Objetivo**: Mostrar o que apps revelam

1. **Peça para abrirem apps normais**:
   - YouTube, Spotify, Jogos
   
2. **Mostre as queries DNS**:
   ```
   "Mesmo sem ver o conteúdo, sabemos que vocês estão:
   - Assistindo YouTube
   - Jogando Minecraft
   - Acessando Instagram"
   ```

3. **Discussão**:
   ```
   "Em WiFi público, qualquer um vê QUAIS apps você usa,
   QUANDO usa, e COM QUEM conversa (pelos IPs)."
   ```

### Experimento 3: Simulação de Ataque (15 minutos)

**Objetivo**: Simular cenário real de cafeteria

1. **Configure cenário**:
   ```
   "Imaginem: vocês estão num shopping com WiFi grátis.
   Vou mostrar o que o DONO do WiFi pode ver..."
   ```

2. **Teste real**:
   - Login em site (use site de teste, não real)
   - Acesse rede social
   - Jogue online

3. **Revele os dados capturados**:
   ```python
   # Mostre o resumo
   lab.export_results("experimento_shopping.txt")
   ```

4. **Discussão**:
   ```
   "Viram? Isso é o que qualquer pessoa com conhecimento
   básico pode fazer. Por isso NUNCA usem WiFi público!"
   ```

---

## 📊 Resultados Típicos

### Dados que SEMPRE vazam:
- ✅ Sites acessados (DNS queries)
- ✅ Apps utilizados
- ✅ Horários de uso
- ✅ Quantidade de dados
- ✅ IPs de destino

### Dados que vazam em HTTP:
- ❌ Senhas
- ❌ Mensagens
- ❌ Cookies de sessão
- ❌ Formulários completos

### Dados que NÃO vazam em HTTPS:
- ✅ Conteúdo da página
- ✅ Senhas
- ✅ Mensagens
- ✅ Dados de formulários

---

## 🎓 Lições Finais para Reforçar

### 1. **Regra de Ouro**
```
NUNCA, EM HIPÓTESE ALGUMA, usar WiFi público aberto!
```

### 2. **Se precisar usar internet fora de casa**:
- ✅ Use dados móveis (4G/5G)
- ✅ Use VPN confiável
- ✅ Use apenas HTTPS
- ❌ NUNCA acesse bancos/senhas

### 3. **Em casa**:
- ✅ Use senha forte no WiFi
- ✅ WPA3 ou WPA2
- ✅ Mude senha regularmente
- ✅ Rede separada para IoT

### 4. **Sinais de alerta**:
- 🚨 WiFi sem senha
- 🚨 Site sem cadeado
- 🚨 Alguém pedindo para "aceitar certificado"
- 🚨 Página de login suspeita

---

## 🔬 Arduino/ESP32 - Dispositivos IoT

### Projeto Extra: Sensor WiFi Educacional

Configure um Arduino para enviar dados e mostre o que pode ser interceptado:

```cpp
// Arduino code
#include <WiFi.h>

void setup() {
  WiFi.begin("SUA_REDE", "SUA_SENHA");
  
  // Envia dados HTTP (inseguro)
  client.println("GET /data HTTP/1.1");
  client.println("Host: exemplo.com");
  client.println("Temperature: 25.5");  // Visível!
  client.println();
}
```

**Lição**: 
- Dispositivos IoT baratos não criptografam
- Smart TVs, lâmpadas, câmeras podem vazar dados
- Sempre use rede separada para IoT

---

## 📝 Scripts Prontos

### Script 1: Captura Rápida
```bash
#!/bin/bash
# quick_lab.sh

echo "🎓 Laboratório WiFi - Sessão Rápida"
echo "Capturando por 30 segundos..."

sudo python3 -c "
from src.education import create_lab_scenario

lab = create_lab_scenario()
lab.start_capture(duration=30)
lab.export_results()
"
```

### Script 2: Análise de Dispositivo Específico
```python
# analyze_device.py

from src.education import WiFiLabInterceptor

lab = WiFiLabInterceptor(interface="wlan0")

# Foque em um dispositivo
lab.register_lab_device("XX:XX:XX:XX:XX:XX", "Phone-Teste", "phone")

print("📱 Analisando apenas este dispositivo...")
lab.start_capture(duration=60)
```

---

## ⚠️ Avisos Legais e Éticos

### ✅ PERMITIDO:
- Sua própria rede doméstica
- Dispositivos da sua família
- Fins educacionais com consentimento

### ❌ PROIBIDO:
- Redes de outras pessoas
- Interceptação sem autorização
- Uso malicioso de dados

### 📜 Responsabilidade:
```
Este laboratório é EXCLUSIVAMENTE educacional.
O autor não se responsabiliza por uso indevido.
Ensine ÉTICA junto com técnica!
```

---

## 🎯 Métricas de Sucesso

**Seus filhos aprenderam se conseguem**:

1. ✅ Identificar site HTTP vs HTTPS
2. ✅ Explicar porque WiFi público é perigoso
3. ✅ Saber quando usar VPN
4. ✅ Verificar cadeado no navegador
5. ✅ Questionar "WiFi Grátis"

---

## 📚 Recursos Adicionais

### Para Crianças (8-12 anos):
- Vídeos: "Como funciona a internet"
- Analogia: "HTTP é carta sem envelope, HTTPS é carta lacrada"

### Para Adolescentes (13-17 anos):
- Documentários sobre cibersegurança
- Projetos práticos com Arduino
- CTF (Capture The Flag) educacionais

### Para Pais:
- Configure controles parentais
- Monitore redes domésticas
- Converse regularmente sobre segurança online

---

## 🏆 Próximos Passos

Depois desta aula, considere:

1. **VPN Familiar**: Configure VPN para toda família
2. **Pi-Hole**: Bloqueie ads e tracking em casa
3. **Firewall**: Ensine sobre proteção de rede
4. **Senha Manager**: Use gerenciador de senhas
5. **2FA**: Ative autenticação de dois fatores

---

## 💬 Discussão Final

**Perguntas para reflexão**:

1. "O que vocês fariam se precisassem usar internet numa viagem?"
2. "Como sabem se um site é seguro?"
3. "O que fazer se um amigo pedir senha do WiFi de casa?"
4. "Por que alguns apps são grátis?"

**Objetivo**: Criar **pensamento crítico** sobre segurança digital.

---

## 🎓 Conclusão

Educação em cibersegurança começa cedo!

```
"A melhor defesa contra ataques cibernéticos 
é uma geração educada digitalmente."
```

**Parabéns por investir na segurança digital dos seus filhos!** 🎉

---

**Author**: Professor JuanCS-Dev ✝️  
**Motto**: *"Soli Deo Gloria - Ensinar com propósito"*  
**Date**: 2025-11-12

**Licença**: Educational Use Only - Compartilhe conhecimento, não códigos maliciosos.
