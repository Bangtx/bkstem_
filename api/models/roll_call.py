from .base import BaseModel
from peewee import CharField, ForeignKeyField
from .teacher import Teacher
from .student import Student
from .classroom import Classroom
from .absent_type import AbsentType


class RollCall(BaseModel):
    classroom_id = ForeignKeyField(Classroom)
    student_id = ForeignKeyField(Student)
    teacher_id = ForeignKeyField(Teacher)
    absent_type_id = ForeignKeyField(AbsentType)

    class Meta:
        db_table = 'roll_call'
