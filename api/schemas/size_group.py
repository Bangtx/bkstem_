from .schema import Schema
from datetime import date
from typing import Optional


class SizeGroupBase(Schema):
    name: str
    name_eng: Optional[str] = None
    yomi: Optional[str] = None
    short_name: Optional[str]


class SizeGroupCreate(SizeGroupBase):
    pass


class SizeGroupSort(Schema):
    id: int
    order_num: Optional[int]


class SizeGroupUpdate(SizeGroupBase):
    pass


class SizeGroup(SizeGroupBase):
    id: int
    order_num: Optional[int]
    search_str: str = None
    active: bool = True
    is_default: bool
    created_at: date
    created_by: int = None
