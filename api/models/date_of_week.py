from .base import BaseModel
from peewee import CharField


class DateOfWeek(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'date_of_week'
