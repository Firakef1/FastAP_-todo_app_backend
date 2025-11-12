from .hash import varify_password, hash_password
from .. import models
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")



def authenticate_user(username, password, db):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user: 
        return False
    if not varify_password(password, user.password):
        return False
    
    return user

def create_access_token(usename: str, user_id: int, expires_delta: timedelta):

    encode = {"sub": usename, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def varify_access_token(token: str):

    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: int = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="invalid token")
    return username