from .account import AccountBase
from datetime import date
from .schema import Schema


class StudentBase(AccountBase):
    pass


class StudentCreate(StudentBase):
    account_id: int


class Student(StudentBase):
    account: AccountBase
    id: int


class StudentUpdate(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str
    phone: str