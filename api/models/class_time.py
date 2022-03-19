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

    @classmethod
    def get_class_times_by_ids(cls, ids):
        class_times = (
            cls.select(
                DateOfWeek.name.alias('date_of_week'),
                cls.start_time,
                cls.stop_time
            ).join(
                DateOfWeek, on=DateOfWeek.id == cls.date_of_week
            ).where(
                cls.active, cls.id << ids
            ).dicts()
        )

        return list(class_times)