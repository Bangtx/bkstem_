from .base import BaseModel
from peewee import CharField, ForeignKeyField, fn, DateField
from .teacher import Teacher
from .student import Student
from .classroom import Classroom


class Notification(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    notification = CharField()
    date = DateField()

    class Meta:
        db_table = 'notification'
