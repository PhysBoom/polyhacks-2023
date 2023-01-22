from pydantic import BaseModel, Field
from .gender import Gender
from .contact_info import ContactInfo

class Bio(BaseModel):
    description: str = Field(...)
    age: int = Field(...)
    gender: Gender = Field(...)
    contact_info: ContactInfo = Field(...)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True