from fastapi import Request, status, Body, Depends, APIRouter, Response
from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.auth.jwt_bearer import jwtBearer
from src.auth.jwt_handler import get_expiry_token
from src.schemas.all_schemas import UserLogin, User
from src.routes.users.user_logic import get_all_users, get_an_users, user_login, create_user


limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', dependencies=[Depends(jwtBearer())], response_model=List[User], status_code=200)
@limiter.limit("60/minute")
async def get(request: Request, response: Response):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    users = get_all_users()

    return users


@router.get('/{user_id}', dependencies=[Depends(jwtBearer())], response_model=User, status_code=200)
@limiter.limit("60/minute")
def get_user(user_id: int, request: Request, response: Response):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    user = get_an_users(user_id)

    return user


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED, tags=["user"])
@limiter.limit("60/minute")
def post(request: Request, user: User):
    new_user = create_user(user)

    return new_user


@router.post("/login", tags=["user"])
@limiter.limit("60/minute")
def post_login(request: Request, user: UserLogin = Body(default=None)):
    access_token = user_login(user)

    return access_token


@router.get('/expiry/token', tags=["user"], dependencies=[Depends(jwtBearer())])
@limiter.limit("60/minute")
async def get(request: Request, response: Response):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    expiry_time = get_expiry_token(request)

    return expiry_time


