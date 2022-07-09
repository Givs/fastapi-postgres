from fastapi import FastAPI, Request, status, HTTPException, Body, Depends, APIRouter
from pydantic import BaseModel
from typing import Optional, List
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import or_

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from database import SessionLocal

from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer
from auth.hash_provider import generate_hash, verify_hash
from validations.validations_for_create_user import office_validation
from schemas.all_schemas import UserLogin, User, Author, Paper
from routes.users import user_routes
from routes.authors import author_routes
from routes.papers import paper_routes

import models

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






