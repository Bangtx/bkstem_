from peewee import CharField, BooleanField
from .base import BaseModel


class OrderType(BaseModel):
    name = CharField()
    name_eng = CharField()
    is_order = BooleanField(default=False)

    class Meta:
        db_table = "order_type"
