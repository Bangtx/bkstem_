from .schema import Schema


class RollCallBase(Schema):
    classroom: int
    student: int
    teacher: int
    absent_type: int


class RollCall(RollCallBase):
    pass


class RollCallCreate(RollCallBase):
    pass