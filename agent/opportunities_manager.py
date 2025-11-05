"""
Opportunities Manager - Tools for managing investment opportunities
Now with persistent storage using SQLAlchemy for production.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import and_

from agent.database import AsyncSessionLocal, OpportunityORM

# --- Pydantic Schemas ---
class Opportunity(BaseModel):
    """Schema for an investment opportunity"""
    id: str = Field(description="Unique identifier for the opportunity")
    title: str = Field(description="Title/name of the opportunity")
    asset: str = Field(description="Asset or cryptocurrency")
    type: str = Field(description="Type: buy, sell, hold, watch")
    confidence: float = Field(description="Confidence level (0-100)", ge=0, le=100)
    rationale: str = Field(description="Why this is an opportunity")
    sources: List[str] = Field(default=[], description="Data sources used")
    metrics: Dict[str, Any] = Field(default={}, description="Relevant metrics")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    expires_at: Optional[str] = Field(default=None, description="When this opportunity expires")
    status: str = Field(default="active", description="active, expired, executed, dismissed")
    tags: List[str] = Field(default=[], description="Tags for categorization")

    class Config:
        orm_mode = True

class AddOpportunityInput(BaseModel):
    """Input for adding an opportunity"""
    title: str = Field(description="Title of the opportunity")
    asset: str = Field(description="Asset or cryptocurrency (e.g., 'bitcoin', 'ethereum')")
    type: str = Field(description="Type: buy, sell, hold, or watch")
    confidence: float = Field(description="Confidence level (0-100)")
    rationale: str = Field(description="Detailed explanation of why this is an opportunity")
    sources: List[str] = Field(default=[], description="List of data sources")
    metrics: Dict[str, Any] = Field(default={}, description="Relevant metrics")
    tags: List[str] = Field(default=[], description="Tags for categorization")

# --- Database Store ---
class OpportunitiesDBStore:
    """
    Handles database operations for opportunities.
    """
    
    def __init__(self):
        self.async_session = AsyncSessionLocal

    async def add(self, opportunity: Opportunity) -> str:
        async with self.async_session() as session:
            async with session.begin():
                db_opp = OpportunityORM(**opportunity.dict())
                session.add(db_opp)
            await session.commit()
            return opportunity.id

    async def get(self, opportunity_id: str) -> Optional[Opportunity]:
        async with self.async_session() as session:
            result = await session.execute(select(OpportunityORM).filter(OpportunityORM.id == opportunity_id))
            db_opp = result.scalars().first()
            return Opportunity.from_orm(db_opp) if db_opp else None

    async def list_all(self, status: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Opportunity]:
        async with self.async_session() as session:
            query = select(OpportunityORM)
            filters = []
            if status:
                filters.append(OpportunityORM.status == status)
            if tags:
                # Basic tag filtering: checks if any of the provided tags are in the opportunity's tags list
                # This is a simplification. For complex queries, JSON functions of the DB would be better.
                query = query.filter(OpportunityORM.tags.op('?')(tags[0])) # Example for one tag in postgres
            
            if filters:
                query = query.filter(and_(*filters))
                
            result = await session.execute(query)
            db_opps = result.scalars().all()
            return [Opportunity.from_orm(opp) for opp in db_opps]

    async def update(self, opportunity_id: str, updates: Dict[str, Any]) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(OpportunityORM).filter(OpportunityORM.id == opportunity_id))
                db_opp = result.scalars().first()
                if not db_opp:
                    return False
                
                for key, value in updates.items():
                    if hasattr(db_opp, key):
                        setattr(db_opp, key, value)
                
                await session.commit()
                return True

    async def delete(self, opportunity_id: str) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(OpportunityORM).filter(OpportunityORM.id == opportunity_id))
                db_opp = result.scalars().first()
                if not db_opp:
                    return False
                
                await session.delete(db_opp)
                await session.commit()
                return True

# --- Global Store Instance ---
opportunities_store = OpportunitiesDBStore()

# --- LangChain Tools (Updated for Async) ---

class AddOpportunityTool(BaseTool):
    """Tool for adding new opportunities"""
    name: str = "add_opportunity"
    description: str = "Add a new investment opportunity to the persistent database. Use this when you identify a potential investment opportunity."
    args_schema: type[BaseModel] = AddOpportunityInput
    
    def _run(self, **kwargs) -> str:
        raise NotImplementedError("Use arun for async operations")

    async def _arun(self, **kwargs) -> str:
        try:
            timestamp = datetime.utcnow().timestamp()
            opp_id = f"opp_{int(timestamp)}"
            opportunity = Opportunity(id=opp_id, **kwargs)
            await opportunities_store.add(opportunity)
            return f"✓ Added opportunity '{opportunity.title}' (ID: {opp_id})"
        except Exception as e:
            return f"✗ Error adding opportunity: {str(e)}"

@tool
async def list_opportunities(dummy: Optional[str] = "") -> str:
    """List all current investment opportunities from the database. Returns a formatted list."""
    try:
        opps = await opportunities_store.list_all()
        if not opps:
            return "No opportunities found in the database."
        
        result = f"📊 Found {len(opps)} opportunities:\n\n"
        for i, opp in enumerate(opps, 1):
            result += f"{i}. **{opp.title}** (ID: {opp.id})\n"
            result += f"   - Asset: {opp.asset.upper()}, Type: {opp.type.upper()}, Status: {opp.status}\n"
            result += f"   - Confidence: {opp.confidence}%\n"
            result += f"   - Rationale: {opp.rationale}\n\n"
        return result
    except Exception as e:
        return f"Error listing opportunities: {str(e)}"

class UpdateOpportunityInput(BaseModel):
    opportunity_id: str = Field(description="ID of the opportunity to update")
    status: Optional[str] = Field(None, description="New status (e.g., 'executed', 'dismissed')")
    confidence: Optional[float] = Field(None, description="New confidence level (0-100)")

class UpdateOpportunityTool(BaseTool):
    name: str = "update_opportunity"
    description: str = "Update an existing opportunity's status or confidence level in the database."
    args_schema: type[BaseModel] = UpdateOpportunityInput

    def _run(self, **kwargs) -> str:
        raise NotImplementedError("Use arun for async operations")

    async def _arun(self, opportunity_id: str, status: Optional[str] = None, confidence: Optional[float] = None) -> str:
        try:
            updates = {k: v for k, v in {"status": status, "confidence": confidence}.items() if v is not None}
            if not updates:
                return "No updates provided."
            
            success = await opportunities_store.update(opportunity_id, updates)
            return f"✓ Updated opportunity {opportunity_id}." if success else f"✗ Opportunity {opportunity_id} not found."
        except Exception as e:
            return f"Error updating opportunity: {str(e)}"

class DeleteOpportunityInput(BaseModel):
    opportunity_id: str = Field(description="ID of the opportunity to delete")

class DeleteOpportunityTool(BaseTool):
    name: str = "delete_opportunity"
    description: str = "Delete an opportunity from the database using its ID."
    args_schema: type[BaseModel] = DeleteOpportunityInput

    def _run(self, **kwargs) -> str:
        raise NotImplementedError("Use arun for async operations")

    async def _arun(self, opportunity_id: str) -> str:
        try:
            success = await opportunities_store.delete(opportunity_id)
            return f"✓ Deleted opportunity {opportunity_id}." if success else f"✗ Opportunity {opportunity_id} not found."
        except Exception as e:
            return f"Error deleting opportunity: {str(e)}"

def get_opportunities_tools() -> List[BaseTool]:
    """Get all opportunities management tools."""
    return [
        AddOpportunityTool(),
        list_opportunities,
        UpdateOpportunityTool(),
        DeleteOpportunityTool(),
    ]

