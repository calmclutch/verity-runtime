from pydantic import BaseModel, Field


class IntentContract(BaseModel):
    objective: str
    capabilities: list[str] = Field(default_factory=list)