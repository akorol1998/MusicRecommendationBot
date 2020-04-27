import sqlalchemy as sa

from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.base import Engine
from src.database.tables import metadata
from src.config import DB_URL, DB



def connection():
    engine: Engine = sa.create_engine(DB_URL)
    conn: Connection = engine.connect()
    
    _drop_tables()
    _create_tables()
    return conn


def _create_tables():
    engine = _create_engine()
    metadata.create_all(engine)


def _create_engine():
    return sa.create_engine(DB_URL)


def _drop_tables():
    engine = _create_engine()
    metadata.drop_all(engine)


conn = connection()