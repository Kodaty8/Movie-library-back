from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCredentials(UserBase):
    password: str


class User(UserBase):
    id: int
    lang: str = "en-US"

    class Config:
        orm_mode = True
