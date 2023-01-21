from pydantic import BaseModel, Field

from .resume import Resume
from .bio import Bio

class Applicant(BaseModel):
    name: str = Field(...)
    bio: Bio = Field(...) # TODO: Implement bio
    resume: Resume = Field(...) # TODO: Implement resume