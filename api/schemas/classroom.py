from .schema import Schema
from .teacher import Teacher
from typing import List
from datetime import date


class ClassRoomBase(Schema):
    name: str
    room: str
    student_ids: List[int]
    class_time_ids: List[int]
    start_date: date = None
    total_days: int = None


class ClassRoom(ClassRoomBase):
    teacher: Teacher


class ClassRoomCreate(ClassRoomBase):
    teacher: int


class ClassRoomUpdate(ClassRoomBase):
    teacher: int