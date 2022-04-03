from .base import BaseModel
from peewee import ForeignKeyField, fn, DateField
from playhouse.postgres_ext import ArrayField
from .teacher import Teacher
from .student import Student
from .classroom import Classroom
from .account import Account


class Score(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    date = DateField()
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    score = ArrayField()

    class Meta:
        db_table = 'score'

    @classmethod
    def get_list(cls):
        students = (
            Student.select(
                Student.id,
                Account.name,
            ).join(
                Account, on=Account.id == Student.account
            ).where(
                Account.active, Student.active
            )
        )

        teachers = (
            Teacher.select(
                Teacher.id,
                Account.name,
            ).join(
                Account, on=Account.id == Teacher.account
            ).where(
                Account.active, Teacher.active
            )
        )

        query = list(
            cls.select(
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('classroom'),
                cls.date,
                cls.score,
                fn.json_build_object(
                    'id', students.c.id,
                    'name', students.c.name
                ).alias('student'),
                fn.json_build_object(
                    'id', teachers.c.id,
                    'name', teachers.c.name
                ).alias('teacher')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                students, on=students.c.id == cls.student
            ).join(
                teachers, on=teachers.c.id == cls.teacher
            ).where(
                cls.active
            ).dicts()
        )
        dates = list(set(list(map(lambda x: str(x['date']), query))))
        datas = []
        for date in dates:
            data = list(filter(lambda x: str(x['date']) == date, query))
            datas.append({
                'date': date,
                'data': data
            })
        return datas

    @classmethod
    def get_score_by_date(cls, date, student_id, class_room_id=None):
        scores = (
            cls.select().where(
                cls.active, cls.date == date, cls.student == student_id
            )
        )
        if class_room_id:
            scores = scores.where(cls.classroom == class_room_id)
        # scores = scores.dicts().get()
        if list(scores):
            scores = scores.dicts().get()
            return scores
        return None