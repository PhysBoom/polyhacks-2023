from pydantic import BaseModel, Field
from .gender import Gender
from .contact_info import ContactInfo

class Bio(BaseModel):
    description: str = Field(...)
    age: int = Field(...)
    gender: Gender = Field(...)
    contact_info: ContactInfo = Field(...)