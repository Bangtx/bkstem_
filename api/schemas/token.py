from .schema import Schema


class Token(Schema):
    id: int
    name: str
    password: str
    mail: str
    phone: str
    role: int
    search_str: str