"""
Graph entry point para LangSmith Deployment
Este arquivo exporta o agent compilado para deploy no LangSmith
"""

import asyncio
from agent.deep_agent import create_crypto_deep_agent

# Criar o agent de forma síncrona para LangSmith
_agent = None

def get_agent():
    """Lazy loading do agent"""
    global _agent
    if _agent is None:
        _agent = asyncio.run(create_crypto_deep_agent())
    return _agent

# Exportar agent para LangSmith
agent = get_agent()

