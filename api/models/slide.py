from models.base import BaseModel
from peewee import CharField, ForeignKeyField, DateField
from models.classroom import Classroom


class Slide(BaseModel):
    title = CharField()
    classroom = ForeignKeyField(Classroom, column_name='classroom')
    remark = CharField()
    url = CharField()

    class Meta:
        db_table = 'slide'

    @classmethod
    def get_slide(cls, classroom):
        query = (
            cls.select().where(
                cls.classroom == classroom,
                cls.active
            ).dicts().order_by(cls.id)
        )

        return list(query)
