from builtins import set

from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    fn,
    JOIN
)
from .account import Account


class Student(BaseModel):
    account = ForeignKeyField(Account, column_name='account_id')
    status = IntegerField()

    LEARN = 1
    QUIT = 2
    TEMP_STOP = 3
    COMPLETE = 4
    CHANGE = 5

    class Meta:
        db_table = 'student'

    @classmethod
    def get_list(cls):
        students = (
            cls.select(
                cls.id,
                Account.name,
                Account.gender,
                cls.status,
                Account.date_of_birth,
                fn.json_build_object(
                    'id', Account.id,
                    'mail', Account.mail,
                    'phone', Account.phone
                ).alias('account')
            ).join(
                Account, on=cls.account_id == Account.id
            ).where(cls.active, Account.active).dicts()
        )

        from .classroom import Classroom
        for student in students:
            student['classrooms'] = Classroom.get_classrooms(student_id=student['id'])

        return list(students)

    @classmethod
    def get_students_by_ids(cls, ids):
        students = (
            cls.select(
                cls.id,
                Account.name,
                Account.gender,
                Account.date_of_birth
            ).join(
                Account, on=Account.id == cls.account
            ).where(
                Account.active, cls.active, cls.id << ids
            ).dicts()
        )
        return list(students)

    @classmethod
    def get_students_by_id(cls, id):
        student = (
            cls.select(
                cls.id,
                Account.name,
                Account.gender,
                Account.date_of_birth,
                Account.mail,
                Account.phone
            ).join(
                Account, JOIN.LEFT_OUTER, on=Account.id == cls.account
            ).where(
                Account.active, cls.active, cls.id == id
            ).dicts()
        )
        if list(student):
            return student.get()
        return None

