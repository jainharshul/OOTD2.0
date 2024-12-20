import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from firebase_admin import firestore
from pydantic import BaseModel

# Firestore database
from database.firebase_setup import db

# JWT Secret Key (replace with a secure key in production)
SECRET_KEY = "mysecretkey"  # Replace this with an environment variable later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User Schema
class User(BaseModel):
    username: str
    password: str

# Utility function to hash passwords
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to create a new user
def create_user(user: User):
    users_ref = db.collection("users")
    # Check if user already exists
    existing_user = users_ref.where("username", "==", user.username).stream()
    if any(existing_user):
        raise ValueError("User already exists")
    
    hashed_pw = hash_password(user.password)
    new_user_ref = users_ref.document()
    new_user_ref.set({
        "username": user.username,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    })
    return {"message": "User created successfully!", "id": new_user_ref.id}

# Function to authenticate a user
def authenticate_user(username: str, password: str):
    users_ref = db.collection("users")
    user_query = users_ref.where("username", "==", username).stream()
    user_doc = next(user_query, None)
    
    if not user_doc:
        raise ValueError("User not found")
    
    user_data = user_doc.to_dict()
    if not verify_password(password, user_data["password"]):
        raise ValueError("Invalid credentials")
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
