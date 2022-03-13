import uuid
from typing import Optional, List
from .schema import Schema
from datetime import date
from .file import Image
from .size_group import SizeGroup
from .quality_group import QualityGroup


class VarietyBase(Schema):
    name: str
    name_eng: Optional[str] = None
    short_name: Optional[str] = None
    yomi: Optional[str] = None


class VarietyCreate(VarietyBase):
    item: int
    size_group_id: Optional[int] = None
    quality_group_id: Optional[int] = None


class VarietyUpdate(VarietyBase):
    item: int
    size_group_id: Optional[int] = None
    quality_group_id: Optional[int] = None


class VarietySort(Schema):
    id: int
    order_num: Optional[int]


class VarietyOfItem(Schema):
    id: int
    name: str


class Variety(VarietyBase):
    id: int
    uuid: uuid.UUID
    order_num: Optional[int]
    search_str: str
    item: VarietyOfItem
    images: List[Image] = []
    size_group: SizeGroup = None
    quality_group: QualityGroup = None
    active: bool = True
    created_at: date
    created_by: int = None


class DefaultUnit(Schema):
    id: int
    name: str


class VarietyGroupByItem(Schema):
    id: int
    uuid: uuid.UUID
    name: str
    name_eng: str = None
    yomi: str = None
    short_name: str = None
    default_unit: DefaultUnit = None
    search_str: str
    order_num: int = None
    size_group: SizeGroup = None
    quality_group: QualityGroup = None
    images: List[Image] = []
    units: List[DefaultUnit] = None
    varieties: List[Variety]
