from peewee import CharField, ForeignKeyField, BigIntegerField, fn, JOIN
from playhouse.postgres_ext import ArrayField
from .master import MasterModel
from .unit import Unit
from .size_group import SizeGroup
from .quality_group import QualityGroup


class Item(MasterModel):
    uuid = CharField()
    name = CharField()
    name_eng = CharField()
    yomi = CharField()
    short_name = CharField()
    default_unit = ForeignKeyField(
        Unit, column_name="default_unit", field="id", null=True
    )
    units = ArrayField(BigIntegerField)
    size_group = ForeignKeyField(
        SizeGroup, column_name="size_group_id", field="id", null=True
    )
    quality_group = ForeignKeyField(
        QualityGroup, column_name="quality_group_id", field="id", null=True
    )

    @classmethod
    def get_list(cls, has_order_num: bool = False, search_input: str = None):
        Units = Unit.alias()

        query = cls.select(
            cls,
            Unit.id,
            Unit.name,
            fn.COALESCE(
                fn.json_agg(
                    fn.jsonb_build_object(
                        "id", Units.id, "name", Units.name
                    )
                ).filter(Units.id.is_null(False)),
                "[]",
            ).alias("units"),
        ).join(Unit, JOIN.LEFT_OUTER, on=Unit.id == cls.default_unit).join(
            Units,
            JOIN.LEFT_OUTER,
            on=Units.id == fn.any(cls.units),
        ).where(cls.active).order_by(
            cls.order_num.asc(), cls.yomi.collate('"C"')
        ).group_by(cls.id, Unit.id, Unit.name)

        if has_order_num:
            query = query.where(cls.order_num.is_null(False))

        if search_input:
            query = query.where(cls.search_str.contains(search_input))

        items = query.execute()
        return items

    @classmethod
    def soft_delete(cls, item_id: int, deleted_by: int = None):
        from .variety import Variety

        varieties = Variety.get_varieties_by_item_id(item_id)

        for variety in varieties:
            Variety.soft_delete(variety.id, deleted_by)

        super().soft_delete(item_id, deleted_by)

    @classmethod
    def get_items_name_and_id_for_list_selecting(cls):
        items = cls.select(cls.id, cls.name).where(cls.active)
        return list(items)
