"""
Deep Agent with MCP Integration and Opportunities Management

Official Implementation using LangChain 1.0 create_agent with middleware
Per Docs by LangChain: https://docs.langchain.com/oss/python/deepagents/middleware

Deep Agent includes by default:
- FilesystemMiddleware: 6 tools (ls, read_file, write_file, edit_file, glob, grep)
- TodoListMiddleware: 1 tool (write_todos)
- SubAgentMiddleware: 1 tool (task)
Plus custom tools: MCP integration & Opportunities management
"""

import os
from dotenv import load_dotenv
from deepagents import create_deep_agent, FilesystemMiddleware, SubAgentMiddleware
from langchain_openai import ChatOpenAI

from agent.mcp_tools import get_mcp_tools
from agent.opportunities_manager import get_opportunities_tools

# Load environment variables
load_dotenv()


async def create_crypto_deep_agent():
    """
    Create a Deep Agent using LangChain 1.0 create_agent with middleware
    
    This agent is now fully async and uses a persistent database for opportunities.
    """
    print("🚀 Initializing Crypto Analyst Deep Agent...")
    
    # Configure model
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    model = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key,
        model="anthropic/claude-3.5-sonnet",
        temperature=0.7,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Crypto Analyst Deep Agent"
        }
    )
    
    # Get custom tools
    mcp_tools = get_mcp_tools()
    opportunities_tools = get_opportunities_tools()
    custom_tools = mcp_tools + opportunities_tools
    
    # System prompt
    system_prompt = """You are an expert cryptocurrency analyst with access to multiple data sources and tools.

Your capabilities:
1. **Market Data Analysis** (via CoinGecko MCP)
   - Get real-time prices and market data
   - Analyze trends and patterns
   - Track market movements

2. **Web Intelligence** (via Firecrawl MCP)
   - Scrape and analyze crypto news
   - Monitor sentiment from blogs and forums
   - Extract insights from web sources

3. **On-Chain & Social Metrics** (via Santiment MCP)
   - Analyze on-chain data
   - Track social sentiment
   - Monitor development activity

4. **Opportunities Management**
   - Add new investment opportunities you identify
   - Update existing opportunities with new data
   - List and filter opportunities
   - Delete outdated opportunities

5. **File System** (built-in Deep Agent tools)
   - Create and edit files with analysis reports
   - Organize data in directories
   - Search for information in files

6. **Task Management** (built-in Deep Agent tools)
   - Create todos for multi-step analysis
   - Track progress on complex tasks

**Your Task:**
Analyze market data, identify investment opportunities, and maintain the opportunities list in the database.
When you identify a potential opportunity:
1. Gather data from multiple sources
2. Analyze the risk/reward
3. Calculate confidence level
4. Add it to the opportunities list with clear rationale

**Guidelines:**
- Be data-driven: Always cite your sources
- Be honest about confidence levels
- Update opportunities when new data emerges
- Use clear, actionable language
- Consider multiple timeframes (short, medium, long)

**Response Style:**
- Start with key insights
- Show your reasoning with data
- Provide clear recommendations
- Include relevant metrics
"""
    
    # Create Deep Agent using official create_deep_agent
    # Per Docs by LangChain, this automatically includes:
    # - FilesystemMiddleware (6 tools)
    # - TodoListMiddleware (1 tool) 
    # - SubAgentMiddleware (1 tool)
    agent = create_deep_agent(
        model=model,
        tools=custom_tools,
        system_prompt=system_prompt,
        name="crypto_analyst_agent",
        description="Asynchronous cryptocurrency analyst agent with persistent storage.",
        # Ensure agent can handle async tools correctly
        handle_parsing_errors=True, 
    )
    
    print("✅ Deep Agent initialized successfully!")
    print(f"📊 Custom tools: {len(custom_tools)}")
    print(f"   - MCP Tools: {len(mcp_tools)}")
    print(f"   - Opportunities Tools: {len(opportunities_tools)}")
    print(f"📁 Built-in Deep Agent tools: ~8")
    print(f"   - Filesystem: 6 (ls, read_file, write_file, edit_file, glob, grep)")
    print(f"   - Todos: 1 (write_todos)")
    print(f"   - Subagents: 1 (task)")
    print(f"🎯 Total tools: {len(custom_tools)} + 8 built-in")
    
    return agent


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        agent = await create_crypto_deep_agent()
        
        # Test query
        print("\n" + "="*60)
        print("Testing agent with a query...")
        print("="*60 + "\n")
        
        result = await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": "Hello! Can you introduce yourself?"
            }]
        })
        
        print("\n" + "="*60)
        print("Agent Response:")
        print("="*60)
        print(result)
    
    asyncio.run(main())

