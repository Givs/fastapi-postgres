from fastapi import Request, APIRouter


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get(request: Request):
    return {'message': 'API is up!'}
