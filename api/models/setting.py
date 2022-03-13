from datetime import datetime
from typing import List

from config.database import db
from fastapi import HTTPException
from peewee import Model
from peewee import BigIntegerField, CharField, DoesNotExist
from playhouse.postgres_ext import DateTimeTZField
from playhouse.shortcuts import model_to_dict


class SettingModel(Model):
    key = CharField()
    value = CharField()
    created_at = DateTimeTZField(default=datetime.now)
    created_by = BigIntegerField()
    modified_at = DateTimeTZField()
    modified_by = BigIntegerField()

    class Meta:
        database = db
        db_table = "setting"

    @classmethod
    def get_setting_by_key(cls, key: str):
        try:
            result = cls.select().where(cls.key == key).get()
            result_dict = model_to_dict(
                result
            )  # model to dictionary type (obj)
            result_value = result_dict.get("value")
            return {
                "id": result_dict["id"],
                "value": list(
                    result_value.split(",")
                ),  # change type: string -> list
            }
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Not Found")

    @classmethod
    def update_setting_by_id(cls, id: int, data: dict):
        # data to update to db: dict {data: dict -> string}
        update_data = {"value": ",".join(data["value"])}
        try:
            cls.update(**update_data, modified_at=datetime.now()).where(
                cls.id == id
            ).execute()
            auction_date = model_to_dict(cls.get_by_id(id))
            return {
                "id": auction_date["id"],
                "value": list(auction_date["value"].split(",")),
            }
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Not Found")
