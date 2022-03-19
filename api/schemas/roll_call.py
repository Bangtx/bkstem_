from .schema import Schema


class RollCall(Schema):
    classroom_id: int
    student_id: int
    teacher_id: int
    absent_type_id: int


class RollCallCreate(RollCall):
    pass