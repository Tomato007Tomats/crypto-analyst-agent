# 🚀 Como Iniciar o Sistema

## Opção 1: Script Automático (2 Terminais)

### Terminal 1 - Backend
```bash
cd "/Users/tomaztinoco/Agents test"
./start_backend.sh
```

Aguarde até ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✅ Agent initialized and ready!
```

### Terminal 2 - Frontend
```bash
cd "/Users/tomaztinoco/Agents test/frontend"
npm run dev
```

Aguarde até ver:
```
✓ Ready in XXXms
○ Local:   http://localhost:3000
```

## Opção 2: Comandos Manuais

### 1. Backend
```bash
cd "/Users/tomaztinoco/Agents test"
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend (em outro terminal)
```bash
cd "/Users/tomaztinoco/Agents test/frontend"
npm run dev
```

## ✅ Verificar se está Rodando

### Backend
```bash
curl http://localhost:8000/api/opportunities
```

Deve retornar:
```json
{
  "opportunities": [],
  "count": 0
}
```

### Frontend
Abra no navegador: http://localhost:3000

## 🐛 Problemas Comuns

### Backend não inicia

**Erro: "Address already in use"**
```bash
# Matar processo na porta 8000
kill -9 $(lsof -t -i:8000)

# Tentar novamente
./start_backend.sh
```

**Erro: "OPENROUTER_API_KEY not found"**
```bash
# Verificar .env
cat .env | grep OPENROUTER

# Se não existir, adicionar:
echo 'OPENROUTER_API_KEY=sk-or-v1-...' >> .env
```

**Erro ao importar módulos**
```bash
# Reinstalar dependências
pip3 install -r requirements-simple.txt
```

### Frontend não inicia

**Erro: "Cannot find module"**
```bash
cd frontend
rm -rf node_modules
npm install
```

**Porta 3000 em uso**
```bash
# Matar processo na porta 3000
kill -9 $(lsof -t -i:3000)

# Ou usar outra porta
PORT=3001 npm run dev
```

## 📝 Logs

### Ver logs do Backend
Os logs aparecem no terminal onde você rodou `start_backend.sh`

### Ver logs do Frontend
Os logs aparecem no terminal onde você rodou `npm run dev`

## 🛑 Parar os Serviços

### Backend
No terminal do backend, pressione: **Ctrl+C**

Ou:
```bash
kill -9 $(lsof -t -i:8000)
```

### Frontend
No terminal do frontend, pressione: **Ctrl+C**

Ou:
```bash
kill -9 $(lsof -t -i:3000)
```

## ✅ Teste Rápido

Depois de iniciar ambos:

1. Abra: http://localhost:3000
2. Vá na aba "Chat with Agent"
3. Envie: "Hello!"
4. Deve receber uma resposta do agente

---

**Dica**: Sempre inicie o Backend ANTES do Frontend!






