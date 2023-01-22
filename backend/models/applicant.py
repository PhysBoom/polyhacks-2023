import random
import randominfo
from pydantic import Field

from controllers.mongodb_client import Database

from .resume import Resume
from .bio import Bio
from .user import User, UserTypes
from controllers.firebase_controller import upload_file_to_firebase_storage

from .previous_job import PreviousJob

class Applicant(User):
    bio: Bio = Field(default=None)  # TODO: Implement bio
    resume: Resume = Field(default=None)
    address: str = Field(default="")

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True
        arbitrary_types_allowed: True

    # init w/ applicant type
    def __init__(self, **data):
        data["user_type"] = UserTypes.APPLICANT
        super().__init__(**data)

    def upload_resume(self, resume: str):  # resume is a path to the image
        # Upload resume to firebase storage
        resume = upload_file_to_firebase_storage(
            resume, f"resumes/{self.firebase_user_key}"
        )
        r = Resume(image=f"resumes/{self.firebase_user_key}")
        self.resume = r
        Database.update_one(
            "users",
            {"firebase_user_key": self.firebase_user_key},
            {"$set": {"resume": self.resume.dict()}},
        )

    def update(self, data):
        # TODO: Make more secure
        if data["first_name"] and data["last_name"]:
            self.name = f"{data['first_name']} {data['last_name']}"
        data["resume"] = self.resume.update(data["resume"])
        for key, value in data.items():
            if key not in ["first_name", "last_name", "firebase_user_key", "user_type"]:
                setattr(self, key, value)
        Database.update_one(
            "users",
            {"firebase_user_key": self.firebase_user_key},
            {"$set": self.as_dict()},
        )

    def push_to_db(self):
        Database.insert_one("users", self.as_dict())

    @staticmethod
    def load_all_applicants():
        print("Loading all applicants...")
        return [
            Applicant(**applicant)
            for applicant in Database.find(
                "users", {"user_type": UserTypes.APPLICANT.value}
            )
        ]


    @staticmethod
    def create_random_applicant():
        degree_types = ['Associates Degree', 'Bachelors Degree', 'Doctorate']
        majors = ['Computer Science', 'Communications', 'Political Science', 'Business', 'Economics', 'English', 'Psychology', 'Nursing', 'Chemical Engineering', 'Biology', 'History', 'Social Sciences', 'Engineering', 'Journalism', 'Education']
        universities = ['Princeton University', 'Massachusetts Institute of Technology', 'Harvard University', 'Stanford University', 'Yale University', 'University of Chicago', 'Johns Hopkins University', 'University of Pennsylvania', 'California Institute of Technology', 'Duke University', 'Northwestern University', 'Dartmouth College', 'Brown University', 'Vanderbilt University', 'Rice University', 'Cornell Univerity', 'Columbia University', 'California Polytechnic State University, SLO', 'University of California, Berkeley', 'University of California, LA', 'Carnegie Mellon University', 'Emory University', 'Georgetown Universtiy', 'New York University', 'University of Michigan', 'Unversity of Southern California', 'University of Virginia']
        skills = ['adaptability', 'attention to detail', 'creativity', 'decision making', 'work ethic', 'time management', 'data analysis', 'event planning', 'food preparation', 'graphic design', 'typing', 'interpersonal communication', 'public speaking', 'teamwork', 'technical writing', 'training', 'verbal communication', 'written communication', 'email management', 'research', 'social media', 'web design', 'marketing', 'patience', 'sales', 'troubleshooting', 'conflict resolution', 'delegation', 'mentorship', 'motivation', 'team management', 'creativity', 'python', 'environmental management']

        degree_type = f"{random.choices(degree_types)[0]}, {random.choices(majors)[0]}"
        university = random.choices(universities)[0]
        gpa = random.uniform(1, 4)
        grad_date = random.choices([random.randrange(948591705, 1674438105), -1], cum_weights=[95, 5])[0]
        skills = random.sample(skills, random.randrange(3, 10))
        employment_history = [
            PreviousJob.random_job_for_resume()
            for _ in range(random.randrange(0, 4))
        ]
        resume = Resume(degree_type=degree_type, university=university, gpa=gpa, grad_date=grad_date, employment_history=employment_history, skills=skills)

        name= f"{randominfo.get_first_name()} {randominfo.get_last_name()}"
        return Applicant(
            firebase_user_key=f"fake_applicant_{random.randrange(1000000000, 9999999999)}",
            name=name,
            email=f"{name.replace(' ', '.')}@gmail.com",
            phone_number=randominfo.get_phone_number(),
            address="1234 Main St.",
            resume=resume,
        )
