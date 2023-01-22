from typing import List
from pydantic import BaseModel, Field

from backend.models.previous_job import PreviousJob

class Resume:
    pdf: str = Field(...) # URL to PDF
    degree_type: str = Field(...)
    university: str = Field(...)
    gpa: float = Field(...)
    grad_date: int = Field(default=-1) # UNIX timestamp to the nearest day, -1 = not graduated yet
    skills: Set[str] = Field(default_factory=list)
    employment_history: List[PreviousJob] = Field(default_factory=list)