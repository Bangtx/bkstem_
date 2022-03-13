from .schema import Schema
from datetime import date
from typing import Optional, List


class SizeBase(Schema):
    name: str
    name_eng: Optional[str] = None
    yomi: Optional[str] = None
    short_name: Optional[str]


class SizeCreate(SizeBase):
    size_group_id: int


class SizeUpdate(SizeBase):
    size_group_id: int


class SizeSort(Schema):
    id: int
    order_num: Optional[int]


class SizeGroupBasicInfo(Schema):
    id: int
    name: str


class Size(SizeBase):
    id: int
    order_num: Optional[int]
    search_str: str = None
    active: bool = True
    size_group: SizeGroupBasicInfo
    created_at: date
    created_by: int = None


class SizesGroupedBySizeGroup(Schema):
    id: int
    name: str
    name_eng: str = None
    yomi: str = None
    short_name: str = None
    order_num: Optional[int]
    search_str: str
    is_default: bool
    sizes: List[Size]
