from peewee import FloatField, ForeignKeyField, DateField, fn, JOIN, CharField
from datetime import datetime

from .base import BaseModel
from .item import Item
from .size import Size
from .unit import Unit
from .variety import Variety
from .quality import Quality
from .color import Color


class HarvestResult(BaseModel):
    harvest_date = DateField()
    item = ForeignKeyField(Item)
    variety = ForeignKeyField(Variety)
    size = ForeignKeyField(Size, null=True)
    color = ForeignKeyField(Color, null=True)
    unit = ForeignKeyField(Unit)
    quality = ForeignKeyField(Quality, null=True)
    stems = FloatField()
    desired_price = FloatField()
    boxes = FloatField()
    quantity = FloatField()
    ordered_stems = FloatField()
    ordered_boxes = FloatField()
    remark = CharField()

    class Meta:
        db_table = "harvest_result"

    @classmethod
    def get_list(cls, start_date=None, end_date=None, harvest_date=None):

        harvest_results = (
            cls.select(
                cls.id,
                cls.harvest_date,
                cls.stems,
                cls.boxes,
                cls.created_at,
                cls.ordered_stems,
                cls.ordered_boxes,
                cls.remark,
                cls.desired_price,
                cls.quantity,
                fn.json_build_object(
                    "id",
                    Item.id,
                    "name",
                    Item.name,
                    "search_str",
                    Item.search_str,
                ).alias("item"),
                fn.json_build_object(
                    "id",
                    Variety.id,
                    "name",
                    Variety.name,
                    "search_str",
                    Variety.search_str,
                ).alias("variety"),
                fn.json_build_object(
                    "id",
                    Size.id,
                    "name",
                    Size.name,
                    "search_str",
                    Size.search_str,
                ).alias("size"),
                fn.json_build_object(
                    "id",
                    Unit.id,
                    "name",
                    Unit.name,
                    "search_str",
                    Unit.search_str,
                ).alias("unit"),
                fn.json_build_object(
                    "id",
                    Quality.id,
                    "name",
                    Quality.name,
                    "search_str",
                    Quality.search_str,
                ).alias("quality"),
                fn.json_build_object(
                    "id",
                    Color.id,
                    "name",
                    Color.name,
                    "code",
                    Color.code,
                ).alias("color"),
            )
            .join(Item, on=cls.item == Item.id)
            .join(Variety, on=cls.variety == Variety.id)
            .join(Size, JOIN.LEFT_OUTER, on=cls.size == Size.id)
            .join(Color, JOIN.LEFT_OUTER, on=cls.color == Color.id)
            .join(Unit, on=cls.unit == Unit.id)
            .join(Quality, JOIN.LEFT_OUTER, on=cls.quality == Quality.id)
            .where(cls.active)
            .order_by(
                Item.order_num.asc(),
                Item.yomi.collate('"C"'),
                Variety.order_num.asc(),
                Variety.yomi.collate('"C"'),
                cls.id.desc(),
            )
        )

        if start_date and end_date:
            harvest_results = harvest_results.where(
                cls.harvest_date >= start_date, cls.harvest_date <= end_date
            )

        if harvest_date:
            harvest_results = harvest_results.where(
                cls.harvest_date == harvest_date
            )

        return list(harvest_results.dicts())

    @classmethod
    def get_harvests(cls, ids, stems, boxes=None):
        order_stems = stems
        order_boxes = boxes if boxes else 0
        harvests = {}

        results = (
            cls.select(
                cls,
                (
                    fn.COALESCE(cls.boxes, 0)
                    - fn.COALESCE(cls.ordered_boxes, 0)
                ).alias("remain_boxes"),
                (cls.stems - fn.COALESCE(cls.ordered_stems, 0)).alias(
                    "remain_stems"
                ),
            )
            .where(cls.id.in_(ids), cls.active)
            .order_by(cls.id)
        )

        for result in results:
            if order_stems == 0:
                break

            if result.remain_stems > 0:
                ordered_stems = (
                    order_stems
                    if order_stems < int(result.remain_stems)
                    else int(result.remain_stems)
                )
                ordered_boxes = (
                    order_boxes
                    if order_boxes < int(result.remain_boxes)
                    else int(result.remain_boxes)
                )

                order_stems = order_stems - ordered_stems
                order_boxes = order_boxes - ordered_boxes

                # Update harvest result
                result.ordered_stems = (
                    int(result.ordered_stems) + ordered_stems
                    if result.ordered_stems
                    else ordered_stems
                )
                result.ordered_boxes = (
                    int(result.ordered_boxes) + ordered_boxes
                    if result.ordered_boxes
                    else ordered_boxes
                )
                result.modified_at = datetime.now()
                result.save()

                harvests[result.id] = {
                    "stems": ordered_stems,
                    "boxes": ordered_boxes,
                }

        return harvests

    @classmethod
    def update_harvest(cls, order_detail_id, stems, boxes=None):
        from .order_detail import OrderDetail

        order_detail = OrderDetail.get_by_id(order_detail_id)

        harvests = order_detail.harvests

        if not harvests:
            return harvests

        ids = list(harvests.keys())

        results = cls.select().where(cls.id.in_(ids)).order_by(cls.id)
        for result in results:
            key = str(result.id)

            ordered = harvests[key]
            result.ordered_stems = result.ordered_stems - ordered["stems"]
            result.ordered_boxes = result.ordered_boxes - ordered["boxes"]
            result.save()

        return cls.get_harvests(ids, stems, boxes)
