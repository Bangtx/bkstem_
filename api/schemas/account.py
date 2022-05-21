from .schema import Schema
from datetime import date
from typing import Optional, List


class AccountLogin(Schema):
    password: str
    phone: str


class AccountBase(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    password: str
    mail: str = None
    phone: str
    role: int = None
    search_str: str = None


class AccountCreate(AccountBase):
    pass

