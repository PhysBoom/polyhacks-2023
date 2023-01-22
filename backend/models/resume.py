from typing import List
from pydantic import BaseModel, Field
from uuid import uuid4
from controllers.mongodb_client import Database
from tempfile import NamedTemporaryFile
from controllers.firebase_controller import download_file_from_firebase_storage

from models.previous_job import PreviousJob
import random
import os


class Resume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    image: str = Field(default=None)  # Firebase storage URL to the image
    degree_type: str = Field(default=None)
    university: str = Field(default=None)
    gpa: float = Field(default=None)
    grad_date: int = Field(
        default=-1
    )  # UNIX timestamp to the nearest day, -1 = not graduated yet
    skills: List[str] = Field(default_factory=list)
    employment_history: List[PreviousJob] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True
        arbitrary_types_allowed: True

    def get_image(self):
        f = NamedTemporaryFile()
        download_file_from_firebase_storage(self.image, f.name)
        # Return f's contents and unlink it
        contents = f.read()
        f.close()
        os.unlink(f.name)
        return contents

    def update(self, data):
        # TODO: Make more secure
        self.employment_history = [
            PreviousJob(**job) for job in data["employment_history"]
        ]
        # lowercase all skills
        data["skills"] = [skill.lower() for skill in data["skills"]]
        for key, value in data.items():
            if key not in ["employment_history", "id"]:
                setattr(self, key, value)
        return self

    @staticmethod
    def get_resume_by_id(resume_id):
        # TODO: Make this better obvs (referencing)
        return Resume(**Database.find_one("users", {"resume.id": resume_id})["resume"])
