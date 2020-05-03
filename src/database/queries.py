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
    try:
        res = execute(table.insert().values(values))
    finally:
        pass
    return res

def update_by_id(table: sa.Table, values: list, id: int):
	query = table.update().values(values).where(table.c.id == id)
	print(query)
	return execute(query)
        

def select_with_id(table: sa.Table, id):
    query = table.select().where(id == table.c.id)
    return fetch_one(execute(query))


def select_by_uid(table: sa.Table, uid: Any):
    query = table.select().where(table.c.uid == uid)
    return fetch_one(execute(query))


# Request to local DB
def select_album_by_uid(table: sa.Table, uid: Any):
    return sp.album(uid)


def fetch_one(result: ResultProxy):
    return result.fetchone()

