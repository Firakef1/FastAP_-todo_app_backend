from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from datetime import timedelta, datetime
from typing import Annotated
import os


from ..utils.hash import hash_password
from ..utils.token import authenticate_user, create_access_token
# from pwdlib import PasswordHash

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")








@router.post("/sign-up", status_code = status.HTTP_201_CREATED)
async def sign_up(user: schemas.CreateUser, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.username == user.username, models.User.email == user.email).first()

    if db_user:

        raise HTTPException(status_code = 409, detail="username or email taken")

    new_user = models.User(
        username = user.username,
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/log-in", status_code = status.HTTP_200_OK)
async def log_in(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code = 401, detail="could not validate user")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {"msg": "Login successful"}


@router.post("/log-out", status_code=status.HTTP_200_OK)
def logout(response: Response, access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No active session")

    # Delete the cookie
    response.delete_cookie(key="access_token")
    return {"msg": "Logged out successfully"}

    