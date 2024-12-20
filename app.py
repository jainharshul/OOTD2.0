from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database.firebase_setup import db
from database.signup_signin import create_user, authenticate_user, User

app = FastAPI()

# Route to sign up a new user
@app.post("/signup/")
async def signup(user: User):
    try:
        result = create_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to sign in a user
@app.post("/signin/")
async def signin(user: User):
    try:
        token = authenticate_user(user.username, user.password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
