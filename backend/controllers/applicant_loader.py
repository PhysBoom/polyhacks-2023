from models.applicant import Applicant

# Static singleton class that loads all resumes and then feeds it back to the job.

class ApplicantLoader:
    __instance = None

    def __init__(self):
        if ApplicantLoader.__instance is not None:
            raise Exception("ResumeLoader is a singleton class!")
        ApplicantLoader.__instance = self
        self.all_applicants = Applicant.load_all_applicants()

    @staticmethod
    def get_instance():
        if ApplicantLoader.__instance is None:
            ApplicantLoader()
        return ApplicantLoader.__instance

    def get_all_applicants(self):
        return self.all_applicants

    def get_all_resumes(self):
        return {
            applicant.resume.id: applicant.resume
            for applicant in self.all_applicants
        }