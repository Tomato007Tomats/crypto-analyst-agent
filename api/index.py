"""
Vercel Serverless Function Entry Point
Adapta o FastAPI app para Vercel Serverless Functions
"""

from api.server import app

# O Vercel procura por uma variável chamada "app" ou "handler"
# FastAPI já expõe o app que pode ser usado diretamente
handler = app

