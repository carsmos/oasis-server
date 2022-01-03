from typing import Optional

from fastapi_users import models
from pydantic import UUID4


class User(models.BaseUser):
    rootfolder: Optional[UUID4] = None
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass