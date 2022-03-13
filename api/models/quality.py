from peewee import CharField, ForeignKeyField
from .master import MasterModel
from .quality_group import QualityGroup


class Quality(MasterModel):
    name = CharField()
    name_eng = CharField()
    short_name = CharField()
    yomi = CharField()
    quality_group = ForeignKeyField(QualityGroup)

    @classmethod
    def get_qualities_grouped_by_quality_group(cls):
        return QualityGroup.get_qualities_grouped_by_quality_group()
