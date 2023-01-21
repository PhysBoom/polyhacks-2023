from pydantic import BaseModel, Field

class Applicant(BaseModel):
    name: str = Field(...)
    bio: Bio = Field(...) # TODO: Implement bio
    resume: Resume = Field(...) # TODO: Implement resume

    def submit_resume():
        pass

    def update_profile():
        pass