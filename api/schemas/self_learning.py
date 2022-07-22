from schemas.schema import Schema
from datetime import date
from typing import List


class SelfLearningBase(Schema):
    classroom: int
    student: int
    absent_type: int = None


class SelfLearningCreate(SelfLearningBase):
    dates: List[date]


class SelfLearningUpdate(SelfLearningBase):
    dates: List[date]
    id: int
