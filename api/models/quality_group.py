from fastapi import HTTPException
from peewee import CharField, BooleanField, fn, JOIN
from .master import MasterModel


class QualityGroup(MasterModel):
    name = CharField()
    name_eng = CharField()
    yomi = CharField()
    short_name = CharField()
    is_default = BooleanField(default=False)

    class Meta:
        db_table = "quality_group"

    @classmethod
    def get_qualities_grouped_by_quality_group(cls):
        from .quality import Quality

        query = (
            QualityGroup.select(
                cls,
                fn.COALESCE(
                    fn.json_agg(
                        fn.json_build_object(
                            "id",
                            Quality.id,
                            "name",
                            Quality.name,
                            "name_eng",
                            Quality.name_eng,
                            "yomi",
                            Quality.yomi,
                            "short_name",
                            Quality.short_name,
                            "active",
                            Quality.active,
                            "order_num",
                            Quality.order_num,
                            "search_str",
                            fn.CONCAT(
                                Quality.search_str, QualityGroup.search_str
                            ),
                            "quality_group",
                            fn.json_build_object(
                                "id", QualityGroup.id, "name", QualityGroup.name
                            ),
                            "created_at",
                            fn.TO_CHAR(Quality.created_at, "YYYY-MM-DD"),
                            "created_by",
                            Quality.created_by,
                        )
                    )
                    .filter(Quality.id.is_null(False))
                    .order_by(
                        Quality.order_num.asc(),
                        Quality.yomi.collate('"C"')
                    ),
                    "[]",
                ).alias("qualities"),
            )
            .where(QualityGroup.active)
            .join(
                Quality,
                JOIN.LEFT_OUTER,
                on=(
                    (QualityGroup.id == Quality.quality_group_id)
                    & Quality.active
                ),
            )
            .group_by(QualityGroup.id, QualityGroup.order_num)
            .order_by(
                QualityGroup.order_num.asc(),
                QualityGroup.yomi.collate('"C"')
            )
        )

        return list(query)

    @classmethod
    def delete_quality_group(cls, group_id):
        # cannot delete default group
        quality_group = cls.get_one(group_id)

        if quality_group.is_default:
            raise HTTPException(
                status_code=400, detail="Cannot delete default group"
            )

        # cannot delete group which still has qualities
        from .quality import Quality

        qualities = Quality.select(Quality).where(
            Quality.active & (Quality.quality_group == group_id)
        )

        if qualities.count() > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete: 1 or more qualities are still existed",
            )

        # other case: delete it
        return cls.soft_delete(group_id)
