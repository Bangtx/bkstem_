from peewee import (
    BigIntegerField,
    BooleanField,
    FloatField,
    ForeignKeyField,
    CharField,
    fn,
    DoesNotExist,
    JOIN,
)
from playhouse.postgres_ext import ArrayField, JSONField
from fastapi import HTTPException
from pydash import order_by

from .base import BaseModel
from .order import Order
from .item import Item
from .size import Size
from .unit import Unit
from .variety import Variety
from .order_type import OrderType
from .quality import Quality
from .customer import Customer


class OrderDetail(BaseModel):
    order = ForeignKeyField(Order, null=True, backref="order_details")
    item = ForeignKeyField(Item)
    variety = ForeignKeyField(Variety, null=True)
    size = ForeignKeyField(Size, null=True)
    color_ids = ArrayField(BigIntegerField)
    unit = ForeignKeyField(Unit, null=True)
    quality = ForeignKeyField(Quality, null=True)
    order_type = ForeignKeyField(OrderType, null=True)
    quantity = FloatField()
    boxes = FloatField()
    stems = FloatField()
    price = FloatField()
    amount = FloatField()
    buyer_info = CharField()
    remark = CharField()
    is_special = BooleanField(default=False)
    is_lock = BooleanField(default=False)
    is_assigned = BooleanField(default=False)
    harvests = JSONField()

    class Meta:
        db_table = "order_detail"

    @classmethod
    def get_list(
        cls,
        order_id: int = None,
        variety_id: str = None,
        auction_date=None,
        start_date=None,
        end_date=None,
        detail_ids: str = None,
        get_assignment: bool = True,
    ):
        from .customer import Customer
        from .assignment import Assignment

        # pylint: disable=no-member

        details = (
            cls.select(
                cls.id,
                cls.quantity,
                cls.boxes,
                cls.stems,
                cls.remark,
                cls.is_special,
                cls.price,
                cls.buyer_info,
                cls.color_ids,
                cls.is_lock,
                cls.is_assigned,
                fn.jsonb_build_object("id", Item.id, "name", Item.name).alias(
                    "item"
                ),
                fn.jsonb_build_object(
                    "id", Variety.id, "name", Variety.name
                ).alias("variety"),
                fn.jsonb_build_object("id", Size.id, "name", Size.name).alias(
                    "size"
                ),
                fn.jsonb_build_object("id", Unit.id, "name", Unit.name).alias(
                    "unit"
                ),
                fn.jsonb_build_object(
                    "id", Quality.id, "name", Quality.name
                ).alias("quality"),
                fn.jsonb_build_object(
                    "id", OrderType.id, "name", OrderType.name
                ).alias("order_type"),
                fn.jsonb_build_object(
                    "id", Quality.id, "name", Quality.name
                ).alias("quality"),
                fn.jsonb_build_object(
                    "id",
                    Order.id,
                    "auction_date",
                    Order.auction_date,
                    "customer",
                    fn.jsonb_build_object(
                        "id",
                        Customer.id,
                        "name",
                        Customer.name,
                        "code",
                        Customer.code,
                    ),
                ).alias("order"),
            )
            .join(Order, on=Order.id == cls.order)
            .join(Customer, on=Order.customer == Customer.id)
            .join(Item, on=cls.item == Item.id)
            .join(Variety, JOIN.LEFT_OUTER, on=cls.variety == Variety.id)
            .join(Size, JOIN.LEFT_OUTER, on=cls.size == Size.id)
            .join(Unit, JOIN.LEFT_OUTER, on=cls.unit == Unit.id)
            .join(Quality, JOIN.LEFT_OUTER, on=cls.quality == Quality.id)
            .join(OrderType, JOIN.LEFT_OUTER, on=cls.order_type == OrderType.id)
            .where(cls.active)
            .order_by(
                Item.order_num.asc(),
                Item.yomi.collate('"C"'),
                Variety.order_num.asc(),
                Variety.yomi.collate('"C"'),
                cls.id.desc(),
            )
        )

        if order_id:
            details = details.where(cls.order == order_id)
        if variety_id:
            details = details.where(cls.variety == variety_id)
        if auction_date:
            details = details.where(Order.auction_date == auction_date)
        if start_date and end_date:
            details = details.where(
                Order.auction_date >= start_date, Order.auction_date <= end_date
            )
        if detail_ids:
            ids = detail_ids.split(",")
            if len(ids) > 0:
                details = details.where(
                    OrderDetail.id.in_(ids)
                )
        if get_assignment:
            details = (
                details.select_extend(
                    fn.SUM(fn.COALESCE(Assignment.stems, 0)).alias(
                        "assign_stems"
                    ),
                    fn.SUM(fn.COALESCE(Assignment.boxes, 0)).alias(
                        "assign_boxes"
                    ),
                )
                .join(
                    Assignment,
                    JOIN.LEFT_OUTER,
                    on=(
                        (cls.id == Assignment.order_detail)
                        & Assignment.active.__eq__(True)
                    ),
                )
                .group_by(
                    cls.id,
                    Order.id,
                    Customer.id,
                    Item.id,
                    Variety.id,
                    Size.id,
                    Unit.id,
                    Quality.id,
                    OrderType.id,
                )
            )

        return list(details.dicts())

    @classmethod
    def get_by_harvest(cls, harvest_ids):
        """
        Get order detail information by harvest result id
        """

        from .assignment import Assignment
        from .customer import Customer

        # pylint: disable=no-member

        order_details = cls.select(
            cls.id, fn.json_object_keys(cls.harvests).alias("harvest_id")
        )

        details = (
            cls.select(cls.id)
            .join(order_details, on=cls.id == order_details.c.id)
            .where(order_details.c.harvest_id.cast("int").in_(harvest_ids))
            .group_by(cls.id)
            .dicts()
        )

        ids = [detail["id"] for detail in details]

        predicate = (cls.id == Assignment.order_detail_id) & (Assignment.active)
        query = (
            cls.select(
                cls.id,
                cls.stems,
                Customer.id.alias("customer_id"),
                Customer.name.alias("customer_name"),
                Customer.code.alias("customer_code"),
                Order.auction_date,
                fn.SUM(fn.coalesce(Assignment.stems, 0)).alias("assign_stems"),
            )
            .join(Assignment, JOIN.LEFT_OUTER, on=predicate)
            .join(Order, JOIN.INNER, on=(cls.order == Order.id))
            .join(Customer, on=Order.customer == Customer.id)
            .where(cls.active, cls.id.in_(ids))
            .group_by(cls.id, Customer.id, Order.id)
            .dicts()
        )

        return list(query)

    @classmethod
    def check_order_detail_legal(cls, id: int):
        try:
            data = cls.get_by_id(id)
            order = Order.select().where(
                Order.id == data.order_id, Order.active
            )
            if not order:
                raise HTTPException(status_code=404, detail="Order not exist")
            return order.exists()
        except DoesNotExist:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )

    @classmethod
    def get_order_detail_for_auto_assign(cls, auction_date, order_detail_ids, order_type_ids = None):
        from .customer import Customer
        from .assignment import Assignment

        query = (
            cls.select(
                cls,
                Customer.id.alias("customer_id"),
                (cls.stems - fn.SUM(fn.COALESCE(Assignment.stems, 0))).alias(
                    "remain_stems"
                ),
            )
            .join(Order, JOIN.INNER, on=(cls.order == Order.id))
            .join(Customer, on=Order.customer == Customer.id)
            .join(
                Assignment,
                JOIN.LEFT_OUTER,
                on=(
                    (cls.id == Assignment.order_detail_id)
                    & (Assignment.active.__eq__(True))
                ),
            )
            .where(
                cls.active,
                cls.is_assigned.__eq__(False),
                cls.is_special == False,
                Order.active,
                Order.auction_date == auction_date
            )
            .group_by(cls.id, Customer.id)
            .having(cls.stems - fn.SUM(fn.COALESCE(Assignment.stems, 0)) > 0)
        )
        if order_type_ids is not None:
            query = query.where(cls.order_type.in_(order_type_ids))
        if order_detail_ids is not None:
            query = query.where(cls.id.in_(order_detail_ids))
        query = query.dicts()

        return list(query)

    @classmethod
    def get_remain_stems(cls, id):
        from .assignment import Assignment

        query = (
            cls.select(
                (cls.stems - fn.SUM(fn.COALESCE(Assignment.stems, 0))).alias(
                    "remain_stems"
                ),
            )
            .join(Order, JOIN.INNER, on=(cls.order == Order.id))
            .join(
                Assignment,
                JOIN.LEFT_OUTER,
                on=(
                    (cls.id == Assignment.order_detail_id)
                    & (Assignment.active.__eq__(True))
                ),
            )
            .where(
                cls.id == id,
                cls.active,
                cls.is_assigned.__eq__(False),
                Order.active
            )
            .group_by(cls.id)
        )
        query = query.dicts()

        return list(query)

    @classmethod
    def check_merge(cls, order_detail_and_order):
        query = list(
            cls.select(
                cls,
                Item.name.alias("item_name"),
                Variety.name.alias("variety_name"),
                Quality.name.alias("quality_name"),
                Size.name.alias("size_name"),
            )
            .join(Item, on=(Item.id == cls.item))
            .join(Variety, JOIN.LEFT_OUTER, on=(Variety.id == cls.variety))
            .join(Quality, JOIN.LEFT_OUTER, on=(Quality.id == cls.quality))
            .join(Size, JOIN.LEFT_OUTER, on=(Size.id == cls.size))
            .where(
                cls.id != order_detail_and_order.detail_id,
                cls.item == order_detail_and_order.item_id,
                cls.variety == order_detail_and_order.variety_id,
                cls.size == order_detail_and_order.size_id,
                cls.quality == order_detail_and_order.quality_id,
                cls.quantity == order_detail_and_order.quantity,
                cls.color_ids == order_detail_and_order.color_ids,
                cls.unit == order_detail_and_order.unit_id,
                cls.buyer_info == order_detail_and_order.buyer_info,
                cls.order_type == order_detail_and_order.order_type_id,
                cls.price == order_detail_and_order.price,
                cls.is_special == order_detail_and_order.is_special,
                cls.active,
            )
            .dicts()
            .execute()
        )
        # print(query)
        if query:
            order_ids = list(map(lambda x: x["order"], query))
            order_data = list(
                Order.select(
                    Order.id.alias("order_id"),
                    Order.customer.alias("customer_id"),
                    Customer.name.alias("customer_name"),
                    Order.auction_date,
                )
                .join(
                    Customer,
                    JOIN.LEFT_OUTER,
                    on=(Order.customer == Customer.id),
                )
                .where(Order.id << order_ids, Order.active)
                .dicts()
            )
            if order_data:
                order_data = list(
                    filter(
                        lambda x: x["customer_id"]
                                  == order_detail_and_order.customer_id
                                  and str(x["auction_date"])
                                  == str(order_detail_and_order.auction_date),
                        order_data,
                    )
                )
                if order_data:
                    return {
                        "id": query[0]["id"],
                        "itemName": query[0]["item_name"],
                        "variety_name": query[0]["variety_name"],
                        "quality_size_name": str(query[0]["quality_name"])
                        + str(query[0]["size_name"]),
                        "stems": query[0]["stems"],
                        "boxes": query[0]["boxes"],
                        "order_id": order_data[0]["order_id"],
                        "customer_id": order_data[0]["customer_id"],
                        "customer_name": order_data[0]["customer_name"],
                        "auction_date": str(order_data[0]["auction_date"]),
                    }
        return {
            "id": None,
            "itemName": None,
            "variety_name": None,
            "quality_size_name": None,
            "stems": None,
            "boxes": None,
            "order_id": None,
            "customer_id": None,
            "customer_name": None,
        }
