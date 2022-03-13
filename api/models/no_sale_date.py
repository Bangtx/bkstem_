from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from i18n import t
from playhouse.shortcuts import model_to_dict
from pydash import filter_

from models.base import BaseModel
from peewee import CharField, BooleanField, DoesNotExist
from playhouse.postgres_ext import DateTimeTZField


class NoSaleDateModel(BaseModel):
    date_from = DateTimeTZField(default=datetime.now)
    date_to = DateTimeTZField()
    note = CharField()
    is_annual = BooleanField(default=False)

    class Meta:
        db_table = "no_sale_date"

    @classmethod
    def get_list(cls):
        return list(
            cls.select()
            .where(cls.active, cls.date_to >= datetime.now().date())
            .order_by(cls.date_from.asc())
            .dicts()
        )

    @classmethod
    def get_previous(cls, count: int):
        query = (
            cls.select()
            .where(cls.active, cls.date_to < datetime.now().date())
            .order_by(cls.date_from.desc())
            .limit(count)
            .dicts()
        )
        return list(query)

    @classmethod
    def check_duplicate(cls, start: datetime, end: datetime):
        no_sale_dates = cls.get_list()
        for i in no_sale_dates:
            date_from = i["date_from"]
            date_to = i["date_to"]
            if (date_from <= start and end <= date_to) or (
                date_from >= start and end >= date_to
            ):
                raise HTTPException(
                    400,
                    {"description": t("fmbiz.master.errors.duplicate_date")},
                )
        # data = cls.select().where(
        #     cls.date_from == start, cls.date_to == end, cls.active
        # )
        # if data:
        #     raise HTTPException(
        #         400, {"description": t("fmbiz.master.errors.duplicate_date")}
        #     )

    @classmethod
    def create_(cls, data: dict):
        now = datetime.now()
        data["created_at"] = now
        cls.check_duplicate(data["date_from"], data["date_to"])
        no_sale_date_id = cls.insert(data).execute()
        return no_sale_date_id

    @classmethod
    def update_no_sale_date_by_id(cls, id: int, data: dict):
        try:
            cls.update(**data, modified_at=datetime.now()).where(
                cls.id == id
            ).execute()
            nosale_date = model_to_dict(cls.get_by_id(id))
            return nosale_date
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Not Found")

    @classmethod
    def get_next_auction_date(cls, day: dict, auction_dates: List[int]):
        auction_dates_min = min(auction_dates)
        auction_dates_max = max(auction_dates)
        if day["week_day_id"] >= auction_dates_max:
            next_auction_date = {
                "week_day_id": auction_dates_min,
                "date": day["date"]
                + timedelta(
                    days=(7 - (day["week_day_id"] - auction_dates_min))
                ),
            }
        else:
            greater_list = filter_(
                auction_dates, lambda i: i > day["week_day_id"]
            )
            # l = []
            # for i in auction_dates_int:
            #     if i > today["week_day_id"]:
            #         l.append(i)
            next_auction_date = {
                "week_day_id": min(greater_list),
                "date": day["date"]
                + timedelta(days=min(greater_list) - day["week_day_id"]),
            }
        return next_auction_date

    @classmethod
    def get_filtered_next_auction_date(cls):
        from .setting import SettingModel

        today = {
            "week_day_id": datetime.today().weekday(),
            "date": datetime.today().date(),
        }

        auction_dates = SettingModel.get_setting_by_key("auction_date").get(
            "value"
        )
        auction_dates_int = [
            int(auction_date) for auction_date in auction_dates
        ]

        next_auction_date = cls.get_next_auction_date(today, auction_dates_int)

        no_sale_dates = cls.get_list()
        # date_range = [
        #     {
        #         "date_from": no_sale_date["date_from"],
        #         "date_to": no_sale_date["date_to"],
        #     }
        #     for no_sale_date in no_sale_dates
        # ]
        is_invalid = True
        while is_invalid:
            is_invalid = False
            for i in no_sale_dates:
                start = i["date_from"]
                end = i["date_to"]
                if start <= next_auction_date["date"] <= end:
                    next_auction_date = cls.get_next_auction_date(
                        next_auction_date, auction_dates_int
                    )
                    is_invalid = True
                    break
        return next_auction_date
