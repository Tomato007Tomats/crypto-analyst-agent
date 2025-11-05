# 🚀 Crypto Analyst Deep Agent

Deep Agent com integração de múltiplos MCP servers para análise de criptomoedas e gerenciamento de oportunidades de investimento.

## 📋 Recursos

- **Deep Agent** com acesso a ferramentas de filesystem
- **MCP Servers Integration**:
  - 🪙 CoinGecko Pro API (preços e dados de mercado)
  - 🔥 Firecrawl (web scraping para notícias)
  - 📊 Santiment (métricas on-chain e sociais)
- **Gerenciamento de Oportunidades**:
  - Adicionar/atualizar/deletar oportunidades
  - Filtrar por status e tags
  - Interface web responsiva
- **Frontend React/Next.js**:
  - Aba de Oportunidades com visualização em grid
  - Chat com o agente em tempo real
  - Atualização automática a cada 5 segundos

## 🏗️ Estrutura do Projeto

```
Agents test/
├── .env                          # Variáveis de ambiente
├── mcp_config.json               # Configuração dos MCP servers
├── requirements.txt              # Dependências Python
├── README.md                     # Este arquivo
├── agent/
│   ├── deep_agent.py            # Deep Agent principal
│   ├── mcp_tools.py             # Ferramentas dos MCP servers
│   └── opportunities_manager.py  # Gerenciamento de oportunidades
├── api/
│   └── server.py                # FastAPI server
└── frontend/
    ├── package.json
    ├── src/
    │   ├── app/
    │   │   └── page.tsx         # Página principal
    │   └── components/
    │       ├── OpportunitiesTab.tsx  # Aba de oportunidades
    │       └── ChatTab.tsx           # Aba de chat
    └── ...
```

## 🚀 Setup & Instalação

### 1. Backend (Python)

```bash
# Instalar dependências
pip install -r requirements.txt

# As variáveis de ambiente já estão no .env
# Verificar se está tudo configurado
cat .env
```

### 2. Frontend (Next.js)

```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install

# Criar arquivo de configuração
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## 🎮 Como Usar

### 1. Iniciar o Backend (API)

```bash
# Na raiz do projeto
python -m api.server

# Ou com uvicorn
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: http://localhost:8000

### 2. Iniciar o Frontend

```bash
# No diretório frontend
cd frontend
npm run dev
```

O frontend estará disponível em: http://localhost:3000

### 3. Testar o Agente (CLI)

```bash
# Teste direto do agente
python -m agent.deep_agent
```

## 📡 Endpoints da API

### Chat
```
POST /api/chat
Body: { "message": "Analyze Bitcoin's market position" }
```

### Oportunidades
```
GET    /api/opportunities              # Listar todas
GET    /api/opportunities/:id          # Obter uma específica
POST   /api/opportunities              # Criar nova
PUT    /api/opportunities/:id          # Atualizar
DELETE /api/opportunities/:id          # Deletar
```

### WebSocket
```
WS /ws/chat  # Chat em tempo real com streaming
```

## 💡 Exemplos de Uso

### Via Chat (Frontend)

1. **Analisar mercado:**
   ```
   Analyze Bitcoin's current market position and add any opportunities you find
   ```

2. **Buscar oportunidades:**
   ```
   Find new investment opportunities for Ethereum
   ```

3. **Listar oportunidades:**
   ```
   Show me all active opportunities
   ```

### Via API (Programático)

```python
import asyncio
from agent.deep_agent import create_crypto_agent

async def main():
    agent, wrapper = await create_crypto_agent(dev_mode=True)
    
    result = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "Analyze the top 5 cryptocurrencies and identify opportunities"
        }]
    })
    
    print(result)
    await wrapper.shutdown()

asyncio.run(main())
```

## 🔧 Configuração dos MCP Servers

Os MCP servers são configurados em `mcp_config.json`:

- **CoinGecko**: Dados de preços e mercado
- **Firecrawl**: Web scraping para análise de sentimento
- **Santiment**: Métricas on-chain e sociais

As API keys já estão configuradas no `.env`.

## 🎨 Interface do Frontend

### Aba de Oportunidades
- Grid responsivo com cards de oportunidades
- Filtros por status e tags
- Modal de detalhes com informações completas
- Ações: marcar como executada, descartar, deletar
- Auto-refresh a cada 5 segundos

### Aba de Chat
- Chat em tempo real com o agente
- Sugestões de prompts
- Histórico de conversas
- Indicador de loading

## 🔐 Modo Dev vs Produção

### Dev Mode (Atual)
- `StateBackend`: Armazenamento efêmero (memória)
- SQLite para checkpointing
- Sem autenticação
- CORS aberto para localhost

### Produção (Para Deploy)
```python
# Configuração de produção
backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/opportunities/": StoreBackend(),  # PostgreSQL
        "/analysis/": StoreBackend(),
        "/reports/": StoreBackend(),
    }
)

# PostgreSQL Store
from langgraph.store.postgres import PostgresStore
store = PostgresStore.from_conn_string("postgresql://...")

# PostgreSQL Checkpointer
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
```

## 🚀 Próximos Passos

1. **Adicionar autenticação** (JWT tokens)
2. **Implementar PostgreSQL** para persistência
3. **Adicionar WebSocket streaming** para respostas em tempo real
4. **Deploy no LangSmith**
5. **Adicionar mais filtros** na aba de oportunidades
6. **Implementar notificações** para novas oportunidades
7. **Adicionar gráficos** para visualização de métricas

## 📝 Notas

- Em modo dev, as oportunidades são armazenadas em memória
- Os MCP servers são configurados mas não inicializados automaticamente
- Para produção, configure PostgreSQL e ajuste o backend
- As API keys dos MCP servers já estão no `.env`

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verificar dependências
pip install -r requirements.txt --upgrade

# Verificar variáveis de ambiente
cat .env
```

### Frontend não conecta
```bash
# Verificar se o backend está rodando
curl http://localhost:8000/

# Verificar variável de ambiente
cat frontend/.env.local
```

### MCP Servers não funcionam
- Em modo dev, os MCPs são simulados
- Para produção, configure os processos dos MCP servers
- Verifique as API keys no `.env`

## 📞 Suporte

Para dúvidas ou problemas, verifique:
- Logs do backend: Terminal onde rodou `python -m api.server`
- Logs do frontend: Terminal onde rodou `npm run dev`
- Console do navegador: F12 → Console

---

**Desenvolvido com Deep Agents, LangGraph, e Next.js** 🚀

