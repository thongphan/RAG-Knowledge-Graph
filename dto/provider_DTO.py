from pydantic import BaseModel, Field
from typing import List, Optional

class ProviderDTO(BaseModel):
    name: str
    bio: str | None = None
    comprehensiveEmbedding:  Optional[List[float]] = None
