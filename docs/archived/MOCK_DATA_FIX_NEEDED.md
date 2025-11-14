# 🐛 Mock Data - Correção Necessária

## Problema Identificado

**Status:** Dashboards 8-11 (DNS, HTTP, Rogue AP, Handshake) não mostram dados em modo mock

## Causa Raiz

Os plugins **TÊM** método `_get_mock_data()` implementado, mas:
1. DNS Monitor - ✅ Funciona (5 queries aparecendo)
2. HTTP Sniffer - ❌ Retorna lista vazia
3. Rogue AP - ❌ Retorna lista vazia  
4. Handshake - ❌ Retorna lista vazia

## Teste Realizado

```python
# HTTP Sniffer
http_data = http_plugin.collect_data()
print(http_data.get('requests', []))  # [] (vazio!)

# Rogue AP
rogue_data = rogue_plugin.collect_data()
print(rogue_data.get('detected_rogues', []))  # [] (vazio!)

# Handshake
handshake_data = handshake_plugin.collect_data()
print(handshake_data.get('captured_handshakes', []))  # [] (vazio!)
```

## Localização do Código

```
src/plugins/http_sniffer_plugin.py:376     - def _get_mock_data()
src/plugins/rogue_ap_detector.py:458       - def _get_mock_data()
src/plugins/handshake_capturer.py:482      - def _get_mock_data()
```

## Solução Necessária

Os métodos `_get_mock_data()` já existem mas parecem não estar sendo chamados corretamente ou não estão populando as estruturas internas dos plugins.

### O que verificar:

1. **HTTP Sniffer** (linha 376):
   - Mock data está definido mas precisa popular `self.http_requests`
   - Chave esperada pela dashboard: `'requests'`

2. **Rogue AP** (linha 458):
   - Mock data precisa popular `self.rogue_alerts`
   - Chave esperada: `'detected_rogues'`

3. **Handshake** (linha 482):
   - Mock data precisa popular `self.captured_handshakes`
   - Chave esperada: `'captured_handshakes'`

## Comparação com Plugin Funcionando

**DNS Monitor** funciona porque:
```python
def _get_mock_data(self) -> Dict[str, Any]:
    # Popula estruturas internas
    self.recent_queries = [...]  # ✅ Popula lista
    return {
        'recent_queries': [q.to_dict() for q in self.recent_queries]  # ✅ Retorna dados
    }
```

## Próximos Passos

1. Abrir cada arquivo e verificar se `_get_mock_data()` está:
   - Sendo chamado por `collect_data()` quando `mock_mode=True`
   - Populando as estruturas internas corretas
   - Retornando as chaves certas esperadas pelas dashboards

2. Testar isoladamente cada plugin após correção

3. Testar no app completo com `python3 app_textual.py --mock`

## Comando de Teste Rápido

```bash
cd ~/Área\ de\ trabalho/REDE_WIFI/wifi_security_education

# Testar HTTP Sniffer
python3 << 'EOF'
from src.plugins.base import PluginConfig
from src.plugins.http_sniffer_plugin import HTTPSnifferPlugin
import time

config = PluginConfig(name="http", rate_ms=1000, config={"mock_mode": True})
plugin = HTTPSnifferPlugin(config)
plugin.initialize()
time.sleep(1)
data = plugin.collect_data()
print(f"Requests: {len(data.get('requests', []))}")
print(f"Keys: {list(data.keys())}")
plugin.cleanup()
EOF
```

## Status Atual

- ✅ DNS Monitor: Funciona perfeitamente
- ❌ HTTP Sniffer: Precisa correção
- ❌ Rogue AP: Precisa correção
- ❌ Handshake: Precisa correção
- ✅ ARP Detector (dash 6): Usar Mock class
- ✅ Traffic Stats (dash 7): Usar Mock class

**Total para corrigir: 3 plugins (HTTP, Rogue AP, Handshake)**

---

**Data:** 2025-11-13  
**Hora:** 00:47 UTC  
**Status:** Identificado, aguardando correção  
**Prioridade:** Média (funciona em real mode, só mock precisa ajuste)

_Soli Deo Gloria ✝️_
