"""
Opportunities Manager - Tools for managing investment opportunities
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field


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




class OpportunitiesStore:
    """
    In-memory store for opportunities (dev mode)
    In production, this would use the LangGraph Store
    """
    
    def __init__(self):
        self.opportunities: Dict[str, Opportunity] = {}
        self._load_default_opportunities()
    
    def _load_default_opportunities(self):
        """Load some default opportunities for demonstration"""
        default_opps = [
            Opportunity(
                id="opp_001",
                title="Bitcoin Accumulation Opportunity",
                asset="bitcoin",
                type="buy",
                confidence=75,
                rationale="Strong support level at $60k with increasing institutional adoption",
                sources=["coingecko", "santiment"],
                metrics={"current_price": 61500, "support_level": 60000},
                tags=["btc", "accumulation", "long-term"]
            ),
            Opportunity(
                id="opp_002",
                title="Ethereum Layer 2 Growth",
                asset="ethereum",
                type="watch",
                confidence=85,
                rationale="Increasing L2 activity and upcoming network upgrades",
                sources=["santiment", "firecrawl"],
                metrics={"l2_tvl": "10B", "network_growth": "+15%"},
                tags=["eth", "layer2", "defi"]
            )
        ]
        
        for opp in default_opps:
            self.opportunities[opp.id] = opp
    
    def add(self, opportunity: Opportunity) -> str:
        """Add a new opportunity"""
        self.opportunities[opportunity.id] = opportunity
        return opportunity.id
    
    def get(self, opportunity_id: str) -> Optional[Opportunity]:
        """Get an opportunity by ID"""
        return self.opportunities.get(opportunity_id)
    
    def list_all(self, status: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Opportunity]:
        """List all opportunities with optional filters"""
        opps = list(self.opportunities.values())
        
        if status:
            opps = [opp for opp in opps if opp.status == status]
        
        if tags:
            opps = [opp for opp in opps if any(tag in opp.tags for tag in tags)]
        
        return opps
    
    def update(self, opportunity_id: str, updates: Dict[str, Any]) -> bool:
        """Update an opportunity"""
        if opportunity_id not in self.opportunities:
            return False
        
        opp = self.opportunities[opportunity_id]
        for key, value in updates.items():
            if hasattr(opp, key):
                setattr(opp, key, value)
        
        return True
    
    def delete(self, opportunity_id: str) -> bool:
        """Delete an opportunity"""
        if opportunity_id in self.opportunities:
            del self.opportunities[opportunity_id]
            return True
        return False


# Global store instance (in dev mode)
opportunities_store = OpportunitiesStore()


class AddOpportunityTool(BaseTool):
    """Tool for adding new opportunities"""
    
    name: str = "add_opportunity"
    description: str = """
    Add a new investment opportunity to the opportunities list.
    Use this when you identify a potential investment opportunity based on market data.
    
    Required fields:
    - title: Clear, descriptive title
    - asset: The cryptocurrency or asset
    - type: One of: buy, sell, hold, watch
    - confidence: Your confidence level (0-100)
    - rationale: Detailed explanation with supporting data
    
    Optional fields:
    - sources: List of data sources used
    - metrics: Relevant metrics (price, volume, etc.)
    - tags: Tags for categorization
    """
    args_schema: type[BaseModel] = AddOpportunityInput
    
    def _run(self, **kwargs) -> str:
        """Add opportunity"""
        try:
            # Generate ID
            timestamp = datetime.utcnow().timestamp()
            opp_id = f"opp_{int(timestamp)}"
            
            # Create opportunity
            opportunity = Opportunity(
                id=opp_id,
                **kwargs
            )
            
            # Add to store
            opportunities_store.add(opportunity)
            
            return f"✓ Added opportunity '{opportunity.title}' (ID: {opp_id})"
        
        except Exception as e:
            return f"✗ Error adding opportunity: {str(e)}"


@tool
def list_opportunities(dummy: Optional[str] = "") -> str:
    """List all current investment opportunities. Returns a formatted list with all details."""
    try:
        opps = opportunities_store.list_all()
        
        if not opps:
            return "No opportunities found. The opportunities list is currently empty."
        
        result = f"📊 Found {len(opps)} opportunities:\n\n"
        
        for i, opp in enumerate(opps, 1):
            result += f"{i}. **{opp.title}**\n"
            result += f"   - Asset: {opp.asset.upper()}\n"
            result += f"   - Type: {opp.type.upper()}\n"
            result += f"   - Confidence: {opp.confidence}%\n"
            result += f"   - Rationale: {opp.rationale}\n"
            result += f"   - Status: {opp.status}\n"
            if opp.tags:
                result += f"   - Tags: {', '.join(opp.tags)}\n"
            result += f"   - ID: {opp.id}\n"
            result += "\n"
        
        return result
    
    except Exception as e:
        return f"Error listing opportunities: {str(e)}"


class UpdateOpportunityInput(BaseModel):
    """Input for updating an opportunity"""
    opportunity_id: str = Field(description="ID of the opportunity to update")
    status: Optional[str] = Field(None, description="New status (active, executed, dismissed)")
    confidence: Optional[float] = Field(None, description="New confidence level (0-100)")


class UpdateOpportunityTool(BaseTool):
    """Tool for updating opportunities"""
    
    name: str = "update_opportunity"
    description: str = """
    Update an existing opportunity's status or confidence level.
    Provide the opportunity_id and the fields you want to update.
    """
    args_schema: type[BaseModel] = UpdateOpportunityInput
    
    def _run(self, opportunity_id: str, status: Optional[str] = None, confidence: Optional[float] = None) -> str:
        """Update opportunity"""
        try:
            updates = {}
            if status:
                updates["status"] = status
            if confidence:
                updates["confidence"] = confidence
                
            if not updates:
                return "No updates provided"
            
            success = opportunities_store.update(opportunity_id, updates)
            
            if success:
                return f"✓ Updated opportunity {opportunity_id} with {updates}"
            else:
                return f"✗ Opportunity {opportunity_id} not found"
        
        except Exception as e:
            return f"Error updating opportunity: {str(e)}"


class DeleteOpportunityInput(BaseModel):
    """Input for deleting an opportunity"""
    opportunity_id: str = Field(description="ID of the opportunity to delete")


class DeleteOpportunityTool(BaseTool):
    """Tool for deleting opportunities"""
    
    name: str = "delete_opportunity"
    description: str = """
    Delete an opportunity from the list.
    Provide the opportunity_id to delete.
    """
    args_schema: type[BaseModel] = DeleteOpportunityInput
    
    def _run(self, opportunity_id: str) -> str:
        """Delete opportunity"""
        try:
            success = opportunities_store.delete(opportunity_id)
            
            if success:
                return f"✓ Deleted opportunity {opportunity_id}"
            else:
                return f"✗ Opportunity {opportunity_id} not found"
        
        except Exception as e:
            return f"Error deleting opportunity: {str(e)}"


def get_opportunities_tools() -> List:
    """Get all opportunities management tools"""
    return [
        AddOpportunityTool(),
        list_opportunities,  # Simple function instead of Tool class
        UpdateOpportunityTool(),
        DeleteOpportunityTool(),
    ]


def get_opportunities_json() -> str:
    """Get all opportunities as JSON (for API)"""
    opps = opportunities_store.list_all()
    return json.dumps([opp.dict() for opp in opps], indent=2)

