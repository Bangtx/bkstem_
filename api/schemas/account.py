from .schema import Schema


class Account(Schema):
    name: str
    password: str
    mail: str = None
    phone: str = None
    role: int = None
    search_str: str = None
