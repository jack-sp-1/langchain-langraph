from typing import List
from pydantic import BaseModel, Field

class Source(BaseModel):
    #propagate this information
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source")
    
    
class AgentResponse(BaseModel):
    # answer and list   ..default_factory all instances get their  list
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer"
    )    