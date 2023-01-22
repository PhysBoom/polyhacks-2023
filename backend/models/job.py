import random
from typing import Dict, Union
from typing import Set
from pydantic import BaseModel, Field
from models.applicant import Applicant
from sentence_transformers import SentenceTransformer, util
from statistics import median

from .resume import Resume


class Job(BaseModel):
    title: str = Field(...)
    description: str = Field(default="")
    salary: int = Field(...)
    job_type: str = Field(...)  # Full-time, Part-time, Internship, etc.
    desired_skills: Set[str] = Field(...)  # Should be all lowercase
    resume_selection_history: Dict[str, int] = Field(
        default_factory=dict
    )  # {resume_id: -1 (not selected), 0 (maybe), 1 (selected)

    def __init__(self, **data):
        data["desired_skills"] = set(data["desired_skills"])
        super().__init__(**data)

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        d["desired_skills"] = list(d["desired_skills"])
        return d

    def find_next_applicant(self) -> Applicant:
        # 1. Get all the applicants
        applicants = Applicant.load_all_applicants()
        job_fitness_scale = max(0.3, 1 - len(self.resume_selection_history) * 0.05)
        resume_fitnesses = {}
        for applicant in applicants:
            resume_applicant_fitness = self._resume_applicant_fitness(applicant.resume) or 0
            resume_job_fitness = self._resume_job_fitness(applicant.resume)
            resume_fitnesses[applicant] = (
                job_fitness_scale * resume_job_fitness
                + (1 - job_fitness_scale) * resume_applicant_fitness
            )
        
        if random.random() < min(0.8, 0.1 + len(self.resume_selection_history) * 0.05):
            # Return the best applicant
            return max(resume_fitnesses, key=resume_fitnesses.get)

        # Select applicant by random weighted choice
        return random.choices(
            list(resume_fitnesses.keys()), weights=list(resume_fitnesses.values())
        )[0]

    def _resume_job_fitness(self, resume: Resume) -> float:
        # semantic against previous job titles
        prev_job_similarity = max(
            self.semantic_similarity(self.title, prev_job.job_title)
            for prev_job in Resume.employment_history
        )

        # skill matches
        matched_skills = Set.union(self.desired_skills, resume.skills)
        skill_match_rate = len(matched_skills) / len(self.desired_skills)

        return 0.5 * prev_job_similarity + 0.5 * skill_match_rate

    def _resume_applicant_fitness(self, resume: Resume) -> Union[float, None]:
        if resume.id in self.resume_selection_history:
            return None

        total_fitness = 0
        for resume_id in self.resume_selection_history:
            cur_resume = Resume.get_resume_by_id(resume_id)
            resume_comp = self._compare_resumes(resume, cur_resume)
            total_fitness += resume_comp * self.resume_selection_history[resume_id]

        return total_fitness / len(self.resume_selection_history)

    def _compare_resumes(self, resume1: Resume, resume2: Resume) -> float:
        # semantic similarity of degree
        if resume1.degree_type is None and resume2.degree_type is None:
            degree_similarity = 1
        elif resume1.degree_type is None or resume2.degree_type is None:
            degree_similarity = 0
        else:
            degree_similarity = self.semantic_similarity(
                resume1.degree_type, resume2.degree_type
            )

        # semanatic sim of previous job titles
        experience_similarity = median(
            self.semantic_similarity(job1.job_title, job2.job_title)
            for job1 in resume1.employment_history
            for job2 in resume2.employment_history
        )

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

        return (
            degree_similarity
            + experience_similarity
            + gpa_similarity
            + skill_similarity
        ) / 4

    def _semantic_similarity(self, s1, s2):
        if self.model is None:
            self.model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
        embedding1 = self.model.encode(s1, convert_to_tensor=True)
        embedding2 = self.model.encode(s2, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(embedding1, embedding2)
        return cos_scores.item()
