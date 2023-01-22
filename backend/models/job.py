from typing import Dict
from typing import Set
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer, util
from statistics import median

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

    def resume_fitness(self, resume: Resume) -> float:
        # semantic against previous job titles
        prev_job_similarity = max(self.semantic_similarity(self.title, prev_job.job_title) for prev_job in Resume.employment_history)

        # skill matches
        matched_skills = Set.union(self.desired_skills, resume.skills)
        skill_match_rate = len(matched_skills) / len(self.desired_skills)

        return 0.5 * prev_job_similarity + 0.5 * skill_match_rate

    def compare_resumes(self, resume1: Resume, resume2: Resume) -> float:
        # semantic similarity of degree
        if resume1.degree_type is None and resume2.degree_type is None:
            degree_similarity = 1
        elif resume1.degree_type is None or resume2.degree_type is None:
            degree_similarity = 0
        else:
            degree_similarity = self.semantic_similarity(resume1.degree_type, resume2.degree_type)
        
        # semanatic sim of previous job titles
        experience_similarity = median(self.semantic_similarity(job1.job_title, job2.job_title) for job1 in resume1.employment_history for job2 in resume2.employment_history)

        # diff of gpa
        if resume1.gpa is None and resume2.gpa is None:
            gpa_similarity = 1
        elif resume1.ga is None or resume2.gpa is None:
            gpa_similarity = 0
        else:
            gpa_similarity = 1 - (resume1.gpa - resume2.gpa) / 5

        # diff of grad date (NOT DOING)

        # match skills
        skill_matches = Set.union(resume1.skills, resume2.skills)
        total_skills = Set.intersection(resume1.skills, resume2.skills)
        skill_similarity = len(skill_matches) / len(total_skills)

        return (degree_similarity + experience_similarity + gpa_similarity + skill_similarity) / 4

    def semantic_similarity(self, s1, s2):
        if self.model is None:
            self.model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        embedding1 = self.model.encode(s1, convert_to_tensor=True)
        embedding2 = self.model.encode(s2, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(embedding1, embedding2)
        return cos_scores.item()
