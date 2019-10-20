import aiopg.sa
from sqlalchemy import (MetaData, Table, Column, Integer)

__all__ = ['unit']
meta = MetaData()

unit = Table(
    'unit', meta,
    Column('unit_id', Integer, primary_key=True),
    Column('supply', Integer, nullable=False),
)


async def create_tables(engine):
    meta.create_all(bind=engine, tables=[unit])


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
