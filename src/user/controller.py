from src.user.dtos import userschema,loginschema
from sqlalchemy.orm import Session
from src.user.models import usermodel
from fastapi import HTTPException, status, Depends
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from src.utils.db import get_db
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


# Registration
def register_user(body:userschema, db: Session):
    is_user = db.query(usermodel).filter(usermodel.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    is_user = db.query(usermodel).filter(usermodel.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(body.password)

    new_user = usermodel(
        name=body.name,
        username=body.username,
        hashed_password=hashed_password,
        email=body.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: userschema, db: Session):
    user = db.query(usermodel).filter(usermodel.email == body.email).first()

    # Deliberately same error for "no such email" and "wrong password" —
    # prevents user enumeration (see DECISIONS.md)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id": user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> usermodel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("_id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
 
    user = db.query(usermodel).filter(usermodel.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
 