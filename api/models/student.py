from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    fn
)
from .account import Account


class Student(BaseModel):
    account = ForeignKeyField(Account, column_name='account_id')

    class Meta:
        db_table = 'student'

    @classmethod
    def get_list(cls):
        student = (
            cls.select(
                cls.id,
                Account.name,
                fn.json_build_object(
                    'id', Account.id,
                    'mail', Account.name,
                    'phone', Account.name
                ).alias('account')
            ).join(
                Account, on=cls.account_id == Account.id
            ).where(cls.active, Account.active).dicts()
        )
        return list(student)


