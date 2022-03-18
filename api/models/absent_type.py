from .base import BaseModel
from peewee import CharField


class AbsentType(BaseModel):
    type = CharField()

    class Meta:
        db_table = 'absent_type'
