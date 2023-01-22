from pydantic import Field

from controllers.mongodb_client import Database

from .user import User, UserTypes
from controllers.firebase_controller import upload_file_to_firebase_storage


class Employer(User):
    job_postings: list = Field(default_factory=list)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True
        arbitrary_types_allowed: True

    def create_posting(self, job):
        self.job_postings.append(job)
        Database.update_one(
            "users",
            {"firebase_user_key": self.firebase_user_key},
            {"$set": self.as_dict()},
        )

    # init w/ applicant type
    def __init__(self, **data):
        data["user_type"] = UserTypes.EMPLOYER
        super().__init__(**data)
