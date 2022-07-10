from fastapi import FastAPI, Request, status, HTTPException, Body, Depends, APIRouter
from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database.database import SessionLocal
from src.auth.jwt_bearer import jwtBearer
from src.schemas.all_schemas import Paper
from src.routes.papers.paper_logic import create_paper, get_and_search_papers, get_a_paper, update_paper, delete_paper


limiter = Limiter(key_func=get_remote_address)

db = SessionLocal()

router = APIRouter(
    prefix="/papers",
    tags=["Paper"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", dependencies=[Depends(jwtBearer())], response_model=Paper, status_code=status.HTTP_201_CREATED, tags=[
    "paper"])
@limiter.limit("60/minute")
def post(request: Request, paper: Paper):
    new_paper = create_paper(paper)

    return new_paper


@router.get('/', dependencies=[Depends(jwtBearer())], response_model=List[Paper], status_code=200)
@limiter.limit("60/minute")
def get(request: Request, term: str = None):
    papers = get_and_search_papers(term)

    return papers


@router.get('/{paper_id}', dependencies=[Depends(jwtBearer())], response_model=Paper, status_code=200)
@limiter.limit("60/minute")
def get_paper(request: Request, paper_id: int):
    paper = get_a_paper(paper_id)

    return paper


@router.patch('/{paper_id}', dependencies=[Depends(jwtBearer())], response_model=Paper, status_code=200)
@limiter.limit("60/minute")
def patch(request: Request, paper_id: int, paper: Paper):
    paper_to_update = update_paper(paper_id, paper)

    return paper_to_update


@router.delete('/{paper_id}', dependencies=[Depends(jwtBearer())], response_model=Paper, status_code=200)
@limiter.limit("60/minute")
def delete(request: Request, paper_id: int):
    paper_to_delete = delete_paper(paper_id)

    return paper_to_delete
