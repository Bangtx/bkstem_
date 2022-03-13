from peewee import CharField, SmallIntegerField, ForeignKeyField, BooleanField
from .base import BaseModel
from .customer import Customer


class CustomerInvoice(BaseModel):
    customer_id = ForeignKeyField(Customer)
    code = CharField()
    name = CharField()
    wholesaler_code = CharField()
    edi_version = SmallIntegerField()
    is_mode = BooleanField(default=False)
    is_chart = BooleanField(default=False)
    is_diff_list = BooleanField(default=False)
    form_type = SmallIntegerField()
    country_type = SmallIntegerField()
    packing_style_type = SmallIntegerField()
    offer_type = SmallIntegerField()
    order_note_type = SmallIntegerField()
    catalog_type = SmallIntegerField()
    desirable_price_type = SmallIntegerField()
    mark_type = SmallIntegerField()
    add_send_num_type = SmallIntegerField()

    class Meta:
        db_table = "customer_invoice"
