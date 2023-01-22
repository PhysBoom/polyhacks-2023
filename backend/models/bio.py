from pydantic import BaseModel, Field
from .gender import Gender

class Bio(BaseModel):
    description: str = Field(...)
    age: int = Field(...)
    gender: Gender = Field(...)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True