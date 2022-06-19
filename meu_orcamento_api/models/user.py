from enum import Enum
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    birth_date: str
    gender: str

class Users(BaseModel):
    users: list[User]
    count: int


class QueryUser(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]