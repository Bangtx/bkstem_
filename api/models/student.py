from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField
)
from .account import Account


class Student(BaseModel):
    account_id = ForeignKeyField(Account)

    class Meta:
        db_table = 'student'


