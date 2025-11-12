# 🚀 TESTE AGORA - Laboratório WiFi Educacional

## ⚡ Para Testar em 30 Segundos

```bash
# 1. Abra um terminal

# 2. Vá para o diretório
cd ~/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# 3. Execute o menu
./START_LAB.sh
```

---

## 🎯 Opções de Teste

### Opção A: Menu Interativo (Mais Fácil)
```bash
./START_LAB.sh
```
- Escolha opção 1, 2 ou 3
- Siga instruções na tela

### Opção B: Teste Direto (Quick Lab)
```bash
sudo python3 scripts/lab_examples/quick_lab.py
```
- Captura por 60 segundos
- Use seu celular normalmente
- Veja resultados!

### Opção C: Teste Programático
```bash
python3 << 'PYEOF'
from src.education import WiFiLabInterceptor

lab = WiFiLabInterceptor(interface="wlan0", lab_mode=True)
print("✅ Módulo carregado com sucesso!")
print(f"📊 Stats iniciais: {lab.stats}")
PYEOF
```

---

## 🧪 Checklist de Teste

- [ ] Módulo importa sem erros
- [ ] Menu interativo funciona
- [ ] Quick Lab executa
- [ ] Capturas funcionam (com sudo)
- [ ] Resultados são exibidos
- [ ] Exportação funciona

---

## 📝 Suas Instruções para os Filhos

Quando for fazer a aula:

```
🎓 "Filhos, hoje vamos fazer um experimento de segurança.
    Vou mostrar o que alguém MAL INTENCIONADO pode ver
    quando vocês usam WiFi em lugares públicos."

1. Execute: ./START_LAB.sh
2. Escolha Lab 1 (Quick Lab)
3. Peça para usarem celular/tablet
4. Deixe captura rodar 60s
5. Mostre resultados
6. DISCUTA!
```

**Perguntas para fazer**:
- "Vocês se surpreenderam?"
- "O que pode dar errado em WiFi público?"
- "Como podemos nos proteger?"

---

## ⚠️ Se Precisar de Ajuda

### Erro: "Permission denied"
```bash
# Use sudo
sudo python3 scripts/lab_examples/quick_lab.py
```

### Erro: "Interface not found"
```bash
# Descubra sua interface:
ip link show

# Edite os scripts e troque "wlan0" pela sua
```

### Erro: "No module named scapy"
```bash
pip install scapy
# ou
pip3 install scapy
```

---

## 📚 Documentação de Apoio

1. **QUICK_START.md** - Guia rápido
2. **PARA_OS_PAIS.md** - Roteiro completo de aula
3. **EDUCATIONAL_LAB_README.md** - Documentação técnica
4. **WIFI_LAB_GUIDE.md** - Manual do professor

---

## 🎯 Objetivo da Aula

Ensinar aos filhos:
```
NUNCA se conectar em WiFi público aberto!
SEMPRE verificar HTTPS (cadeado 🔒)
Usar VPN ou dados móveis quando necessário
```

---

## 🏆 Após a Aula

- [ ] Discutir resultados
- [ ] Configurar VPN nos dispositivos
- [ ] Criar "plano de segurança familiar"
- [ ] Imprimir certificado (em PARA_OS_PAIS.md)

---

## 💬 Feedback

Depois de testar, reflita:
- ✅ Sistema funcionou?
- ✅ Crianças entenderam?
- ✅ Mudaram comportamento?

---

**Professor JuanCS-Dev ✝️**

🎓 **COMECE AGORA! BOA AULA!** 🎓

```bash
./START_LAB.sh
```
