""" Models for RecSys Backend routers"""
import time
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class NewItemsEvent(BaseModel):
    """ Input for /add_items router """
    item_ids: List[str] = Field(description="Identifiers of new items")

class RecommendationsRequest(BaseModel):
    """ Input for /recs/{user_id} router """
    user_id: str = Field(description="Identifier of user")

class RecommendationsResponse(BaseModel):
    """ Output for /recs/{user_id} router """
    user_id: str = Field(description="Identifier of user")
    item_ids: List[int] = Field(description="Identifiers of interacted items")
    actions: List[Literal['like', 'dislike']] = Field(
        description="Positive or Negative reaction for items"
    )
    timestemp: Optional[float] = Field(time.time(), description="Timestamp of event")

class InteractEvent(BaseModel):
    """ TODO """
    user_id: str = Field(description="Identifier of user")
    item_ids: List[str] = Field(description="Identifiers of interacted items")
    actions: List[Literal['like', 'dislike']] = Field(
        description="Positive or negative reaction for items"
    )
    timestamp: Optional[float] = Field(time.time(), description="timestamp of event")
