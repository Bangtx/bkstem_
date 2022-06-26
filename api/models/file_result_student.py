from models.base import BaseModel
from models.home_work_file import HomeWorkFile
from models.classroom import Classroom
from models.student import Student
from peewee import ForeignKeyField, CharField, fn
import itertools
from models.account import Account


class FileResultStudent(BaseModel):
    home_work_file = ForeignKeyField(HomeWorkFile, column_name='home_work_file')
    class_room = ForeignKeyField(Classroom, column_name='class_room')
    student = ForeignKeyField(Student, column_name='student')
    msg = CharField()
    name = CharField()
    url = CharField()

    class Meta:
        db_table = 'file_result_student'

    @classmethod
    def get_file_result_student(cls, classroom_id, student_id, home_work_file):
        students = (
            Student.select(
                Student.id,
                Account.name,
                Account.gender,
            ).join(
                Account, on=Student.account_id == Account.id
            ).where(Student.active, Account.active).alias('students')
        )

        query = (
            cls.select(
                cls.id,
                cls.class_room,
                fn.json_build_object(
                    'id', students.c.id,
                    'name', students.c.name
                ).alias('student'),
                cls.msg,
                cls.name,
                cls.url,
                cls.home_work_file
            ).join(
                students, on=students.c.id == cls.student
            ).where(
                cls.active
            ).order_by(
                cls.student,
                cls.id
            ).dicts()
        )

        if classroom_id:
            query = query.where(cls.class_room == classroom_id)

        if student_id:
            query = query.where(cls.student == student_id)

        if home_work_file:
            query = query.where(cls.home_work_file == home_work_file)

        data = list(query)

        results = []

        groups = itertools.groupby(data, key=lambda x: x['student']['id'])
        for key, value in groups:
            value = list(value)
            results += value

        return results
    