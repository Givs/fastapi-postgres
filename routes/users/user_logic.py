from fastapi import Body
from database import SessionLocal
from errors.error_instance import error_instance
from schemas.all_schemas import UserLogin, User
from auth.hash_provider import generate_hash, verify_hash
from auth.jwt_handler import signJWT
from validations.validations_for_create_user import office_validation, password_validation, email_validation

import models

db = SessionLocal()


def get_all_users():
    users = db.query(models.User).all()
    return users


def get_an_users(user_id):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        error_instance(404, "User not found")

    return user


def check_user(data: UserLogin):
    query = db.query(models.User).filter(models.User.email == data.email).all()

    if len(query) == 1:
        user = query[0]
        is_valid_password = verify_hash(data.password, user.password)
        if is_valid_password:
            return True
    else:
        return False


def user_login(user: UserLogin = Body(default=None)):
    if check_user(user):
        get_user_office = db.query(models.User).filter(models.User.email == user.email).all()
        return signJWT(user.email, get_user_office[0].office)
    else:
        error_instance(401, "Invalid Email or password")


def create_user(user: User):
    password_validation(user.password)
    office_validation(user.office)
    email_validation(user)

    user.password = generate_hash(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        office=user.office
    )

    db_user = db.query(models.User).filter_by(email=new_user.email).count()

    if db_user >= 1:
        error_instance(400, "Email already exists")

    token = signJWT(user.email, user.office)

    if token:
        db.add(new_user)
        db.commit()
        return new_user
