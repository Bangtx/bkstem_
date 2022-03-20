from .schema import Schema
from .teacher import Teacher
from typing import List


class ClassRoomBase(Schema):
    name: str
    student_ids: List[int]
    class_time_ids: List[int]


class ClassRoom(ClassRoomBase):
    teacher: Teacher


class ClassRoomCreate(ClassRoomBase):
    teacher: int