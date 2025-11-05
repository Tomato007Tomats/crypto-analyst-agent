# 🚀 Quick Start Guide

## Começar em 3 minutos

### Opção 1: Script Automático (Recomendado)

```bash
# Dar permissão ao script
chmod +x start.sh

# Rodar tudo
./start.sh
```

Isso vai:
1. ✅ Verificar Python
2. ✅ Instalar dependências Python
3. ✅ Instalar dependências Node.js
4. ✅ Iniciar backend (porta 8000)
5. ✅ Iniciar frontend (porta 3000)

### Opção 2: Manual

#### Terminal 1 - Backend
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar API
python -m api.server
```

#### Terminal 2 - Frontend
```bash
# Instalar dependências
cd frontend
npm install

# Criar .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Iniciar frontend
npm run dev
```

## 🎯 Acessar

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Testar

### 1. Via Frontend
1. Abra http://localhost:3000
2. Vá na aba "Chat with Agent"
3. Envie: "Analyze Bitcoin's market position"

### 2. Via API
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find investment opportunities for Ethereum"}'
```

### 3. Via Python
```python
import asyncio
from agent.deep_agent import create_crypto_agent

async def main():
    agent, wrapper = await create_crypto_agent()
    
    result = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "Analyze the market"
        }]
    })
    
    print(result)
    await wrapper.shutdown()

asyncio.run(main())
```

## 📱 Usar a Interface

### Aba: Oportunidades
- Veja todas as oportunidades de investimento
- Clique em um card para ver detalhes
- Marque como executada/descartada
- Auto-atualiza a cada 5 segundos

### Aba: Chat
- Converse com o agente
- Peça análises de mercado
- Solicite novas oportunidades
- Use os prompts sugeridos

## 💡 Exemplos de Prompts

```
"Analyze Bitcoin's current market position and add opportunities"
"Find new investment opportunities for top 10 cryptos"
"What are the trending coins right now?"
"Scrape the latest crypto news and summarize"
"Show me on-chain metrics for Ethereum"
```

## 🐛 Problemas?

### Backend não inicia
```bash
pip install -r requirements.txt --upgrade
python -m api.server
```

### Frontend não conecta
```bash
# Verificar se backend está rodando
curl http://localhost:8000/

# Reinstalar dependências
cd frontend
rm -rf node_modules
npm install
```

### MCP Tools não funcionam
Em modo dev, os MCP tools são simulados. Para produção:
1. Configure os MCP servers reais
2. Veja `mcp_config.json` para configuração

## 📚 Próximos Passos

1. ✅ Teste o chat com o agente
2. ✅ Veja a aba de oportunidades
3. ✅ Adicione manualmente uma oportunidade (via API)
4. ✅ Peça ao agente para analisar um crypto específico

## 🔥 Features

- [x] Deep Agent com múltiplos MCP servers
- [x] Gerenciamento de oportunidades
- [x] Interface web responsiva
- [x] Chat em tempo real
- [x] Auto-refresh das oportunidades
- [ ] WebSocket streaming (próximo)
- [ ] Autenticação (próximo)
- [ ] Deploy LangSmith (próximo)

---

Divirta-se! 🎉

