from .schema import Schema


class AccountBase(Schema):
    name: str
    password: str
    mail: str = None
    phone: str = None
    role: int = None
    search_str: str = None


class AccountCreate(AccountBase):
    pass

