from typing import Dict
from pydantic import BaseModel, Field


class Job(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    company: str = Field(...)
    location: str = Field(...)
    salary: int = Field(...)
    start_date: int = Field(...) # UNIX timestamp to the nearest day
    end_date: int = Field(default=-1) # UNIX timestamp to the nearest day, -1 = still employed
    job_type: str = Field(...) # Full-time, Part-time, Internship, etc.
    job_category: str = Field(...) # Software Engineering, Data Science, etc.
    resume_selection_history: Dict[str, int] = Field(default_factory=dict) # {resume_id: 0 (not selected), 1 (maybe), 2 (selected)
    min_degree_type: str = Field(...) # High School, Associate's, Bachelor's, Master's, PhD

    