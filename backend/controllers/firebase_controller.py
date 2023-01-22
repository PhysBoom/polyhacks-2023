import pyrebase
import firebase_admin

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDohzKb71rDitSdPy9ESNnMxTS9nx3X9_0",
    "authDomain": "polyhacks-2023.firebaseapp.com",
    "databaseURL": "https://polyhacks-2023.firebaseio.com/",
    "storageBucket": "polyhacks-2023.appspot.com",
    "serviceAccount": "firebase-conf.json",
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()
db = firebase.database()


def create_new_user(email, password):
    return auth.create_user_with_email_and_password(email, password)


def get_user_id_from_firebase_token(token):
    try:
        decoded_token = auth.get_account_info(token)
        return decoded_token["users"][0]["localId"]
    except Exception:
        return None


def login_user(email, password):
    return auth.sign_in_with_email_and_password(email, password)


# Uploads a file to Firebase Storage
def upload_file_to_firebase_storage(file, file_name):
    storage = firebase.storage()
    storage.child(file_name).put(file)


# Downloads a file from Firebase Storage
def download_file_from_firebase_storage(target_path, destination_path):
    storage = firebase.storage()
    storage.child(target_path).download(destination_path)
