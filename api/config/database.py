from contextvars import ContextVar
from typing import Any
import peewee
import contextlib

import psycopg2.extensions
import psycopg2.extras

from pydantic.utils import GetterDict
from playhouse.postgres_ext import PostgresqlExtDatabase

from .setting import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

db_state_default = {
    "closed": None,
    "conn": None,
    "ctx": None,
    "transactions": None,
}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = PostgresqlExtDatabase(
    POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    autorollback=True,
)

db._state = PeeweeConnectionState()


@contextlib.contextmanager
def bare_cursor(db_: peewee.Database, cursor_factory=None):
    """Gets the bare cursor which has no transaction context."""
    connection: psycopg2.extensions.connection = db_.connection()
    old_isolation_level = connection.isolation_level

    connection.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )
    try:
        yield connection.cursor(cursor_factory=cursor_factory)
    finally:
        connection.set_isolation_level(old_isolation_level)
