from flask import Flask, Blueprint, request, jsonify

from models.employer import Employer
from models.job import Job
from .auth_blueprint import token_required
from functools import wraps
import tempfile
import os

employer_blueprint = Blueprint("employer", __name__, url_prefix="/employer")


@employer_blueprint.route("/job", methods=["POST"])
@token_required
def create_posting(user):
    """
    Create a posting
    """
    data = request.get_json()
    user = Employer(**user)
    data['employer_id'] = user.firebase_user_key
    data['desired_skills'] = [skill.lower() for skill in data['desired_skills']]
    user.create_posting(Job(**data))
    return jsonify({"message": "Posting created successfully!"}), 200

@employer_blueprint.route("/job/<job_id>/next-applicant", methods=["GET"])
@token_required
def get_next_applicant(user, job_id):
    """
    Get the next applicant for a job
    """
    user = Employer(**user)
    applicant = user.job_postings[job_id].find_next_applicant()
    return jsonify(applicant.as_dict()), 200

@employer_blueprint.route("/job/<job_id>/resume/<resume_id>/rating", methods=["POST"])
@token_required
def rate_applicant(user, job_id, resume_id):
    """
    Rate an applicant
    """
    data = request.get_json()
    user = Employer(**user)
    user.rate_resume(job_id, resume_id, data['rating'])
    return jsonify({"message": "Applicant rated successfully!"}), 200

