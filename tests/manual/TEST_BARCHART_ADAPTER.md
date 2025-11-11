# Manual Test: Barchart Adapter

**Sprint:** 4 (Bar Charts)
**Author:** Dev Sênior Rafael
**Date:** 2025-11-11
**Status:** ✅ Código Implementado - Aguarda Teste Manual

---

## Objetivo

Validar que o BarchartAdapter funciona corretamente, gerando gráficos de barras para dados categóricos com plotext.

## Pré-requisitos

- ✅ BarchartAdapter implemented (src/adapters/barchart_adapter.py)
- ✅ plotext compatibility validado (Sprint 1)
- ✅ Config de teste criado (config/test_barchart_pycui.yml)

## Comando de Teste

```bash
cd /home/maximus/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# Teste com mock data
python3 main_v2.py --config config/test_barchart_pycui.yml --pycui-mode --mock
```

## Resultado Esperado

Devem aparecer 2 barcharts:

### Barchart 1: Protocol Distribution
- **Posição:** (x=0, y=0), 80x30
- **Título:** "Protocol Distribution"
- **Conteúdo:** Barras horizontais mostrando protocolos (HTTPS, DNS, HTTP, H264, QUIC, etc)
- **Orientação:** Horizontal (barras da esquerda para direita)
- **Cor:** Blue
- **Max bars:** 8 protocolos
- **Taxa:** Atualiza a cada 2 segundos

**Exemplo esperado:**
```
Protocol Distribution
┌────────────────────────────────
│ HTTPS ███████████████ 450
│   DNS ████ 89
│  HTTP █ 32
│  H264 ██████ 156
│  QUIC ██ 78
└────────────────────────────────
```

### Barchart 2: Top Source IPs
- **Posição:** (x=0, y=35), 80x25
- **Título:** "Top Source IPs"
- **Conteúdo:** Barras verticais mostrando top 5 IPs
- **Orientação:** Vertical (barras de baixo para cima)
- **Cor:** Yellow
- **Max bars:** 5 IPs
- **Taxa:** Atualiza a cada 3 segundos

## Validação Visual

- [ ] Dashboard inicia sem erros
- [ ] 2 barcharts visíveis
- [ ] Posições corretas (um acima, outro abaixo)
- [ ] Títulos corretos
- [ ] **Barchart 1:** Barras horizontais
- [ ] **Barchart 2:** Barras verticais
- [ ] Cores blue e yellow aplicadas
- [ ] Labels truncados se longos (>20 ou >15 chars)
- [ ] Valores numéricos mostrados
- [ ] Barras ordenadas por valor (maior primeiro)

## Detalhes Técnicos

### plotext Bar Charts
```python
# Horizontal
plt.bar(categories, values, orientation="horizontal")

# Vertical
plt.bar(categories, values, orientation="vertical")

# Output capture (mesmo do Runchart)
output = io.StringIO()
sys.stdout = output
plt.show()
sys.stdout = old_stdout
chart_text = output.getvalue()
```

### Features Implementadas
- ✅ Categorical data parsing (dict or list of tuples)
- ✅ Orientation (horizontal/vertical)
- ✅ Max bars limit (top N)
- ✅ Label truncation (max_label_length)
- ✅ Sorting by value (descending)
- ✅ Color mapping
- ✅ Graceful error handling

## Troubleshooting

### Barras não aparecem
**Causa:** Plugin não fornecendo dados categóricos
**Solução:** Verificar mock mode habilitado, PacketAnalyzerPlugin ativo

### Erro: "cannot unpack non-iterable"
**Causa:** Data format incorreto (não é dict nem lista)
**Solução:** Verificar que plugin retorna `{'label': value}` ou `[(label, value)]`

### Barras todas com mesmo tamanho
**Causa:** Valores todos iguais ou plotext scaling issue
**Solução:** Verificar que mock data gera valores variados

## Diferenças: Runchart vs Barchart

| Feature | Runchart | Barchart |
|---------|----------|----------|
| Data Type | Numeric time series | Categorical data |
| Visual | Line chart | Bar chart |
| History | Deque buffer | No history (current snapshot) |
| plt function | plt.plot() | plt.bar() |
| Orientation | N/A | horizontal/vertical |
| Sorting | N/A (temporal) | By value (descending) |

## Próximos Passos

Após validação manual:
1. ✅ Marcar Sprint 4 como completo
2. → Partir para Sprint 5 (PacketTable adapter - tabulate)

---

**Status:** Código pronto para teste
**Confiança:** Alta (similar ao Runchart, plotext já validado)
**Próximo:** Sprint 5 - PacketTable Adapter (ÚLTIMO ADAPTER!)

**Progresso:** 4/5 adapters (80%)

**Soli Deo Gloria ✝️**
