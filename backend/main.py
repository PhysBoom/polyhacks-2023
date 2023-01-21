from flask import Flask, request
from controllers.mongodb_client import Database
from dotenv import load_dotenv

app = Flask(__name__)

@app.before_first_request
def initialize_app():
    load_dotenv()
    Database.initialize()

if __name__ == "__main__":
    app.run(debug=True)