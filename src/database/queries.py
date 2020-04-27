from __future__ import annotations
from typing import Any

from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from sqlalchemy.engine.result import ResultProxy

from src.database.startup import conn
from src.database.tables import User


def execute(query):
    return conn.execute(query)


def insert(table: sa.Table, values):
    query = table.insert().values(values)
    # print(query)
    try:
        res = conn.execute(query)
    finally:
        pass
    return res
        


def select_by_uid(table: sa.Table, uid: Any):
    query = table.select().where(table.c.uid == uid)
    return fetch_one(conn.execute(query))


# Request to local DB
def select_album_by_uid(table: sa.Table, uid: Any):
    return sp.album(uid)


def fetch_one(result: ResultProxy):
    return result.fetchone()

