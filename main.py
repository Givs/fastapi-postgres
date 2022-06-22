from fastapi import FastAPI, status, HTTPException, Body, Depends
from pydantic import BaseModel
from typing import Optional, List
from email_validator import validate_email, EmailNotValidError

from pydantic.networks import EmailStr

from database import SessionLocal
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer
from auth.hash_provider import generate_hash, verify_hash

import models

app = FastAPI()


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


db = SessionLocal()


@app.get('/users', dependencies=[Depends(jwtBearer())], response_model=List[User], status_code=200)
def get_all_users():
    users = db.query(models.User).all()

    return users


@app.post('/users', response_model=User, status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user: User):
    user.password = generate_hash(user.password)
    try:
        validEmail = validate_email(user.email).email
    except EmailNotValidError as e:
        raise HTTPException(status_code=510, detail="Email format is incorect")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        office=user.office
    )

    db_user = db.query(models.User).filter_by(email=new_user.email).count()

    if db_user >= 1:
        raise HTTPException(status_code=400, detail="Email already exists")

    token = signJWT(user.email, user.office)

    if token:
        db.add(new_user)
        db.commit()
        return new_user


def check_user(data: UserLogin):
    query = db.query(models.User).filter(models.User.email == data.email).all()
    if len(query) == 1:
        user = query[0]
        isValidPassword = verify_hash(data.password, user.password)
        if isValidPassword:
            return True
    else:
        return False


@app.post("/users/login", tags=["user"])
def user_login(user: UserLogin = Body(default=None)):
    if check_user(user):
        get_user_office = db.query(models.User).filter(models.User.email == user.email).all()
        return signJWT(user.email, get_user_office[0].office)
    else:
        raise HTTPException(status_code=401, detail="Invalid Email or password")

@app.post("/authors", dependencies=[Depends(jwtBearer())], response_model=Author, status_code=status.HTTP_201_CREATED, tags=["author"])
def create_author(author: Author):
    new_author = models.Author(
        name=author.name
    )

    db.add(new_author)
    db.commit()
    return new_author


@app.get('/authors', dependencies=[Depends(jwtBearer())], response_model=List[Author], status_code=200)
def get_all_authors():
    authors = db.query(models.Author).all()

    return authors


@app.post("/papers", dependencies=[Depends(jwtBearer())], response_model=Paper, status_code=status.HTTP_201_CREATED, tags=["paper"])
def create_paper(paper: Paper):
    new_paper = models.Paper(
        author_id=paper.author_id,
        title=paper.title,
        sumary=paper.sumary
    )

    find_author_id = db.query(models.Author).filter(models.User.id == paper.author_id).count()
    if not find_author_id:
        raise HTTPException(status_code=404, detail="Author doesn't exist.")

    db.add(new_paper)
    db.commit()
    return new_paper

@app.get('/papers', dependencies=[Depends(jwtBearer())], response_model=List[Paper], status_code=200)
def get_all_papers():
    papers = db.query(models.Paper).all()

    return papers

