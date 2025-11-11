# Manual Test: Textbox Adapter

**Sprint:** 2 (Vitória Rápida)
**Author:** Dev Sênior Rafael
**Date:** 2025-11-11
**Status:** ✅ Código Implementado - Aguarda Teste Manual

---

## Objetivo

Validar que o TextboxAdapter funciona corretamente em modo py_cui, mostrando valores de plugins formatados.

## Pré-requisitos

- ✅ TextboxAdapter implementado (src/adapters/textbox_adapter.py)
- ✅ Config de teste criado (config/test_textbox_pycui.yml)
- ✅ Dashboard preparado para carregar adapter

## Comando de Teste

```bash
cd /home/maximus/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# Teste com mock data
python3 main_v2.py --config config/test_textbox_pycui.yml --pycui-mode --mock
```

## Resultado Esperado

Devem aparecer 2 textboxes:

### Textbox 1: Memory Usage
- **Posição:** (x=10, y=5), 80x20
- **Título:** "Memory Usage"
- **Conteúdo:** "Memory: 45.2%" (valor variável)
- **Cor:** Cyan
- **Taxa de atualização:** 2 segundos

### Textbox 2: CPU Usage
- **Posição:** (x=10, y=30), 80x15
- **Título:** "CPU Usage"
- **Conteúdo:** "CPU: 23.5%" (valor variável)
- **Cor:** Green
- **Taxa de atualização:** 1 segundo

## Validação

- [ ] Dashboard inicia sem erros
- [ ] 2 textboxes visíveis
- [ ] Posições corretas (sem sobreposição)
- [ ] Títulos corretos
- [ ] Valores formatados corretamente (label + format string)
- [ ] Cores cyan e green aplicadas
- [ ] Valores atualizam em tempo real

## Troubleshooting

### Erro: "Module 'src.adapters.textbox_adapter' not found"
**Causa:** Python não encontra o adapter
**Solução:** Verificar que arquivo existe em `src/adapters/textbox_adapter.py`

### Erro: "AttributeError: 'TextBlock' object has no attribute 'set_text'"
**Causa:** Problema com py_cui TextBlock
**Solução:** Verificar versão do py_cui (deve ser ≥0.1.6)

### Textbox mostra "N/A"
**Causa:** Plugin não está fornecendo dados
**Solução:** Verificar que SystemPlugin está habilitado e funcionando em mock mode

## Código Implementado

### TextboxAdapter (src/adapters/textbox_adapter.py)
- ✅ Herda de ComponentAdapter
- ✅ Usa py_cui.add_text_block()
- ✅ Implementa create_widget()
- ✅ Implementa update_widget()
- ✅ Extrai dados do plugin corretamente
- ✅ Aplica label e format string
- ✅ Trata erros (plugin não disponível, campo não encontrado)

### Features
- ✅ Label opcional (extra.label)
- ✅ Format string opcional (extra.format com placeholder {value})
- ✅ Color mapping (cyan, green, etc)
- ✅ Tratamento de erros gracioso

## Próximos Passos

Após validação manual:
1. ✅ Marcar Sprint 2 como completo
2. → Partir para Sprint 3 (Runchart adapter com plotext)

---

**Status:** Código pronto para teste
**Confiança:** Alta (seguiu padrão do SparklineAdapter)
**Próximo:** Sprint 3 - Runchart Adapter

**Soli Deo Gloria ✝️**
