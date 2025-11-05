# 🚀 Guia de Deploy - Crypto Analyst Deep Agent

Este guia explica como fazer o deploy do projeto no GitHub e Vercel.

## 📋 Arquitetura do Deploy

Este projeto possui duas partes principais:

1. **Frontend (Next.js)** - Deploy no Vercel
2. **Backend (FastAPI + LangGraph)** - Deploy separado (Render, Railway, etc.)

## 🔧 Preparação

### 1. Variáveis de Ambiente

Antes do deploy, você precisa configurar as seguintes variáveis de ambiente:

```bash
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_project_name
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 2. Estrutura do Projeto

```
Agents test/
├── frontend/          # Next.js app (deploy no Vercel)
├── agent/            # Deep Agent code
├── api/              # FastAPI server
└── requirements.txt  # Python dependencies
```

## 🚀 Deploy no GitHub

### 1. Criar Repositório no GitHub

```bash
# Inicializar git (se ainda não foi feito)
git init

# Adicionar remote
git remote add origin https://github.com/seu-usuario/crypto-analyst-agent.git

# Fazer commit inicial
git add .
git commit -m "Initial commit: Crypto Analyst Deep Agent"

# Push para GitHub
git push -u origin master
```

## 🌐 Deploy do Frontend no Vercel

### Opção 1: Via Interface Web do Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Clique em "New Project"
3. Importe seu repositório do GitHub
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Adicione as variáveis de ambiente:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
   (Atualize depois com a URL do backend em produção)

6. Clique em "Deploy"

### Opção 2: Via CLI do Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Fazer login
vercel login

# Deploy do frontend
cd frontend
vercel --prod
```

## 🖥️ Deploy do Backend (Opções)

### Opção 1: Render.com (Recomendado - Free Tier)

1. Crie uma conta em [render.com](https://render.com)
2. Clique em "New Web Service"
3. Conecte seu repositório do GitHub
4. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.server:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `.` (raiz do projeto)

5. Adicione as variáveis de ambiente (mesmas do `.env.example`)

6. Clique em "Create Web Service"

### Opção 2: Railway.app

1. Crie uma conta em [railway.app](https://railway.app)
2. Clique em "New Project" → "Deploy from GitHub repo"
3. Selecione seu repositório
4. Railway detectará automaticamente Python
5. Configure as variáveis de ambiente
6. Deploy automático!

### Opção 3: Fly.io

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Criar app
fly launch

# Deploy
fly deploy
```

## 🔗 Conectar Frontend ao Backend

Depois de fazer deploy do backend, atualize a variável de ambiente no Vercel:

1. Vá para o projeto no Vercel
2. Settings → Environment Variables
3. Atualize `NEXT_PUBLIC_API_URL` com a URL do backend:
   ```
   NEXT_PUBLIC_API_URL=https://seu-backend.render.com
   ```
4. Redeploy o frontend

## 🧪 Testar o Deploy

### Frontend
Acesse: `https://seu-projeto.vercel.app`

### Backend
Acesse: `https://seu-backend.render.com/docs` (documentação automática da API)

### Teste de integração
```bash
# Testar endpoint de saúde
curl https://seu-backend.render.com/

# Testar chat
curl -X POST https://seu-backend.render.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze Bitcoin"}'
```

## 📝 Notas Importantes

### CORS
O backend já está configurado para aceitar requisições do frontend. Se precisar ajustar:

```python
# api/server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Persistência
Em produção, considere:
- Usar PostgreSQL ao invés de SQLite
- Configurar Redis para cache
- Usar um storage service (S3, etc.) para arquivos

### Monitoramento
- Vercel: Logs automáticos no dashboard
- Render/Railway: Logs integrados
- LangSmith: Tracing automático com `LANGSMITH_TRACING=true`

## 🔐 Segurança

1. **Nunca commite** o arquivo `.env` com API keys reais
2. Use sempre variáveis de ambiente nas plataformas de deploy
3. Configure rate limiting no backend
4. Adicione autenticação se necessário

## 🚨 Troubleshooting

### Frontend não conecta ao backend
- Verifique se `NEXT_PUBLIC_API_URL` está correta
- Verifique CORS no backend
- Veja os logs no console do navegador (F12)

### Backend não inicia
- Verifique as variáveis de ambiente
- Veja os logs na plataforma de deploy
- Teste localmente primeiro: `uvicorn api.server:app --reload`

### MCP Servers não funcionam
- Em produção, configure os processos dos MCP servers adequadamente
- Verifique se as API keys estão configuradas
- Veja logs de erro no LangSmith

## 📞 Suporte

Para problemas:
1. Verifique os logs da plataforma de deploy
2. Teste localmente primeiro
3. Consulte a documentação:
   - [Vercel Docs](https://vercel.com/docs)
   - [Render Docs](https://render.com/docs)
   - [LangSmith Docs](https://docs.smith.langchain.com/)

---

**Desenvolvido com Deep Agents, LangGraph, Next.js e muito ☕**

