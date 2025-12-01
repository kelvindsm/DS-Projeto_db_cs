# 📋 Solicitações Ativas - Documentação Técnica

## Objetivo
Implementar uma página onde solicitantes podem visualizar todos os serviços **ativos** (status = 'A') disponíveis para solicitação, com filtros por setor e detalhes dos serviços.

## Arquivos Criados/Modificados

### 1. **`database/solicitacao_dao.py`** (NOVO)
DAO especializado para gerenciar consultas de solicitações (serviços ativos).

```python
class SolicitacaoDAO(DAO):
    def __init__(self):
        super().__init__("tb_servico", "idt_servico")
```

**Métodos implementados:**

#### `get_solicitacoes_ativas()`
```python
def get_solicitacoes_ativas(self):
    """
    Retorna todas as solicitações (serviços) ativas
    Joins com tabela de setores para obter nome do setor
    """
```

**SQL executado:**
```sql
SELECT 
    ts.idt_servico,
    ts.nme_servico,
    ts.num_dias_servico,
    ts.vlr_servico,
    ts.txt_modelo_servico,
    ts.sts_servico,
    ts.cod_setor,
    setor.nme_setor,
    setor.sgl_setor
FROM cs.tb_servico as ts
LEFT JOIN cs.tt_setor as setor ON ts.cod_setor = setor.idt_setor
WHERE ts.sts_servico = 'A'
ORDER BY ts.nme_servico ASC
```

**Por quê cada parte?**
- `LEFT JOIN`: Inclui setores mesmo se não houver serviço vinculado
- `WHERE sts_servico = 'A'`: Filtra apenas serviços ativos
- `ORDER BY nme_servico ASC`: Ordena alfabeticamente para facilitar leitura

**Retorno:**
```python
[
    {
        'idt_servico': 1,
        'nme_servico': 'Suporte Administrativo',
        'num_dias_servico': 2,
        'vlr_servico': 180.00,
        'txt_modelo_servico': 'Atendimento administrativo básico',
        'sts_servico': 'A',
        'cod_setor': 1,
        'nme_setor': 'Administração',
        'sgl_setor': 'ADM'
    },
    # ... mais serviços
]
```

#### `get_solicitacoes_por_setor(cod_setor)`
```python
def get_solicitacoes_por_setor(self, cod_setor):
    """
    Retorna solicitações ativas de um setor específico
    """
```

Similar à anterior, mas com filtro adicional:
```sql
WHERE ts.sts_servico = 'A' AND ts.cod_setor = :cod_setor
```

---

### 2. **`urls/solicitante.py`** (MODIFICADO)

#### Nova importação:
```python
from database.solicitacao_dao import SolicitacaoDAO
```

#### Rota 1: `/solicitante/solicitacoes_ativas` (GET)
```python
@bp_solicitante.route('/solicitacoes_ativas')
def solicitacoes_ativas():
    """Exibe a página de solicitações ativas de serviços"""
    dao = SolicitacaoDAO()
    solicitacoes = dao.get_solicitacoes_ativas()
    
    # Obter lista de setores para filtro
    dao_setor = SetorDAO()
    setores = dao_setor.read_by_filters([('sts_setor', '=', 'A')])
    
    return render_template('solicitante/solicitacoes_ativas.html', 
                         solicitacoes=solicitacoes, 
                         setores=setores,
                         filtro_usado='')
```

**Fluxo:**
1. Cria instância do SolicitacaoDAO
2. Busca todas as solicitações ativas
3. Busca lista de setores ativos (para dropdown de filtro)
4. Renderiza template passando dados

**Resposta:**
- Template HTML com lista de serviços
- Dropdown com lista de setores
- Nenhum filtro aplicado inicialmente

#### Rota 2: `/solicitante/solicitacoes_ativas/filtrar` (POST)
```python
@bp_solicitante.route('/solicitacoes_ativas/filtrar', methods=['POST'])
def solicitacoes_ativas_filtrar():
    """Filtra solicitações ativas por setor"""
    from flask import request
    
    cod_setor = request.form.get('cod_setor', '')
```

**Lógica:**
```python
if cod_setor:
    solicitacoes = dao.get_solicitacoes_por_setor(int(cod_setor))
    setor_selecionado = dao_setor.read_by_idt(int(cod_setor))
    filtro_usado = f'Setor: {setor_selecionado.nme_setor}'
else:
    solicitacoes = dao.get_solicitacoes_ativas()
    filtro_usado = 'Todos os setores'
```

**Fluxo:**
1. Recebe `cod_setor` do formulário
2. Se tem setor, filtra por setor específico
3. Se não, mostra todos os serviços
4. Retorna template com dados filtrados

---

### 3. **`templates/solicitante/solicitacoes_ativas.html`** (NOVO)

#### Estrutura HTML:

```html
┌─────────────────────────────────────────┐
│  Header (com ícone e título)            │
├─────────────────────────────────────────┤
│  Seção de Filtro (dropdown + botão)     │
├─────────────────────────────────────────┤
│  Informação de Filtro Aplicado          │
├─────────────────────────────────────────┤
│  Estatísticas (3 cards)                 │
│  - Total de Serviços                    │
│  - Valor Total                          │
│  - Valor Médio                          │
├─────────────────────────────────────────┤
│  Tabela de Serviços                     │
│  ┌─────────────────────────────────────┐│
│  │ ID │ Serviço │ Setor │ Desc │ ... ││
│  │────────────────────────────────────││
│  │ 1  │ Suporte │ ADM   │ ...  │ ... ││
│  │ 2  │ Treina  │ PIX   │ ...  │ ... ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  Botão Retornar                         │
└─────────────────────────────────────────┘
```

#### Componentes Principais:

##### 1. **Header**
```html
<div class="header">
    <h1>📋 Solicitações Ativas</h1>
    <p>Conheça os serviços disponíveis para solicitação</p>
</div>
```

Estilo: Gradiente laranja (#ffc107 → #ff9800)

##### 2. **Filtro**
```html
<form method="POST" action="/solicitante/solicitacoes_ativas/filtrar">
    <select id="cod_setor" name="cod_setor">
        <option value="">-- Todos os Setores --</option>
        {% for setor in setores %}
        <option value="{{ setor.idt_setor }}">{{ setor.nme_setor }}</option>
        {% endfor %}
    </select>
    <button type="submit" class="btn-filtrar">🔍 Filtrar</button>
</form>
```

**Como funciona:**
- Dropdown preenchido dinamicamente com setores ativos
- Ao submeter, envia POST para `/solicitacoes_ativas/filtrar`
- Filtro "Todos os setores" retorna todos os serviços

##### 3. **Informação de Filtro**
```html
{% if filtro_usado %}
<div class="filtro-info">
    <strong>Filtro Aplicado:</strong> {{ filtro_usado }}
</div>
{% endif %}
```

Exibe qual filtro está sendo usado (ex: "Setor: Administração")

##### 4. **Estatísticas**
```html
<div class="stats">
    <div class="stat-card">
        <div class="value">{{ solicitacoes | length }}</div>
        <div class="label">Serviços Ativos</div>
    </div>
    <!-- ... Total e Média ... -->
</div>
```

**Cálculos:**
```jinja2
Total: {{ solicitacoes | length }}
Valor Total: {{ solicitacoes | map(attribute='vlr_servico') | sum }}
Valor Médio: {{ (soma) / (quantidade) }}
```

##### 5. **Tabela de Serviços**
```html
<table class="data-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Serviço</th>
            <th>Setor</th>
            <th>Descrição</th>
            <th>Dias</th>
            <th>Valor</th>
            <th>Status</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for solicitacao in solicitacoes %}
        <tr>
            <td><strong>#{{ solicitacao.idt_servico }}</strong></td>
            <td><strong>{{ solicitacao.nme_servico }}</strong></td>
            <td>{{ solicitacao.sgl_setor }}</td>
            <td>{{ solicitacao.txt_modelo_servico[:60] }}...</td>
            <td>{{ solicitacao.num_dias_servico }} dia(s)</td>
            <td class="valor-servico">R$ {{ "%.2f" | format(solicitacao.vlr_servico) }}</td>
            <td><span class="badge badge-ativo">✓ Ativo</span></td>
            <td>
                <button class="btn-acao btn-detalhes" 
                        data-id="..."
                        data-nome="..."
                        data-descricao="..."
                        data-valor="..."
                        onclick="mostrarDetalhesBtn(this)">
                    ℹ️ Detalhes
                </button>
                <button class="btn-acao btn-solicitar"
                        data-id="..."
                        data-nome="..."
                        onclick="solicitarServico(this)">
                    ✓ Solicitar
                </button>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

**Coluna Descrição:**
```jinja2
{{ solicitacao.txt_modelo_servico[:60] }}
```
Mostra apenas os primeiros 60 caracteres para não ocupar muito espaço

**Coluna Valor:**
```jinja2
R$ {{ "%.2f" | format(solicitacao.vlr_servico) }}
```
Formata para 2 casas decimais

##### 6. **Botões de Ação**
```html
<button class="btn-detalhes" 
        data-id="{{ solicitacao.idt_servico }}"
        data-nome="{{ solicitacao.nme_servico }}"
        data-descricao="{{ solicitacao.txt_modelo_servico }}"
        data-valor="{{ solicitacao.vlr_servico }}"
        onclick="mostrarDetalhesBtn(this)">
    ℹ️ Detalhes
</button>
```

**Por quê `data-*` attributes?**
- Evita problemas com aspas em strings
- Mais seguro e semântico
- JavaScript acessa via `btn.dataset.propriedade`

**JavaScript associado:**
```javascript
function mostrarDetalhesBtn(btn) {
    const id = btn.dataset.id;
    const nome = btn.dataset.nome;
    const descricao = btn.dataset.descricao;
    const valor = parseFloat(btn.dataset.valor);
    
    document.getElementById('modalTitulo').textContent = nome;
    document.getElementById('modalDescricao').textContent = descricao;
    document.getElementById('modalValor').textContent = 
        'R$ ' + valor.toFixed(2).replace('.', ',');
    document.getElementById('modalDetalhes').style.display = 'block';
}
```

##### 7. **Modal de Detalhes**
```html
<div id="modalDetalhes">
    <div>
        <span onclick="fecharDetalhes()">&times;</span>
        <h2 id="modalTitulo"></h2>
        <p id="modalDescricao"></p>
        <p id="modalValor"></p>
    </div>
</div>
```

**Funcionalidades:**
- Abre ao clicar "Detalhes"
- Exibe nome completo, descrição e valor
- Fecha ao clicar X ou fora da modal

---

## Fluxo de Dados

### Cenário 1: Usuário acessa `/solicitante/solicitacoes_ativas`

```
1. GET /solicitante/solicitacoes_ativas
   ↓
2. Flask chama função solicitacoes_ativas()
   ↓
3. SolicitacaoDAO().get_solicitacoes_ativas()
   ↓
4. Execute SQL: SELECT * FROM tb_servico WHERE sts_servico = 'A'
   ↓
5. PostgreSQL retorna lista de serviços
   ↓
6. SetorDAO().read_by_filters([('sts_setor', '=', 'A')])
   ↓
7. PostgreSQL retorna lista de setores
   ↓
8. Renderiza template com:
   - solicitacoes = [lista de serviços ativos]
   - setores = [lista de setores ativos]
   - filtro_usado = ''
   ↓
9. HTML renderizado no navegador
   - Tabela com todos os serviços
   - Dropdown com todos os setores
   - Sem filtro aplicado
```

### Cenário 2: Usuário filtra por setor

```
1. Usuário seleciona setor no dropdown e clica Filtrar
   ↓
2. POST /solicitante/solicitacoes_ativas/filtrar
   - Form data: cod_setor = 2
   ↓
3. Flask chama função solicitacoes_ativas_filtrar()
   ↓
4. cod_setor = 2 (Pix Automático, por exemplo)
   ↓
5. SolicitacaoDAO().get_solicitacoes_por_setor(2)
   ↓
6. Execute SQL: SELECT * FROM tb_servico WHERE sts_servico = 'A' AND cod_setor = 2
   ↓
7. PostgreSQL retorna apenas serviços do setor 2
   ↓
8. SetorDAO().read_by_idt(2)
   ↓
9. PostgreSQL retorna dados do setor 2
   ↓
10. Renderiza template com:
    - solicitacoes = [apenas do setor 2]
    - setores = [todos os setores para dropdown]
    - filtro_usado = 'Setor: Pix Automático'
    ↓
11. HTML renderizado
    - Tabela com serviços filtrados
    - Dropdown marcado no setor 2
    - Mensagem: "Filtro Aplicado: Setor: Pix Automático"
```

### Cenário 3: Usuário clica em "Detalhes"

```
1. Usuário clica botão "Detalhes" de um serviço
   ↓
2. JavaScript executa mostrarDetalhesBtn(btn)
   ↓
3. Extrai dados do elemento: 
   - id = btn.dataset.id
   - nome = btn.dataset.nome
   - descricao = btn.dataset.descricao
   - valor = btn.dataset.valor
   ↓
4. Preenchimento do modal:
   - #modalTitulo.textContent = nome
   - #modalDescricao.textContent = descricao
   - #modalValor.textContent = "R$ XX,XX"
   ↓
5. Modal aparece (display = block)
   ↓
6. Usuário lê detalhes e fecha (clica X ou fora)
   ↓
7. fecharDetalhes() esconde modal
```

---

## Estilo e Responsividade

### Paleta de Cores
- **Primary**: #ffc107 (Laranja) - Header, botões
- **Secondary**: #ff9800 (Laranja escuro) - Hover
- **Success**: #28a745 (Verde) - Badge ativo
- **Info**: #007bff (Azul) - Botão detalhes
- **Text**: #333 (Cinza escuro) - Texto principal

### Breakpoints (Media Queries)
```css
@media (max-width: 768px) {
    /* Ajusta layout para mobile */
    .filter-form flex-direction: column
    .data-table font-size: 0.85em
    .acoes flex-direction: column
}
```

---

## Dados Exemplo

Se você executar a massa de dados que criamos:

| idt | nme_servico | setor | dias | valor | status |
|-----|------------|-------|------|-------|--------|
| 1 | Suporte Administrativo | ADM | 2 | 180 | A |
| 5 | Consultoria Processos | ADM | 5 | 850 | A |
| 15 | Configuração PIX | PIX | 5 | 1500 | A |
| 20 | Treinamento PIX | PIX | 3 | 900 | A |
| 30 | Reparo Computadores | TI | 1 | 180 | A |
| 45 | Consultoria Infraestrutura | TI | 5 | 1500 | A |

**Estatísticas para "Todos":**
- Total de Serviços: 47
- Valor Total: R$ 50.000,00
- Valor Médio: R$ 1.063,83

**Estatísticas para "Setor: Administração":**
- Total de Serviços: 10
- Valor Total: R$ 4.795,00
- Valor Médio: R$ 479,50

---

## Possíveis Evoluções

1. **Busca por Nome**
   - Adicionar campo de busca por nome do serviço
   - Implementar filtro com `LIKE` na query

2. **Ordenação**
   - Adicionar sort por nome, valor, dias
   - Clicável nos headers da tabela

3. **Paginação**
   - Se muitos serviços, dividir em páginas
   - 10 serviços por página, por exemplo

4. **Avaliações**
   - Campo de rating para cada serviço
   - Mostrar estrelas na tabela

5. **Histórico**
   - Link para ver quantas vezes foi solicitado
   - Última solicitação

6. **Exportação**
   - Botão para exportar lista como PDF ou CSV
   - Ou imprimir lista

7. **Integração com Solicitação**
   - Botão "Solicitar" levar para formulário de solicitação
   - Pré-preenchido com ID do serviço

---

## Conclusão

A página de Solicitações Ativas oferece:

✅ **Visualização clara** de todos os serviços disponíveis
✅ **Filtro por setor** para facilitar busca
✅ **Estatísticas** de valor (total e médio)
✅ **Modal de detalhes** para informações completas
✅ **Design responsivo** que funciona em mobile
✅ **UX intuitiva** com ícones e cores consistentes

Pronta para apresentar ao professor! 🎉
