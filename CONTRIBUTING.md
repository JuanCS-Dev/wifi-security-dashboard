# Contributing to WiFi Security Education Dashboard

Obrigado por considerar contribuir! Este projeto segue a **Constituição Vértice v3.0** para garantir qualidade e consistência.

## 📋 Princípios de Contribuição (P1-P6)

### P1: Completude Obrigatória
- ❌ **Não envie** código com TODO, FIXME, ou placeholders
- ✅ **Envie** código completo e funcional
- ✅ **Inclua** testes para toda nova funcionalidade

### P2: Validação Preventiva
- ❌ **Não assuma** que APIs/bibliotecas existem
- ✅ **Valide** com try/except antes de usar
- ✅ **Forneça** mensagens de erro claras

### P3: Ceticismo Crítico
- ❌ **Não assuma** que dados são válidos
- ✅ **Valide** ranges, boundaries, e edge cases
- ✅ **Escreva** testes para casos extremos

### P4: Rastreabilidade Total
- ❌ **Não faça** commits vagos ("fix bug", "update")
- ✅ **Escreva** mensagens descritivas (>10 palavras)
- ✅ **Documente** decisões em docstrings

### P5: Consciência Sistêmica
- ❌ **Não crie** inconsistências entre módulos
- ✅ **Mantenha** nomes de campos padronizados
- ✅ **Siga** interfaces existentes

### P6: Eficiência de Token
- ❌ **Não envie** múltiplos commits corrigindo o mesmo bug
- ✅ **Corrija** issues em ≤2 iterações
- ✅ **Documente** aprendizados de erros

---

## 🚀 Processo de Contribuição

### 1. Fork e Clone

```bash
# Fork no GitHub, depois:
git clone https://github.com/[seu-usuario]/wifi_security_education.git
cd wifi_security_education
```

### 2. Configurar Ambiente

```bash
# Instalar dependências
make setup
# ou
pip3 install -r requirements-v2.txt

# Verificar instalação
make check-deps
```

### 3. Criar Branch

```bash
# Branch para feature
git checkout -b feature/minha-feature

# Branch para bugfix
git checkout -b fix/corrigir-bug
```

### 4. Desenvolver

```bash
# Rode testes frequentemente
make test-unit

# Valide P1-P6
make validate

# Verifique coverage
make coverage
```

### 5. Commit

```bash
# Formato de commit:
git commit -m "tipo: Descrição curta

- Mudança 1 detalhada
- Mudança 2 detalhada
- Testes adicionados: X, Y, Z

Framework: Constituição Vértice v3.0 (P1-P6)
"
```

**Tipos de commit:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `test:` Adicionar/modificar testes
- `refactor:` Refatoração (sem mudar comportamento)
- `perf:` Melhoria de performance
- `style:` Formatação (sem mudar lógica)

### 6. Pull Request

1. Push para seu fork
2. Abra PR no repositório original
3. Descreva:
   - O que foi mudado
   - Por que foi mudado
   - Como testar
   - Referências (issues, etc)

---

## 🧪 Testes Obrigatórios

### Toda feature deve ter:

1. **Testes unitários** (tests/unit/)
   ```python
   def test_minha_feature():
       # Arrange
       setup = criar_setup()

       # Act
       resultado = minha_feature(setup)

       # Assert
       assert resultado == esperado
   ```

2. **Docstrings completas**
   ```python
   def minha_feature(param: str) -> int:
       """
       Descrição clara do que faz.

       Args:
           param: O que é este parâmetro

       Returns:
           O que retorna

       Raises:
           ValueError: Quando param é inválido
       """
   ```

3. **Validação de inputs (P3)**
   ```python
   def minha_feature(param: str) -> int:
       if not param:
           raise ValueError("param não pode ser vazio")
       if not isinstance(param, str):
           raise TypeError("param deve ser string")
       # ... resto da lógica
   ```

### Executar Testes

```bash
# Todos os testes
make test

# Apenas unitários
make test-unit

# Com coverage
make coverage

# Validar P1-P6
make validate

# Calcular métricas
make metrics
```

---

## 🎯 Áreas para Contribuir

### Prioridade Alta
- [ ] Screenshots do dashboard
- [ ] `docs/ARCHITECTURE.md`
- [ ] `docs/PLUGIN_API.md`
- [ ] `docs/MOCK_MODE.md`

### Prioridade Média
- [ ] Modo "Explicação Detalhada"
- [ ] Exportar relatórios (TXT/JSON)
- [ ] Mais testes de edge cases
- [ ] Suporte a mais idiomas

### Prioridade Baixa
- [ ] Web interface
- [ ] Gamificação
- [ ] Histórico de 24h

---

## 🐛 Reportar Bugs

### Antes de reportar:
1. Verifique se já existe issue similar
2. Rode `make check-deps` para validar setup
3. Teste em mock mode

### Template de Bug Report:

```markdown
**Descrição:**
Breve descrição do bug

**Passos para Reproduzir:**
1. Executar X
2. Fazer Y
3. Ver erro Z

**Comportamento Esperado:**
O que deveria acontecer

**Comportamento Atual:**
O que está acontecendo

**Ambiente:**
- OS: Ubuntu 22.04
- Python: 3.10.12
- Versão: v2.0.0

**Logs:**
```
cole logs aqui
```
```

---

## 📝 Checklist de PR

Antes de enviar PR, verifique:

- [ ] Código segue princípios P1-P6
- [ ] Testes adicionados e passando (`make test`)
- [ ] Coverage mantido/melhorado (`make coverage`)
- [ ] Validação P1-P6 passa (`make validate`)
- [ ] Docstrings completas
- [ ] Commit message descritivo
- [ ] README atualizado (se necessário)
- [ ] Sem arquivos temporários commitados

---

## 💡 Dicas para Contribuidores

### Escrevendo Plugins

```python
from src.plugins.base import Plugin, PluginConfig, PluginStatus

class MeuPlugin(Plugin):
    def initialize(self) -> None:
        # P2: Valide APIs antes de usar
        try:
            import biblioteca_necessaria
            self.lib = biblioteca_necessaria
        except ImportError:
            raise RuntimeError("biblioteca_necessaria não instalada")

        # Mock mode (P5: Consciência Sistêmica)
        self._mock_mode = self.config.config.get('mock_mode', False)
        if self._mock_mode:
            from src.utils.mock_data_generator import get_mock_generator
            self._mock_generator = get_mock_generator()

        self._status = PluginStatus.READY

    def collect_data(self) -> Dict[str, Any]:
        # P3: Valide suposições
        if self._mock_mode:
            return self._mock_generator.get_meus_dados()

        # Coleta real com validação
        dados = self.lib.coletar()

        # P3: Valide ranges
        if not (0 <= dados['valor'] <= 100):
            raise ValueError(f"Valor fora do range: {dados['valor']}")

        return dados

    def cleanup(self) -> None:
        self._status = PluginStatus.STOPPED
```

### Estrutura de Testes

```python
# tests/unit/test_meu_plugin.py
import pytest
from src.plugins.meu_plugin import MeuPlugin
from src.plugins.base import PluginConfig, PluginStatus

class TestMeuPlugin:
    """Testes para MeuPlugin"""

    def test_initialize_sucesso(self):
        """Test P2: Inicialização com validação"""
        config = PluginConfig(name="meu", enabled=True)
        plugin = MeuPlugin(config)
        plugin.initialize()

        assert plugin.status == PluginStatus.READY

    def test_collect_data_valida_range(self):
        """Test P3: Validação de ranges"""
        plugin = MeuPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()

        # P3: Valide suposições
        assert 0 <= data['valor'] <= 100

    def test_mock_mode(self):
        """Test P5: Mock mode consistente"""
        config = PluginConfig(name="meu", enabled=True)
        config.config['mock_mode'] = True

        plugin = MeuPlugin(config)
        plugin.initialize()
        data = plugin.collect_data()

        # Deve funcionar sem biblioteca real
        assert data is not None
```

---

## 🤝 Código de Conduta

### Seja Respeitoso
- Critique código, não pessoas
- Seja paciente com iniciantes
- Celebre sucessos dos outros

### Seja Construtivo
- Explique o "porquê" nos code reviews
- Sugira melhorias, não apenas aponte problemas
- Compartilhe conhecimento

### Seja Profissional
- Mantenha discussões técnicas
- Respeite decisões de design
- Aceite feedback construtivamente

---

## 📞 Dúvidas?

- **Issues**: Para bugs e feature requests
- **Discussions**: Para perguntas gerais
- **Code Review**: PR com questões específicas

---

**Desenvolvido seguindo Constituição Vértice v3.0**

**Obrigado por contribuir!** ✝️
