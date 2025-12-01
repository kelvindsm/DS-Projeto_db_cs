# 📊 Análise de Valores de Serviços por Setor - Documentação Técnica

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura da Solução](#arquitetura-da-solução)
3. [Componentes Implementados](#componentes-implementados)
4. [Fluxo de Dados](#fluxo-de-dados)
5. [Análise Detalhada do Código](#análise-detalhada-do-código)
6. [Tecnologias Utilizadas](#tecnologias-utilizadas)
7. [Como Funciona](#como-funciona)

---

## Visão Geral

### Objetivo
Implementar um módulo de análise de valores de serviços agrupados por setor, com visualização em gráfico interativo usando ECharts. A feature permite que solicitantes visualizem dados estatísticos (mínimo, máximo e média) de valores de serviços para cada setor do sistema.

### Requisitos Atendidos
- ✅ Rota `/solicitante/graficos` para exibir a página de gráficos
- ✅ API JSON para retornar dados de análise
- ✅ Gráfico interativo com ECharts (3 séries de dados)
- ✅ Design responsivo e moderno
- ✅ Tratamento de erros e loading states

---

## Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR (Frontend)                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │  templates/solicitante/graficos.html             │   │
│  │  - UI do gráfico                                 │   │
│  │  - JavaScript para requisições AJAX              │   │
│  │  - Inicialização do ECharts                      │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↑ ↓                              │
│              REQUISIÇÃO HTTP (JSON)                      │
│                         ↑ ↓                              │
└─────────────────────────────────────────────────────────┘
                         ↓ ↑
┌─────────────────────────────────────────────────────────┐
│                   SERVIDOR (Backend)                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │  urls/solicitante.py                             │   │
│  │  - Rota GET /solicitante/graficos                │   │
│  │  - Rota GET /solicitante/api/analise-valores    │   │
│  │  - Formata dados em JSON                         │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓ ↑                              │
│            CHAMADAS AO DAO (Banco de Dados)             │
│                         ↓ ↑                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  database/servico_dao.py                         │   │
│  │  - get_analise_valores_por_setor()               │   │
│  │  - Executa query SQL agregada                    │   │
│  │  - Retorna dados estatísticos                    │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓ ↑                              │
└─────────────────────────────────────────────────────────┘
                         ↓ ↑
┌─────────────────────────────────────────────────────────┐
│                  BANCO DE DADOS (PostgreSQL)            │
│  cs.tb_servico - Tabela com dados de serviços          │
│  cs.tt_setor - Tabela com dados de setores             │
└─────────────────────────────────────────────────────────┘
```

---

## Componentes Implementados

### 1. **Rota Principal: `/solicitante/graficos`**
**Arquivo:** `urls/solicitante.py`

```python
@bp_solicitante.route('/graficos')
def graficos():
    return render_template('solicitante/graficos.html')
```

**Função:** Renderiza a página HTML com o gráfico
**Por quê:** Quando um usuário acessa `/solicitante/graficos`, esta função é chamada para servir o template HTML com toda a estrutura visual e scripts JavaScript.

---

### 2. **Rota da API: `/solicitante/api/analise-valores-servicos`**
**Arquivo:** `urls/solicitante.py`

```python
@bp_solicitante.route('/api/analise-valores-servicos')
def api_analise_valores_servicos():
    dao = ServicoDAO()
    dados = dao.get_analise_valores_por_setor()
    
    # Verifica se dados é None, vazio ou não é uma lista
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return jsonify({
            'setores': [],
            'minimos': [],
            'maximos': [],
            'medias': []
        })
    
    try:
        setores = [d['nme_setor'] for d in dados]
        minimos = [float(d['min_valor']) if d['min_valor'] is not None else 0 for d in dados]
        maximos = [float(d['max_valor']) if d['max_valor'] is not None else 0 for d in dados]
        medias = [float(d['media_valor']) if d['media_valor'] is not None else 0 for d in dados]
        
        return jsonify({
            'setores': setores,
            'minimos': minimos,
            'maximos': maximos,
            'medias': medias
        })
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'setores': [],
            'minimos': [],
            'maximos': [],
            'medias': []
        })
```

**Linha por linha:**

| Linha | O que faz | Por quê |
|-------|-----------|---------|
| `dao = ServicoDAO()` | Cria instância do DAO de serviços | Precisa do DAO para executar queries no banco |
| `dados = dao.get_analise_valores_por_setor()` | Chama método que busca dados agregados | Obtém os dados estatísticos do banco |
| `if not dados or ...` | Verifica se retornou dados válidos | Trata casos onde não há dados ou erro |
| `setores = [d['nme_setor'] for d in dados]` | Lista com nomes dos setores | ECharts precisa dos nomes para eixo X |
| `minimos = [float(...) if ... else 0]` | Converte para float, evita None | Garante que haverá valor numérico |
| `return jsonify({...})` | Retorna resposta JSON | Browser recebe dados em formato JSON |

**Por quê essa estrutura?**
- Separação de responsabilidades: API retorna apenas dados, sem lógica visual
- Tratamento de erros: Se houver problema, retorna dados vazios ao invés de crash
- Conversão de tipos: float() garante que ECharts recebe números válidos

---

### 3. **Método DAO: `get_analise_valores_por_setor()`**
**Arquivo:** `database/servico_dao.py`

```python
def get_analise_valores_por_setor(self):
    try:
        sql = """
        SELECT 
            ts.nme_setor,
            MIN(CAST(ts_servico.vlr_servico AS NUMERIC)) as min_valor,
            MAX(CAST(ts_servico.vlr_servico AS NUMERIC)) as max_valor,
            AVG(CAST(ts_servico.vlr_servico AS NUMERIC)) as media_valor,
            COUNT(ts_servico.idt_servico) as total_servicos
        FROM cs.tb_servico as ts_servico
        INNER JOIN cs.tt_setor as ts ON ts_servico.cod_setor = ts.idt_setor
        GROUP BY ts.nme_setor, ts.idt_setor
        ORDER BY ts.nme_setor
        """
        
        result = self.execute_sql_and_fetch(sql)
        
        if result is None:
            return []
        
        dados = []
        for row in result:
            dados.append({
                'nme_setor': row[0],
                'min_valor': row[1],
                'max_valor': row[2],
                'media_valor': row[3],
                'total_servicos': row[4]
            })
        
        return dados
    except Exception as e:
        print(f"Erro ao obter análise de valores por setor: {e}")
        import traceback
        traceback.print_exc()
        return []
```

#### Análise da Query SQL:

```sql
SELECT 
    ts.nme_setor,                                    -- Nome do setor
    MIN(CAST(ts_servico.vlr_servico AS NUMERIC))    -- Valor MÍNIMO
        as min_valor,
    MAX(CAST(ts_servico.vlr_servico AS NUMERIC))    -- Valor MÁXIMO
        as max_valor,
    AVG(CAST(ts_servico.vlr_servico AS NUMERIC))    -- Valor MÉDIO
        as media_valor,
    COUNT(ts_servico.idt_servico)                   -- Total de serviços
        as total_servicos
FROM cs.tb_servico as ts_servico                    -- Tabela de serviços
INNER JOIN cs.tt_setor as ts                        -- Junta com tabela de setores
    ON ts_servico.cod_setor = ts.idt_setor          -- Na relação: setor_do_serviço = id_setor
GROUP BY ts.nme_setor, ts.idt_setor                 -- Agrupa por setor
ORDER BY ts.nme_setor                               -- Ordena alfabeticamente
```

**Por que cada função de agregação?**
- **MIN()**: Mostra o serviço mais barato do setor (análise de custo mínimo)
- **MAX()**: Mostra o serviço mais caro do setor (análise de custo máximo)
- **AVG()**: Mostra o preço médio (análise de custo esperado)
- **COUNT()**: Quantidade de serviços (análise de volume)

**Por que CAST(...AS NUMERIC)?**
- O campo `vlr_servico` pode estar armazenado como string ou tipo decimal
- NUMERIC garante que as funções de agregação (MIN, MAX, AVG) funcionem corretamente
- Sem isso, podia dar erro ou resultado incorreto

**Por que INNER JOIN?**
- Precisa do nome do setor (que está em `tt_setor`)
- INNER JOIN garante que só aparecem serviços com setor válido
- Se houvesse serviço sem setor, seria excluído (comportamento correto)

**Por que GROUP BY?**
- Agrupa todos os serviços por setor
- Aplica as funções de agregação dentro de cada grupo
- Sem GROUP BY, teria apenas 1 linha com agregação de TODOS os serviços

#### Processamento dos dados:

```python
dados = []                    # Lista para armazenar resultados
for row in result:           # Para cada linha retornada pela query
    dados.append({           # Cria dicionário com estrutura clara
        'nme_setor': row[0],           # Coluna 0 - nome setor
        'min_valor': row[1],           # Coluna 1 - valor mínimo
        'max_valor': row[2],           # Coluna 2 - valor máximo
        'media_valor': row[3],         # Coluna 3 - valor médio
        'total_servicos': row[4]       # Coluna 4 - total
    })
```

**Por quê usar dicionários?**
- Mais legível que acessar por índice (row[0] vs d['nme_setor'])
- Facilita manutenção futura
- Na rota, pode fazer list comprehension: `[d['nme_setor'] for d in dados]`

---

### 4. **Modificação em `cs.py`**
**Arquivo:** `cs.py`

```python
from urls.solicitante import bp_solicitante  # Nova importação

# ... outras importações ...

app.register_blueprint(bp_solicitante)  # Registra o blueprint
```

**Por quê?**
- Flask organiza rotas em Blueprints (módulos de rotas)
- Cada blueprint precisa ser registrado na app principal
- Sem isso, as rotas `/solicitante/*` não existiriam

---

## Fluxo de Dados

### Cenário: Usuário acessa `/solicitante/graficos`

```
1. Usuário digita URL ou clica em link
   ↓
2. Navegador faz GET request para /solicitante/graficos
   ↓
3. Flask processa request na função graficos()
   ↓
4. Renderiza template solicitante/graficos.html
   ↓
5. HTML é enviado ao navegador (com CSS e JavaScript)
   ↓
6. Navegador renderiza HTML
   ↓
7. JavaScript DOMContentLoaded event dispara
   ↓
8. carregarDadosGrafico() faz fetch para /api/analise-valores-servicos
   ↓
9. Flask processa GET /api/analise-valores-servicos
   ↓
10. Cria ServicoDAO e chama get_analise_valores_por_setor()
    ↓
11. DAO executa query SQL no PostgreSQL
    ↓
12. PostgreSQL retorna dados agregados
    ↓
13. DAO converte em lista de dicionários
    ↓
14. Rota transforma em JSON
    ↓
15. JSON é enviado ao navegador
    ↓
16. JavaScript recebe JSON
    ↓
17. inicializarGrafico() processa dados
    ↓
18. ECharts renderiza o gráfico
    ↓
19. Usuário vê o gráfico interativo! 🎉
```

---

## Análise Detalhada do Código

### 4.1 Template HTML - `templates/solicitante/graficos.html`

#### Seção HEAD e Imports:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gráficos - Análise de Valores de Serviços</title>
    <link href="static/estilo.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
```

**Por quê cada elemento?**

| Elemento | Função | Importância |
|----------|--------|-------------|
| `charset="UTF-8"` | Codificação de caracteres | Permite acentuação em português |
| `viewport` | Responsividade mobile | Gráfico funciona em smartphones |
| `ECharts CDN` | Biblioteca de gráficos | Sem isso, não há gráfico |

#### CSS Principal:

```css
.chart-container {
    width: 100%;
    height: 400px;
    position: relative;
    min-height: 400px;
    display: block;
}
```

**Por quê essas propriedades?**

| Propriedade | Motivo |
|------------|--------|
| `width: 100%` | Gráfico ocupa toda largura do container |
| `height: 400px` | Altura fixa para visibilidade |
| `min-height: 400px` | Garante altura mínima em qualquer caso |
| `position: relative` | Permite posicionamento de filhos dentro |
| `display: block` | Força renderização como bloco (não inline) |

**O problema original:** ECharts precisa de dimensões conhecidas para inicializar. Se o container não tiver altura definida, o gráfico fica comprimido até redimensionar a janela.

---

### 4.2 JavaScript - Carregamento de Dados

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Pequeno delay para garantir que todo o DOM está renderizado
    setTimeout(carregarDadosGrafico, 50);
});
```

**Por quê setTimeout?**
1. Garante que todo o DOM foi renderizado
2. O container `#chart1` terá suas dimensões CSS aplicadas
3. ECharts pode inicializar com dimensões corretas

**50ms é suficiente porque:**
- Navegadores modernos renderizam rapidamente
- 50ms é imperceptível ao usuário
- É o mínimo necessário para browser processar CSS

```javascript
function carregarDadosGrafico() {
    // Fazer requisição à API
    fetch('/solicitante/api/analise-valores-servicos')
        .then(response => response.json())
        .then(data => {
            if (data.setores && data.setores.length > 0) {
                inicializarGrafico(data);
                document.getElementById('loading-chart1').style.display = 'none';
                document.getElementById('chart1').style.display = 'block';
                document.getElementById('chart1-info').style.display = 'block';
            } else {
                mostrarErro('Nenhum dado de serviços encontrado no sistema.');
                document.getElementById('loading-chart1').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar dados:', error);
            mostrarErro('Erro ao carregar dados do servidor. Tente novamente mais tarde.');
            document.getElementById('loading-chart1').style.display = 'none';
        });
}
```

**Linha por linha:**

| Linha | Explicação |
|-------|-----------|
| `fetch(...)` | Faz requisição HTTP assincrona (não bloqueia UI) |
| `.then(response => response.json())` | Converte resposta para JSON |
| `.then(data => {...})` | Processa dados quando chegam |
| `if (data.setores && ...)` | Valida se há dados válidos |
| `document.getElementById(...).style.display` | Mostra/esconde elementos |
| `.catch(error => {...})` | Captura erros de rede |

**Por quê Fetch API?**
- Moderna e simples
- Promessas (then/catch) são mais legíveis que callbacks
- Nativa no navegador (sem jQuery necessário)

---

### 4.3 JavaScript - Inicialização do Gráfico

```javascript
function inicializarGrafico(dados) {
    // Garantir que o container está visível e tem dimensões corretas
    const container = document.getElementById('chart1');
    container.style.display = 'block';
    
    // Pequeno delay para garantir que o DOM foi renderizado
    setTimeout(() => {
        // Inicializar o ECharts
        const chart1 = echarts.init(container);
        
        const option = {
            // Configurações do gráfico
        };
        
        // Setar opções e fazer resize
        chart1.setOption(option);
        chart1.resize();
        
        // Responsividade
        window.addEventListener('resize', function() {
            chart1.resize();
        });
    }, 100);
}
```

**Por quê 100ms neste setTimeout?**
- 100ms garante que o display:block foi aplicado
- ECharts consegue medir dimensões do container
- Mais seguro que 50ms anterior

**chart1.resize()?**
- Força ECharts a recalcular dimensões do container
- Essencial depois de setar opções
- Sem isso, gráfico fica comprimido

---

### 4.4 Configuração do ECharts

```javascript
const option = {
    tooltip: {
        trigger: 'axis',
        formatter: function(params) {
            let result = params[0].axisValue + '<br/>';
            params.forEach(param => {
                result += `${param.seriesName}: R$ ${parseFloat(param.value).toFixed(2).replace('.', ',')}<br/>`;
            });
            return result;
        }
    },
    xAxis: {
        type: 'category',
        data: dados.setores,
        axisLabel: {
            rotate: 45,  // Rotaciona labels para não sobrepor
            fontSize: 11
        }
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: function(value) {
                return 'R$ ' + value.toFixed(0);
            }
        }
    },
    series: [
        {
            name: 'Valor Mínimo',
            data: dados.minimos,
            type: 'bar',
            itemStyle: { color: '#28a745' }  // Verde
        },
        {
            name: 'Valor Máximo',
            data: dados.maximos,
            type: 'bar',
            itemStyle: { color: '#dc3545' }  // Vermelho
        },
        {
            name: 'Valor Médio',
            data: dados.medias,
            type: 'bar',
            itemStyle: { color: '#007bff' }  // Azul
        }
    ]
};
```

**Explicação de cada seção:**

#### tooltip
```javascript
tooltip: {
    trigger: 'axis',  // Mostra info quando passa mouse sobre eixo
    formatter: function(params) {  // Formata o texto do tooltip
        // Adiciona nome do setor
        // Para cada série, adiciona nome e valor em formato moeda
        return result;
    }
}
```

**Resultado no mouse over:**
```
Administração
Valor Mínimo: R$ 150,00
Valor Máximo: R$ 1.200,00
Valor Médio: R$ 583,00
```

#### xAxis (Eixo Horizontal)
```javascript
xAxis: {
    type: 'category',      // Eixo com categorias (setores)
    data: dados.setores,   // Array com nomes dos setores
    axisLabel: {
        rotate: 45,        // Rotaciona 45° para não sobrepor
        fontSize: 11       // Fonte pequena para caber
    }
}
```

**Por quê rotate 45?**
- Nomes de setores são longos
- Horizontal ficaria ilegível
- 45° é ângulo ótimo legibilidade/espaço

#### yAxis (Eixo Vertical)
```javascript
yAxis: {
    type: 'value',         // Eixo com valores numéricos
    axisLabel: {
        formatter: function(value) {
            return 'R$ ' + value.toFixed(0);  // Formata como moeda
        }
    }
}
```

**Resultado no eixo:**
```
R$ 0
R$ 500
R$ 1000
R$ 1500
R$ 2000
```

#### series (Dados do Gráfico)
```javascript
series: [
    {
        name: 'Valor Mínimo',
        data: dados.minimos,      // [95, 150, 120, ...]
        type: 'bar',              // Tipo de gráfico = barras
        itemStyle: {
            color: '#28a745'      // Verde (Bootstrap)
        }
    },
    // ... Máximo (vermelho) ...
    // ... Médio (azul) ...
]
```

**Por quê 3 séries separadas?**
- Permite comparação visual entre min, máx e média
- Cores distintas para diferenciar
- ECharts agrupa barras automaticamente por setor

**Cores escolhidas:**
- `#28a745` (Verde): Tradicional para mínimo/positivo
- `#dc3545` (Vermelho): Tradicional para máximo/alerta
- `#007bff` (Azul): Cor neutra para média

---

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework Python para web
- **SQLAlchemy**: ORM para queries ao banco
- **PostgreSQL**: Banco de dados relacional

### Frontend
- **HTML5**: Estrutura da página
- **CSS3**: Estilização responsiva
- **JavaScript ES6**: Requisições AJAX e lógica
- **ECharts 5**: Biblioteca de gráficos interativos

### Padrões de Arquitetura
- **DAO Pattern**: Abstração da camada de dados
- **MVC**: Model (DAO) - View (HTML) - Controller (rotas Flask)
- **REST API**: Dados retornados em JSON
- **Separação de Responsabilidades**: Backend calcula, Frontend visualiza

---

## Como Funciona

### Exemplo Prático

Suponha que no banco temos:

```
Setor: Administração
- Serviço 1: R$ 150
- Serviço 2: R$ 250
- Serviço 3: R$ 850

Setor: Tecnologia
- Serviço 1: R$ 180
- Serviço 2: R$ 750
```

### Passo 1: Query SQL executa

```sql
GROUP BY nme_setor
MIN(...) = R$ 150 (para Admin), R$ 180 (para TI)
MAX(...) = R$ 850 (para Admin), R$ 750 (para TI)
AVG(...) = R$ 416,67 (para Admin), R$ 465 (para TI)
```

### Passo 2: DAO retorna

```python
[
    {
        'nme_setor': 'Administração',
        'min_valor': 150,
        'max_valor': 850,
        'media_valor': 416.67,
        'total_servicos': 3
    },
    {
        'nme_setor': 'Tecnologia',
        'min_valor': 180,
        'max_valor': 750,
        'media_valor': 465,
        'total_servicos': 2
    }
]
```

### Passo 3: Rota transforma em JSON

```json
{
    "setores": ["Administração", "Tecnologia"],
    "minimos": [150, 180],
    "maximos": [850, 750],
    "medias": [416.67, 465]
}
```

### Passo 4: ECharts renderiza

```
     |
850  |     ███ (Admin Max)
     |     ███ ███ (TI Max)
750  |     ███ ███
     |     ███ ███ ░░░ (TI Min)
650  |     ███ ███ ░░░
     |     ███ ███ ░░░
     |     ███ ░░░ ░░░ (Admin Min)
150  | ░░░ ░░░ ░░░
     |___________________
        Admin  TI
     (verde) (azul) (vermelho)
```

---

## Benefícios da Implementação

### Para o Usuário (Solicitante)
✅ Visualiza facilmente comparação de preços entre setores
✅ Entende custo mínimo, máximo e médio esperado
✅ Interface interativa e responsiva
✅ Gráfico atualiza automaticamente se dados mudarem

### Para o Desenvolvedor
✅ Código bem estruturado e modular
✅ Fácil adicionar novos gráficos (mesmo padrão)
✅ Reutilizável em outros contextos
✅ Separação clara entre backend e frontend

### Para a Aplicação
✅ Query otimizada (usa GROUP BY, não Python loops)
✅ Resposta rápida (apenas dados necessários)
✅ Escalável (funciona com 10 ou 10.000 serviços)
✅ RESTful (segue boas práticas web)

---

## Possíveis Melhorias Futuras

1. **Filtros Adicionais**
   - Filtrar por data (últimos 30 dias, por exemplo)
   - Filtrar por status (ativo/inativo)
   - Range de preços customizado

2. **Mais Gráficos**
   - Gráfico de pizza com distribuição de serviços
   - Gráfico de linha com histórico temporal
   - Tabela com detalhes de cada setor

3. **Exportação**
   - Exportar dados como CSV
   - Gerar PDF com gráfico
   - Integração com Google Sheets

4. **Performance**
   - Cache de dados (Redis)
   - Paginação se houver muitos setores
   - Compressão de resposta JSON

5. **Segurança**
   - Autenticação de usuário
   - Verificar se usuário tem permissão
   - Rate limiting na API

---

## Conclusão

Esta feature implementa uma solução completa de análise de dados com:
- **Backend robusto** que calcula estatísticas no banco
- **API RESTful** que retorna dados estruturados
- **Frontend responsivo** com visualização interativa

O código segue boas práticas de:
- Separação de responsabilidades
- Tratamento de erros
- Validação de dados
- Design responsivo
- Performance (query otimizada)

Tudo isso para proporcionar melhor experiência ao usuário ao visualizar análise de valores de serviços! 📊

