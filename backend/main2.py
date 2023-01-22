from controllers.mongodb_client import Database
from models.applicant import Applicant
from dotenv import load_dotenv

load_dotenv()
Database.initialize()

for _ in range(1000):
    Applicant.create_random_applicant().push_to_db()