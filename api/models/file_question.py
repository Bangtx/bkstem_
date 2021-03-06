from models.base import BaseModel
from peewee import CharField


class FileQuestion(BaseModel):
    name = CharField()
    url = CharField()

    class Meta:
        db_table = 'file_question'
