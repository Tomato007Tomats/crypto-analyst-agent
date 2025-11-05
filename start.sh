#!/bin/bash

# Script para iniciar o Crypto Analyst Deep Agent em modo dev

echo "🚀 Starting Crypto Analyst Deep Agent..."
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para cleanup quando Ctrl+C
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    
    # Matar processos nas portas 8000 e 3000
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        kill -9 $(lsof -t -i:8000) 2>/dev/null
        echo -e "${GREEN}✓ Backend stopped${NC}"
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        kill -9 $(lsof -t -i:3000) 2>/dev/null
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    fi
    
    exit 0
}

trap cleanup INT TERM

# 1. Verificar Python
echo -e "${BLUE}[1/5] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
echo ""

# 2. Verificar Node.js
echo -e "${BLUE}[2/5] Checking Node.js...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found. Please install Node.js${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo -e "${GREEN}✓ npm found: $(npm --version)${NC}"
echo ""

# 3. Instalar dependências Python
echo -e "${BLUE}[3/5] Installing Python dependencies...${NC}"
pip3 install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ Error installing Python dependencies${NC}"
    exit 1
fi
echo ""

# 4. Instalar dependências Frontend
echo -e "${BLUE}[4/5] Installing Frontend dependencies...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    else
        echo -e "${RED}❌ Error installing frontend dependencies${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Node modules already installed${NC}"
fi

# Criar .env.local se não existir
if [ ! -f ".env.local" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo -e "${GREEN}✓ Created frontend/.env.local${NC}"
fi

cd ..
echo ""

# 5. Verificar se portas estão livres
echo -e "${BLUE}[5/5] Checking ports...${NC}"

# Verificar porta 8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 8000 is in use, killing process...${NC}"
    kill -9 $(lsof -t -i:8000) 2>/dev/null
    sleep 2
fi

# Verificar porta 3000
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 3000 is in use, killing process...${NC}"
    kill -9 $(lsof -t -i:3000) 2>/dev/null
    sleep 2
fi

echo -e "${GREEN}✓ Ports 8000 and 3000 are available${NC}"
echo ""

# Iniciar serviços
echo "========================================="
echo -e "${GREEN}🎯 STARTING SERVICES${NC}"
echo "========================================="
echo ""
echo -e "${BLUE}📊 Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}📚 API Docs:${NC} http://localhost:8000/docs"
echo -e "${BLUE}🌐 Frontend:${NC} http://localhost:3000"
echo ""
echo -e "${YELLOW}⌨️  Press Ctrl+C to stop all services${NC}"
echo ""
echo "========================================="
echo ""

# Criar diretório para logs se não existir
mkdir -p logs

# Iniciar backend
echo -e "${BLUE}Starting Backend...${NC}"
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

# Aguardar backend inicializar
echo "Waiting for backend to initialize..."
sleep 8

# Verificar se backend está rodando
if curl -s http://localhost:8000/api/opportunities >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is responding${NC}"
else
    echo -e "${RED}❌ Backend failed to start. Check logs/backend.log${NC}"
    cat logs/backend.log | tail -20
    cleanup
fi

echo ""

# Iniciar frontend
echo -e "${BLUE}Starting Frontend...${NC}"
cd frontend
PORT=3000 npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

cd ..

echo ""
echo "========================================="
echo -e "${GREEN}✅ ALL SERVICES RUNNING${NC}"
echo "========================================="
echo ""
echo "📊 Backend:  http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   - Backend:  logs/backend.log"
echo "   - Frontend: logs/frontend.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Aguardar Ctrl+C
wait

