from .schema import Schema
from datetime import time
from .date_of_week import DateOfWeek


class ClassTimeBase(Schema):
    start_time: time = '18:00:00'
    stop_time: time = '20:00:00'


class ClassTimeCreate(ClassTimeBase):
    date_of_week: int


class ClassTime(ClassTimeBase):
    id: int
    date_of_week: DateOfWeek
