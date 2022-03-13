from peewee import CharField, ForeignKeyField
from .master import MasterModel
from .size_group import SizeGroup


class Size(MasterModel):
    name = CharField()
    name_eng = CharField()
    yomi = CharField()
    short_name = CharField()
    size_group = ForeignKeyField(SizeGroup)

    @classmethod
    def get_sizes_grouped_by_size_group(cls):
        return SizeGroup.get_sizes_grouped_by_size_group()
