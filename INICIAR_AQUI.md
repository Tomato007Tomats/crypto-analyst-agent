# 🚀 COMO INICIAR O DEEP AGENT

## ✅ Sistema Pronto com Deep Agent Oficial!

Seu sistema agora tem um **Deep Agent de verdade** com:
- ✅ **15 ferramentas** (7 custom + 8 built-in)
- ✅ **Filesystem tools** para gerenciar arquivos
- ✅ **Todo management** para planejamento
- ✅ **Subagents** para tarefas complexas
- ✅ **MCP integration** (CoinGecko, Firecrawl, Santiment)
- ✅ **Opportunities management**

---

## 🎯 Iniciar Tudo (1 Comando)

```bash
cd "/Users/tomaztinoco/Agents test"
./start.sh
```

Isso vai:
1. ✅ Verificar Python e Node.js
2. ✅ Instalar todas as dependências
3. ✅ Verificar e liberar portas 8000 e 3000
4. ✅ Iniciar Backend (Deep Agent) na porta 8000
5. ✅ Iniciar Frontend na porta 3000
6. ✅ Criar logs em `logs/backend.log` e `logs/frontend.log`

---

## 🌐 Acessar

Depois que o script iniciar, acesse:

**Frontend**: http://localhost:3000

Você verá:
- **📊 Aba "Opportunities"**: Gerenciamento de oportunidades
- **💬 Aba "Chat with Agent"**: Converse com o Deep Agent

---

## 💬 Testar o Deep Agent

No chat, teste estes prompts:

### 1. Introdução
```
Hello! Can you introduce yourself and list all your capabilities?
```

### 2. Usar Filesystem Tools
```
Create a file called 'bitcoin-analysis.md' with Bitcoin's current market overview
```

### 3. Usar Todo Management
```
Create a todo list for analyzing the top 5 cryptocurrencies
```

### 4. Usar Opportunities
```
Analyze Bitcoin and add any opportunities you find to the opportunities list
```

### 5. Usar MCP Tools
```
Get Bitcoin's current price from CoinGecko and analyze the trend
```

---

## 📊 Ferramentas Disponíveis

### Built-in Deep Agent Tools (8):
1. `write_file` - Criar/escrever arquivos
2. `ls` - Listar diretórios
3. `read_file` - Ler arquivos
4. `edit_file` - Editar arquivos
5. `glob` - Buscar por padrão de arquivo
6. `grep` - Buscar em conteúdo de arquivo
7. `write_todos` - Gerenciar lista de tarefas
8. `task` - Criar subagents para tarefas complexas

### Custom MCP Tools (3):
9. `coingecko_query` - Dados de preços e mercado
10. `firecrawl_scrape` - Web scraping de notícias
11. `santiment_query` - Métricas on-chain e sociais

### Custom Opportunities Tools (4):
12. `add_opportunity` - Adicionar oportunidade
13. `list_opportunities` - Listar oportunidades
14. `update_opportunity` - Atualizar oportunidade
15. `delete_opportunity` - Deletar oportunidade

---

## 🛑 Parar os Serviços

No terminal onde rodou `./start.sh`, pressione:

**Ctrl+C**

O script vai automaticamente parar backend e frontend.

---

## 📝 Ver Logs

### Logs em Tempo Real

**Backend:**
```bash
tail -f logs/backend.log
```

**Frontend:**
```bash
tail -f logs/frontend.log
```

### Ver Últimas 50 Linhas

```bash
cat logs/backend.log | tail -50
cat logs/frontend.log | tail -50
```

---

## 🐛 Troubleshooting

### "Address already in use"
```bash
# Matar processos nas portas
lsof -ti:8000,3000 | xargs kill -9

# Rodar novamente
./start.sh
```

### Backend não responde
```bash
# Ver logs
cat logs/backend.log

# Testar manualmente
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

### Frontend não carrega
```bash
# Ver logs
cat logs/frontend.log

# Reinstalar dependências
cd frontend
rm -rf node_modules
npm install
```

---

## 🎯 Estrutura do Sistema

```
Usuario Front-end (Browser)
        ↓
http://localhost:3000
        ↓
    Next.js App
        ↓
    [OpportunitiesTab | ChatTab]
        ↓
    Fetch/API calls
        ↓
http://localhost:8000/api/*
        ↓
    FastAPI Server
        ↓
    Deep Agent (create_deep_agent)
        ↓
    ┌─────────────────────────┐
    │ Built-in Tools (8):     │
    │ - Filesystem (6)        │
    │ - Todos (1)             │
    │ - Subagents (1)         │
    └─────────────────────────┘
        ↓
    ┌─────────────────────────┐
    │ Custom Tools (7):       │
    │ - MCP Tools (3)         │
    │ - Opportunities (4)     │
    └─────────────────────────┘
```

---

## ✨ Features do Deep Agent

### 1. Multi-Step Reasoning
O Deep Agent pode:
- Criar planos complexos
- Dividir tarefas em etapas
- Executar múltiplas ferramentas em sequência

### 2. Context Management
- Salvar análises em arquivos
- Organizar dados em diretórios
- Buscar informações quando necessário

### 3. Task Delegation
- Criar subagents para tarefas isoladas
- Executar trabalhos em paralelo
- Retornar resultados consolidados

### 4. State Persistence
- Mantém contexto entre conversas
- Checkpointing automático
- Memória de longo prazo (com Store)

---

## 📚 Próximos Passos

1. ✅ Rode `./start.sh`
2. ✅ Acesse http://localhost:3000
3. ✅ Teste o chat com diferentes prompts
4. ✅ Veja as oportunidades sendo criadas
5. 🔜 Deploy no LangSmith
6. 🔜 Adicionar autenticação
7. 🔜 Configurar PostgreSQL para produção

---

**Tudo pronto! Execute `./start.sh` e comece a usar! 🚀**



