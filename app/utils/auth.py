import json
from datetime import timedelta, datetime

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils import crud, models, schemas

with open('app/config.json', 'r') as f:
    cfg = json.load(f)
    SECRET_KEY = cfg['jwt-encryption-key']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    user_dict = get_user_dict(username, db)
    if not user_dict:
        return False
    user = schemas.UserCredentials(**user_dict)
    if not verify_password(password, user.password):
        return False
    return user


def get_user_dict(username, db):
    user_list = crud.read(models.User, [["username", username]], db)
    if not user_list:
        return None
    user_dict = user_list[0].__dict__
    return user_dict


def hash_password(pw):
    return pwd_context.hash(pw)


def decode_token(token, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = TokenData(username=username)
    except JWTError:
        return False

    user_dict = get_user_dict(token_data.username, db)
    if not user_dict:
        return False
    user = schemas.User(**user_dict)
    return user
