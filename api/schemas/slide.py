from schemas.schema import Schema


class Slide(Schema):
    title: str
    remark: str = None
    url: str
    classroom: int
