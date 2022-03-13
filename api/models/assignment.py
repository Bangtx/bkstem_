from fastapi import HTTPException
from peewee import (
    FloatField,
    ForeignKeyField,
    BigIntegerField,
    CharField,
    DateField,
    JOIN,
    fn,
)
from playhouse.postgres_ext import ArrayField
from playhouse.sqlite_ext import JSONField
# from wheel.cli.pack import pack

from .base import BaseModel
from .packing_result import PackingResult
from .harvest_result import HarvestResult
from .order_detail import OrderDetail
from .item import Item
from .size import Size
from .unit import Unit
from .variety import Variety
from .order_type import OrderType
from .quality import Quality
from .customer import Customer
from .boxtype import BoxType
from i18n import t


class Assignment(BaseModel):
    packing_result = ForeignKeyField(PackingResult, null=True)
    harvest_result = ForeignKeyField(HarvestResult, null=True)
    order_detail = ForeignKeyField(OrderDetail, null=True)
    customer = ForeignKeyField(Customer)
    auction_date = DateField()
    item = ForeignKeyField(Item)
    variety = ForeignKeyField(Variety)
    size = ForeignKeyField(Size, null=True)
    unit = ForeignKeyField(Unit, null=True)
    quality = ForeignKeyField(Quality, null=True)
    order_type = ForeignKeyField(OrderType, null=True)
    box_type = ForeignKeyField(BoxType)
    quantity = FloatField()
    color_ids = ArrayField(BigIntegerField)
    price = FloatField()
    amount = FloatField()
    boxes = FloatField()
    stems = FloatField()
    buyer_info = CharField()
    remark = CharField()
    breakdowns = JSONField()

    class Meta:
        db_table = "assignment"

    @classmethod
    def get_list(
            cls,
            auction_date=None,
            start_date=None,
            end_date=None,
            is_filter_has_order_detail=False
    ):
        assignments = (
            cls.select(
                cls.id,
                cls.auction_date,
                cls.color_ids,
                cls.stems,
                cls.quantity,
                cls.boxes,
                cls.packing_result_id,
                cls.order_detail_id,
                fn.json_build_object(
                    "id",
                    Item.id,
                    "name",
                    Item.name,
                ).alias("item"),
                fn.json_build_object(
                    "id",
                    Variety.id,
                    "name",
                    Variety.name,
                ).alias("variety"),
                fn.json_build_object(
                    "id",
                    Size.id,
                    "name",
                    Size.name,
                ).alias("size"),
                fn.json_build_object(
                    "id",
                    Unit.id,
                    "name",
                    Unit.name,
                ).alias("unit"),
                fn.json_build_object(
                    "id",
                    Quality.id,
                    "name",
                    Quality.name,
                ).alias("quality"),
                fn.json_build_object(
                    "id",
                    Customer.id,
                    "name",
                    Customer.name,
                    "code",
                    Customer.code,
                ).alias("customer"),
                fn.json_build_object(
                    "id",
                    OrderType.id,
                    "name",
                    OrderType.name,
                ).alias("order_type"),
                fn.json_build_object(
                    "id",
                    BoxType.id,
                    "name",
                    BoxType.name,
                ).alias("box_type"),
            )
            .join(Item, on=cls.item == Item.id)
            .join(Variety, on=cls.variety == Variety.id)
            .join(Size, JOIN.LEFT_OUTER, on=cls.size == Size.id)
            .join(Unit, JOIN.LEFT_OUTER, on=cls.unit == Unit.id)
            .join(Quality, JOIN.LEFT_OUTER, on=cls.quality == Quality.id)
            .join(BoxType, JOIN.LEFT_OUTER, on=cls.box_type == BoxType.id)
            .join(OrderType, JOIN.LEFT_OUTER, on=cls.order_type == OrderType.id)
            .join(Customer, JOIN.LEFT_OUTER, on=cls.customer == Customer.id)
            .where(cls.active)
            .order_by(
                Item.order_num.asc(),
                Item.yomi.collate('"C"'),
                Variety.order_num.asc(),
                Variety.yomi.collate('"C"'),
                cls.id.desc(),
            )
        )

        if auction_date:
            assignments = assignments.where(cls.auction_date == auction_date)
        if start_date and end_date:
            assignments = assignments.where(
                cls.auction_date >= start_date, cls.auction_date <= end_date
            )
        if is_filter_has_order_detail:
            assignments = assignments.where(cls.order_detail_id != None)

        return list(assignments.dicts())

    @classmethod
    def batch_assign(cls, data):
        # pylint: disable=no-member

        from .order import Order
        from .customer import Customer

        assignment = data["assignment"]

        if assignment["quantity"] == 0:
            return

        order_details = (
            OrderDetail.select(
                OrderDetail,
                Customer.id.alias("customer_id"),
            )
            .join(Order)
            .join(Customer, on=Order.customer == Customer.id)
            .where(
                OrderDetail.id.in_(data["order_detail_ids"]),
                OrderDetail.active,
                OrderDetail.is_assigned.__eq__(False),
            )
            .dicts()
        )

        insert_data = []
        details = [
            detail
            for detail in order_details
            if detail["stems"] % assignment["quantity"] == 0
        ]

        for detail in details:
            assign_data = assignment.copy()
            assign_data["order_detail_id"] = detail["id"]
            assign_data["customer_id"] = detail["customer_id"]
            assign_data["buyer_info"] = detail["buyer_info"]
            assign_data["stems"] = detail["stems"]
            assign_data["boxes"] = assign_data["stems"] / assignment["quantity"]

            insert_data.append(assign_data)

        cls.insert_many(insert_data).execute()

        return {"ids": [detail["id"] for detail in details]}

    @classmethod
    def auto_assign(cls, param):
        auction_date = param["auction_date"]
        order_type_ids = param["order_type_ids"]
        order_detail_ids = param["order_detail_ids"]

        order_details = OrderDetail.get_order_detail_for_auto_assign(
            auction_date, order_detail_ids, order_type_ids
        )

        packing_results = PackingResult.get_packing_result_for_auto_assign(
            param["start_date"], param["end_date"]
        )

        # for calculate assigned order
        order_assigned = []
        assigments = []
        order_not_enough = []
        for order_detail in order_details:
            for packing_result in packing_results:
                # remove this packing result if it is fully assigned
                if packing_result["remain_stems"] == 0:
                    continue

                if cls.compare_for_auto_assign(order_detail, packing_result):
                    stems = (
                        order_detail["remain_stems"]
                        if order_detail["remain_stems"]
                        <= packing_result["remain_stems"]
                        else packing_result["remain_stems"]
                    )

                    price = (
                        order_detail["price"]
                        if order_detail["price"] is not None
                        else packing_result["desired_price"]
                    )
                    if price is not None:
                        amount = int(price) * int(stems)
                    else:
                        amount = None

                    # Save to DB
                    assignment_create_body = {
                        "auction_date": auction_date,
                        "buyer_info": order_detail["buyer_info"],
                        "customer": order_detail["customer_id"],
                        "order_detail": order_detail["id"],
                        "packing_result": packing_result["id"],
                        "item": order_detail["item"],
                        "variety": order_detail["variety"],
                        "size": order_detail["size"],
                        "unit": order_detail["unit"],
                        "quality": order_detail["quality"],
                        "quantity": order_detail["quantity"],
                        "order_type": order_detail["order_type"],
                        "box_type": packing_result["box_type"],
                        "color_ids": order_detail["color_ids"],
                        "boxes": float(stems) / packing_result["quantity"],
                        "stems": stems,
                        "remark": order_detail["remark"],
                        "price": price,
                        "amount": amount,
                    }
                    assigments.append(assignment_create_body)

                    order_detail["remain_stems"] = (
                        order_detail["remain_stems"] - stems
                    )

                    packing_result["remain_stems"] = (
                        packing_result["remain_stems"] - stems
                    )

                    new_packing_data = list(
                        PackingResult.select(
                            PackingResult.assigned_boxes,
                            PackingResult.assigned_stems
                        ).where(
                            PackingResult.id == packing_result['id']
                        ).dicts()
                    )
                    new_packing_data = new_packing_data[0]

                    PackingResult.update(
                        assigned_boxes=float(stems)/packing_result["quantity"]+float(new_packing_data['assigned_boxes']),
                        assigned_stems=float(stems) + float(new_packing_data['assigned_stems'])
                    ).where(
                        PackingResult.id == packing_result['id']
                    ).execute()
                    # skipped if this order_detail is fully assigned
                    if order_detail["remain_stems"] == 0:
                        order_assigned.append(order_detail["id"])
                        break
                    else:
                        order_not_enough.append(order_detail["id"])

        if assigments:
            cls.insert_many(assigments).execute()

        if order_assigned:
            query = OrderDetail.update(is_assigned=True).where(
                OrderDetail.id.in_(order_assigned)
            )
            query.execute()

        return {
            "assigned_order": len(order_assigned),
            "assign_inserted": len(assigments),
            "order": len(order_details),
            "order_not_enough": order_not_enough
        }

    @classmethod
    def compare_for_auto_assign(cls, order_detail, packing_result):
        if (
            order_detail["item"] is None
            or order_detail["variety"] is None
            or order_detail["size"] is None
            or order_detail["quality"] is None
            or order_detail["unit"] is None
        ):
            return False
        # check property existed in packing_result
        if (
            packing_result["item"] is None
            or packing_result["variety"] is None
            or packing_result["size"] is None
            or packing_result["quantity"] is None
            or (
                order_detail["color_ids"] and packing_result["color"] is None
            )
            or packing_result["quality"] is None
            or packing_result["unit"] is None
        ):
            return False
        # check if info in order_detail is match with info in packing_result
        # for model object, should use its id
        if (
            order_detail["item"] == packing_result["item"]
            and order_detail["variety"] == packing_result["variety"]
            and order_detail["size"] == packing_result["size"]
            and order_detail['stems'] % packing_result['quantity'] == 0
            and (
                not order_detail['color_ids']
                or (
                    packing_result['color']
                    in order_detail['color_ids']
                )
            )
            # and packing_result["color"] in order_detail["color_ids"]
            and order_detail["quality"] == packing_result["quality"]
            and order_detail["unit"] == packing_result["unit"]
        ):
            return True

        return False

    @classmethod
    def get_id_assign_seri_from_packing(cls, auction_date, packing_result_id, customer_id):
        query = cls.select(cls.id).where(
            cls.active,
            cls.auction_date.__eq__(auction_date),
            cls.packing_result_id.__eq__(packing_result_id),
            cls.customer_id.__eq__(customer_id)
        )
        query = query.dicts()

        return list(query)
