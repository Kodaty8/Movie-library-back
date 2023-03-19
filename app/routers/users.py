from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils import crud, models, schemas, database, auth

models.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/users"
)


@router.post("/signup")
async def signup(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = auth.get_user_dict(user.username, db)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    hashed_password = auth.hash_password(user.password)
    row = models.User(username=user.username, password=hashed_password)
    account = crud.create(row, db)
    access_token = auth.create_access_token(
        data={"sub": account.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    user = auth.decode_token(token, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
