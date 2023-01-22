import random
from pydantic import BaseModel, Field
import os

class PreviousJob(BaseModel):
    employer: str = Field(...)
    start_date: int = Field(...)  # UNIX timestamp to the nearest day
    end_date: int = Field(
        default=-1
    )  # UNIX timestamp to the nearest day, -1 = still employed
    job_title: str = Field(...)

    @staticmethod
    def random_job_for_resume():
        companies = ['Luxury Boutique', 'Best Restaurant', 'Smart Tech', 'Math Accounting', 'Smart Consulting', 'Tall Bar', 'Beautiful Art', 'Clear Crystal', '102 Kitchen', 'Smooth Skincare Salon', 'Crazy Coffee', 'Shiny Jewelry', 'Fishi Sushi', 'Thrifty Thrift Shop', 'Battle Bar Arcade', 'Rolling Bikes', 'Yumme Cafe', 'Pause Records']
        with open(f"{os.getcwd()}/models/jobs.txt", "r") as file:
            job_titles = file.readlines()
        
        title = random.choices(job_titles)[0].strip()
        employer = random.choices(companies)[0]
        start_date = random.randrange(948591705, 1674438105)
        end_date = random.randrange(start_date, 1674438105)
        return PreviousJob(employer=employer, start_date=start_date, end_date=end_date, job_title=title)