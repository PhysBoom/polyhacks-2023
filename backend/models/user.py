from pydantic import BaseModel, Field
from controllers.mongodb_client import Database
from controllers.firebase_controller import get_user_id_from_firebase_token, create_new_user, login_user

class User(BaseModel):
    firebase_user_key: str = Field(...)

    @staticmethod
    def get_user_with_firebase_token(token):
        return Database.find_one("users", {"firebase_user_key": get_user_id_from_firebase_token(token)})

    @staticmethod
    def register(email, password):
        try:
            firebase_user_key = create_new_user(email, password)['localId']
            user = User(firebase_user_key=firebase_user_key)
            Database.insert_one("users", user.dict())
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def login(email, password):
        try:
            login_resp = login_user(email, password)
            return login_resp['idToken']
        except Exception:
            return None
