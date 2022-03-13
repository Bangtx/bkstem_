from peewee import Model, BooleanField, BigIntegerField
from playhouse.postgres_ext import DateTimeTZField
from config.database import db
from datetime import datetime
from peewee import DoesNotExist
from fastapi import HTTPException


class BaseModel(Model):
    created_at = DateTimeTZField(default=datetime.now)
    created_by = BigIntegerField()
    modified_at = DateTimeTZField()
    modified_by = BigIntegerField()
    deleted_at = DateTimeTZField()
    deleted_by = BigIntegerField()
    active = BooleanField(default=True)

    class Meta:
        database = db

    @classmethod
    def get_one(cls, id: int):
        try:
            data = cls.get_by_id(id)
            if data.active is False:
                raise HTTPException(
                    status_code=404, detail=f"{cls.__name__} not found"
                )
            return data
        except DoesNotExist:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )

    @classmethod
    def get_list(cls):
        return list(cls.select().where(cls.active))

    @classmethod
    def update_one(cls, id: int, data_update: dict):
        try:
            query = cls.update(**data_update, modified_at=datetime.now()).where(
                cls.id == id
            )
            query.execute()

            data = cls.get_by_id(id)
            return data
        except DoesNotExist:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )

    @classmethod
    def soft_delete(cls, id: int, deleted_by: int = None):
        try:
            data = cls.get_by_id(id)
            data.active = False
            data.deleted_at = datetime.now()
            data.deleted_by = deleted_by
            data.save()
            return {"detail": f"Deleted {cls.__name__} {id}"}
        except DoesNotExist:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )
