from .base import BaseModel
from peewee import (
    fn,
    ForeignKeyField
)
from .account import Account
from playhouse.shortcuts import model_to_dict


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
                fn.json_build_object(
                    'id', Account.id,
                    'mail', Account.name,
                    'phone', Account.name
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
                Account.name
            ).join(
                Account, on=Account.id == Teacher.account
            ).where(
                Account.active, Teacher.active, Teacher.id == id
            ).dicts()
        )
        return teacher.get()