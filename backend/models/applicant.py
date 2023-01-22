from pydantic import Field

from controllers.mongodb_client import Database

from .resume import Resume
from .bio import Bio
from .user import User, UserTypes
from controllers.firebase_controller import upload_file_to_firebase_storage

class Applicant(User):
    bio: Bio = Field(default=None) # TODO: Implement bio
    resume: Resume = Field(default=None)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True
        arbitrary_types_allowed: True

    # init w/ applicant type
    def __init__(self, **data):
        data["user_type"] = UserTypes.APPLICANT
        super().__init__(**data)

    def upload_resume(self, resume: str): # resume is a path to the image
        # Upload resume to firebase storage
        resume = upload_file_to_firebase_storage(resume, f"resumes/{self.firebase_user_key}")
        r = Resume(image=f"resumes/{self.firebase_user_key}")
        self.resume = r
        Database.update_one("users", {"firebase_user_key": self.firebase_user_key}, {"$set": {"resume": self.resume.dict()}})

    @staticmethod
    def load_all_applicants():
        return [Applicant(**applicant) for applicant in Database.find("users", {"user_type": UserTypes.APPLICANT.value})]