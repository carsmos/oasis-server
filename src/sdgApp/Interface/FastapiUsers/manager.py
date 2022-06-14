from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import MongoDBUserDatabase

from sdgApp.Infrastructure.MongoDB.session_maker import mongo_db
from .users_model import User, UserCreate, UserDB, UserUpdate
from .insert_default_config import insert_default
from sdgApp.Application.log.usercase import loggerd

SECRET = "7165bf1355c0bddf29d0b6326af2ac9b6e876ee8514c93ae887796c540e33ddf"

db = mongo_db.db
collection = db["users"]


class UserManager(BaseUserManager[UserCreate, UserDB]):
  user_db_model = UserDB
  reset_password_token_secret = SECRET
  verification_token_secret = SECRET

  async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
    loggerd.info(f"User {user.id} has registered.")
    await insert_default(db, user)


  async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
    loggerd.info(f"User {user.id} has forgot their password. Reset token: {token}")


  async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
    loggerd.info(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_db():
    yield MongoDBUserDatabase(UserDB, collection)

async def get_user_manager(user_db: MongoDBUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
