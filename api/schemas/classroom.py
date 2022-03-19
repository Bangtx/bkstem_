from .schema import Schema
from typing import List


class ClassRoom(Schema):
    name: int
    teacher_id: int
    student_ids: List[int]
    class_time_ids: List[int]


class ClassRoomCreate(ClassRoom):
    pass