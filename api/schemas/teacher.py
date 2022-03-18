from .account import AccountBase


class Teacher(AccountBase):
    account_id: int


class TeacherCreate(Teacher):
    pass