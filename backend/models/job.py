from typing import Dict
from typing import Set
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer, util

from resume import Resume


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
    desired_skills: Set[str] = Field(...) # Should be all lowercase
    resume_selection_history: Dict[str, int] = Field(default_factory=dict) # {resume_id: 0 (not selected), 1 (maybe), 2 (selected)
    min_degree_type: str = Field(...) # High School, Associate's, Bachelor's, Master's, PhD

    def resume_similarity(self, resume: Resume) -> float:
        # semantic against previous job titles
        prev_job_similarity = max(self.semantic_similarity(self.title, prev_job.job_title) for prev_job in Resume.employment_history)

        # skill matches
        matched_skills = Set.union(self.desired_skills, resume.skills)
        skill_match_rate = len(matched_skills) / len(self.desired_skills)

        return 0.5 * prev_job_similarity + 0.5 * skill_match_rate

    def semantic_similarity(self, s1, s2):
        if self.model is None:
            self.model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        embedding1 = self.model.encode(s1, convert_to_tensor=True)
        embedding2 = self.model.encode(s2, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(embedding1, embedding2)
        return cos_scores.item()
