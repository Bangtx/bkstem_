from fastapi import HTTPException
from peewee import CharField, fn, JOIN, BooleanField
from .master import MasterModel


class SizeGroup(MasterModel):
    name = CharField()
    name_eng = CharField()
    yomi = CharField()
    short_name = CharField()
    is_default = BooleanField(default=False)

    class Meta:
        db_table = "size_group"

    @classmethod
    def get_sizes_grouped_by_size_group(cls):
        from .size import Size

        query = (
            SizeGroup.select(
                cls,
                fn.COALESCE(
                    fn.json_agg(
                        fn.json_build_object(
                            "id",
                            Size.id,
                            "name",
                            Size.name,
                            "name_eng",
                            Size.name_eng,
                            "yomi",
                            Size.yomi,
                            "short_name",
                            Size.short_name,
                            "active",
                            Size.active,
                            "order_num",
                            Size.order_num,
                            "search_str",
                            fn.CONCAT(Size.search_str, SizeGroup.search_str),
                            "size_group",
                            fn.json_build_object(
                                "id", SizeGroup.id, "name", SizeGroup.name
                            ),
                            "created_at",
                            fn.TO_CHAR(Size.created_at, "YYYY-MM-DD"),
                            "created_by",
                            Size.created_by,
                        )
                    )
                    .filter(Size.id.is_null(False))
                    .order_by(Size.order_num.asc(), Size.yomi.collate('"C"')),
                    "[]",
                ).alias("sizes"),
            )
            .where(SizeGroup.active)
            .join(
                Size,
                JOIN.LEFT_OUTER,
                on=((SizeGroup.id == Size.size_group_id) & Size.active),
            )
            .group_by(SizeGroup.id, SizeGroup.order_num)
            .order_by(SizeGroup.order_num.asc(), SizeGroup.yomi.collate('"C"'))
        )

        return list(query)

    @classmethod
    def delete_size_group(cls, group_id):
        # cannot delete default group
        size_group = cls.get_one(group_id)

        if size_group.is_default:
            raise HTTPException(
                status_code=400, detail="Cannot delete default group"
            )

        # cannot delete group which still has sizes
        from .size import Size

        sizes = Size.select(Size).where(
            Size.active & (Size.size_group == group_id)
        )

        if sizes.count() > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete: 1 or more sizes are still existed",
            )

        # other case: delete it
        return cls.soft_delete(group_id)
