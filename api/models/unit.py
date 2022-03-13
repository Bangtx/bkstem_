from fastapi import HTTPException
from i18n import t
from peewee import CharField
from .master import MasterModel


class Unit(MasterModel):
    name = CharField()
    yomi = CharField()
    short_name = CharField()

    @classmethod
    def check_used_in_item(cls, unit_id):
        from .item import Item

        items = Item.select().where(Item.default_unit == unit_id, Item.active)

        def get_mess(entity: str, ids: str):
            return t(
                "fmbiz.master.errors.can_not_delete",
                table="unit",
                entity=entity,
                ids=ids,
            )

        error_mess = []
        if items:
            item_ids = ", ".join([str(item.id) for item in items])

            error_mess.append(get_mess("Item", item_ids))

        if error_mess:
            raise HTTPException(status_code=400, detail=error_mess)
        return True
