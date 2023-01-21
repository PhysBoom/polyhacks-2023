from pydantic import Field

from .resume import Resume
from .bio import Bio
from .user import User

class Applicant(User):
    name: str = Field(...)
    bio: Bio = Field(...) # TODO: Implement bio
    resume: Resume = Field(...) # TODO: Implement resume