from flask import Blueprint
from .auth_blueprint import auth_blueprint
from .applicant_blueprint import applicant_blueprint
from .employer_blueprint import employer_blueprint

v1_blueprint = Blueprint("v1", __name__, url_prefix="/v1")

v1_blueprint.register_blueprint(auth_blueprint)
v1_blueprint.register_blueprint(applicant_blueprint)
v1_blueprint.register_blueprint(employer_blueprint)
