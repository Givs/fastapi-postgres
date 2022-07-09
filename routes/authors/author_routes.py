from fastapi import Request, Depends, APIRouter, status
from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from database import SessionLocal
from auth.jwt_bearer import jwtBearer
from schemas.all_schemas import Author
from routes.authors.author_logic import create_author, search_author, get_an_author, update_author, delete_author


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
def post(request: Request, author: Author):
    new_author = create_author(author)

    return new_author


@router.get('/', dependencies=[Depends(jwtBearer())], response_model=List[Author], status_code=200)
@limiter.limit("60/minute")
def get(request: Request, term: str = None):
    authors = search_author(term)

    return authors


@router.get('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def get_author(request: Request, author_id: int):
    author = get_an_author(author_id)

    return author


@router.patch('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def patch(request: Request, author_id: int, author: Author):
    author_to_update = update_author(author_id, author)

    return author_to_update


@router.delete('/{author_id}', dependencies=[Depends(jwtBearer())], response_model=Author, status_code=200)
@limiter.limit("60/minute")
def delete(request: Request, author_id: int):
    author_to_delete = delete_author(author_id)

    return author_to_delete
