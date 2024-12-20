import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to your Firebase private key
firebase_key_path = "database/info.json"

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

# Get Firestore database
db = firestore.client()
