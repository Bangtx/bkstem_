from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField
)
from playhouse.postgres_ext import ArrayField
from .teacher import Teacher


class Classroom(BaseModel):
    name = CharField()
    teacher_id = ForeignKeyField(Teacher)
    student_ids = ArrayField()
    class_time_ids = ArrayField()

    class Meta:
        db_table = 'classroom'

    @classmethod
    def get_classrooms(cls):
        classrooms = cls.get_list()
        print(classrooms)

    @classmethod
    def check_teacher_class_times_exits(cls):
        pass