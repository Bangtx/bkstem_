from .account import AccountBase


class TeacherBase(AccountBase):
    pass


class Teacher(TeacherBase):
    pass


class TeacherCreate(TeacherBase):
    account: int