from typing import Dict
from pydantic import Field
from .job import Job

from controllers.mongodb_client import Database

from .user import User, UserTypes
from controllers.firebase_controller import upload_file_to_firebase_storage


class Employer(User):
    job_postings: Dict[str, Job] = Field(default_factory=dict)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True
        arbitrary_types_allowed: True

    def create_posting(self, job):
        # TODO: Probably use referencing but for now just store the job
        self.job_postings[job.id] = job
        Database.update_one(
            "users",
            {"firebase_user_key": self.firebase_user_key},
            {"$set": self.as_dict()},
        )

    def rate_resume(self, job_id, resume_id, rating):
        self.job_postings[job_id].rate_resume(resume_id, rating)
        Database.update_one(
            "users",
            {"firebase_user_key": self.firebase_user_key},
            {"$set": {f"job_postings.{job_id}": self.job_postings[job_id].dict()}},
        )

    # init w/ applicant type
    def __init__(self, **data):
        data["user_type"] = UserTypes.EMPLOYER
        super().__init__(**data)
