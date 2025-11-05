"""
Vercel Serverless Function Entry Point
Adapta o FastAPI app para Vercel Serverless Functions
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from api.server import app

# Mangum adapta FastAPI para AWS Lambda/Vercel
handler = Mangum(app, lifespan="off")

