from .base import BaseModel
from peewee import (
    fn,
    ForeignKeyField
)
from .account import Account


class Teacher(BaseModel):
    account = ForeignKeyField(Account, column_name='account_id')

    class Meta:
        db_table = 'teacher'

    @classmethod
    def get_list(cls):
        query = (
            cls.select(
                cls.id,
                Account.name,
                Account.gender,
                Account.date_of_birth,
                fn.json_build_object(
                    'id', Account.id,
                    'mail', Account.mail,
                    'phone', Account.phone
                ).alias('account')
            )
            .join(
                Account, on=cls.account_id == Account.id
            )
            .where(cls.active, Account.active)
            .dicts()
        )
        return list(query)

    @classmethod
    def get_teacher_by_id(cls, id):
        teacher = (
            Teacher.select(
                Teacher.id,
                Account.name,
                Account.gender,
                Account.date_of_birth,
                Account.mail,
                Account.phone
            ).join(
                Account, on=Account.id == Teacher.account
            ).where(
                Account.active, Teacher.active, Teacher.id == id
            ).dicts()
        )
        return teacher.get()