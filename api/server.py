"""
FastAPI Server for Crypto Analyst Agent
Provides REST API for the front-end
"""

import os
import json
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agent.deep_agent import create_crypto_deep_agent
from agent.opportunities_manager import opportunities_store, Opportunity

# Load environment
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Crypto Analyst Agent API",
    description="API for cryptocurrency analysis and opportunities management",
    version="1.0.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    global agent
    print("🚀 Starting API server...")
    try:
        agent = await create_crypto_deep_agent()
        print("✅ Deep Agent initialized and ready!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        import traceback
        traceback.print_exc()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Server shutdown complete")


# Pydantic models for API
class ChatMessage(BaseModel):
    content: str
    role: str = "user"


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    thread_id: Optional[str] = None


class OpportunityCreate(BaseModel):
    title: str
    asset: str
    type: str
    confidence: float
    rationale: str
    sources: List[str] = []
    metrics: Dict = {}
    tags: List[str] = []


class OpportunityUpdate(BaseModel):
    updates: Dict


# API Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Crypto Analyst Agent API",
        "version": "1.0.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the agent
    """
    global agent
    
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Invoke agent
        result = await agent.ainvoke(
            {"messages": [("user", request.message)]},
            config={"configurable": {"thread_id": request.thread_id or "default"}}
        )
        
        # Extract response
        if "output" in result:
            response_text = result["output"]
        elif "messages" in result:
            last_message = result["messages"][-1]
            if isinstance(last_message, dict):
                response_text = last_message.get("content", str(last_message))
            else:
                response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        else:
            response_text = str(result)
        
        return ChatResponse(
            response=response_text,
            thread_id=request.thread_id
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/opportunities")
async def get_opportunities(
    status: Optional[str] = None,
    tags: Optional[str] = None  # comma-separated
):
    """
    Get all opportunities
    Optional filters: status, tags
    """
    try:
        tag_list = tags.split(",") if tags else None
        opps = opportunities_store.list_all(status=status, tags=tag_list)
        
        return {
            "opportunities": [opp.dict() for opp in opps],
            "count": len(opps)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/opportunities")
async def create_opportunity(opportunity: OpportunityCreate):
    """
    Create a new opportunity
    """
    try:
        from datetime import datetime
        
        # Generate ID
        opp_id = f"opp_{int(datetime.utcnow().timestamp())}"
        
        # Create opportunity object
        new_opp = Opportunity(
            id=opp_id,
            **opportunity.dict()
        )
        
        # Add to store
        opportunities_store.add(new_opp)
        
        return {
            "success": True,
            "opportunity_id": opp_id,
            "opportunity": new_opp.dict()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/opportunities/{opportunity_id}")
async def get_opportunity(opportunity_id: str):
    """
    Get a specific opportunity by ID
    """
    opp = opportunities_store.get(opportunity_id)
    
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    return opp.dict()


@app.put("/api/opportunities/{opportunity_id}")
async def update_opportunity(opportunity_id: str, update: OpportunityUpdate):
    """
    Update an opportunity
    """
    success = opportunities_store.update(opportunity_id, update.updates)
    
    if not success:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    updated_opp = opportunities_store.get(opportunity_id)
    return {
        "success": True,
        "opportunity": updated_opp.dict()
    }


@app.delete("/api/opportunities/{opportunity_id}")
async def delete_opportunity(opportunity_id: str):
    """
    Delete an opportunity
    """
    success = opportunities_store.delete(opportunity_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    return {"success": True, "message": f"Deleted opportunity {opportunity_id}"}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with streaming
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process with agent
            result = await agent.ainvoke(
                {"messages": [("user", message.get("content", ""))]},
                config={"configurable": {"thread_id": "ws_session"}}
            )
            
            # Extract response
            if "output" in result:
                response = result["output"]
            elif "messages" in result:
                last_msg = result["messages"][-1]
                response = last_msg.get("content", str(last_msg)) if isinstance(last_msg, dict) else str(last_msg)
            else:
                response = str(result)
            
            # Send response
            await websocket.send_json({
                "type": "response",
                "content": response
            })
    
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes in dev
        log_level="info"
    )

