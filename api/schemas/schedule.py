from .schema import Schema


class ScheduleBase(Schema):
    id: int


class ScheduleCreate(ScheduleBase):
    classroom: int


class ScheduleUpdate(ScheduleBase):
    classroom: int