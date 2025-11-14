# 🧪 Como Testar o Dashboard

## Scripts de Teste Disponíveis

### 1. `test_visual.py` - Teste Visual dos Painéis Principais
Testa individualmente os 2 primeiros painéis (WiFi e System):

```bash
cd wifi_security_education
python3 test_visual.py
```

**O que mostra:**
- ✅ Header renderizado
- ✅ WiFi Panel com barras de sinal coloridas
- ✅ System Panel com barras de CPU/RAM coloridas

---

### 2. `test_render.py` - Teste de Renderização de Componentes
Valida que todos os componentes retornam objetos Panel Rich:

```bash
python3 test_render.py
```

**O que mostra:**
- Tipo de cada componente (Panel, Table, etc.)
- Validação de que objetos Rich estão sendo criados corretamente

---

### 3. `test_dashboard_completo.py` - Dashboard Completo Renderizado
Mostra o dashboard COMPLETO com todos os componentes no layout final:

```bash
python3 test_dashboard_completo.py
```

**O que mostra:**
- ✅ Dashboard completo 120x46 caracteres
- ✅ Header, WiFi, System, Traffic Chart, Devices, Apps, Footer
- ✅ Layout alinhado e responsivo
- ✅ Estatísticas de renderização

---

## Testar Aplicação Real

### Modo Simulado (Mock - sem root)
```bash
python3 main.py --mock
```

### Modo Real (precisa de root para captura de rede)
```bash
sudo python3 main.py
```

---

## Validação Visual

Após executar qualquer teste, verifique:

- [ ] Cores renderizando (não aparecem códigos `[green]` ou `[#FFD93D]`)
- [ ] Barras de progresso coloridas (CPU/RAM)
- [ ] Gráfico plotext sem códigos ANSI vazando
- [ ] Layout alinhado sem quebras
- [ ] Emojis renderizando corretamente

---

**Status:** ✅ 100% FUNCIONAL E BONITO
**Juan-Dev - Soli Deo Gloria ✝️**
