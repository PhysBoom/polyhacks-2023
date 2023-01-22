from pydantic import Field

from controllers.mongodb_client import Database

from .resume import Resume
from .bio import Bio
from .user import User, UserTypes

class Applicant(User):
    bio: Bio = Field(...) # TODO: Implement bio
    resume: Resume = Field(...) # TODO: Implement resume

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True

    # init w/ applicant type
    def __init__(self, **data):
        data["user_type"] = UserTypes.APPLICANT
        super().__init__(**data)

    def upload_resume(self, resume: str): # resume is a URL to the PDF
        r = Resume(pdf=resume)
        r.parse_from_pdf()
        self.resume = r
        Database.update_one("users", {"firebase_user_key": self.firebase_user_key}, {"$set": {"resume": self.resume.dict()}})

    @staticmethod
    def load_all_applicants():
        return [Applicant(**applicant) for applicant in Database.find("users", {"user_type": UserTypes.APPLICANT.value})]