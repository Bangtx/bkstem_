from .base import BaseModel
from peewee import ForeignKeyField, CharField, fn
from .classroom import Classroom


class Schedule(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    title = CharField()

    class Meta:
        db_table = 'schedule'

    @classmethod
    def get_schedules(cls, classroom_id: int):
        query = (
            cls.select(
                cls.id,
                cls.title,
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('classroom')
            ).join(
                Classroom, on=cls.classroom == Classroom.id
            ).where(
                cls.active, Classroom.active, cls.classroom == classroom_id
            ).dicts()
        )

        return list(query)
