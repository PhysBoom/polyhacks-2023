from flask import Blueprint
from .auth_blueprint import auth_blueprint

v1_blueprint = Blueprint("v1", __name__, url_prefix="/v1")

v1_blueprint.register_blueprint(auth_blueprint)