from pydantic import BaseModel, Field

class PatientDTO(BaseModel):
    name: str
    age: int | None = None
    gender: str | None = None
    condition: str | None = None

