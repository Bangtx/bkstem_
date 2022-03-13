from peewee import BigIntegerField, ForeignKeyField, DateField, JOIN, fn
from playhouse.postgres_ext import DateTimeTZField
from .base import BaseModel
from .customer import Customer

# pylint: disable=no-member


class Order(BaseModel):
    pic = BigIntegerField()
    customer = ForeignKeyField(Customer)
    auction_date = DateField()
    sales_confirmed_by = BigIntegerField()
    sales_confirmed_at = DateTimeTZField()

    @classmethod
    def get_list(cls, auction_date=None, customer_id=None):
        from .order_detail import OrderDetail
        from .assignment import Assignment

        predicate = (cls.id == OrderDetail.order_id) & OrderDetail.active
        assignment_predicate = (
            OrderDetail.id == Assignment.order_detail_id
        ) & (Assignment.active)

        orders = (
            cls.select(
                cls,
                fn.SUM(fn.coalesce(OrderDetail.boxes, 0)).alias("total_boxes"),
                fn.SUM(
                    fn.coalesce(OrderDetail.price, 0)
                    * fn.coalesce(OrderDetail.boxes, 0)
                ).alias("total_amount"),
                fn.coalesce(
                    fn.SUM(
                        fn.coalesce(OrderDetail.price, 0)
                        * fn.coalesce(OrderDetail.boxes, 0)
                    ).filter(Assignment.id.is_null(False)),
                    0,
                ).alias("assign_amount"),
            )
            .join(OrderDetail, JOIN.LEFT_OUTER, on=predicate)
            .join(Assignment, JOIN.LEFT_OUTER, on=assignment_predicate)
            .where(cls.active)
            .group_by(cls.id)
            .order_by(cls.id.desc())
        )
        if auction_date:
            orders = orders.where(cls.auction_date == auction_date)

        if customer_id:
            orders = orders.where(cls.customer_id == customer_id)

        return list(orders)

    @classmethod
    def group_by_date(cls):
        """Get order information group by sales date"""
        from .order_detail import OrderDetail
        from .assignment import Assignment

        predicate = (cls.id == OrderDetail.order_id) & (OrderDetail.active)
        assignment_predicate = (
            OrderDetail.id == Assignment.order_detail_id
        ) & (Assignment.active)

        data = (
            cls.select(
                cls.auction_date,
                fn.SUM(fn.coalesce(OrderDetail.boxes, 0)).alias("total_boxes"),
                fn.SUM(fn.coalesce(OrderDetail.stems, 0)).alias("total_stems"),
                fn.SUM(fn.coalesce(Assignment.boxes, 0)).alias("assign_boxes"),
                fn.SUM(fn.coalesce(Assignment.stems, 0)).alias("assign_stems"),
            )
            .join(OrderDetail, JOIN.LEFT_OUTER, on=predicate)
            .join(Assignment, JOIN.LEFT_OUTER, on=assignment_predicate)
            .where(cls.active)
            .group_by(cls.auction_date)
            .order_by(cls.auction_date.desc())
        )
        return list(data)

    @classmethod
    def group_by_customer(cls, auction_date=None):
        """Get order information group by customer, filter by auction date"""
        from .order_detail import OrderDetail
        from .assignment import Assignment

        predicate = (cls.id == OrderDetail.order_id) & (OrderDetail.active)
        assignment_predicate = (
            OrderDetail.id == Assignment.order_detail_id
        ) & (Assignment.active)
        query = (
            cls.select(
                Customer.id,
                Customer.name,
                Customer.search_str,
                fn.ARRAY_AGG(fn.DISTINCT(cls.id)).alias("ids"),
                fn.SUM(fn.coalesce(OrderDetail.boxes, 0)).alias("total_boxes"),
                fn.SUM(fn.coalesce(OrderDetail.stems, 0)).alias("total_stems"),
                fn.SUM(fn.coalesce(Assignment.boxes, 0)).alias("assign_boxes"),
                fn.SUM(fn.coalesce(Assignment.stems, 0)).alias("assign_stems"),
            )
            .join(OrderDetail, JOIN.LEFT_OUTER, on=predicate)
            .join(Assignment, JOIN.LEFT_OUTER, on=assignment_predicate)
            .switch(cls)
            .join(Customer, on=(cls.customer == Customer.id))
            .where(cls.active)
            .order_by(cls.customer.desc())
        )
        if auction_date:
            query = query.where(cls.auction_date == auction_date)

        data = query.group_by(cls.customer_id, Customer.id, Customer.name)
        return list(data)

    def get_total_boxes(self):
        from .order_detail import OrderDetail

        details = OrderDetail.select(
            fn.coalesce(OrderDetail.boxes, 0).alias("boxes")
        ).where(OrderDetail.order_id == self.id, OrderDetail.active)
        total_boxes = 0
        for detail in details:
            total_boxes = total_boxes + detail.boxes
        return total_boxes

    @classmethod
    def get_full_orders_list_by_date(cls, auction_date):
        """Get order full information by auction date"""
        """Using in assign function"""

        """Get order's detail"""
        from .order_detail import OrderDetail
        from .color import Color
        from .unit import Unit
        from .size import Size
        from .variety import Variety
        from .quality import Quality
        from .item import Item
        from .assignment import Assignment

        orders = (
            cls.select(
                cls.id,
                cls.pic,
                cls.auction_date,
                fn.jsonb_build_object(
                    "id",
                    Customer.id,
                    "code",
                    Customer.code,
                    "name",
                    Customer.name,
                ).alias("customer"),
            )
            .join(Customer)
            .where(cls.auction_date == auction_date, cls.active)
        ).dicts()

        order_ids = [order["id"] for order in orders]

        detail_predicate = (
            OrderDetail.order_id.in_(order_ids) & OrderDetail.active
        )

        details_colors = (
            OrderDetail.select(
                OrderDetail.id,
                fn.array_agg(
                    fn.jsonb_build_object(
                        "id", Color.id, "code", Color.code, "name", Color.name
                    )
                ).alias("colors"),
            )
            .join(
                Color,
                JOIN.LEFT_OUTER,
                on=Color.id == fn.any(OrderDetail.color_ids),
            )
            .where(detail_predicate)
            .group_by(OrderDetail.id)
        )

        assignment_predicate = (
            Assignment.order_detail_id == OrderDetail.id
        ) & Assignment.active
        details_assigment_stems = (
            OrderDetail.select(
                OrderDetail.id,
                fn.SUM(fn.COALESCE(Assignment.stems, 0)).alias("assign_stems"),
            )
            .join(Assignment, JOIN.LEFT_OUTER, on=assignment_predicate)
            .where(detail_predicate)
            .group_by(OrderDetail.id, Assignment.order_detail)
        )

        order_details = (
            OrderDetail.select(
                OrderDetail.id,
                OrderDetail.order_id.alias("order_id"),
                OrderDetail.boxes,
                OrderDetail.stems,
                OrderDetail.remark,
                OrderDetail.is_lock,
                OrderDetail.price,
                details_colors.c.colors,
                details_assigment_stems.c.assign_stems,
                fn.jsonb_build_object("id", Size.id, "name", Size.name).alias(
                    "size"
                ),
                fn.jsonb_build_object("id", Unit.id, "name", Unit.name).alias(
                    "unit"
                ),
                fn.jsonb_build_object(
                    "id", Variety.id, "name", Variety.name
                ).alias("variety"),
                fn.jsonb_build_object(
                    "id", Quality.id, "name", Quality.name
                ).alias("quality"),
                fn.jsonb_build_object("id", Item.id, "name", Item.name).alias(
                    "item"
                ),
            )
            .join(details_colors, on=(details_colors.c.id == OrderDetail.id))
            .switch(OrderDetail)
            .join(
                details_assigment_stems,
                on=(details_assigment_stems.c.id == OrderDetail.id),
            )
            .switch(OrderDetail)
            .join(Unit, JOIN.LEFT_OUTER)
            .switch(OrderDetail)
            .join(Size, JOIN.LEFT_OUTER)
            .switch(OrderDetail)
            .join(Variety, JOIN.LEFT_OUTER)
            .switch(OrderDetail)
            .join(Quality, JOIN.LEFT_OUTER)
            .switch(OrderDetail)
            .join(Item, JOIN.LEFT_OUTER)
            .where(detail_predicate)
        ).dicts()

        for order in orders:
            details = [
                detail
                for detail in order_details
                if detail["order_id"] == order["id"]
            ]
            order["order_details"] = details

        return list(orders)
