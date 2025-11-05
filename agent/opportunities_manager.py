"""
Opportunities Manager - Tools for managing investment opportunities
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from langchain.tools import ToolRuntime, tool
from langgraph.store.base import BaseStore
from pydantic import BaseModel, Field


class Opportunity(BaseModel):
    """Schema for an investment opportunity"""

    id: str = Field(description="Unique identifier for the opportunity")
    title: str = Field(description="Title/name of the opportunity")
    asset: str = Field(description="Asset or cryptocurrency")
    type: str = Field(description="Type: buy, sell, hold, watch")
    confidence: float = Field(description="Confidence level (0-100)", ge=0, le=100)
    rationale: str = Field(description="Why this is an opportunity")
    sources: List[str] = Field(default_factory=list, description="Data sources used")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Relevant metrics")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    expires_at: Optional[str] = Field(default=None, description="When this opportunity expires")
    status: str = Field(default="active", description="active, expired, executed, dismissed")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    updated_at: Optional[str] = Field(default=None, description="Last update timestamp")


DEFAULT_OPPORTUNITIES: List[Opportunity] = [
    Opportunity(
        id="opp_001",
        title="Bitcoin Accumulation Opportunity",
        asset="bitcoin",
        type="buy",
        confidence=75,
        rationale="Strong support level at $60k with increasing institutional adoption",
        sources=["coingecko", "santiment"],
        metrics={"current_price": 61500, "support_level": 60000},
        tags=["btc", "accumulation", "long-term"],
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
        tags=["eth", "layer2", "defi"],
    ),
]

STORE_NAMESPACE = ("opportunities",)


class InMemoryOpportunities:
    """Fallback in-memory store used when LangGraph Store is unavailable."""

    def __init__(self):
        self._items: Dict[str, Opportunity] = {opp.id: opp for opp in DEFAULT_OPPORTUNITIES}

    def add(self, opportunity: Opportunity) -> None:
        self._items[opportunity.id] = opportunity

    def list_all(self) -> List[Opportunity]:
        return list(self._items.values())

    def get(self, opportunity_id: str) -> Optional[Opportunity]:
        return self._items.get(opportunity_id)

    def update(self, opportunity_id: str, updates: Dict[str, Any]) -> bool:
        if opportunity_id not in self._items:
            return False
        current = self._items[opportunity_id]
        updated_data = current.dict()
        updated_data.update(updates)
        updated_data["updated_at"] = datetime.utcnow().isoformat()
        self._items[opportunity_id] = Opportunity(**updated_data)
        return True

    def delete(self, opportunity_id: str) -> bool:
        return self._items.pop(opportunity_id, None) is not None


_fallback_store = InMemoryOpportunities()


def _get_runtime_store(runtime: Optional[ToolRuntime]) -> Optional[BaseStore]:
    if runtime is None:
        return None
    return getattr(runtime, "store", None)


def _seed_store_if_empty(store: BaseStore) -> None:
    try:
        existing = store.search(STORE_NAMESPACE, limit=1)
    except Exception:
        existing = []
    if existing:
        return
    for opportunity in DEFAULT_OPPORTUNITIES:
        store.put(STORE_NAMESPACE, opportunity.id, opportunity.dict())


def _list_from_store(store: BaseStore) -> List[Opportunity]:
    _seed_store_if_empty(store)
    try:
        items = store.search(STORE_NAMESPACE, limit=500)
    except Exception:
        items = []
    opportunities: List[Opportunity] = []
    for item in items or []:
        try:
            opportunities.append(Opportunity(**item.value))
        except Exception:
            continue
    opportunities.sort(key=lambda opp: opp.created_at)
    return opportunities


def _get_from_store(store: BaseStore, opportunity_id: str) -> Optional[Opportunity]:
    try:
        item = store.get(STORE_NAMESPACE, opportunity_id)
    except Exception:
        return None
    if not item:
        return None
    try:
        return Opportunity(**item.value)
    except Exception:
        return None


def _save_to_store(store: BaseStore, opportunity: Opportunity) -> None:
    store.put(STORE_NAMESPACE, opportunity.id, opportunity.dict())


def _delete_from_store(store: BaseStore, opportunity_id: str) -> bool:
    existing = _get_from_store(store, opportunity_id)
    if not existing:
        return False
    store.delete(STORE_NAMESPACE, opportunity_id)
    return True


@tool
def add_opportunity(
    title: str,
    asset: str,
    type: str,
    confidence: float,
    rationale: str,
    runtime: ToolRuntime,
    sources: Optional[List[str]] = None,
    metrics: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
) -> str:
    """Add a new investment opportunity to the opportunities list.

    Args:
        title: Title/name of the opportunity
        asset: Asset or cryptocurrency
        type: Type: buy, sell, hold, watch
        confidence: Confidence level (0-100)
        rationale: Why this is an opportunity
        runtime: Runtime context (injected automatically)
        sources: Data sources used
        metrics: Relevant metrics
        tags: Tags for categorization
    """

    opportunity_id = f"opp_{uuid4().hex[:12]}"
    created_at = datetime.utcnow().isoformat()
    opportunity = Opportunity(
        id=opportunity_id,
        title=title,
        asset=asset,
        type=type,
        confidence=confidence,
        rationale=rationale,
        sources=sources or [],
        metrics=metrics or {},
        tags=tags or [],
        created_at=created_at,
        updated_at=created_at,
    )

    store = _get_runtime_store(runtime)
    if store:
        _seed_store_if_empty(store)
        _save_to_store(store, opportunity)
    else:
        _fallback_store.add(opportunity)

    return f"✓ Added opportunity '{opportunity.title}' (ID: {opportunity.id})"


@tool
def list_opportunities(runtime: ToolRuntime) -> str:
    """List all current investment opportunities with their details.

    Args:
        runtime: Runtime context (injected automatically)
    """

    store = _get_runtime_store(runtime)
    if store:
        opportunities = _list_from_store(store)
    else:
        opportunities = _fallback_store.list_all()

    if not opportunities:
        return "No opportunities found. The opportunities list is currently empty."

    result = f"📊 Found {len(opportunities)} opportunities:\n\n"
    for index, opp in enumerate(opportunities, 1):
        result += f"{index}. **{opp.title}**\n"
        result += f"   - Asset: {opp.asset.upper()}\n"
        result += f"   - Type: {opp.type.upper()}\n"
        result += f"   - Confidence: {opp.confidence}%\n"
        result += f"   - Status: {opp.status}\n"
        result += f"   - Created: {opp.created_at}\n"
        if opp.updated_at:
            result += f"   - Updated: {opp.updated_at}\n"
        result += f"   - Rationale: {opp.rationale}\n"
        if opp.metrics:
            metrics_str = ", ".join(f"{k}: {v}" for k, v in opp.metrics.items())
            result += f"   - Metrics: {metrics_str}\n"
        if opp.sources:
            result += f"   - Sources: {', '.join(opp.sources)}\n"
        if opp.tags:
            result += f"   - Tags: {', '.join(opp.tags)}\n"
        result += f"   - ID: {opp.id}\n\n"

    return result.strip()


@tool
def update_opportunity(
    opportunity_id: str,
    runtime: ToolRuntime,
    status: Optional[str] = None,
    confidence: Optional[float] = None,
) -> str:
    """Update the status or confidence of an existing opportunity.

    Args:
        opportunity_id: ID of the opportunity to update
        runtime: Runtime context (injected automatically)
        status: New status (optional)
        confidence: New confidence level (optional)
    """

    if not status and confidence is None:
        return "No updates provided"

    updates: Dict[str, Any] = {}
    if status:
        updates["status"] = status
    if confidence is not None:
        updates["confidence"] = confidence
    updates["updated_at"] = datetime.utcnow().isoformat()

    store = _get_runtime_store(runtime)
    if store:
        existing = _get_from_store(store, opportunity_id)
        if not existing:
            return f"✗ Opportunity {opportunity_id} not found"
        updated_data = existing.dict()
        updated_data.update(updates)
        _save_to_store(store, Opportunity(**updated_data))
    else:
        success = _fallback_store.update(opportunity_id, updates)
        if not success:
            return f"✗ Opportunity {opportunity_id} not found"

    return f"✓ Updated opportunity {opportunity_id}"


@tool
def delete_opportunity(opportunity_id: str, runtime: ToolRuntime) -> str:
    """Delete an opportunity from the opportunities list.

    Args:
        opportunity_id: ID of the opportunity to delete
        runtime: Runtime context (injected automatically)
    """

    store = _get_runtime_store(runtime)
    if store:
        success = _delete_from_store(store, opportunity_id)
    else:
        success = _fallback_store.delete(opportunity_id)

    if success:
        return f"✓ Deleted opportunity {opportunity_id}"
    return f"✗ Opportunity {opportunity_id} not found"


def get_opportunities_tools() -> List:
    """Return the opportunities management tools list."""

    return [
        add_opportunity,
        list_opportunities,
        update_opportunity,
        delete_opportunity,
    ]


def get_opportunities_json(store: Optional[BaseStore] = None) -> str:
    """Utility helper to export opportunities as JSON."""

    if store:
        opportunities = [opp.dict() for opp in _list_from_store(store)]
    else:
        opportunities = [opp.dict() for opp in _fallback_store.list_all()]
    return json.dumps(opportunities, indent=2)

