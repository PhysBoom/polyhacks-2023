from typing import List
from pydantic import BaseModel, Field
from uuid import uuid4
from controllers.mongodb_client import Database
from pyresparser import ResumeParser
from tempfile import NamedTemporaryFile
import requests

from backend.models.previous_job import PreviousJob

class Resume:
    id: str = Field(default_factory=lambda: str(uuid4()))
    pdf: str = Field(...) # URL to PDF
    degree_type: str = Field(...)
    university: str = Field(...)
    gpa: float = Field(...)
    grad_date: int = Field(default=-1) # UNIX timestamp to the nearest day, -1 = not graduated yet
    skills: Set[str] = Field(default_factory=list)
    employment_history: List[PreviousJob] = Field(default_factory=list)

    def parse_from_pdf(self):
        # Get the PDF from the URL
        pdf = requests.get(self.pdf).content
        with NamedTemporaryFile() as temp_pdf:
            temp_pdf.write(pdf)
            temp_pdf.seek(0)
            parsed_resume = ResumeParser(temp_pdf.name).get_extracted_data()
            self.degree_type = parsed_resume.get("degree", "")
            self.university = parsed_resume.get("college_name", "")
            self.skills = set(parsed_resume.get("skills", []))
        # NOTE: We only parse these three things since that's all that the
        # resume parser returns lol. We can add more later if we want.
        # Update the database
        Database.update_one("resumes", {"id": self.id}, {"$set": self.dict()})

    @staticmethod
    def get_resume_by_id(resume_id):
        return Resume(**Database.find_one("resumes", {"id": resume_id}))
