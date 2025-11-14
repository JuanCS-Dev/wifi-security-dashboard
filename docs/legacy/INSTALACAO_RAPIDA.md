# ⚡ Instalação Rápida - Dashboard WiFi Educacional

## 🚀 3 Passos Para Começar!

### Passo 1: Instalar Dependências
```bash
# Opção A: pip (recomendado)
pip3 install rich plotext asciichartpy scapy netifaces --user

# Opção B: apt (Debian/Ubuntu)
sudo apt-get update
sudo apt-get install python3-rich python3-scapy
pip3 install plotext asciichartpy netifaces --user
```

### Passo 2: Executar!
```bash
cd "/home/maximus/Área de trabalho/REDE_WIFI"
./run_educational_dashboard.sh
```

### Passo 3: Aproveitar! 🎉
- Dashboard aparece em tela cheia
- Observe os dados em tempo real
- Mostre para seus filhos!

---

## 🔧 Solução Rápida de Problemas

### Erro: "No module named 'rich'"
```bash
pip3 install rich --user
```

### Erro: "Permission denied" no script
```bash
chmod +x run_educational_dashboard.sh
```

### Erro: Interface não encontrada
```bash
# Lista interfaces disponíveis
ip link show

# Use interface específica
cd wifi_security_education
python3 main.py -i wlan0
```

### Dashboard não aparece corretamente
- Aumente o terminal: mínimo 120x40 caracteres
- Use fonte com suporte Unicode
- Fundo escuro recomendado

---

## 📋 Requisitos Mínimos

- **Python**: 3.8+
- **Terminal**: 120x40 caracteres
- **Sistema**: Linux (Debian/Ubuntu testado)
- **Memória**: 100 MB RAM
- **Root**: Opcional (para dados reais)

---

## ✅ Verificação Rápida

```bash
# Testa se tudo está OK
python3 << 'EOF'
try:
    import rich, plotext, scapy
    print("✅ Todas bibliotecas instaladas!")
except ImportError as e:
    print(f"❌ Faltando: {e}")
EOF
```

---

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| `Q` | Sair |
| `P` | Pausar/Continuar |
| `R` | Reset |

---

## 📞 Suporte

Se tiver problemas:
1. Verifique README.md completo
2. Veja PARA_AS_CRIANCAS.md
3. Consulte MISSAO_COMPLETA.md

---

**Pronto! Agora é só curtir com seus filhos!** 🎉
