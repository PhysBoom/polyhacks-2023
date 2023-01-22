from flask import Flask, request
from controllers.applicant_loader import ApplicantLoader
from controllers.mongodb_client import Database
from dotenv import load_dotenv
from flask_cors import CORS

from blueprints.v1.v1_blueprint import v1_blueprint

app = Flask(__name__)
app.register_blueprint(v1_blueprint)
CORS(app)


@app.before_first_request
def initialize_app():
    load_dotenv()
    Database.initialize()
    ApplicantLoader.get_instance()


if __name__ == "__main__":
    app.run(debug=True)
