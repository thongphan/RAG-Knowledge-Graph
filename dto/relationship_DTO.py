from pydantic import BaseModel

class RelationshipDTO(BaseModel):
    provider: str
    patient: str
    specialization: str
    location: str