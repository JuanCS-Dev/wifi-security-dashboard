# 📦 Legacy Code - Dashboard v1.0

**Status:** ARCHIVED - For reference only

Este diretório contém o código original do Dashboard WiFi Security Education **v1.0**, que foi substituído pela arquitetura modular **v2.0**.

---

## 📂 Conteúdo

### main_v1.py
Entry point da versão 1.0 com:
- Banner JUAN colorido (verde → amarelo → azul)
- Interface monolítica
- Modo mock e modo real
- Dashboard educacional completo

### v1_modules/
Módulos da arquitetura v1.0:

```
v1_modules/
├── models/           # NetworkSnapshot, DeviceInfo, AppInfo, etc
├── data_collectors/  # SystemCollector, WiFiCollector, NetworkSniffer
├── renderers/        # ChartRenderer, TableRenderer, ProgressRenderer
└── themes/           # DashboardColors
```

---

## 🚀 Como Executar (Referência)

**⚠️ IMPORTANTE:** Use a versão v2.0 no diretório principal!

Se realmente precisar executar a v1.0:

```bash
# Modo mock (simulado)
cd docs/legacy
python3 main_v1.py --mock

# Modo real (requer sudo)
sudo python3 main_v1.py
```

---

## 🔄 Migração v1.0 → v2.0

### O que mudou:

| v1.0 (Legacy) | v2.0 (Atual) |
|---------------|--------------|
| Monolítico | Plugin-based |
| Hardcoded components | YAML config |
| models/ local | src/core/ |
| Sem testes | 352 testes (96% coverage) |
| Banner em classe | Banner em função |

### Banner JUAN
O banner colorido **foi migrado para v2.0** em `main_v2.py:show_juan_banner()`

---

## 📊 Métricas v1.0

- **Linhas de código:** ~2,717
- **Testes:** 18 funcionais
- **Coverage:** Não medido
- **Conformidade:** 100% Vértice v3.0 (na época)

---

## ✅ Por Que v2.0 é Melhor?

1. **Modular:** Plugin system extensível
2. **Testado:** 352 testes, 96% coverage
3. **Configurável:** YAML config files
4. **Escalável:** Adicione plugins sem código
5. **Mantível:** Separação de responsabilidades
6. **Documentado:** 15+ arquivos de docs

---

## 📜 Histórico

- **2025-11-08:** v1.0 criada com banner JUAN
- **2025-11-09:** Sprint 1-3 (v2.0) completados
- **2025-11-10:** v1.0 arquivada, banner migrado para v2.0

---

**Soli Deo Gloria ✝️**

---

**Use a v2.0 no diretório principal!**
