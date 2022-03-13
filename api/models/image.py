from peewee import CharField, IntegerField, BooleanField
from .base import BaseModel


class Image(BaseModel):
    name = CharField()
    uuid = CharField()
    token = CharField()
    s3url = CharField()
    format = CharField()
    size = IntegerField()
    is_default = BooleanField()
