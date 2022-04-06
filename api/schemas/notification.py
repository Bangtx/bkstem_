from .schema import Schema
from datetime import date


class NotificationBase(Schema):
    classroom: int
    student: int
    teacher: int
    notification: str
    date: date


class Notification(NotificationBase):
    pass


class NotificationCreate(NotificationBase):
    pass
