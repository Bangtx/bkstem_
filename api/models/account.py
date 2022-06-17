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

    @classmethod
    def get_accounts_by_name(cls, name):
        query = (
            cls.select(
                cls.id,
                cls.name,
                cls.phone
            ).where(
                cls.active, cls.name == name
            ).order_by(cls.id).dicts()
        )
        return list(query)