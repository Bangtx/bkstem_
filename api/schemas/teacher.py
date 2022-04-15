from .account import AccountBase
from datetime import date
from .schema import Schema


class TeacherBase(AccountBase):
    pass


class Teacher(TeacherBase):
    pass


class TeacherCreate(TeacherBase):
    account: int


class TeacherUpdate(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str
    phone: str