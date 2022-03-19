from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    TimeField
)
from .date_of_week import DateOfWeek


class ClassTime(BaseModel):
    date_of_week = ForeignKeyField(DateOfWeek, column_name='date_of_week_id')
    start_time = TimeField()
    stop_time = TimeField()

    class Meta:
        db_table = 'class_time'
