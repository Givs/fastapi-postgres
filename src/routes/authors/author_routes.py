from fastapi import Request, Depends, APIRouter, status, Response
from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database.database import SessionLocal
from src.auth.jwt_bearer import jwtBearer
from src.schemas.all_schemas import Author
from src.auth.jwt_handler import get_expiry_token
from src.routes.authors.author_logic import create_author, search_author, get_an_author, update_author, delete_author


limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])


db = SessionLocal()


router = APIRouter(
    prefix="/authors",
    tags=["Author"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", dependencies=[Depends(jwtBearer())], response_model=Author,
             status_code=status.HTTP_201_CREATED, tags=["author"])
@limiter.limit("60/minute")
def post(request: Request, response: Response, author: Author):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    new_author = create_author(author)

    return new_author


@router.get('/', dependencies=[Depends(jwtBearer())], response_model=List[Author], status_code=200)
@limiter.limit("60/minute")
def get(request: Request, response: Response, term: str = None):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    authors = search_author(term)

    return authors


@router.get('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def get_author(request: Request, response: Response, author_id: int):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    author = get_an_author(author_id)

    return author


@router.patch('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def patch(request: Request, response: Response, author_id: int, author: Author):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    author_to_update = update_author(author_id, author)

    return author_to_update


@router.delete('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def delete(request: Request, response: Response, author_id: int):
    expiry_time = get_expiry_token(request)
    response.headers["expiry-time"] = expiry_time['message']
    author_to_delete = delete_author(author_id)

    return author_to_delete
