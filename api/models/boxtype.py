from peewee import CharField, BigIntegerField
from .master import MasterModel


class BoxType(MasterModel):
    name = CharField()
    short_name = CharField()
    yomi = CharField()
    name_eng = CharField()
    bundle_size = BigIntegerField()

    class Meta:
        db_table = "box_type"
