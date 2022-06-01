from .base import BaseModel
from peewee import (
    CharField,
    DateField
)


class Account(BaseModel):
    name = CharField()
    date_of_birth = DateField()
    gender = CharField()
    password = CharField()
    mail = CharField()
    phone = CharField()
    search_str = CharField()

    class Meta:
        db_table = 'account'

    @classmethod
    def is_duplicate(cls, mail, phone):
        query = list(
            cls.select().where(
                cls.active, cls.phone == phone
            )
        )
        if query:
            return True
        return False
