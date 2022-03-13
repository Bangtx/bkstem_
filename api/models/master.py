from .base import BaseModel
from peewee import BigIntegerField, CharField, fn
from utils.db import EXCLUDED, transaction
from datetime import datetime
from fastapi import HTTPException
from i18n import t


class MasterModel(BaseModel):
    order_num = BigIntegerField()
    search_str = CharField()

    @classmethod
    def get_list(cls):
        return list(
            cls.select()
            .where(cls.active)
            .order_by(cls.order_num.asc(), cls.yomi.collate('"C"'))
        )

    @classmethod
    def get_order_num(cls):
        first = (
            cls.select()
            .where(cls.active)
            .order_by(cls.order_num.desc())
            .first()
        )

        order_num = first.order_num + 1 if first and first.order_num else 1
        return order_num

    @classmethod
    @transaction
    def update_order_num(cls, rows: list):
        (
            cls.insert_many(
                rows,
                fields=[cls.id, cls.order_num],  # pylint: disable=no-member
            )
            .on_conflict(
                action="update",
                conflict_target=[cls.id],  # pylint: disable=no-member
                update={
                    cls.order_num: EXCLUDED.order_num,
                    cls.modified_at: datetime.now(),
                },
            )
            .execute()
        )
        return {"detail": f"Sort {cls.__name__}"}

    @classmethod
    def check_duplicate(cls, name: str, id=None):
        items = cls.select().where(
            cls.id != id, fn.lower(cls.name) == fn.lower(name), cls.active
        )
        if items:
            raise HTTPException(
                status_code=400,
                detail=t("fmbiz.master.errors.duplicate_name"),
            )
        return True

    @classmethod
    def gen_search_str(cls, **kwargs):
        params = []
        for key in kwargs:
            arg = kwargs.get(key)
            if arg:
                params.append(arg)

        params = set(params)
        search_str = "|".join(params)
        return search_str.lower()
