from fastapi import FastAPI, Request, status, HTTPException, Body, Depends, APIRouter


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.get('/')
def get(request: Request):
    return {'message': 'API is up!'}