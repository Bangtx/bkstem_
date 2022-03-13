from .schema import Schema
from datetime import date
from typing import Optional


class UnitBase(Schema):
    name: str
    yomi: Optional[str] = None
    short_name: Optional[str]


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    pass


class UnitSort(Schema):
    id: int
    order_num: Optional[int]


class Unit(UnitBase):
    id: int
    order_num: Optional[int]
    search_str: str = None
    active: bool = True
    created_at: date
    created_by: int = None
