from .base import BaseModel
from peewee import (
    CharField,
    IntegerField
)

class Account(BaseModel):
    name = CharField()
    password = CharField()
    mail = CharField()
    phone = CharField()
    role = IntegerField()
    search_str = CharField()