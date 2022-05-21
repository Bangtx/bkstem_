from .account import AccountBase
from datetime import date
from .schema import Schema
from typing import List


class StudentBase(AccountBase):
    pass


class StudentCreate(StudentBase):
    classrooms: List[int] = []


class Student(StudentBase):
    account: AccountBase
    id: int


class StudentUpdate(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str = None
    phone: str
    classrooms: List[int] = []
