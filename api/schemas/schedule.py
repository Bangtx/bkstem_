from .schema import Schema


class ScheduleBase(Schema):
    id: int


class ScheduleCreate(Schema):
    classroom: int
    title: str


class ScheduleUpdate(ScheduleCreate):
    pass
