# Manual Test: Runchart Adapter

**Sprint:** 3 (Plotext Integration)
**Author:** Dev Sênior Rafael
**Date:** 2025-11-11
**Status:** ✅ Código Implementado - Aguarda Teste Manual

---

## Objetivo

Validar que o RunchartAdapter funciona corretamente, gerando gráficos ASCII de linha temporal com plotext.

## Pré-requisitos

- ✅ RunchartAdapter implementado (src/adapters/runchart_adapter.py)
- ✅ plotext compatibility validado (Sprint 1 spike test)
- ✅ Config de teste criado (config/test_runchart_pycui.yml)

## Comando de Teste

```bash
cd /home/maximus/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# Teste com mock data (recomendado - gera dados variáveis)
python3 main_v2.py --config config/test_runchart_pycui.yml --pycui-mode --mock
```

## Resultado Esperado

Devem aparecer 2 runcharts com gráficos animados:

### Runchart 1: CPU Usage Over Time
- **Posição:** (x=0, y=0), 80x30
- **Título:** "CPU Usage Over Time"
- **Conteúdo:** Gráfico de linha ASCII mostrando últimos 50 valores
- **Marker:** braille (linha suave)
- **Cor:** Green
- **Taxa:** Atualiza a cada 1 segundo
- **Comportamento:** Linha deve subir/descer mostrando variação de CPU

### Runchart 2: Memory Usage Trend
- **Posição:** (x=0, y=35), 80x25
- **Título:** "Memory Usage Trend"
- **Conteúdo:** Gráfico de linha ASCII mostrando últimos 40 valores
- **Marker:** dot (pontos)
- **Cor:** Cyan
- **Taxa:** Atualiza a cada 2 segundos
- **Comportamento:** Linha mais estável que CPU

## Validação Visual

- [ ] Dashboard inicia sem erros
- [ ] 2 runcharts visíveis
- [ ] Posições corretas (um acima, outro abaixo)
- [ ] Títulos corretos nos charts
- [ ] **Gráficos animados** (linhas se movendo da direita para esquerda)
- [ ] Eixo Y mostra valores numéricos
- [ ] Eixo X mostra tempo (implícito - últimos N samples)
- [ ] Cores green e cyan aplicadas
- [ ] Marker "braille" vs "dot" visualmente diferentes

## Detalhes Técnicos

### plotext Output Capture
```python
# Como funciona internamente:
plt.clf()
plt.plot(data, marker="braille")
plt.title("Chart Title")

# Capturar stdout
output = io.StringIO()
sys.stdout = output
plt.show()
sys.stdout = old_stdout

chart_text = output.getvalue()  # ~4300 caracteres
widget.set_text(chart_text)
```

### Features Implementadas
- ✅ History buffer (deque with max_samples)
- ✅ Dynamic Y-axis scaling (10% margin)
- ✅ plotext markers (braille, dot, etc)
- ✅ Color mapping
- ✅ Graceful error handling (non-numeric values skipped)

## Troubleshooting

### Gráfico não aparece / Tela preta
**Causa:** History ainda vazia ou plotext output não chegou ao widget
**Solução:** Aguardar ~5 segundos para histórico acumular valores

### Erro: "list indices must be integers or slices, not str"
**Causa:** plotext recebendo dados no formato errado
**Solução:** Verificar que plugin fornece valores numéricos (float)

### Gráfico estático / Não anima
**Causa:** Mock data não está variando
**Solução:** Verificar MockDataGenerator está gerando valores aleatórios

### Erro de plotext: "AttributeError"
**Causa:** Versão incompatível do plotext
**Solução:** Verificar plotext ≥5.0.0 (`pip list | grep plotext`)

## Performance

- **CPU Usage:** < 5% (plotext é leve)
- **Memory:** < 50MB adicional
- **Latência:** < 100ms por update

## Comparação com Sparkline

| Feature | Sparkline | Runchart |
|---------|-----------|----------|
| Visual | ▁▂▃▄▅▆▇█ (bars) | ASCII line chart |
| Library | None (Unicode) | plotext |
| Axes | None | X/Y axes com labels |
| Markers | N/A | braille, dot, fhd, etc |
| Complexity | Baixa | Média |

## Próximos Passos

Após validação manual:
1. ✅ Marcar Sprint 3 como completo
2. → Partir para Sprint 4 (Barchart adapter - similar ao Runchart)

---

**Status:** Código pronto para teste
**Confiança:** Alta (plotext validado em spike, seguiu padrão)
**Próximo:** Sprint 4 - Barchart Adapter

**Soli Deo Gloria ✝️**
