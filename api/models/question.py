from .base import BaseModel
from playhouse.postgres_ext import JSONField, IntegerField
from peewee import CharField


class Question(BaseModel):
    answers = JSONField()
    result = CharField()
    type = IntegerField()
    image = CharField()
    audio = CharField()

    class Meta:
        db_table = 'question'

    @classmethod
    def get_questions(cls):
        query = (
            cls.select(
                cls.id,
                cls.answers,
                cls.type,
                cls.image,
                cls.audio
            ).where(
                cls.active
            ).dicts()
        )

        return list(query)
