from fastapi import HTTPException
from peewee import CharField
from i18n import t
from .master import MasterModel


class Customer(MasterModel):
    name = CharField()
    yomi = CharField()
    short_name = CharField()
    tel = CharField()
    fax = CharField()
    email = CharField()
    code = CharField()
    zip_code = CharField()
    address_1 = CharField()
    address_2 = CharField()
    default_invoice_method = CharField()
    allow_pre_sale = CharField()
    level_customer = CharField()
    @classmethod
    def check_used_in_order(cls, id: int):
        from .order import Order

        orders = Order.select().where(Order.customer == id, Order.active)

        def get_mess(entity: str, ids: str):
            return t(
                "fmbiz.master.errors.can_not_delete",
                table="customer",
                entity=entity,
                ids=ids,
            )

        error_mess = []
        if orders:
            order_ids = ", ".join([str(order.id) for order in orders])
            error_mess.append(get_mess("Order", order_ids))

        if error_mess:
            raise HTTPException(status_code=400, detail=error_mess)

        return True
