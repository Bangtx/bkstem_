from peewee import CharField, ForeignKeyField, JOIN, fn
from .master import MasterModel
from fastapi import HTTPException
from i18n import t
from .item import Item
from .image import Image
from .unit import Unit
from .size_group import SizeGroup
from .quality_group import QualityGroup
from utils.thumbnail import get_link_thumbnail

import peewee as p


class Variety(MasterModel):
    uuid = CharField()
    name = CharField()
    name_eng = CharField()
    yomi = CharField()
    short_name = CharField()
    item = ForeignKeyField(Item)
    size_group = ForeignKeyField(
        SizeGroup, column_name="size_group_id", field="id", null=True
    )
    quality_group = ForeignKeyField(
        QualityGroup, column_name="quality_group_id", field="id", null=True
    )

    @classmethod
    def get_order_num(cls, item_id: int):
        first = (
            cls.select()
            .where(cls.active & (cls.item == item_id))
            .order_by(cls.order_num.desc())
            .first()
        )

        order_num = first.order_num + 1 if first and first.order_num else 1
        return order_num

    @classmethod
    def get_with_img(cls):
        temp_word = "9999/99/99"
        temp_link = get_link_thumbnail(temp_word)
        varieties = cls.select(
            cls.id,
            cls.name,
            cls.active,
            cls.created_at,
            cls.uuid,
            cls.name_eng,
            cls.order_num,
            cls.search_str,
            cls.short_name,
            cls.yomi,
            fn.jsonb_build_object(
                'id', QualityGroup.id, 'name', QualityGroup.name,
                'name_eng', QualityGroup.name_eng, 'yomi', QualityGroup.yomi,
                'short_name', QualityGroup.short_name, 'search_str', QualityGroup.search_str,
                'order_num', QualityGroup.order_num
            ).alias('quality_group'),
            fn.jsonb_build_object(
                'id', SizeGroup.id, 'name', SizeGroup.name,
                'name_eng', SizeGroup.name_eng, 'yomi', SizeGroup.yomi,
                'short_name', SizeGroup.short_name, 'search_str', QualityGroup.search_str,
                'order_num', SizeGroup.order_num
            ).alias('size_group'),
            fn.jsonb_build_object(
                'id', Item.id, 'name', Item.name,
                'name_eng', Item.name_eng, 'yomi', Item.yomi,
                'short_name', Item.short_name, 'search_str', Item.search_str,
                'order_num', Item.order_num
            ).alias('item'),
            fn.COALESCE(
                fn.array_agg(
                    fn.jsonb_build_object(
                        "id", Image.id,
                        "uuid", Image.uuid,
                        "url", fn.REPLACE(temp_link, temp_word, Image.s3url),
                        "name", Image.name
                    )
                ).filter(Image.id.is_null(False)), "{}",
            ).alias('images')
        ).join(
            Item
        ).join(
            QualityGroup,
            JOIN.LEFT_OUTER,
            on=((QualityGroup.id == cls.quality_group) & QualityGroup.active)
        ).join(
            SizeGroup,
            JOIN.LEFT_OUTER,
            on=((SizeGroup.id == cls.size_group) & SizeGroup.active)
        ).join(
            Image,
            JOIN.LEFT_OUTER,
            on=(Image.uuid == cls.uuid)
        ).where(
            cls.active, Item.active
        ).order_by(
            Item.order_num.asc(),
            Item.yomi.collate('"C"'),
            cls.order_num.asc(),
            cls.yomi.collate('"C"')
        ).group_by(cls.id, Item.id, QualityGroup.id, SizeGroup.id).dicts()
        return list(varieties)

    @classmethod
    def get_no_img(cls):
        varieties = cls.select(
            cls.id,
            cls.name,
            cls.active,
            cls.created_at,
            cls.uuid,
            cls.name_eng,
            cls.order_num,
            cls.search_str,
            cls.short_name,
            cls.yomi,
            fn.jsonb_build_object(
                'id', QualityGroup.id, 'name', QualityGroup.name,
                'name_eng', QualityGroup.name_eng, 'yomi', QualityGroup.yomi,
                'short_name', QualityGroup.short_name, 'search_str', QualityGroup.search_str,
                'order_num', QualityGroup.order_num
            ).alias('quality_group'),
            fn.jsonb_build_object(
                'id', SizeGroup.id, 'name', SizeGroup.name,
                'name_eng', SizeGroup.name_eng, 'yomi', SizeGroup.yomi,
                'short_name', SizeGroup.short_name, 'search_str', QualityGroup.search_str,
                'order_num', SizeGroup.order_num
            ).alias('size_group'),
            fn.jsonb_build_object(
                'id', Item.id, 'name', Item.name,
                'name_eng', Item.name_eng, 'yomi', Item.yomi,
                'short_name', Item.short_name, 'search_str', Item.search_str,
                'order_num', Item.order_num
            ).alias('item')
        ).join(
            Item
        ).join(
            QualityGroup,
            JOIN.LEFT_OUTER,
            on=((QualityGroup.id == cls.quality_group) & QualityGroup.active)
        ).join(
            SizeGroup,
            JOIN.LEFT_OUTER,
            on=((SizeGroup.id == cls.size_group) & SizeGroup.active)
        ).where(
            cls.active, Item.active
        ).order_by(
            Item.order_num.asc(),
            Item.yomi.collate('"C"'),
            cls.order_num.asc(),
            cls.yomi.collate('"C"')
        ).dicts()
        return list(varieties)

    @classmethod
    def get_varieties_grouped_by_item(cls):
        from utils.thumbnail import get_link_thumbnail

        # create a random string for thumbnail
        # (can't use python function in query)
        temp_word = "9999/99/99"
        temp_link = get_link_thumbnail(temp_word)

        # create temporary table for variety join with images
        varieties_with_img = (
            cls.select(
                cls.id,
                cls.name,
                cls.item,
                cls.uuid,
                cls.name_eng,
                cls.short_name,
                cls.yomi,
                cls.search_str,
                cls.active,
                cls.created_at,
                cls.created_by,
                cls.order_num,
                p.Case(
                    SizeGroup.id.is_null(False),
                    [
                        (
                            True,
                            fn.jsonb_build_object(
                                "id",
                                SizeGroup.id,
                                "name",
                                SizeGroup.name,
                                "name_eng",
                                SizeGroup.name_eng,
                                "yomi",
                                SizeGroup.yomi,
                                "short_name",
                                SizeGroup.short_name,
                                "is_default",
                                SizeGroup.is_default,
                                "order_num",
                                SizeGroup.order_num,
                                "search_str",
                                SizeGroup.search_str,
                                "active",
                                SizeGroup.active,
                                "created_at",
                                fn.TO_CHAR(SizeGroup.created_at, "YYYY-MM-DD"),
                            ),
                        ),
                        (False, None),
                    ],
                ).alias("size_group"),
                p.Case(
                    QualityGroup.id.is_null(False),
                    [
                        (
                            True,
                            fn.jsonb_build_object(
                                "id",
                                QualityGroup.id,
                                "name",
                                QualityGroup.name,
                                "name_eng",
                                QualityGroup.name_eng,
                                "yomi",
                                QualityGroup.yomi,
                                "short_name",
                                QualityGroup.short_name,
                                "is_default",
                                QualityGroup.is_default,
                                "order_num",
                                QualityGroup.order_num,
                                "search_str",
                                QualityGroup.search_str,
                                "active",
                                QualityGroup.active,
                                "created_at",
                                fn.TO_CHAR(
                                    QualityGroup.created_at, "YYYY-MM-DD"
                                ),
                            ),
                        ),
                        (False, None),
                    ],
                ).alias("quality_group"),
                fn.COALESCE(
                    fn.jsonb_agg(
                        fn.jsonb_build_object(
                            "id",
                            Image.id,
                            "name",
                            Image.name,
                            "uuid",
                            Image.uuid,
                            "url",
                            fn.REPLACE(temp_link, temp_word, Image.s3url),
                        )
                    ).filter(Image.id.is_null(False)),
                    "[]",
                ).alias("images"),
            )
            .join(
                Image,
                JOIN.LEFT_OUTER,
                on=((Image.uuid == Variety.uuid) & Image.active),
            )
            .join(
                SizeGroup,
                JOIN.LEFT_OUTER,
                on=(
                    (SizeGroup.id == Variety.size_group)
                    & SizeGroup.id.is_null(False)
                    & SizeGroup.active
                ),
            )
            .join(
                QualityGroup,
                JOIN.LEFT_OUTER,
                on=(
                    (QualityGroup.id == Variety.quality_group)
                    & QualityGroup.id.is_null(False)
                    & QualityGroup.active
                ),
            )
            .where(cls.active)
            .group_by(cls.id, cls.order_num, SizeGroup.id, QualityGroup.id)
            .order_by(cls.order_num)
            .cte("varieties_with_img")
        )

        # create temporary table for item join with unit
        Units = Unit.alias()
        item_with_units = (
            Item.select(
                Item.id.alias("id"),
                p.Case(
                    Unit.id.is_null(False),
                    [
                        (
                            True,
                            fn.jsonb_build_object(
                                "id", Unit.id, "name", Unit.name
                            ),
                        ),
                        (False, None),
                    ],
                ).alias("item_default_unit"),
                fn.COALESCE(
                    fn.jsonb_agg(
                        fn.DISTINCT(
                            fn.jsonb_build_object(
                                "id", Units.id, "name", Units.name
                            )
                        )
                    ).filter(Units.id.is_null(False)),
                    "[]",
                ).alias("units"),
            )
            .join(Unit, JOIN.LEFT_OUTER, on=(Unit.id == Item.default_unit))
            .join(
                Units,
                JOIN.LEFT_OUTER,
                on=(Units.id == fn.any(Item.units)),
            )
            .where(Item.active)
            .group_by(Item.id, Unit.id, Unit.name)
            .cte("item_with_units")
        )

        # create temporary table for item join with images
        item_with_images = (
            Item.select(
                Item.id.alias("id"),
                fn.COALESCE(
                    fn.jsonb_agg(
                        fn.jsonb_build_object(
                            "id",
                            Image.id,
                            "name",
                            Image.name,
                            "uuid",
                            Image.uuid,
                            "url",
                            fn.REPLACE(temp_link, temp_word, Image.s3url),
                        )
                    ).filter(Image.id.is_null(False)),
                    "[]",
                ).alias("images"),
            )
            .join(
                Image,
                JOIN.LEFT_OUTER,
                on=((Image.uuid == Item.uuid) & Image.active),
            )
            .where(Item.active)
            .group_by(Item.id)
            .cte("item_with_images")
        )

        # create temporary table for item join with size group
        item_with_size_group = (
            Item.select(
                Item.id.alias("id"),
                p.Case(
                    SizeGroup.id.is_null(False),
                    [
                        (
                            True,
                            fn.jsonb_build_object(
                                "id",
                                SizeGroup.id,
                                "name",
                                SizeGroup.name,
                                "name_eng",
                                SizeGroup.name_eng,
                                "yomi",
                                SizeGroup.yomi,
                                "short_name",
                                SizeGroup.short_name,
                                "is_default",
                                SizeGroup.is_default,
                                "order_num",
                                SizeGroup.order_num,
                                "search_str",
                                SizeGroup.search_str,
                                "active",
                                SizeGroup.active,
                                "created_at",
                                fn.TO_CHAR(SizeGroup.created_at, "YYYY-MM-DD"),
                            ),
                        ),
                        (False, None),
                    ],
                ).alias("item_size_group"),
            )
            .join(
                SizeGroup,
                JOIN.LEFT_OUTER,
                on=(
                    (SizeGroup.id == Item.size_group)
                    & SizeGroup.id.is_null(False)
                    & SizeGroup.active
                ),
            )
            .where(Item.active)
            .group_by(Item.id, SizeGroup.id)
            .cte("item_with_size_group")
        )

        # create temporary table for item join with size group
        item_with_quality_group = (
            Item.select(
                Item.id.alias("id"),
                p.Case(
                    QualityGroup.id.is_null(False),
                    [
                        (
                            True,
                            fn.jsonb_build_object(
                                "id",
                                QualityGroup.id,
                                "name",
                                QualityGroup.name,
                                "name_eng",
                                QualityGroup.name_eng,
                                "yomi",
                                QualityGroup.yomi,
                                "short_name",
                                QualityGroup.short_name,
                                "is_default",
                                QualityGroup.is_default,
                                "order_num",
                                QualityGroup.order_num,
                                "search_str",
                                QualityGroup.search_str,
                                "active",
                                QualityGroup.active,
                                "created_at",
                                fn.TO_CHAR(
                                    QualityGroup.created_at, "YYYY-MM-DD"
                                ),
                            ),
                        ),
                        (False, None),
                    ],
                ).alias("item_quality_group"),
            )
            .join(
                QualityGroup,
                JOIN.LEFT_OUTER,
                on=(
                    (QualityGroup.id == Item.quality_group)
                    & QualityGroup.id.is_null(False)
                    & QualityGroup.active
                ),
            )
            .where(Item.active)
            .group_by(Item.id, QualityGroup.id)
            .cte("item_with_quality_group")
        )

        query = (
            Item.select(
                Item.id.alias("id"),
                Item.uuid.alias("uuid"),
                Item.name.alias("name"),
                Item.name_eng.alias("name_eng"),
                Item.yomi.alias("yomi"),
                Item.short_name.alias("short_name"),
                Item.order_num.alias("order_num"),
                item_with_units.c.item_default_unit,
                item_with_units.c.units.alias("units"),
                item_with_size_group.c.item_size_group,
                item_with_quality_group.c.item_quality_group,
                Item.search_str.alias("search_str"),
                item_with_images.c.images.alias("images"),
                fn.COALESCE(
                    fn.jsonb_agg(
                        fn.jsonb_build_object(
                            "id",
                            varieties_with_img.c.id,
                            "name",
                            varieties_with_img.c.name,
                            "uuid",
                            varieties_with_img.c.uuid,
                            "name_eng",
                            varieties_with_img.c.name_eng,
                            "short_name",
                            varieties_with_img.c.short_name,
                            "yomi",
                            varieties_with_img.c.yomi,
                            "order_num",
                            varieties_with_img.c.order_num,
                            "search_str",
                            fn.CONCAT(
                                Item.search_str, "|", varieties_with_img.c.search_str
                            ),
                            "item",
                            fn.jsonb_build_object(
                                "id", Item.id, "name", Item.name
                            ),
                            "active",
                            varieties_with_img.c.active,
                            "created_at",
                            fn.TO_CHAR(
                                varieties_with_img.c.created_at, "YYYY-MM-DD"
                            ),
                            "created_by",
                            varieties_with_img.c.created_by,
                            "images",
                            varieties_with_img.c.images,
                            "size_group",
                            varieties_with_img.c.size_group,
                            "quality_group",
                            varieties_with_img.c.quality_group,
                        )
                    )
                    .filter(varieties_with_img.c.id.is_null(False))
                    .order_by(
                        varieties_with_img.c.order_num,
                        varieties_with_img.c.yomi.collate('"C"')
                    ),
                    "[]",
                ).alias("varieties"),
            )
            .where(Item.active)
            .join(
                varieties_with_img,
                JOIN.LEFT_OUTER,
                on=(
                    (Item.id == varieties_with_img.c.item_id)
                    & varieties_with_img.c.active
                ),
            )
            .join(
                item_with_units,
                JOIN.LEFT_OUTER,
                on=(Item.id == item_with_units.c.id),
            )
            .join(
                item_with_images,
                JOIN.LEFT_OUTER,
                on=(Item.id == item_with_images.c.id),
            )
            .join(
                item_with_size_group,
                JOIN.LEFT_OUTER,
                on=(Item.id == item_with_size_group.c.id),
            )
            .join(
                item_with_quality_group,
                JOIN.LEFT_OUTER,
                on=(Item.id == item_with_quality_group.c.id),
            )
            .group_by(
                Item.id,
                Item.order_num,
                item_with_units.c.item_default_unit,
                item_with_units.c.units,
                item_with_images.c.images,
                item_with_size_group.c.item_size_group,
                item_with_quality_group.c.item_quality_group,
            )
            .order_by(Item.order_num.asc(), Item.yomi.collate('"C"'))
            .with_cte(
                varieties_with_img,
                item_with_units,
                item_with_images,
                item_with_size_group,
                item_with_quality_group,
            )
        )

        return list(query.dicts())

    @classmethod
    def get_varieties_by_item_id(cls, item_id):
        query = (
            cls.select()
            .where(cls.item_id == item_id)
            .order_by(cls.order_num.asc())
        )
        return list(query)

    @classmethod
    def get_varieties_name_and_id_for_list_selecting(cls):
        varieties = cls.select(cls.id, cls.name).where(cls.active)
        return list(varieties)

    @classmethod
    def check_duplicate(cls, name: str, item_id: int, id=None):
        varieties = cls.select().where(
            cls.id != id, cls.item_id == item_id, cls.active
        )
        for variety in varieties:
            if variety.name.lower() == name.lower():
                raise HTTPException(
                    status_code=400,
                    detail=t("fmbiz.master.errors.duplicate_name"),
                )
        return True
