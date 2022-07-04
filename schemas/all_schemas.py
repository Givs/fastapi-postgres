from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int = None
    name: str
    email: str
    password: str
    office: str

    class Config:
        orm_mode = True


class Author(BaseModel):
    id: int = None
    name: str

    class Config:
        orm_mode = True


class Paper(BaseModel):
    id: int = None
    author_id: int
    title: str
    sumary: str

    class Config:
        orm_mode = True
