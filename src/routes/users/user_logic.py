from fastapi import Body
from src.database.database import SessionLocal
from src.errors.error_instance import error_instance
from src.schemas.all_schemas import UserLogin, User
from src.auth.hash_provider import generate_hash, verify_hash
from src.auth.jwt_handler import signJWT
from src.validations.validations_for_create_user import office_validation, password_validation, email_validation

import src.database.models

db = SessionLocal()


def get_all_users():
    users = db.query(src.database.models.User).all()
    return users


def get_an_users(user_id):
    user = db.query(src.database.models.User).filter(src.database.models.User.id == user_id).first()

    if not user:
        error_instance(404, "User not found")

    return user


def check_user(data: UserLogin):
    query = db.query(src.database.models.User).filter(src.database.models.User.email == data.email).all()

    if len(query) == 1:
        user = query[0]
        is_valid_password = verify_hash(data.password, user.password)
        if is_valid_password:
            return True
    else:
        return False


def user_login(user: UserLogin = Body(default=None)):
    if check_user(user):
        get_user_office = db.query(src.database.models.User).filter(src.database.models.User.email == user.email).all()
        return signJWT(user.email, get_user_office[0].office)
    else:
        error_instance(401, "Invalid Email or password")


def create_user(user: User):
    password_validation(user.password)
    user.office = user.office.capitalize()
    office_validation(user.office)
    email_validation(user)

    user.password = generate_hash(user.password)

    new_user = src.database.models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        office=user.office
    )

    db_user = db.query(src.database.models.User).filter_by(email=new_user.email).count()

    if db_user >= 1:
        error_instance(400, "Email already exists")

    token = signJWT(user.email, user.office)

    if token:
        db.add(new_user)
        db.commit()
        return new_user
