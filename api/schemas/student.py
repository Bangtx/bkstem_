from .account import AccountBase


class Student(AccountBase):
    account_id: int


class StudentCreate(Student):
    pass