from schemas.question import Question
from .base import BaseModel
from playhouse.postgres_ext import JSONField, IntegerField
from .classroom import Classroom
from .question import Question
from .schedule import Schedule
from peewee import CharField, DateField, ForeignKeyField, fn, JOIN


class HomeWork(BaseModel):
    date = DateField()
    deadline = DateField()
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    question = ForeignKeyField(Question, column_name='question_id')
    schedule = ForeignKeyField(Schedule, column_name='schedule_id')

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
                ).alias('question'),
                fn.json_build_object(
                    'id', Schedule.id,
                    'title', Schedule.title
                ).alias('unit')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                Question, on=Question.id == cls.question
            ).join(
                Schedule, on=Schedule.id == cls.schedule
            ).where(
                cls.active,
                Classroom.active,
                Question.active
            ).dicts()
        )

        return list(query)

    @classmethod
    def get_questions_by_unit(cls, unit, result):
        # question = (
        #     Question.select(
        #         Question.id, Question.answers, Question.type
        #     ).where(Question.active).alias('questions').group_by(Question.id)
        # )
        home_works = list(
            cls.select(
                cls.id,
                fn.json_build_object(
                    'id', Question.id, 'answers', Question.answers, 'type', Question.type
                ).alias('questions'),
                Question.result
            ).join(
                Question, JOIN.LEFT_OUTER, on=Question.id == cls.question
            ).where(
                cls.schedule == unit, cls.active
            ).group_by(
                cls.id, Question.id
            ).dicts()
        )
        data = []
        for home_work in home_works:
            if not result:
                home_work.pop('result', None)

            data.append(home_work['questions'])

        return home_works

    @classmethod
    def get_questions_group_by_unit(cls, classroom_id, result):
        units = list(
            Schedule.select(
                Schedule.id, Schedule.title
            ).where(
                Schedule.classroom == classroom_id
            ).dicts()
        )

        for unit in units:
            unit['home_work'] = HomeWork.get_questions_by_unit(unit['id'], result)

        return units
