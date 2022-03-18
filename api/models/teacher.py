from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField
)
from .account import Account


class Teacher(BaseModel):
    account_id = ForeignKeyField(Account)

    class Meta:
        db_table = 'teacher'
