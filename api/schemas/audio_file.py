from .schema import Schema


class File(Schema):
    name: str
    payload: str
    type: str
    size: int


class AudioFile(Schema):
    id: int
    url: str