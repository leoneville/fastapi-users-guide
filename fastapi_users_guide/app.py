from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from fastapi_users_guide.db import User, create_db_and_tables
from fastapi_users_guide.schemas import UserCreate, UserRead, UserUpdate
from fastapi_users_guide.users import (
    auth_backend, 
    current_active_user, 
    fastapi_users,
    google_oauth_client,
)
from fastapi_users_guide.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix='/auth/jwt', 
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client, 
        auth_backend, 
        settings.SECRET, 
        is_verified_by_default=True,
    ),
    prefix='/auth/google',
    tags=['auth']
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {'message': f'Hello {user.email}!'}