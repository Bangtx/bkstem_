from .base import BaseModel
from peewee import CharField


class AudioFile(BaseModel):
    url = CharField()

    class Meta:
        db_table = 'audio_file'


