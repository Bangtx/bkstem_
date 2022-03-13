from peewee import (
    DateField,
    CharField,
    FloatField,
    fn,
    ForeignKeyField,
    JOIN,
    SQL,
    Case,
)
from playhouse.sqlite_ext import JSONField
from .item import Item
from .size import Size
from .boxtype import BoxType
from .unit import Unit
from .quality import Quality
from .variety import Variety
from .color import Color
from .base import BaseModel


class PackingResult(BaseModel):
    packed_date = DateField()
    item = ForeignKeyField(Item)
    variety = ForeignKeyField(Variety)
    size = ForeignKeyField(Size)
    unit = ForeignKeyField(Unit)
    color = ForeignKeyField(Color, null=True)
    box_type = ForeignKeyField(BoxType)
    quality = ForeignKeyField(Quality)
    quantity = FloatField()
    boxes = FloatField()
    total_stems = FloatField()
    search_str = CharField()
    desired_price = FloatField()
    breakdowns = JSONField()
    ordered_boxes = FloatField()
    ordered_stems = FloatField()
    assigned_boxes = FloatField()
    assigned_stems = FloatField()
    remark = CharField()

    class Meta:
        db_table = "packing_result"

    @classmethod
    def get_packing_result(cls, id):
        from .assignment import Assignment
        from .order_type import OrderType
        from .customer import Customer

        query = (
            cls.select(
                cls,
                fn.COALESCE(
                    fn.array_agg(fn.json_build_object(
                        'id', Assignment.id,
                        'auction_date', Assignment.auction_date,
                        'order_type', fn.json_build_object(
                            'id', OrderType.id,
                            'name', OrderType.name,
                        ),
                        'customer', fn.json_build_object(
                            'id', Customer.id,
                            'name', Customer.name,
                        ),
                        'buyer_info', Assignment.buyer_info,
                        'boxes', Assignment.boxes,
                        'stems', Assignment.stems,
                        'price', Assignment.price,
                        'amount', Assignment.amount
                    ))
                        .order_by(Assignment.id.asc())
                        .filter(Assignment.id.is_null(False)),
                    "{}",
                ).alias('assignments')
            )
            .where(cls.active & (cls.id == id))
            .join(
                Assignment,
                JOIN.LEFT_OUTER,
                on=(cls.id == Assignment.packing_result_id) & Assignment.active,
            )
            .join(
                Customer,
                JOIN.LEFT_OUTER,
                on=(Assignment.customer_id == Customer.id) & Customer.active,
            )
            .join(
                OrderType,
                JOIN.LEFT_OUTER,
                on=(Assignment.order_type_id == OrderType.id) & OrderType.active,
            )
            .group_by(cls.id)
        )

        result = list(query)

        if len(result):
            return result[0]

        return None

    @classmethod
    def get_packing_result_by_date(cls, packed_date):
        from .assignment import Assignment

        query = (
            cls.select(
                cls,
                fn.SUM(fn.COALESCE(Assignment.boxes, 0)).alias("assign_boxes"),
                fn.SUM(fn.COALESCE(Assignment.stems, 0)).alias("assign_stems"),
                cls.total_stems,
            )
            .where((cls.packed_date == packed_date), cls.active)
            .join(
                Assignment,
                JOIN.LEFT_OUTER,
                on=(cls.id == Assignment.packing_result_id) & Assignment.active,
            )
            .group_by(cls.id, Assignment.packing_result)
        )

        return list(query)

    @classmethod
    def get_packing_result_by_range(
        cls, start_date, end_date, get_assignment: bool = True
    ):
        from .assignment import Assignment

        query = (
            cls.select(
                cls.id,
                cls.packed_date,
                cls.quantity,
                cls.boxes,
                cls.total_stems,
                cls.search_str,
                cls.desired_price,
                cls.breakdowns,
                cls.ordered_boxes,
                cls.ordered_stems,
                cls.assigned_boxes,
                cls.assigned_stems,
                cls.remark,
                fn.json_build_object("id", Item.id, "name", Item.name).alias(
                    "item"
                ),
                fn.json_build_object(
                    "id", Variety.id, "name", Variety.name
                ).alias("variety"),
                fn.jsonb_build_object(
                    "id", Color.id, "name", Color.name, "code", Color.code
                ).alias("color"),
                fn.jsonb_build_object("id", Size.id, "name", Size.name).alias(
                    "size"
                ),
                fn.jsonb_build_object("id", Unit.id, "name", Unit.name).alias(
                    "unit"
                ),
                fn.jsonb_build_object(
                    "id", BoxType.id, "name", BoxType.name
                ).alias("box_type"),
                fn.jsonb_build_object(
                    "id", Quality.id, "name", Quality.name
                ).alias("quality"),
                fn.jsonb_build_object(
                    "id", Quality.id, "name", Quality.name
                ).alias("quality"),
            )
            .where(cls.active)
            .join(Item, on=(cls.item == Item.id) & Item.active)
            .join(Variety, on=(cls.variety == Variety.id) & Variety.active)
            .join(Size, on=(cls.size == Size.id) & Size.active)
            .join(Unit, on=(cls.unit == Unit.id) & Unit.active)
            .join(Quality, on=(cls.quality == Quality.id) & Quality.active)
            .join(BoxType, on=(cls.box_type == BoxType.id) & BoxType.active)
            .join(
                Color,
                JOIN.LEFT_OUTER,
                on=(cls.color == Color.id) & Color.active,
            )
            .order_by(
                Item.order_num.asc(),
                Item.yomi.collate('"C"'),
                Variety.order_num.asc(),
                Variety.yomi.collate('"C"'),
                cls.id.desc(),
            )
        )
        if end_date:
            query = query.where(cls.packed_date.between(start_date, end_date))
        else:
            query = query.where(cls.packed_date >= start_date)

        if get_assignment:
            query = (
                query.select_extend(
                    fn.SUM(fn.COALESCE(Assignment.boxes, 0)).alias(
                        "assign_boxes"
                    ),
                    fn.SUM(fn.COALESCE(Assignment.stems, 0)).alias(
                        "assign_stems"
                    ),
                )
                .join(
                    Assignment,
                    JOIN.LEFT_OUTER,
                    on=(cls.id == Assignment.packing_result_id)
                    & Assignment.active,
                )
                .group_by(
                    cls.id,
                    Assignment.packing_result,
                    Item.id,
                    Variety.id,
                    Size.id,
                    Unit.id,
                    Quality.id,
                    BoxType.id,
                    Color.id,
                )
            )

        return list(query.dicts())

    @classmethod
    def gen_search_str(cls, packing_result: dict):
        from .quality import Quality

        quality_query = (
            Quality.select(Quality.search_str)
            .where(packing_result.quality_id == Quality.id, Quality.active)
            .get()
        )
        from .variety import Variety

        variety_query = (
            Variety.select(Variety.search_str)
            .where(packing_result.variety_id == Variety.id, Variety.active)
            .get()
        )

        from .item import Item

        item_query = (
            Item.select(Item.search_str)
            .where(packing_result.item_id == Item.id, Item.active)
            .get()
        )

        from .size import Size

        size_query = (
            Size.select(Size.search_str)
            .where(packing_result.size_id == Size.id, Size.active)
            .get()
        )

        from .unit import Unit

        unit_query = (
            Unit.select(Unit.search_str)
            .where(packing_result.unit_id == Unit.id, Unit.active)
            .get()
        )

        color_name = ''
        if packing_result.color_id:
            from .color import Color

            color_query = (
                Color.select(Color.name)
                .where(packing_result.color_id == Color.id, Color.active)
                .get()
            )
            color_name = color_query.name

        search_dict = (
            packing_result.packed_date,
            quality_query.search_str,
            variety_query.search_str,
            item_query.search_str,
            size_query.search_str,
            unit_query.search_str,
            color_name,
        )

        search_str = ""
        for param in search_dict:
            if param and param is not None:
                search_str += str(param) + "|"

        return search_str

    @classmethod
    def get_packing_result_for_auto_assign(cls, start_date, end_date):
        from .assignment import Assignment

        query = (
            cls.select(
                cls,
                (
                    cls.total_stems - fn.SUM(fn.COALESCE(Assignment.stems, 0))
                ).alias("remain_stems"),
            )
            .join(
                Assignment,
                JOIN.LEFT_OUTER,
                on=(
                    (cls.id == Assignment.packing_result_id)
                    & (Assignment.active.__eq__(True))
                ),
            )
            .where(cls.active, cls.packed_date.between(start_date, end_date))
            .group_by(cls.id)
            .order_by(cls.created_at.desc())
            .having(
                cls.total_stems - fn.SUM(fn.COALESCE(Assignment.stems, 0)) > 0
            )
            .dicts()
        )

        return list(query)
