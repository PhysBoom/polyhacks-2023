import random
from typing import Dict, Union
from typing import Set
from uuid import uuid4
from pydantic import BaseModel, Field
from controllers.applicant_loader import ApplicantLoader
from models.applicant import Applicant
from sentences import SentenceAnalyzer
from statistics import median
from controllers.mongodb_client import Database

from .resume import Resume


class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    employer_id: str = Field(...)
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
        applicants = ApplicantLoader.get_instance().get_all_applicants()
        all_relevant_resumes = ApplicantLoader.get_instance().get_all_resumes()
        job_fitness_scale = max(0.3, 1 - len(self.resume_selection_history) * 0.05)
        resume_fitnesses = {}
        for applicant in applicants:
            if applicant.resume.id in self.resume_selection_history:
                continue
            resume_applicant_fitness = self._resume_applicant_fitness(applicant.resume, all_relevant_resumes) or 0
            resume_job_fitness = self._resume_job_fitness(applicant.resume)
            resume_fitnesses[applicant.firebase_user_key] = (
                job_fitness_scale * resume_job_fitness
                + (1 - job_fitness_scale) * resume_applicant_fitness
            )

        if not resume_fitnesses:
            return None
        
        if random.random() < min(0.8, 0.1 + len(self.resume_selection_history) * 0.05):
            # Return the best applicant
            key = max(resume_fitnesses, key=resume_fitnesses.get)
            for applicant in applicants:
                if applicant.firebase_user_key == key:
                    return applicant

        # Select applicant by random weighted choice
        key = random.choices(
            list(resume_fitnesses.keys()), weights=[elem if elem > 0 else 0.01 for elem in resume_fitnesses.values()]
        )[0]
        for applicant in applicants:
            if applicant.firebase_user_key == key:
                return applicant

    def rate_resume(self, resume_id: str, rating: int):
        self.resume_selection_history[resume_id] = rating

    def _resume_job_fitness(self, resume: Resume) -> float:
        # semantic against previous job titles
        prev_job_similarity = max(
            self._semantic_similarity(self.title, prev_job.job_title)
            for prev_job in resume.employment_history
        ) if len(resume.employment_history) > 0 else 0

        # skill matches
        matched_skills = Set.intersection(self.desired_skills, resume.skills)
        skill_match_rate = len(matched_skills) / len(self.desired_skills)

        return 0.5 * prev_job_similarity + 0.5 * skill_match_rate

    def _resume_applicant_fitness(self, resume: Resume, all_relevant_resumes) -> Union[float, None]:

        total_fitness = 0
        for resume_id in self.resume_selection_history:
            resume_comp = self._compare_resumes(resume, all_relevant_resumes[resume_id])
            total_fitness += resume_comp * self.resume_selection_history[resume_id]

        return total_fitness / len(self.resume_selection_history) if len(self.resume_selection_history) > 0 else 0

    def _compare_resumes(self, resume1: Resume, resume2: Resume) -> float:
        # semantic similarity of degree
        if resume1.degree_type is None and resume2.degree_type is None:
            degree_similarity = 1
        elif resume1.degree_type is None or resume2.degree_type is None:
            degree_similarity = 0
        else:
            degree_similarity = self._semantic_similarity(
                resume1.degree_type, resume2.degree_type
            )

        # semanatic sim of previous job titles
        if not resume1.employment_history and not resume2.employment_history:
            experience_similarity = 1
        elif not resume1.employment_history or not resume2.employment_history:
            experience_similarity = 0
        else:
            experience_similarity = median(
                self._semantic_similarity(job1.job_title, job2.job_title)
                for job1 in resume1.employment_history
                for job2 in resume2.employment_history
            )

        # diff of gpa
        if resume1.gpa is None and resume2.gpa is None:
            gpa_similarity = 1
        elif resume1.gpa is None or resume2.gpa is None:
            gpa_similarity = 0
        else:
            gpa_similarity = 1 - (resume1.gpa - resume2.gpa) / 5

        # diff of grad date (NOT DOING)

        # match skills
        skill_matches = Set.intersection(set(resume1.skills), set(resume2.skills))
        total_skills = Set.union(set(resume1.skills), set(resume2.skills))
        skill_similarity = len(skill_matches) / len(total_skills)

        return (
            degree_similarity
            + experience_similarity
            + gpa_similarity
            + skill_similarity
        ) / 4

    def _semantic_similarity(self, s1, s2):
        return SentenceAnalyzer.get_instance().get_similarity_scores(s1, s2)
