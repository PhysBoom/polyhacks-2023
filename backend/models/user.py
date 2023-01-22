from enum import Enum
from pydantic import BaseModel, Field
from controllers.mongodb_client import Database
from controllers.firebase_controller import get_user_id_from_firebase_token, create_new_user, login_user

class UserTypes(Enum):
    APPLICANT = "applicant"
    EMPLOYER = "employer"
    UNVERIFIED = "unverified"

class User(BaseModel):
    firebase_user_key: str = Field(...)
    user_type: UserTypes = Field(default=UserTypes.UNVERIFIED)
    name: str = Field(default="")
    email: str = Field(default="")
    phone_number: str = Field(default="")

    class Config:
        allow_population_by_field_name: True
        use_enum_values: True

    def as_dict(self):
        dict_without_enums = self.dict()
        dict_without_enums["user_type"] = self.user_type.value
        return dict_without_enums

    def load_user_from_db(self):
        return User(**Database.find_one("users", {"firebase_user_key": self.firebase_user_key}))

    @staticmethod
    def get_user_with_firebase_token(token):
        return Database.find_one("users", {"firebase_user_key": get_user_id_from_firebase_token(token)})

    @staticmethod
    def register(email, password, name, phone_number, type: UserTypes):
        try:
            firebase_user_key = create_new_user(email, password)['localId']
            user = User(firebase_user_key=firebase_user_key, user_type=type, email=email, name=name, phone_number=phone_number)
            Database.insert_one("users", user.as_dict())
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
