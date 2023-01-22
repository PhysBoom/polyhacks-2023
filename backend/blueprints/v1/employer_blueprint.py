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
    data['desired_skills'] = [skill.lower() for skill in data['desired_skills']]
    user.create_posting(Job(**data))
    return jsonify({"message": "Posting created successfully!"}), 200
