from .base import BaseModel
from peewee import ForeignKeyField
from .classroom import Classroom


class Schedule(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')

    class Meta:
        db_table = 'schedule'
