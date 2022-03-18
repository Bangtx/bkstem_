from .base import BaseModel
from peewee import (
    CharField
)


class Account(BaseModel):
    name = CharField()
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
                cls.active, cls.mail == mail or cls.phone == phone
            )
        )
        print(query)
        if query:
            return True
        return False
