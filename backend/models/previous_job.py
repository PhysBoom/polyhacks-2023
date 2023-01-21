from pydantic import BaseModel, Field

class PreviousJob(BaseModel):
    employer: str = Field(...)
    start_date: int = Field(...) # UNIX timestamp to the nearest day
    end_date: int = Field(default=-1) # UNIX timestamp to the nearest day, -1 = still employed
    job_title: str = Field(...)