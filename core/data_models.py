from pydantic import BaseModel
from typing import Optional


class UserCredentials(BaseModel):
    username: str
    password: str
    remember: bool = False


class LoginData(BaseModel):
    valid: UserCredentials
    invalid_password: UserCredentials
    invalid_username: UserCredentials
    empty_username: UserCredentials
    empty_password: UserCredentials
