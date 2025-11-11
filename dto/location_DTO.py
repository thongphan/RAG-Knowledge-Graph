from pydantic import BaseModel, Field

class LocationDTO(BaseModel):
    name: str