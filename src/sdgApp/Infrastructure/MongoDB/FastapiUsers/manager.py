from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

from sdgApp.Infrastructure.MongoDB.session_maker import async_mongo_session
from .users_model import User, UserCreate, UserDB, UserUpdate

SECRET = "7165bf1355c0bddf29d0b6326af2ac9b6e876ee8514c93ae887796c540e33ddf"

class UserManager(BaseUserManager[UserCreate, UserDB]):
  user_db_model = UserDB
  reset_password_token_secret = SECRET
  verification_token_secret = SECRET

  async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
    print(f"User {user.id} has registered.")


  async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


  async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


client, db = async_mongo_session()
collection = db["users"]

async def get_user_db():
    yield MongoDBUserDatabase(UserDB, collection)

async def get_user_manager(user_db: MongoDBUserDatabase = Depends(get_user_db)):
  yield UserManager(user_db)

jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
