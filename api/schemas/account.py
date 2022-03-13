from .schema import Schema


class Account(Schema):
    name: str
    password: str
    mail: str
    phone: str
    role: int
    search_str: str
