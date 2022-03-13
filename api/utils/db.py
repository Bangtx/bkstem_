import peewee
from functools import wraps


def transaction(func):
    """Decorator for wrapping whole function inside a transaction"""
    from config.database import db

    @wraps(func)
    def decorated(*args, **kwargs):
        with db.atomic():
            return func(*args, **kwargs)

    return decorated


class _Excluded:
    """Shortcut for EXCLUDED table for INSERT ON CONFLICT query"""

    def __getattr__(self, column):
        return peewee.NodeList(
            (peewee.SQL("EXCLUDED"), peewee.ensure_entity(column)), glue="."
        )


EXCLUDED = _Excluded()
