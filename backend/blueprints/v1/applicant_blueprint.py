from flask import Flask, Blueprint, request, jsonify

from models.applicant import Applicant
from .auth_blueprint import token_required
from functools import wraps
import tempfile
import os

applicant_blueprint = Blueprint("applicant", __name__, url_prefix="/applicant")


@applicant_blueprint.route("/upload-resume", methods=["POST"])
@token_required
def upload_resume(user):
    """
    Upload a resume
    """
    data = request.files["resume"]
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data.read())
    user = Applicant(**user)
    user.upload_resume(f.name)
    f.close()
    os.unlink(f.name)
    return jsonify({"message": "Resume uploaded successfully!"}), 200


@applicant_blueprint.route("", methods=["GET"])
@token_required
def get_applicant(user):
    """
    Get an applicant
    """
    user = Applicant(**user)
    return jsonify(user.to_dict()), 200


@applicant_blueprint.route("", methods=["PATCH"])
@token_required
def update_applicant(user):
    """
    Update an applicant
    """
    data = request.get_json()
    user = Applicant(**user)
    user.update(data)
    return jsonify({"message": "Applicant updated successfully!"}), 200
