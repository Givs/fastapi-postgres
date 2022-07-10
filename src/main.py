from fastapi import FastAPI, APIRouter

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


import uvicorn
from src.database.database import SessionLocal


from src.routes.users import user_routes
from src.routes.authors import author_routes
from src.routes.papers import paper_routes


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

db = SessionLocal()

router = APIRouter()
router.include_router(user_routes.router)
router.include_router(author_routes.router)
router.include_router(paper_routes.router)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)



