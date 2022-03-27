from .schema import Schema
from datetime import date


class AccountBase(Schema):
    name: str
    gender: str
    date_of_birth: date
    password: str
    mail: str = None
    phone: str = None
    role: int = None
    search_str: str = None


class AccountCreate(AccountBase):
    pass

