from peewee import CharField, BareField
from .base import BaseModel
from utils.aws import get_user_from_cognito


class Member(BaseModel):
    email = CharField()
    setting = BareField()

    @classmethod
    def find_by_email(cls, email: str):
        query = Member.select().where(Member.email == email, Member.active)
        return list(query)

    @classmethod
    def get_current_member(cls, token: str):
        user_info = get_user_from_cognito(token)
        return cls.find_by_email(user_info["email"])
