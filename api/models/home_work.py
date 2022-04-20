from .base import BaseModel
from playhouse.postgres_ext import JSONField, IntegerField
from .classroom import Classroom
from .question import Question
from peewee import CharField, DateField, ForeignKeyField, fn


class HomeWork(BaseModel):
    date = DateField()
    deadline = DateField()
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    question = ForeignKeyField(Question, column_name='question_id')

    class Meta:
        db_table = 'home_work'

    @classmethod
    def get_home_works(cls):
        query = (
            cls.select(
                cls.id,
                cls.date,
                cls.deadline,
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('classroom'),
                fn.json_build_object(
                    'id', Question.id,
                    'answers', Question.answers,
                    'type', Question.type
                ).alias('question')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                Question, on=Question.id == cls.question
            ).where(
                cls.active,
                Classroom.active,
                Question.active
            ).dicts()
        )

        return list(query)