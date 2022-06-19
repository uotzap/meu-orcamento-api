from unicodedata import decimal
from pydantic import BaseModel

class Spendings(BaseModel):
    id: int
    user_id: int
    date: str
    account: str
    value: str
    category: str