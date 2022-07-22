from models.base import BaseModel
from peewee import ForeignKeyField, fn, JOIN, DateField
from models.classroom import Classroom
from models.absent_type import AbsentType
from models.student import Student
from models.account import Account
from datetime import datetime
import calendar


class SelfLearning(BaseModel):
    date = DateField()
    classroom = ForeignKeyField(Classroom, column_name='classroom')
    absent_type = ForeignKeyField(AbsentType, column_name='absent_type')
    student = ForeignKeyField(Student, column_name='student')

    class Meta:
        db_table = 'self_learning'

    @classmethod
    def get_self_learning(cls, classroom: int, student=None):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        first, last = calendar.monthrange(currentYear, currentMonth)
        # get students id
        student_ids = Classroom.get_or_none(id=classroom).student_ids

        students = (
            Student.select(
                Student.id,
                Account.name
            ).join(
                Account, JOIN.LEFT_OUTER, on=Account.id == Student.account
            ).where(
                Account.active, Student.active, Student.id << student_ids
            ).alias('students')
        )
        query = (
            cls.select(
                cls.id,
                AbsentType.type.alias('absent_type'),
                fn.json_build_object(
                    'id', students.c.id,
                    'name', students.c.name
                ).alias('student'),
                cls.date
            ).join(
                AbsentType, JOIN.LEFT_OUTER, on=AbsentType.id == cls.absent_type
            ).join(
                students, JOIN.LEFT_OUTER, on=students.c.id == cls.student
            ).where(
                cls.active,
                cls.date <= f'{currentYear}-{currentMonth}-{last}',
                cls.date >= f'{currentYear}-{currentMonth}-{first}'
            ).order_by(
                cls.date
            ).dicts()
        )

        return list(query)
