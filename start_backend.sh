#!/bin/bash

echo "🚀 Iniciando Backend API..."
echo "================================"
echo ""

cd "/Users/tomaztinoco/Agents test"

# Verificar se já está rodando
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta 8000 já está em uso"
    echo "Matando processo anterior..."
    kill -9 $(lsof -t -i:8000) 2>/dev/null
    sleep 2
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado"
    exit 1
fi

echo "✅ Iniciando servidor..."
echo ""
echo "📍 URL: http://localhost:8000"
echo "📍 Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "-----------------------------------"

# Iniciar servidor
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload






