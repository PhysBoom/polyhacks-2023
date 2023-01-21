from flask import Flask, Blueprint, request, jsonify
from models.user import User
from functools import wraps

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        user = User.get_user_with_firebase_token(token)
        return (
            f(user, *args, **kwargs)
            if user
            else (jsonify({"message": "Token is invalid!"}), 403)
        )

    return decorated


@auth_blueprint.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    """
    data = request.get_json()
    res = User.register(data["email"], data["password"])  # type: ignore
    return (
        jsonify({"message": "User created successfully!"}), 201
        if res
        else (jsonify({"message": "Username or email already exists"}), 400)
    )


@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    Login a user
    """
    data = request.get_json()
    login_data = User.login(data["email"], data["password"])  # type: ignore
    return (
        jsonify({"token": login_data}), 200
        if login_data is not None
        else (jsonify({"message": "Invalid username or password"}), 401)
    )
