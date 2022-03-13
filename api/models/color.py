from peewee import CharField, BigIntegerField
from .base import BaseModel


class Color(BaseModel):
    code = CharField()
    name = CharField()
    name_eng = CharField()
    short_name = CharField()
    order_num = BigIntegerField()
