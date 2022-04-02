from .schema import Schema
from .teacher import Teacher
from typing import List
from datetime import date


class ClassRoomBase(Schema):
    name: str
    room: str
    student_ids: List[int]
    class_time_ids: List[int]
    start_date: date
    total_days: int


class ClassRoom(ClassRoomBase):
    teacher: Teacher


class ClassRoomCreate(ClassRoomBase):
    teacher: int