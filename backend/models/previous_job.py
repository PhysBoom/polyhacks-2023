import random
from pydantic import BaseModel, Field


class PreviousJob(BaseModel):
    employer: str = Field(...)
    start_date: int = Field(...)  # UNIX timestamp to the nearest day
    end_date: int = Field(
        default=-1
    )  # UNIX timestamp to the nearest day, -1 = still employed
    job_title: str = Field(...)

    # job_titles = ['Accountant', 'Accounting Clerk', 'Controller', 'Office manager', 'Administrative Assistant', 'Receptionist', 'Internal Help Desk Technician,' 'IT Manager', 'HR Coordinator', 'HR Manager', 'Recruiting Manager', 'Health and Safety Manager', 'Sales Representative, Account Manager', 'Sales Manager', 'Sales Director', 'Sales VP', 'Customer Service Representative', 'Technical Customer Support Specialist', 'Customer Service Manager', 'Graphic Designer', 'Marketing Coordinator', 'Product Manager', 'Marketing Manager', 'Marketing Director', 'Chief Executive Officer', 'Chief Operating Officer', 'Chief Financial Officer', 'Chief Information Officer', 'Chief Technology Officer', 'Chief Marketing Officer']
    companies = ['Luxury Boutique', 'Best Restaurant', 'Smart Tech', 'Math Accounting', 'Smart Consulting', 'Tall Bar', 'Beautiful Art', 'Clear Crystal', '102 Kitchen', 'Smooth Skincare Salon', 'Crazy Coffee', 'Shiny Jewelry', 'Fishi Sushi', 'Thrifty Thrift Shop', 'Battle Bar Arcade', 'Rolling Bikes', 'Yumme Cafe', 'Pause Records']

    @staticmethod
    def random_job_for_resume():
        with open('jobs.txt', 'r') as file:
            job_titles = file.readlines()
        job = PreviousJob()
        job.title = random.choices(job_titles)[0]
        job.employer = random.choices(PreviousJob.companies)[0]
        job.start_date = random.randrange(948591705, 1674438105)
        job.end_date = random.randrange(job.start_date, 1674438105)
        return job