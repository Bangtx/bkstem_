from fastapi import HTTPException
from peewee import BigIntegerField, ForeignKeyField
from .master import MasterModel
from .item import Item
from .variety import Variety
from .size import Size
from .quality import Quality
from .unit import Unit
from i18n import t


class QuickInput(MasterModel):
    code = BigIntegerField()
    item = ForeignKeyField(Item)
    variety = ForeignKeyField(Variety, null=True)
    size = ForeignKeyField(Size, null=True)
    quality = ForeignKeyField(Quality, null=True)
    unit = ForeignKeyField(Unit, null=True)
    quantity = BigIntegerField()

    class Meta:
        db_table = "quick_input"

    @classmethod
    def get_list(cls):
        return list(cls.select().where(cls.active).order_by(cls.code.asc()))

    @classmethod
    def check_duplicate(cls, code: int, id=None):
        quick_input = cls.select().where(
            cls.id != id, cls.code == code, cls.active
        )
        if quick_input:
            raise HTTPException(
                status_code=400,
                detail=t("fmbiz.master.errors.duplicate_code"),
            )
        return True
