from .account import AccountBase


class StudentBase(AccountBase):
    pass


class StudentCreate(StudentBase):
    account_id: int


class Student(StudentBase):
    account: AccountBase
    id: int