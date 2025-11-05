# 📁 Estrutura do Projeto

```
Agents test/
│
├── 📄 .env                          # Variáveis de ambiente (API keys)
├── 📄 .gitignore                    # Arquivos ignorados pelo Git
├── 📄 mcp_config.json               # Configuração dos MCP servers
├── 📄 requirements.txt              # Dependências Python
├── 📄 README.md                     # Documentação completa
├── 📄 QUICKSTART.md                 # Guia rápido de início
├── 📄 STRUCTURE.md                  # Este arquivo
├── 🚀 start.sh                      # Script automático de inicialização
│
├── 🤖 agent/                        # Deep Agent e ferramentas
│   ├── __init__.py
│   ├── deep_agent.py                # ⭐ Deep Agent principal
│   ├── mcp_tools.py                 # ⭐ Ferramentas dos MCP servers
│   └── opportunities_manager.py     # ⭐ Gerenciamento de oportunidades
│
├── 🌐 api/                          # Backend API (FastAPI)
│   ├── __init__.py
│   └── server.py                    # ⭐ FastAPI server com endpoints
│
└── 💻 frontend/                     # Frontend (Next.js + React)
    ├── package.json
    ├── tsconfig.json
    ├── next.config.js
    ├── tailwind.config.ts
    ├── postcss.config.js
    │
    └── src/
        ├── app/
        │   ├── page.tsx              # ⭐ Página principal
        │   ├── layout.tsx            # Layout da aplicação
        │   └── globals.css           # Estilos globais
        │
        └── components/
            ├── OpportunitiesTab.tsx  # ⭐ Aba de oportunidades
            └── ChatTab.tsx           # ⭐ Aba de chat
```

## 🔑 Arquivos Principais

### Backend (Python)

#### `agent/deep_agent.py`
- Deep Agent principal
- Inicializa MCP servers
- Configura ferramentas e backend
- System prompt especializado em crypto

#### `agent/mcp_tools.py`
- Ferramentas dos MCP servers:
  - CoinGeckoMCPTool (preços e mercado)
  - FirecrawlMCPTool (web scraping)
  - SantimentMCPTool (on-chain metrics)

#### `agent/opportunities_manager.py`
- Schema de Oportunidades (Pydantic)
- Store em memória (dev mode)
- Ferramentas CRUD:
  - AddOpportunityTool
  - ListOpportunitiesTool
  - UpdateOpportunityTool
  - DeleteOpportunityTool

#### `api/server.py`
- FastAPI server
- Endpoints REST:
  - POST `/api/chat` - Chat com agente
  - GET `/api/opportunities` - Listar oportunidades
  - POST `/api/opportunities` - Criar oportunidade
  - PUT `/api/opportunities/:id` - Atualizar
  - DELETE `/api/opportunities/:id` - Deletar
- WebSocket `/ws/chat` para streaming

### Frontend (Next.js)

#### `src/app/page.tsx`
- Página principal
- Sistema de tabs
- Header e footer

#### `src/components/OpportunitiesTab.tsx`
- Grid de oportunidades
- Modal de detalhes
- Filtros por status/tags
- Auto-refresh (SWR)
- Ações: executar, descartar, deletar

#### `src/components/ChatTab.tsx`
- Interface de chat
- Histórico de mensagens
- Input com textarea
- Sugestões de prompts
- Loading states

## 🔄 Fluxo de Dados

```
                     ┌─────────────────┐
                     │   Frontend      │
                     │  (Next.js)      │
                     └────────┬────────┘
                              │
                              │ HTTP/WS
                              │
                     ┌────────▼────────┐
                     │   FastAPI       │
                     │   Server        │
                     └────────┬────────┘
                              │
                              │
                     ┌────────▼────────┐
                     │   Deep Agent    │
                     └────────┬────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
       ┌────────▼─────┐  ┌───▼────┐  ┌────▼─────┐
       │ MCP Tools    │  │ Opps   │  │ File     │
       │ - CoinGecko  │  │ Manager│  │ System   │
       │ - Firecrawl  │  │        │  │          │
       │ - Santiment  │  │        │  │          │
       └──────────────┘  └────────┘  └──────────┘
```

## 🎨 Tech Stack

### Backend
- **Deep Agents**: Framework de agentes
- **LangGraph**: Orquestração de workflows
- **LangChain**: Ferramentas e integrações
- **FastAPI**: API REST moderna
- **Pydantic**: Validação de dados
- **OpenRouter**: LLM gateway (Claude)

### Frontend
- **Next.js 14**: Framework React
- **React 18**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **SWR**: Data fetching
- **Lucide React**: Ícones

### MCP Servers
- **CoinGecko Pro**: Market data
- **Firecrawl**: Web scraping
- **Santiment**: On-chain metrics

## 🚀 Desenvolvimento

### Modo Dev (Atual)
- StateBackend (ephemeral)
- SQLite checkpointer (opcional)
- CORS aberto para localhost
- MCP tools simulados

### Modo Produção (Futuro)
- CompositeBackend com StoreBackend
- PostgreSQL para persistência
- Autenticação JWT
- MCP servers reais em background
- Rate limiting
- Logging estruturado

## 📊 Schemas de Dados

### Opportunity
```python
{
  "id": "opp_123456",
  "title": "Bitcoin Accumulation",
  "asset": "bitcoin",
  "type": "buy",
  "confidence": 75.0,
  "rationale": "Strong support...",
  "sources": ["coingecko", "santiment"],
  "metrics": {"price": 61500, "volume": "25B"},
  "created_at": "2025-01-01T12:00:00",
  "expires_at": null,
  "status": "active",
  "tags": ["btc", "long-term"]
}
```

### ChatMessage
```typescript
{
  role: "user" | "assistant",
  content: string,
  timestamp: Date
}
```

## 🔧 Configuração

### Variáveis de Ambiente (`.env`)
```bash
# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=pr-...

# OpenRouter (Claude)
OPENROUTER_API_KEY=sk-or-v1-...

# MCP API Keys
COINGECKO_PRO_API_KEY=CG-...
FIRECRAWL_API_KEY=fc-...

# Database
DATABASE_PATH=./data/agent.db
```

### MCP Config (`mcp_config.json`)
```json
{
  "mcpServers": {
    "coingecko_mcp_local": { ... },
    "firecrawl-mcp": { ... },
    "santiment": { ... }
  }
}
```

## 📝 Próximos Passos

1. [ ] Implementar WebSocket streaming
2. [ ] Adicionar autenticação
3. [ ] Migrar para PostgreSQL
4. [ ] Deploy no LangSmith
5. [ ] Adicionar testes
6. [ ] CI/CD pipeline
7. [ ] Monitoring e alertas
8. [ ] Documentação da API (OpenAPI)

---

**Estrutura criada em:** 2025-01-01  
**Versão:** 1.0.0-dev

